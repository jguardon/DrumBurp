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
Created on 4 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore
from QStaff import QStaff
from QSection import QSection
from QMeasure import QMeasure
from QMetaData import QMetaData
from QKitData import QKitData
from Data.Score import ScoreFactory
from DBCommands import (MetaDataCommand, ScoreWidthCommand,
                        DeleteMeasureCommand, InsertAndPasteMeasures,
                        ClearMeasureCommand, PasteMeasuresCommand,
                        SetPaperSizeCommand, SetDefaultCountCommand,
                        SetSystemSpacingCommand, InsertMeasuresCommand,
                        SetFontCommand, SetFontSizeCommand,
                        SetVisibilityCommand)
import DBMidi
import functools
_SCORE_FACTORY = ScoreFactory()

def delayCall(method):
    @functools.wraps(method)
    def delayer(*args, **kwargs):
        QtCore.QTimer.singleShot(0, lambda: method(*args, **kwargs))
    return delayer

def _metaDataProperty(varname):
    def _getData(self):
        return getattr(self.score.scoreData, varname)
    def _setData(self, value):
        if getattr(self, varname) != value:
            command = MetaDataCommand(self, varname,
                                      self.metadataChanged, value)
            self.addCommand(command)
    return property(fget = _getData, fset = _setData)


