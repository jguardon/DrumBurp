'''
Created on 31 Jul 2010

@author: Mike Thomas

'''

from ui_drumburp import Ui_DrumBurpWindow
from PyQt4.QtGui import (QMainWindow, QFontDatabase,
                         QFileDialog, QMessageBox,
                         QPrintPreviewDialog, QWhatsThis)
from PyQt4.QtCore import QTimer, pyqtSignature, SIGNAL, QSettings, QVariant
from QScore import QScore
from QDisplayProperties import QDisplayProperties
from QNewScoreDialog import QNewScoreDialog
from QAsciiExportDialog import QAsciiExportDialog
import DBUtility
from Data.TimeCounter import counterMaker
import DBIcons
import os

APPNAME = "DrumBurp"
#pylint:disable-msg=R0904
class DrumBurp(QMainWindow, Ui_DrumBurpWindow):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(DrumBurp, self).__init__(parent)
        self._state = None
        self.setupUi(self)
        DBIcons.initialiseIcons()
        settings = QSettings()
        self.recentFiles = [unicode(fname) for fname in
                            settings.value("RecentFiles").toStringList()]
        self.filename = (None
                         if len(self.recentFiles) == 0
                         else self.recentFiles[0])
        self.updateRecentFiles()
        self.songProperties = QDisplayProperties(settings)
        self.scoreScene = QScore(self)
        self.scoreView.setScene(self.scoreScene)
        self.fontComboBox.setWritingSystem(QFontDatabase.Latin)
        xValue, yValue, lValue = self.songProperties.proportionalSpacing()
        QTimer.singleShot(0, lambda: self.spaceSlider.setValue(xValue))
        QTimer.singleShot(0, lambda: self.verticalSlider.setValue(yValue))
        QTimer.singleShot(0, lambda: self.lineSpaceSlider.setValue(lValue))
        QTimer.singleShot(0, self.scoreView.startUp)
        self.beatsSpinBox.setValue(self.songProperties.beatsPerMeasure)
        DBUtility.populateCounterCombo(self.beatCountComboBox,
                                       self.songProperties.beatCounter)
        font = self.scoreScene.font()
        self.fontComboBox.setCurrentFont(font)
        self.connect(self.scoreScene, SIGNAL("dirty"), self.setWindowModified)
        beatsChanged = self.songProperties.measureBeatsChanged
        self.connect(self.beatsSpinBox, SIGNAL("valueChanged(int)"),
                                               beatsChanged)
        self.updateStatus("Welcome to %s" % APPNAME)
        self.restoreGeometry(settings.value("Geometry").toByteArray())
        self.restoreState(settings.value("MainWindow/State").toByteArray())

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        if self.filename is not None:
            self.setWindowTitle("DrumBurp - %s[*]"
                                % os.path.basename(self.filename))
        else:
            self.setWindowTitle("DrumBurp - Untitled[*]")
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
            settings = QSettings()
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
            directory = ""
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
                directory = os.path.join(os.path.dirname(self.recentFiles[-1]),
                                         suggestion)
            else:
                directory = suggestion
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
            beats = self.songProperties.beatsPerMeasure
            counter = self.songProperties.beatCounter
            dialog = QNewScoreDialog(self.parent(),
                                     beats,
                                     counter)
            if dialog.exec_():
                nMeasures, beats, counter = dialog.getValues()
                counter = counterMaker(counter)
                mWidth = beats * counter.beatLength
                self.scoreScene.newScore(numMeasures = nMeasures,
                                         measureWidth = mWidth,
                                         counter = counter)
                self.filename = None
                self.updateRecentFiles()
                self.beatsSpinBox.setValue(beats)
                DBUtility.populateCounterCombo(self.beatCountComboBox,
                                               counter)
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
                def openRecentFile(filename = fname):
                    if not self.okToContinue():
                        return
                    if self.scoreScene.loadScore(filename):
                        self.filename = filename
                        self.updateStatus("Successfully loaded %s" % filename)
                        self.addToRecentFiles()
                        self.updateRecentFiles()
                action = self.menuRecentScores.addAction(fname)
                action.setIcon(DBIcons.getIcon("score"))
                self.connect(action, SIGNAL("triggered()"),
                             openRecentFile)

    @pyqtSignature("int")
    def on_beatCountComboBox_currentIndexChanged(self, index):
        if index == -1:
            return
        counter = self.beatCountComboBox.itemData(index)
        counter = counter.toInt()[0]
        counter = counterMaker(counter)
        self.songProperties.beatCounter = counter

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
        fname = self.filename if self.filename is not None else ""
        if os.path.splitext(fname)[-1] == '.brp':
            fname = os.path.splitext(fname)[0] + '.txt'
        asciiDialog = QAsciiExportDialog(fname, self)
        if not asciiDialog.exec_():
            return
        fname = asciiDialog.getFilename()
        options = asciiDialog.getOptions()
        try:
            with open(fname, 'w') as txtHandle:
                self.scoreScene.score.exportASCII(txtHandle, options)
        except StandardError:
            QMessageBox.warning(self.parent(), "Export failed!",
                                "Could not export to " + fname)
            raise
        else:
            self.updateStatus("Successfully exported ASCII to " + fname)


    @pyqtSignature("")
    def on_actionPrint_triggered(self):
        dialog = QPrintPreviewDialog(self)
        self.connect(dialog, SIGNAL("paintRequested(QPrinter *)"),
                     self.scoreScene.printScore)
        dialog.exec_()

    @pyqtSignature("")
    def on_actionWhatsThis_triggered(self):
        QWhatsThis.enterWhatsThisMode()
