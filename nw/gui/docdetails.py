# -*- coding: utf-8 -*-
"""novelWriter GUI Document Details

 novelWriter – GUI Document Details
====================================
 Class holding the left side document details panel

 File History:
 Created: 2019-04-24 [0.0.1]

"""

import logging
import nw

from os              import path
from PyQt5.QtGui     import QFont
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel

from nw.enum         import nwItemType, nwItemClass, nwItemLayout
from nw.project.item import NWItem

logger = logging.getLogger(__name__)

class GuiDocDetails(QFrame):

    C_NAME   = 0
    C_COUNT  = 1
    C_FLAGS  = 2
    C_HANDLE = 3

    def __init__(self, theProject):
        QFrame.__init__(self)

        logger.debug("Initialising DocDetails ...")
        self.mainConf   = nw.CONFIG
        self.debugGUI   = self.mainConf.debugGUI
        self.theProject = theProject

        self.mainBox = QGridLayout(self)
        self.mainBox.setVerticalSpacing(1)
        self.mainBox.setHorizontalSpacing(15)
        self.setLayout(self.mainBox)

        self.fntOne = QFont()
        self.fntOne.setPointSize(10)
        self.fntOne.setBold(True)

        self.fntTwo = QFont()
        self.fntTwo.setPointSize(10)

        colOne = ["Name","Status","Class","Layout"]
        for nRow in range(4):
            lblOne = QLabel(colOne[nRow])
            lblOne.setFont(self.fntOne)
            self.mainBox.addWidget(lblOne,nRow+1,0)
    
        self.mainBox.setColumnStretch(0,0)
        self.mainBox.setColumnStretch(1,1)

        logger.debug("DocDetails initialisation complete")

        return

    def buildViewBox(self, tHandle):

        nwItem     = self.theProject.getItem(tHandle)
        itemStatus = nwItem.itemStatus
        if itemStatus < 0 or itemStatus >= len(self.theProject.statusLabels):
            itemStatus = 0

        colTwo = [
            nwItem.itemName,
            self.theProject.statusLabels[itemStatus],
            NWItem.CLASS_NAME[nwItem.itemClass],
            NWItem.LAYOUT_NAME[nwItem.itemLayout],
        ]

        for nRow in range(4):
            lblTwo = QLabel(colTwo[nRow])
            lblTwo.setFont(self.fntTwo)
            self.mainBox.addWidget(lblTwo,nRow+1,1)

        return

# END Class GuiDocDetails