class QScore(QtGui.QGraphicsScene):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        super(QScore, self).__init__(parent)
        self._scale = 1
        self._qStaffs = []
        self._qSections = []
        self._properties = parent.songProperties
        self._score = None
        self._dirty = None
        self._ignoreNext = False
        self.measureClipboard = []
        self._playingMeasure = None
        self._dragStart = None
        self._lastDrag = None
        self._dragSelection = []
        self._dragged = []
        self._undoStack = QtGui.QUndoStack(self)
        self._undoStack.canUndoChanged.connect(self.canUndoChanged)
        self._undoStack.undoTextChanged.connect(self.undoTextChanged)
        self._undoStack.canRedoChanged.connect(self.canRedoChanged)
        self._undoStack.redoTextChanged.connect(self.redoTextChanged)
        self._metaData = QMetaData(self)
        self._metaData.setPos(self.xMargins,
                              self.yMargins)
        self._metaData.setVisible(self._properties.metadataVisible)
        self.metadataChanged.connect(lambda n_, v_: self.reBuild())
        self.paperSizeChanged.connect(parent.setPaperSize)
        self._kitData = QKitData(self)
        self._kitData.setPos(self.xMargins, 0)
        self._kitData.setVisible(self._properties.kitDataVisible)
        if parent.filename is not None:
            if not self.loadScore(parent.filename, quiet = True):
                parent.filename = None
                self.newScore()
        else:
            self.newScore()
        self.defaultCountChanged.connect(parent.setDefaultCount)
        self.spacingChanged.connect(parent.setSystemSpacing)
        self.sectionsChanged.connect(parent.setSections)
        self._properties.connectScore(self)

    canUndoChanged = QtCore.pyqtSignal(bool)
    canRedoChanged = QtCore.pyqtSignal(bool)
    undoTextChanged = QtCore.pyqtSignal(str)
    redoTextChanged = QtCore.pyqtSignal(str)
    metadataChanged = QtCore.pyqtSignal(str, object)
    paperSizeChanged = QtCore.pyqtSignal(str)
    defaultCountChanged = QtCore.pyqtSignal(object)
    spacingChanged = QtCore.pyqtSignal(int)
    sectionsChanged = QtCore.pyqtSignal()
    dragHighlight = QtCore.pyqtSignal(bool)

    def addCommand(self, command):
        self._undoStack.push(command)
        self.dirty = not self._undoStack.isClean()

    def addRepeatedCommand(self, name, command, arguments):
        self._undoStack.beginMacro(name)
        for args in arguments:
            self.addCommand(command(self, *args))
        self._undoStack.endMacro()

    def beginMacro(self, name):
        self._undoStack.beginMacro(name)

    def endMacro(self):
        self._undoStack.endMacro()

    def undo(self):
        self._undoStack.undo()
        self.dirty = not self._undoStack.isClean()

    def redo(self):
        self._undoStack.redo()
        self.dirty = not self._undoStack.isClean()

    def startUp(self):
        self.metadataChanged.emit("width", self.scoreWidth)

    def _getscoreWidth(self):
        if self._score is not None:
            return self._score.scoreData.width
        else:
            return None
    def _setscoreWidth(self, value):
        if self._score is None:
            return
        if self.scoreWidth != value:
            command = ScoreWidthCommand(self, value)
            self.addCommand(command)
    scoreWidth = property(fget = _getscoreWidth,
                          fset = _setscoreWidth)

    artist = _metaDataProperty("artist")
    artistVisible = _metaDataProperty("artistVisible")
    creator = _metaDataProperty("creator")
    creatorVisible = _metaDataProperty("creatorVisible")
    title = _metaDataProperty("title")
    bpm = _metaDataProperty("bpm")
    bpmVisible = _metaDataProperty("bpmVisible")

    @property
    def displayProperties(self):
        return self._properties

    def _getdirty(self):
        return self._dirty
    def _setdirty(self, value):
        if self._dirty != value:
            self._dirty = value
            self.dirtySignal.emit(self._dirty)
    dirty = property(fget = _getdirty, fset = _setdirty)
    dirtySignal = QtCore.pyqtSignal(bool)

    @property
    def kitSize(self):
        return len(self._score.drumKit)

    @property
    def lineOffsets(self):
        yOffsets = [(drumIndex + 1) * self.ySpacing
                    for drumIndex in range(0, self.kitSize)]
        yOffsets.reverse()
        return yOffsets

    def _setScore(self, score):
        if score != self._score:
            score.gridFormatScore(None)
            self._score = score
            if score is not None:
                self.startUp()
            self._score.setCallBack(self.dataChanged)
            self._build()
            self._properties.lineSpacing = self._score.systemSpacing - 101
            self.paperSizeChanged.emit(self._score.paperSize)
            self.defaultCountChanged.emit(self._score.defaultCount)
            self.spacingChanged.emit(self._score.systemSpacing)
            self.sectionsChanged.emit()
            self._properties.newScore(self)
            self._kitData.setVisible(self._properties.kitDataVisible)
            self._metaData.setVisible(self._properties.metadataVisible)
            DBMidi.setKit(score.drumKit)
            self._undoStack.clear()
            self._undoStack.setClean()
            for view in self.views():
                view.setWidth(self.scoreWidth)
            self.reBuild()
            self.dirty = False

    @property
    def score(self):
        return self._score

    def _getscale(self):
        return self._scale
    def _setscale(self, value):
        if self._scale != value:
            self._scale = value
            yOffset = self.yMargins
            self._metaData.setPos(self.xMargins,
                                  yOffset)
            if self._properties.metadataVisible:
                yOffset += self._metaData.boundingRect().height()
            self._kitData.setPos(self.xMargins, yOffset)
            self._build()
            self.invalidate()
    scale = property(fget = _getscale, fset = _setscale)

    @property
    def xSpacing(self):
        return self._properties.xSpacing * self.scale

    @property
    def ySpacing(self):
        return self._properties.ySpacing * self.scale

    @property
    def lineSpacing(self):
        return self._properties.lineSpacing * self.scale

    @property
    def xMargins(self):
        return self._properties.xMargins * self.scale

    @property
    def yMargins(self):
        return self._properties.yMargins * self.scale

    def _build(self):
        self._clearStaffs()
        for staff in self._score.iterStaffs():
            self._addStaff(staff)
        for title in self._score.iterSections():
            self._addSection(title)
        self._placeStaffs()

    @delayCall
    def reBuild(self):
        self._score.gridFormatScore(None)
        self._build()
        self.invalidate()

    def checkFormatting(self):
        if self._score.gridFormatScore(None):
            self.reBuild()

    def __iter__(self):
        return iter(self._qStaffs)

    def _clearStaffs(self):
        for qStaff in self._qStaffs:
            self.removeItem(qStaff)
        self._qStaffs = []
        for qSection in self._qSections:
            self.removeItem(qSection)
        self._qSections = []

    def _addStaff(self, staff):
        qStaff = QStaff(staff, len(self._qStaffs), self)
        self._qStaffs.append(qStaff)

    def _addSection(self, title):
        qSection = QSection(title, qScore = self)
        qSection.setIndex(len(self._qSections))
        self._qSections.append(qSection)

    def setSectionTitle(self, index, title):
        qSection = self._qSections[index]
        qSection.setTitle(title)

    def setPaperSize(self, newPaperSize):
        if newPaperSize != self._score.paperSize:
            command = SetPaperSizeCommand(self,
                                          newPaperSize)
            self.addCommand(command)

    def getQSection(self, sectionIndex):
        if 0 <= sectionIndex < len(self._qSections):
            return self._qSections[sectionIndex]

    def _getdefaultCount(self):
        return self._score.defaultCount
    def _setdefaultCount(self, newCount):
        if newCount != self._score.defaultCount:
            command = SetDefaultCountCommand(self, newCount)
            self.addCommand(command)
    defaultCount = property(_getdefaultCount,
                            _setdefaultCount)

    def _getsystemSpacing(self):
        return self._score.systemSpacing
    def _setsystemSpacing(self, value):
        if self._score.systemSpacing != value:
            command = SetSystemSpacingCommand(self, value)
            self.addCommand(command)
    systemSpacing = property(_getsystemSpacing, _setsystemSpacing)

    def _placeStaffs(self, staffCall = QStaff.placeMeasures):
        xMargins = self.xMargins
        yMargins = self.yMargins
        lineSpacing = self.lineSpacing
        yOffset = self.yMargins
        if self._properties.metadataVisible:
            yOffset += self._metaData.boundingRect().height()
        if self._properties.kitDataVisible:
            self._kitData.setY(yOffset)
            yOffset += self._kitData.boundingRect().height()
        newSection = True
        sectionIndex = 0
        maxWidth = 0
        for qStaff in self:
            if newSection:
                newSection = False
                if sectionIndex < len(self._qSections):
                    qSection = self._qSections[sectionIndex]
                    sectionIndex += 1
                    qSection.setPos(xMargins, yOffset)
                    yOffset += qSection.boundingRect().height()
            newSection = qStaff.isSectionEnd()
            qStaff.setPos(xMargins, yOffset)
            if staffCall is not None:
                staffCall(qStaff)
            yOffset += qStaff.height() + lineSpacing
            maxWidth = max(maxWidth, qStaff.width())
            newSection = qStaff.isSectionEnd()
        self.setSceneRect(0, 0,
                          maxWidth + 2 * xMargins,
                          yOffset - lineSpacing + yMargins)

    def xSpacingChanged(self):
        self._placeStaffs(QStaff.xSpacingChanged)

    def ySpacingChanged(self):
        self._placeStaffs(QStaff.ySpacingChanged)

    def lineSpacingChanged(self):
        self._placeStaffs(None)

    def sectionFontChanged(self):
        self._metaData.fontChanged()
        for qsection in self._qSections:
            qsection.setFont(self._properties.sectionFont)
        self.lineSpacingChanged()

    def metadataVisibilityChanged(self):
        self._metaData.setVisible(self._properties.metadataVisible)
        self.reBuild()

    def metadataFontChanged(self):
        self._metaData.fontChanged()
        self.lineSpacingChanged()

    def kitDataVisibleChanged(self):
        self._kitData.setVisible(self._properties.kitDataVisible)
        self.reBuild()

    def dataChanged(self, notePosition):
        staff = self._qStaffs[notePosition.staffIndex]
        staff.dataChanged(notePosition)

    def ignoreNextClick(self):
        self._ignoreNext = True

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos())
        if not isinstance(item, QMeasure):
            self.clearDragSelection()
        event.ignore()
        if self._ignoreNext:
            self._ignoreNext = False
        else:
            super(QScore, self).mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.clearDragSelection()
        event.ignore()
        return super(QScore, self).keyPressEvent(event)

    def copyMeasures(self, np = None):
        if np is not None:
            self.measureClipboard = [self._score.copyMeasure(np)]
        elif self.hasDragSelection():
            self.measureClipboard = [self._score.copyMeasure(dragNP)
                                     for (unusedMeasure, unusedIndex, dragNP)
                                     in self.iterDragSelection()]

    def clearMeasures(self, np = None):
        if np is not None:
            command = ClearMeasureCommand(self, [np])
        else:
            command = ClearMeasureCommand(self,
                                          [dragNP for (unusedMeasure,
                                                       unusedIndex,
                                                       dragNP)
                                           in self.iterDragSelection()])
        self.addCommand(command)

    def deleteMeasures(self, np = None):
        if np is not None:
            command = DeleteMeasureCommand(self, np)
            self.addCommand(command)
        else:
            if not self.hasDragSelection():
                return
            start = self._dragSelection[0]
            measureIndex = self._score.getMeasureIndex(start)
            self.beginMacro("delete measures")
            for unused in self.iterDragSelection():
                command = DeleteMeasureCommand(self, start, measureIndex)
                self.addCommand(command)
            self.endMacro()

    @delayCall
    def insertMeasures(self, np):
        if len(self.measureClipboard) > 0:
            command = InsertAndPasteMeasures(self, np, self.measureClipboard)
            self.addCommand(command)

    @delayCall
    def pasteMeasuresOver(self, repeating = False):
        if len(self.measureClipboard) == 0 or not self.hasDragSelection():
            return
        start = self._dragSelection[0]
        measureIndex = self._score.getMeasureIndex(start)
        sourceLength = len(self.measureClipboard)
        targetLength = len(list(self.iterDragSelection()))
        self.beginMacro("paste over measures")
        measureCount = 0
        clearPositions = []
        if repeating:
            resultLength = targetLength
            while measureCount < resultLength:
                clearPositions.append(self.score.getMeasurePosition(measureIndex + measureCount))
                measureCount += 1
            command = ClearMeasureCommand(self, clearPositions)
            self.addCommand(command)
            measureData = []
            while len(measureData) < resultLength:
                measureData.extend(self.measureClipboard)
            measureData = measureData[:targetLength]
        else:
            resultLength = min([sourceLength, targetLength])
            while measureCount < resultLength:
                clearPositions.append(self.score.getMeasurePosition(measureIndex + measureCount))
                measureCount += 1
            command = ClearMeasureCommand(self, clearPositions)
            self.addCommand(command)
            while measureCount < targetLength:
                deletePosition = self.score.getMeasurePosition(measureIndex + sourceLength)
                command = DeleteMeasureCommand(self, deletePosition, measureIndex + sourceLength)
                self.addCommand(command)
                measureCount += 1
            if measureCount < sourceLength:
                command = InsertMeasuresCommand(self,
                                                self.score.getMeasurePosition(measureIndex + measureCount),
                                                sourceLength - measureCount,
                                                self.defaultCount)
                self.addCommand(command)
            measureData = self.measureClipboard
            measureData = measureData[:sourceLength]
        command = PasteMeasuresCommand(self, start, measureData)
        self.addCommand(command)
        self.endMacro()

    def changeRepeatCount(self, np):
        qStaff = self._qStaffs[np.staffIndex]
        qStaff.changeRepeatCount(np)

    def loadScore(self, filename, quiet = False):
        try:
            newScore = _SCORE_FACTORY(filename = filename)
        except IOError, exc:
            if not quiet:
                msg = "Error loading DrumBurp file %s" % filename
                QtGui.QMessageBox.warning(self.parent(),
                                          "Score load error",
                                          msg + "\n" + str(exc))
            return False
        except StandardError, exc:
            raise
        self._setScore(newScore)
        return True

    def saveScore(self, filename):
        try:
            _SCORE_FACTORY.saveScore(self._score, filename)
        except StandardError, exc:
            msg = "Error saving DrumBurp file: %s" % str(exc)
            QtGui.QMessageBox.warning(self.parent(),
                                      "Score save error",
                                      msg)
            return False
        self._undoStack.setClean()
        self.dirty = False
        return True

    def newScore(self, numMeasures = 16,
                 counter = None):
        if counter is None:
            if self._score is None:
                counter = None
            else:
                counter = self.defaultCount
        newScore = _SCORE_FACTORY(numMeasures = numMeasures,
                                  counter = counter)
        self._setScore(newScore)

    def printScore(self, qprinter, scoreView):
        painter = QtGui.QPainter(qprinter)
        rect = qprinter.pageRect()
        printerDpi = float(qprinter.resolution())
        painter.save()
        painter.setFont(self._properties.metadataFont)
        fm = QtGui.QFontMetrics(painter.font())
        self._metaData.setRect(fm)
        painter.setFont(self._properties.noteFont)
        fm = QtGui.QFontMetrics(painter.font())
        self._kitData.setRect(fm)
        painter.restore()
        self.scale = printerDpi / scoreView.logicalDpiX()
        painter.save()
        painter.setFont(self._properties.sectionFont)
        for qSection in self._qSections:
            qSection.setFont(painter.font())
        painter.restore()
        self._placeStaffs()
        topLeft = QtCore.QPointF(self.xMargins, self.yMargins)
        bottomRight = QtCore.QPointF(self.sceneRect().right() - self.xMargins,
                                     self.yMargins)
        for staff in self._qStaffs:
            newBottom = staff.y() + staff.height()
            if newBottom - topLeft.y() > rect.height():
                sceneRect = QtCore.QRectF(topLeft, bottomRight)
                if sceneRect.width() > rect.width():
                    sceneRect.setWidth(rect.width())
                pageRect = QtCore.QRectF(0, 0,
                                         sceneRect.width(), sceneRect.height())
                self.render(painter, pageRect, sceneRect)
                qprinter.newPage()
                topLeft.setY(bottomRight.y() + self.lineSpacing)
            bottomRight.setY(newBottom)
        sceneRect = QtCore.QRectF(topLeft, bottomRight)
        if sceneRect.width() > rect.width():
            sceneRect.setWidth(rect.width())
        pageRect = QtCore.QRectF(0, 0, sceneRect.width(), sceneRect.height())
        self.render(painter, pageRect, sceneRect)
        painter.end()
        self._metaData.setRect()
        self._kitData.setRect()
        self.scale = 1

    def setScoreFontSize(self, size, fontType):
        fontName = fontType + "FontSize"
        if size == getattr(self._properties, fontName):
            return
        command = SetFontSizeCommand(self, size, fontType)
        self.addCommand(command)

    def setScoreFont(self, font, fontType):
        fontName = fontType + "Font"
        if self._properties is not None:
            fontFamily = getattr(self._properties, fontName)
            if fontFamily is None:
                setattr(self._properties, fontName, font)
                return
            elif font.family() == fontFamily.family():
                return
        command = SetFontCommand(self, font, fontType)
        self.addCommand(command)

    def setElementVisibility(self, onOff, elementName, text):
        element = elementName + "Visible"
        if getattr(self._properties, element) == onOff:
            return
        command = SetVisibilityCommand(self, onOff, elementName, text)
        self.addCommand(command)

    def getQMeasure(self, position):
        return self._qStaffs[position.staffIndex].getQMeasure(position)

    def highlightPlayingMeasure(self, position):
        if position == self._playingMeasure:
            return
        if self._playingMeasure != None:
            qMeasure = self.getQMeasure(self._playingMeasure)
            qMeasure.setPlaying(False)
        self._playingMeasure = position
        if self._playingMeasure == None:
            return
        qMeasure = self.getQMeasure(self._playingMeasure)
        qMeasure.setPlaying(True)

    def changeKit(self, kit, changes):
        self.score.changeKit(kit, changes)
        DBMidi.setKit(kit)
        self.reBuild()
        self.dirty = True

    def startDragging(self, qmeasure):
        self._dragStart = qmeasure
        self._lastDrag = qmeasure
        self._dragSelection = [qmeasure.makeNotePosition(None, None),
                               qmeasure.makeNotePosition(None, None)]
        self._dragged = []
        self._updateDragged()
        self.dragHighlight.emit(True)

    def _updateDragged(self):
        if not self.hasDragSelection():
            for index, position in self._dragged:
                # Turn off
                self.setDragHighlight(position, False)
            self._dragged = []
            return
        newDragged = [(index, position) for (unused, index, position) in
                      self.score.iterMeasuresBetween(*self._dragSelection)]
        for index, position in newDragged:
            if all(x[0] != index for x in self._dragged): # Turn on
                self.setDragHighlight(position, True)
        for index, position in self._dragged:
            if all(x[0] != index for x in newDragged): # Turn off
                self.setDragHighlight(position, False)
        self._dragged = newDragged

    def dragging(self, qmeasure):
        if self._dragStart is None:
            self.startDragging(qmeasure)
        elif self._lastDrag != qmeasure:
            self._lastDrag = qmeasure
            self._dragSelection[1] = self._lastDrag.makeNotePosition(None, None)
            self._updateDragged()

    def isDragging(self):
        return self._dragStart is not None

    def endDragging(self):
        self._dragStart = None
        self._lastDrag = None

    def hasDragSelection(self):
        return len(self._dragSelection) == 2

    def iterDragSelection(self):
        if self.hasDragSelection():
            return self.score.iterMeasuresBetween(*self._dragSelection)
        else:
            return iter([])

    def clearDragSelection(self):
        self._dragSelection = []
        self._updateDragged()
        self.dragHighlight.emit(False)

    def setDragHighlight(self, position, onOff):
        staff = self._qStaffs[position.staffIndex]
        qmeasure = staff.getQMeasure(position)
        qmeasure.setDragHighlight(onOff)

    def inDragSelection(self, np):
        if not self.hasDragSelection():
            return False
        start, end = self._dragSelection
        return ((start.staffIndex == np.staffIndex
                 and start.measureIndex <= np.measureIndex
                 and (np.staffIndex < end.staffIndex or
                      np.measureIndex <= end.measureIndex))
                or (start.staffIndex < np.staffIndex < end.staffIndex)
                or (np.staffIndex == end.staffIndex
                    and np.measureIndex <= end.measureIndex))

    def metaChange(self):
        return _metaChangeContext(self, self._metaData)

class _metaChangeContext(object):
    def __init__(self, qScore, metaData):
        self._qScore = qScore
        self._metaData = metaData
        self._metaSize = metaData.boundingRect().height()
    def __enter__(self):
        return self
    def __exit__(self, excType, excValue, excTraceback):
        self._metaData.update()
        if self._metaData.boundingRect().height() != self._metaSize:
            self._qScore.reBuild()
        return False
