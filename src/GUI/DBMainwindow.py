# Copyright 2011 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

from ui_drumburp import Ui_DrumBurpWindow
from PyQt4.QtGui import (QMainWindow, QFontDatabase,
                         QFileDialog, QMessageBox,
                         QPrintPreviewDialog, QWhatsThis,
                         QPrinterInfo,
                         QPrinter, QDesktopServices)
from PyQt4.QtCore import pyqtSignature, QSettings, QVariant, QTimer
from QScore import QScore
from QDisplayProperties import QDisplayProperties
from QNewScoreDialog import QNewScoreDialog
from QAsciiExportDialog import QAsciiExportDialog
from QComplexCountDialog import QComplexCountDialog
from DBInfoDialog import DBInfoDialog
from DBStartupDialog import DBStartupDialog
import Data.MeasureCount
import DBIcons
import os

APPNAME = "DrumBurp"
DB_VERSION = "0.1"
#pylint:disable-msg=R0904

class FakeQSettings(object):
    def value(self, key_):
        return QVariant()

    def setValue(self, key_, value_):
        return


class DrumBurp(QMainWindow, Ui_DrumBurpWindow):
    '''
    classdocs
    '''

    def __init__(self, parent = None, fakeStartup = False, filename = None):
        '''
        Constructor
        '''
        self._fakeStartup = fakeStartup
        super(DrumBurp, self).__init__(parent)
        self._state = None
        self._asciiSettings = None
        self._printer = QPrinter()
        self.setupUi(self)
        DBIcons.initialiseIcons()
        self.paperBox.clear()
        for name in dir(QPrinter):
            if isinstance(getattr(QPrinter, name), QPrinter.PageSize):
                self.paperBox.addItem(name)
        settings = self._makeQSettings()
        self.recentFiles = [unicode(fname) for fname in
                            settings.value("RecentFiles").toStringList()
                            if os.path.exists(unicode(fname))]
        if filename is None:
            filename = (None
                        if len(self.recentFiles) == 0
                        else self.recentFiles[0])
        self.filename = filename
        self.addToRecentFiles()
        self.updateRecentFiles()
        self.songProperties = QDisplayProperties()
        self.scoreScene = QScore(self)
        self.scoreView.setScene(self.scoreScene)
        self.fontComboBox.setWritingSystem(QFontDatabase.Latin)
        self.sectionFontCombo.setWritingSystem(QFontDatabase.Latin)
        self.sectionFontSizeSpinbox.setValue(self.songProperties.
                                             sectionFontSize)
        self.sectionFontCombo.setWritingSystem(QFontDatabase.Latin)
        self.sectionFontSizeSpinbox.setValue(self.songProperties.
                                             metadataFontSize)
        self.lineSpaceSlider.setValue(10)
        self.scoreView.startUp()
        font = self.scoreScene.font()
        self.fontComboBox.setCurrentFont(font)
        self.noteSizeSpinBox.setValue(9)
        self.noteSizeSpinBox.setValue(10)
        self.sectionFontCombo.setCurrentFont(font)
        self.sectionFontSizeSpinbox.setValue(19)
        self.sectionFontSizeSpinbox.setValue(20)
        self.metadataFontCombo.setCurrentFont(font)
        self.metadataFontSizeSpinbox.setValue(19)
        self.metadataFontSizeSpinbox.setValue(20)
        self.scoreScene.dirtySignal.connect(self.setWindowModified)
        self.actionUndo.setEnabled(False)
        self.actionRedo.setEnabled(False)
        self.scoreScene.canUndoChanged.connect(self.actionUndo.setEnabled)
        changeUndoText = lambda txt:self.actionUndo.setText("Undo " + txt)
        self.scoreScene.undoTextChanged.connect(changeUndoText)
        self.scoreScene.canRedoChanged.connect(self.actionRedo.setEnabled)
        changeRedoText = lambda txt:self.actionRedo.setText("Redo " + txt)
        self.scoreScene.redoTextChanged.connect(changeRedoText)
        self.defaultMeasureTabs.beatChanged.connect(self._beatChanged)
        self.defaultMeasureTabs.setup(None,
                                      self.songProperties.counterRegistry,
                                      Data.MeasureCount,
                                      QComplexCountDialog)
        self.restoreGeometry(settings.value("Geometry").toByteArray())
        self.restoreState(settings.value("MainWindow/State").toByteArray())
        QTimer.singleShot(0, self._startUp)

    def _startUp(self):
        dlg = DBStartupDialog(DB_VERSION)
        dlg.exec_()
        self.updateStatus("Welcome to %s v%s" % (APPNAME, DB_VERSION))


    def _makeQSettings(self):
        if self._fakeStartup:
            return FakeQSettings()
        else:
            return QSettings()

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        if self.filename is not None:
            self.setWindowTitle("DrumBurp v%s - %s[*]"
                                % (DB_VERSION, os.path.basename(self.filename)))
        else:
            self.setWindowTitle("DrumBurp v%s - Untitled[*]" % DB_VERSION)
        self.setWindowModified(self.scoreScene.dirty)

    def okToContinue(self):
        if self.scoreScene.dirty:
            reply = QMessageBox.question(self,
                                         "DrumBurp - Unsaved Changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes,
                                         QMessageBox.No,
                                         QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                if not self.fileSave():
                    msg = ("DrumBurp could not save the file."
                           "\n\n"
                           "Continue anyway? "
                           "All unsaved changes will be lost!")
                    failReply = QMessageBox.warning(self,
                                                    "Failed Save!",
                                                    msg,
                                                    QMessageBox.Yes,
                                                    QMessageBox.No)
                    return failReply == QMessageBox.Yes
        return True

    def closeEvent(self, event):
        if self.okToContinue():
            settings = self._makeQSettings()
            settings.setValue("RecentFiles",
                              QVariant(self.recentFiles))
            settings.setValue("Geometry",
                              QVariant(self.saveGeometry()))
            settings.setValue("MainWindow/State",
                              QVariant(self.saveState()))
            self.songProperties.save(settings)
        else:
            event.ignore()

    @pyqtSignature("")
    def on_actionFitInWindow_triggered(self):
        widthInPixels = self.scoreView.width()
        maxColumns = self.songProperties.maxColumns(widthInPixels)
        self.widthSpinBox.setValue(maxColumns)

    @pyqtSignature("")
    def on_actionLoad_triggered(self):
        if not self.okToContinue():
            return
        caption = "Choose a DrumBurp file to open"
        directory = self.filename
        if len(self.recentFiles) > 0:
            directory = os.path.dirname(self.recentFiles[-1])
        else:
            directory = QDesktopServices.storageLocation(QDesktopServices.HomeLocation)
        fname = QFileDialog.getOpenFileName(parent = self,
                                            caption = caption,
                                            directory = directory,
                                            filter = "DrumBurp files (*.brp)")
        if len(fname) == 0:
            return
        if self.scoreScene.loadScore(fname):
            self.filename = unicode(fname)
            self.updateStatus("Successfully loaded %s" % self.filename)
            self.addToRecentFiles()
            self.updateRecentFiles()

    def _getFileName(self):
        directory = self.filename
        if directory is None:
            suggestion = unicode(self.scoreScene.title)
            if len(suggestion) == 0:
                suggestion = "Untitled"
            suggestion = os.extsep.join([suggestion, "brp"])
            if len(self.recentFiles) > 0:
                directory = os.path.dirname(self.recentFiles[-1])
            else:
                directory = str(QDesktopServices.storageLocation(QDesktopServices.HomeLocation))
            directory = os.path.join(directory,
                                     suggestion)
        if os.path.splitext(directory)[-1] == os.extsep + 'brp':
            directory = os.path.splitext(directory)[0]
        caption = "Choose a DrumBurp file to save"
        fname = QFileDialog.getSaveFileName(parent = self,
                                            caption = caption,
                                            directory = directory,
                                            filter = "DrumBurp files (*.brp)")
        if len(fname) == 0 :
            return False
        self.filename = unicode(fname)
        return True

    def fileSave(self):
        if self.filename is None:
            if not self._getFileName():
                return False
            self.addToRecentFiles()
            self.updateRecentFiles()
        return self.scoreScene.saveScore(self.filename)

    @pyqtSignature("")
    def on_actionSave_triggered(self):
        if self.fileSave():
            self.updateStatus("Successfully saved %s" % self.filename)

    @pyqtSignature("")
    def on_actionSaveAs_triggered(self):
        if self._getFileName():
            self.scoreScene.saveScore(self.filename)
            self.updateStatus("Successfully saved %s" % self.filename)
            self.addToRecentFiles()
            self.updateRecentFiles()

    @pyqtSignature("")
    def on_actionNew_triggered(self):
        if self.okToContinue():
            counter = self.songProperties.defaultCounter
            registry = self.songProperties.counterRegistry
            dialog = QNewScoreDialog(self.parent(),
                                     counter,
                                     registry)
            if dialog.exec_():
                nMeasures, counter = dialog.getValues()
                self.scoreScene.newScore(numMeasures = nMeasures,
                                         counter = counter)
                self.filename = None
                self.updateRecentFiles()
                self.defaultMeasureTabs.setBeat(counter)
                self.updateStatus("Created a new blank score")

    def addToRecentFiles(self):
        if self.filename is not None:
            if self.filename in self.recentFiles:
                self.recentFiles.remove(self.filename)
            self.recentFiles.insert(0, self.filename)
            if len(self.recentFiles) > 10:
                self.recentFiles.pop()

    def updateRecentFiles(self):
        self.menuRecentScores.clear()
        for fname in self.recentFiles:
            if fname != self.filename and os.path.exists(fname):
                def openRecentFile(bool_, filename = fname):
                    if not self.okToContinue():
                        return
                    if self.scoreScene.loadScore(filename):
                        self.filename = filename
                        self.updateStatus("Successfully loaded %s" % filename)
                        self.addToRecentFiles()
                        self.updateRecentFiles()
                action = self.menuRecentScores.addAction(fname)
                action.setIcon(DBIcons.getIcon("score"))
                action.triggered.connect(openRecentFile)

    def _beatChanged(self):
        counter = self.defaultMeasureTabs.getCounter()
        if counter != self.songProperties.defaultCounter:
            self.songProperties.defaultCounter = counter

    def hideEvent(self, event):
        self._state = self.saveState()
        super(DrumBurp, self).hideEvent(event)

    def showEvent(self, event):
        if self._state is not None:
            self.restoreState(self._state)
            self._state = None
        super(DrumBurp, self).showEvent(event)

    @pyqtSignature("")
    def on_actionExportASCII_triggered(self):
        fname = self.filename
        if self.filename is None:
            fname = QDesktopServices.storageLocation(QDesktopServices.HomeLocation)
            fname = os.path.join(str(fname), 'Untitled.txt')
        if os.path.splitext(fname)[-1] == '.brp':
            fname = os.path.splitext(fname)[0] + '.txt'
        self._asciiSettings = self.songProperties.generateAsciiSettings(self._asciiSettings)
        asciiDialog = QAsciiExportDialog(fname, self,
                                         settings = self._asciiSettings)
        if not asciiDialog.exec_():
            return
        fname = asciiDialog.getFilename()
        self._asciiSettings = asciiDialog.getOptions()
        try:
            with open(fname, 'w') as txtHandle:
                self.scoreScene.score.exportASCII(txtHandle, self._asciiSettings)
        except StandardError:
            QMessageBox.warning(self.parent(), "Export failed!",
                                "Could not export to " + fname)
            raise
        else:
            self.updateStatus("Successfully exported ASCII to " + fname)

    @pyqtSignature("")
    def on_actionPrint_triggered(self):
        self._printer = QPrinter(QPrinterInfo(self._printer),
                                 QPrinter.HighResolution)
        self._printer.setPaperSize(self._getPaperSize())
        dialog = QPrintPreviewDialog(self._printer, parent = self)
        def updatePages(qprinter):
            self.scoreScene.printScore(qprinter, self.scoreView)
        dialog.paintRequested.connect(updatePages)
        dialog.exec_()

    @pyqtSignature("")
    def on_actionExportPDF_triggered(self):
        try:
            printer = QPrinter(mode = QPrinter.HighResolution)
            printer.setPaperSize(self._getPaperSize())
            if self.filename:
                outfileName = list(os.path.splitext(self.filename)[:-1])
                outfileName = os.extsep.join(outfileName + ["pdf"])
            else:
                outfileName = "Untitled.pdf"
            printer.setOutputFileName(outfileName)
            printer.setPaperSize(self._getPaperSize())
            dialog = QPrintPreviewDialog(printer, parent = self)
            def updatePages(qprinter):
                self.scoreScene.printScore(qprinter, self.scoreView)
            dialog.paintRequested.connect(updatePages)
            dialog.exec_()
            self.updateStatus("Exported to PDF %s" % outfileName)
        except StandardError:
            QMessageBox.warning(self.parent(), "Export failed!",
                                "Could not export PDF to " + outfileName)


    @pyqtSignature("")
    def on_actionWhatsThis_triggered(self):
        QWhatsThis.enterWhatsThisMode()

    @pyqtSignature("")
    def on_actionUndo_triggered(self):
        self.scoreScene.undo()

    @pyqtSignature("")
    def on_actionRedo_triggered(self):
        self.scoreScene.redo()

    @pyqtSignature("")
    def on_actionAboutDrumBurp_triggered(self):
        dlg = DBInfoDialog(DB_VERSION)
        dlg.exec_()

    def _getPaperSize(self):
        return getattr(QPrinter, str(self.paperBox.currentText()))

    @pyqtSignature("")
    def on_actionFitPage_triggered(self):
        papersize = self._getPaperSize()
        printer = QPrinter()
        printer.setPaperSize(papersize)
        widthInPixels = printer.pageRect().width()
        maxColumns = self.songProperties.maxColumns(widthInPixels)
        self.widthSpinBox.setValue(maxColumns)
