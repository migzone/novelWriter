# -*- coding: utf-8 -*-
"""novelWriter GUI Session Log Viewer

 novelWriter – GUI Session Log Viewer
======================================
 Class holding the session log view window

 File History:
 Created: 2019-10-20 [0.3]

 This file is a part of novelWriter
 Copyright 2020, Veronica Berglyd Olsen

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful, but
 WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import nw

from os import path
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    qApp, QDialog, QTreeWidget, QTreeWidgetItem, QDialogButtonBox, QGridLayout,
    QLabel, QGroupBox
)

from nw.constants import nwConst, nwFiles, nwAlert
from nw.gui.custom import QSwitch

logger = logging.getLogger(__name__)

class GuiSessionLog(QDialog):

    C_TIME   = 0
    C_LENGTH = 1
    C_COUNT  = 2
    C_BAR    = 3

    def __init__(self, theParent, theProject):
        QDialog.__init__(self, theParent)

        logger.debug("Initialising GuiSessionLog ...")

        self.mainConf   = nw.CONFIG
        self.theParent  = theParent
        self.theProject = theProject
        self.theTheme   = theParent.theTheme
        self.optState   = theProject.optState

        self.logData    = []
        self.timeFilter = 0.0
        self.timeTotal  = 0.0
        self.maxWords   = 0

        self.setWindowTitle("Session Log")
        self.setMinimumWidth(self.mainConf.pxInt(420))
        self.setMinimumHeight(self.mainConf.pxInt(400))
        self.resize(
            self.mainConf.pxInt(self.optState.getInt("GuiSessionLog", "winWidth",  550)),
            self.mainConf.pxInt(self.optState.getInt("GuiSessionLog", "winHeight", 500))
        )

        # List Box
        wCol0 = self.mainConf.pxInt(
            self.optState.getInt("GuiSessionLog", "widthCol0", 180)
        )
        wCol1 = self.mainConf.pxInt(
            self.optState.getInt("GuiSessionLog", "widthCol1", 80)
        )
        wCol2 = self.mainConf.pxInt(
            self.optState.getInt("GuiSessionLog", "widthCol2", 80)
        )

        self.listBox = QTreeWidget()
        self.listBox.setHeaderLabels(["Session Start","Length","Words","Histogram"])
        self.listBox.setIndentation(0)
        self.listBox.setColumnWidth(self.C_TIME, wCol0)
        self.listBox.setColumnWidth(self.C_LENGTH, wCol1)
        self.listBox.setColumnWidth(self.C_COUNT, wCol2)
        self.listBox.resizeColumnToContents(self.C_COUNT)

        hHeader = self.listBox.headerItem()
        hHeader.setTextAlignment(self.C_LENGTH, Qt.AlignRight)
        hHeader.setTextAlignment(self.C_COUNT, Qt.AlignRight)

        self.monoFont = QFont()
        self.monoFont.setPointSizeF(0.9*self.theTheme.fontPointSize)
        self.monoFont.setFamily(self.theTheme.guiFontFixed.family())

        sortValid = (Qt.AscendingOrder, Qt.DescendingOrder)
        sortCol = self.optState.validIntRange(
            self.optState.getInt("GuiSessionLog", "sortCol", 0), 0, 2, 0
        )
        sortOrder = self.optState.validIntTuple(
            self.optState.getInt("GuiSessionLog", "sortOrder", Qt.DescendingOrder),
            sortValid, Qt.DescendingOrder
        )
        self.listBox.sortByColumn(sortCol, sortOrder)
        self.listBox.setSortingEnabled(True)

        # Word Bar
        self.barHeight = int(round(0.5*self.theTheme.fontPixelSize))
        self.barImage = QPixmap(self.barHeight, self.barHeight)
        self.barImage.fill(self.palette().highlight().color())

        # Session Info
        self.infoBox  = QGroupBox("Sum Totals", self)
        self.infoForm = QGridLayout(self)
        self.infoBox.setLayout(self.infoForm)

        self.labelTotal = QLabel(self._formatTime(0))
        self.labelTotal.setFont(self.monoFont)
        self.labelTotal.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        self.labelFilter = QLabel(self._formatTime(0))
        self.labelFilter.setFont(self.monoFont)
        self.labelFilter.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        self.infoForm.addWidget(QLabel("Total Time:"),    0, 0)
        self.infoForm.addWidget(self.labelTotal,          0, 1)
        self.infoForm.addWidget(QLabel("Filtered Time:"), 1, 0)
        self.infoForm.addWidget(self.labelFilter,         1, 1)
        self.infoForm.setRowStretch(2, 1)

        # Filter Options
        sPx = self.theTheme.baseIconSize

        self.filterBox  = QGroupBox("Filters", self)
        self.filterForm = QGridLayout(self)
        self.filterBox.setLayout(self.filterForm)

        self.labelZeros = QLabel("Hide zero word count")
        self.hideZeros = QSwitch(width=2*sPx, height=sPx)
        self.hideZeros.setChecked(
            self.optState.getBool("GuiSessionLog", "hideZeros", True)
        )
        self.hideZeros.clicked.connect(self._updateListBox)

        self.labelNegative = QLabel("Hide negative word count")
        self.hideNegative = QSwitch(width=2*sPx, height=sPx)
        self.hideNegative.setChecked(
            self.optState.getBool("GuiSessionLog", "hideNegative", False)
        )
        self.hideNegative.clicked.connect(self._updateListBox)

        self.labelByDay = QLabel("Group entries by day")
        self.groupByDay = QSwitch(width=2*sPx, height=sPx)
        self.groupByDay.setChecked(
            self.optState.getBool("GuiSessionLog", "groupByDay", False)
        )
        self.groupByDay.clicked.connect(self._updateListBox)

        self.filterForm.addWidget(self.labelZeros,    0, 0)
        self.filterForm.addWidget(self.hideZeros,     0, 1)
        self.filterForm.addWidget(self.labelNegative, 1, 0)
        self.filterForm.addWidget(self.hideNegative,  1, 1)
        self.filterForm.addWidget(self.labelByDay,    2, 0)
        self.filterForm.addWidget(self.groupByDay,    2, 1)

        # Buttons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        self.buttonBox.rejected.connect(self._doClose)

        # Assemble
        self.outerBox = QGridLayout()
        self.outerBox.addWidget(self.listBox,   0, 0, 1, 2)
        self.outerBox.addWidget(self.infoBox,   1, 0)
        self.outerBox.addWidget(self.filterBox, 1, 1)
        self.outerBox.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.outerBox.setRowStretch(0, 1)

        self.setLayout(self.outerBox)

        logger.debug("GuiSessionLog initialisation complete")

        qApp.processEvents()
        self._loadLogFile()
        self._updateListBox()

        return

    ##
    #  Slots
    ##

    def _doClose(self):
        """Save the state of the window, clear cache, end close.
        """
        self.logData = []

        winWidth     = self.mainConf.rpxInt(self.width())
        winHeight    = self.mainConf.rpxInt(self.height())
        widthCol0    = self.mainConf.rpxInt(self.listBox.columnWidth(0))
        widthCol1    = self.mainConf.rpxInt(self.listBox.columnWidth(1))
        widthCol2    = self.mainConf.rpxInt(self.listBox.columnWidth(2))
        sortCol      = self.listBox.sortColumn()
        sortOrder    = self.listBox.header().sortIndicatorOrder()
        hideZeros    = self.hideZeros.isChecked()
        hideNegative = self.hideNegative.isChecked()
        groupByDay   = self.groupByDay.isChecked()

        self.optState.setValue("GuiSessionLog", "winWidth",     winWidth)
        self.optState.setValue("GuiSessionLog", "winHeight",    winHeight)
        self.optState.setValue("GuiSessionLog", "widthCol0",    widthCol0)
        self.optState.setValue("GuiSessionLog", "widthCol1",    widthCol1)
        self.optState.setValue("GuiSessionLog", "widthCol2",    widthCol2)
        self.optState.setValue("GuiSessionLog", "sortCol",      sortCol)
        self.optState.setValue("GuiSessionLog", "sortOrder",    sortOrder)
        self.optState.setValue("GuiSessionLog", "hideZeros",    hideZeros)
        self.optState.setValue("GuiSessionLog", "hideNegative", hideNegative)
        self.optState.setValue("GuiSessionLog", "groupByDay",   groupByDay)

        self.optState.saveSettings()
        self.close()

        return

    ##
    #  Internal Functions
    ##

    def _loadLogFile(self):
        """Load the content of the log file into a buffer.
        """
        self.logData = []
        logger.debug("Loading session log file")

        try:
            logFile = path.join(self.theProject.projMeta, nwFiles.SESS_INFO)
            with open(logFile, mode="r", encoding="utf8") as inFile:
                for inLine in inFile:

                    inData = inLine.split()
                    if len(inData) != 8:
                        continue

                    dStart = datetime.strptime(
                        "%s %s" % (inData[1], inData[2]), nwConst.tStampFmt
                    )
                    dEnd = datetime.strptime(
                        "%s %s" % (inData[4], inData[5]), nwConst.tStampFmt
                    )

                    nWords = int(inData[7])
                    tDiff = dEnd - dStart
                    sDiff = tDiff.total_seconds()
                    self.timeTotal += sDiff

                    self.logData.append((dStart, sDiff, nWords))
                    self.maxWords = max(self.maxWords, nWords)

        except Exception as e:
            self.theParent.makeAlert(
                ["Failed to read session log file.",str(e)], nwAlert.ERROR
            )
            return False

        self.labelTotal.setText(self._formatTime(self.timeTotal))

        return True

    def _updateListBox(self):
        """Load/reload the content of the list box.
        """
        self.listBox.clear()
        self.timeFilter = 0.0

        hideZeros    = self.hideZeros.isChecked()
        hideNegative = self.hideNegative.isChecked()
        groupByDay   = self.groupByDay.isChecked()

        # Group the data
        if groupByDay:
            listData = []
            listMax  = 0

            dayDate  = None
            daySDiff = 0
            dayWords = 0

            for n, (dStart, sDiff, nWords) in enumerate(self.logData):
                if n == 0:
                    dayDate = dStart.date()
                if dayDate != dStart.date():
                    listData.append((dayDate, daySDiff, dayWords))
                    listMax  = max(listMax, dayWords)
                    dayDate  = dStart.date()
                    daySDiff = sDiff
                    dayWords = nWords
                else:
                    daySDiff += sDiff
                    dayWords += nWords

            if dayDate is not None:
                listData.append((dayDate, daySDiff, dayWords))

        else:
            listData = self.logData
            listMax  = self.maxWords

        # Populate the list
        for dStart, sDiff, nWords in listData:

            if hideZeros and nWords == 0:
                continue
            if hideNegative and nWords < 0:
                continue

            self.timeFilter += sDiff

            if groupByDay:
                sStart = dStart.strftime(nwConst.dStampFmt)
            else:
                sStart = dStart.strftime(nwConst.tStampFmt)

            newItem = QTreeWidgetItem()
            newItem.setText(self.C_TIME, sStart)
            newItem.setText(self.C_LENGTH, self._formatTime(sDiff))
            newItem.setText(self.C_COUNT, str(nWords))

            if nWords > 0:
                theBar = self.barImage.scaled(
                    int(200*nWords/listMax),
                    self.barHeight,
                    Qt.IgnoreAspectRatio,
                    Qt.FastTransformation
                )
                newItem.setData(self.C_BAR, Qt.DecorationRole, theBar)

            newItem.setTextAlignment(self.C_LENGTH, Qt.AlignRight)
            newItem.setTextAlignment(self.C_COUNT, Qt.AlignRight)
            newItem.setTextAlignment(self.C_BAR, Qt.AlignLeft | Qt.AlignVCenter)

            newItem.setFont(self.C_TIME, self.monoFont)
            newItem.setFont(self.C_LENGTH, self.monoFont)
            newItem.setFont(self.C_COUNT, self.monoFont)

            self.listBox.addTopLevelItem(newItem)

        self.labelFilter.setText(self._formatTime(self.timeFilter))

        return True

    def _formatTime(self, tS):
        """Format the time spent in 00:00:00 format.
        """
        tM = int(tS/60)
        tH = int(tM/60)
        tM = tM - tH*60
        tS = tS - tM*60 - tH*3600
        return "%02d:%02d:%02d" % (tH,tM,tS)

# END Class GuiSessionLog
