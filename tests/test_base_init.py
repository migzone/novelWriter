# -*- coding: utf-8 -*-
"""novelWriter Main Init Tester
"""

import nw
import pytest
import logging
import sys

from dummy import DummyMain

@pytest.mark.base
def testBaseInit_Launch(caplog, monkeypatch, tmpDir):
    """Check launching the main GUI.
    """
    monkeypatch.setattr("nw.guimain.GuiMain", DummyMain)

    # Testmode launch
    nwGUI = nw.main(
        ["--testmode", "--config=%s" % tmpDir, "--data=%s" % tmpDir]
    )
    assert isinstance(nwGUI, DummyMain)

    # Darwin launch
    monkeypatch.setitem(sys.modules, "Foundation", None)
    osDarwin = nw.CONFIG.osDarwin
    nw.CONFIG.osDarwin = True
    nwGUI = nw.main(
        ["--testmode", "--config=%s" % tmpDir, "--data=%s" % tmpDir]
    )
    assert isinstance(nwGUI, DummyMain)
    assert "Foundation" in caplog.messages[1]
    nw.CONFIG.osDarwin = osDarwin

    # Normal launch
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication.__init__", lambda *args: None)
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication.setApplicationName", lambda *args: None)
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication.setApplicationVersion", lambda *args: None)
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication.setWindowIcon", lambda *args: None)
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication.setOrganizationDomain", lambda *args: None)
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication.exec_", lambda *args: 0)
    with pytest.raises(SystemExit) as ex:
        nw.main(["--config=%s" % tmpDir, "--data=%s" % tmpDir])

    assert ex.value.code == 0

    monkeypatch.undo()

# END Test testBaseInit_Launch

@pytest.mark.base
def testBaseInit_Options(monkeypatch, tmpDir):
    """Test command line options for logging level.
    """
    monkeypatch.setattr("nw.guimain.GuiMain", DummyMain)
    monkeypatch.setattr(sys, "argv", [
        "novelWriter.py", "--testmode", "--config=%s" % tmpDir, "--data=%s" % tmpDir
    ])

    # Defaults w/None Args
    nwGUI = nw.main()
    assert nw.logger.getEffectiveLevel() == logging.WARNING
    assert nw.CONFIG.debugInfo is False
    assert nwGUI.closeMain() == "closeMain"

    # Defaults
    nwGUI = nw.main(
        ["--testmode", "--config=%s" % tmpDir, "--data=%s" % tmpDir, "--style=Fusion"]
    )
    assert nw.logger.getEffectiveLevel() == logging.WARNING
    assert nw.CONFIG.debugInfo is False
    assert nwGUI.closeMain() == "closeMain"

    # Log Levels
    nwGUI = nw.main(
        ["--testmode", "--info", "--config=%s" % tmpDir, "--data=%s" % tmpDir]
    )
    assert nw.logger.getEffectiveLevel() == logging.INFO
    assert nw.CONFIG.debugInfo is False
    assert nwGUI.closeMain() == "closeMain"

    nwGUI = nw.main(
        ["--testmode", "--debug", "--config=%s" % tmpDir, "--data=%s" % tmpDir]
    )
    assert nw.logger.getEffectiveLevel() == logging.DEBUG
    assert nw.CONFIG.debugInfo is True
    assert nwGUI.closeMain() == "closeMain"

    nwGUI = nw.main(
        ["--testmode", "--verbose", "--config=%s" % tmpDir, "--data=%s" % tmpDir]
    )
    assert nw.logger.getEffectiveLevel() == 5
    assert nw.CONFIG.debugInfo is True
    assert nwGUI.closeMain() == "closeMain"

    # Help and Version
    with pytest.raises(SystemExit) as ex:
        nwGUI = nw.main(
            ["--testmode", "--help", "--config=%s" % tmpDir, "--data=%s" % tmpDir]
        )
    assert nwGUI.closeMain() == "closeMain"
    assert ex.value.code == 0

    with pytest.raises(SystemExit) as ex:
        nwGUI = nw.main(
            ["--testmode", "--version", "--config=%s" % tmpDir, "--data=%s" % tmpDir]
        )
    assert nwGUI.closeMain() == "closeMain"
    assert ex.value.code == 0

    # Invalid options
    with pytest.raises(SystemExit) as ex:
        nwGUI = nw.main(
            ["--testmode", "--invalid", "--config=%s" % tmpDir, "--data=%s" % tmpDir]
        )
    assert nwGUI.closeMain() == "closeMain"
    assert ex.value.code == 2

    # Project Path
    nwGUI = nw.main(
        ["--testmode", "--config=%s" % tmpDir, "--data=%s" % tmpDir, "sample/"]
    )
    assert nw.CONFIG.cmdOpen == "sample/"
    assert nwGUI.closeMain() == "closeMain"

    monkeypatch.undo()

# END Test testBaseInit_Options

@pytest.mark.base
def testBaseInit_Imports(caplog, monkeypatch, tmpDir):
    """Check import error handling.
    """
    monkeypatch.setattr("nw.guimain.GuiMain", DummyMain)
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication.__init__", lambda *args: None)
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication.exec_", lambda *args: 0)
    monkeypatch.setattr("PyQt5.QtWidgets.QErrorMessage.__init__", lambda *args: None)
    monkeypatch.setattr("PyQt5.QtWidgets.QErrorMessage.resize", lambda *args: None)
    monkeypatch.setattr("PyQt5.QtWidgets.QErrorMessage.showMessage", lambda *args: None)
    monkeypatch.setitem(sys.modules, "lxml", None)
    monkeypatch.setattr("sys.hexversion", 0x0)
    monkeypatch.setattr("nw.CONFIG.verQtValue", 50000)
    monkeypatch.setattr("nw.CONFIG.verPyQtValue", 50000)

    with pytest.raises(SystemExit) as ex:
        _ = nw.main(
            ["--testmode", "--config=%s" % tmpDir, "--data=%s" % tmpDir]
        )

    assert ex.value.code & 4 == 4   # Python version not satisfied
    assert ex.value.code & 8 == 8   # Qt version not satisfied
    assert ex.value.code & 16 == 16 # PyQt version not satisfied
    assert ex.value.code & 32 == 32 # lxml package missing

    assert "At least Python" in caplog.messages[0]
    assert "At least Qt5" in caplog.messages[1]
    assert "At least PyQt5" in caplog.messages[2]
    assert "lxml" in caplog.messages[3]

    monkeypatch.undo()

# END Test testBaseInit_Imports
