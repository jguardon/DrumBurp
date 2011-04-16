'''
Created on 5 Jan 2011

@author: Mike Thomas

'''

from PyQt4 import QtGui, QtCore

from Data.NotePosition import NotePosition
from Data.TimeCounter import counterMaker
from Data import DBConstants

from DBCommands import (ToggleNote,
                        SetRepeatCountCommand,
                        EditMeasurePropertiesCommand,
                        SetAlternateCommand)
from QEditMeasureDialog import QEditMeasureDialog
from QRepeatCountDialog import QRepeatCountDialog
from QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from QMeasureContextMenu import QMeasureContextMenu
from QAlternateDialog import QAlternateDialog


class QMeasure(QtGui.QGraphicsItem):
    '''
    classdocs
    '''


    def __init__(self, index, qScore, measure, parent):
        '''
        Constructor
        '''
        super(QMeasure, self).__init__(parent)
        self._props = qScore.displayProperties
        self._qScore = qScore
        self._measure = None
        self._index = index
        self._width = 0
        self._height = 0
        self._highlight = None
        self._rect = QtCore.QRectF(0, 0, 0, 0)
        self._repeatCountRect = None
        self._startClick = None
        self._alternate = None
        self.setAcceptsHoverEvents(True)
        self.setMeasure(measure)

    def numLines(self):
        return self.parentItem().numLines()

    def lineIndex(self, index):
        return self.parentItem().lineIndex(index)

    def _setDimensions(self):
        self.prepareGeometryChange()
        self._width = self._props.xSpacing * len(self._measure)
        self._height = (self.numLines() + 1) * self._props.ySpacing
        if self._props.beatCountVisible:
            self._height += self._props.ySpacing
        self._rect.setBottomRight(QtCore.QPointF(self._width, self._height))

    def boundingRect(self):
        return self._rect

    def width(self):
        return self._width

    def height(self):
        return self._height

    def setMeasure(self, measure):
        if self._measure != measure:
            self._measure = measure
            self._setDimensions()
            self.update()

    def _paintNotes(self, painter, xValues):
        font = painter.font()
        fontMetric = QtGui.QFontMetrics(font)
        baseline = self.numLines() * self._props.ySpacing
        for drumIndex in range(0, self.numLines()):
            lineHeight = baseline + (self._props.ySpacing / 2.0) - 1
            lineIndex = self.lineIndex(drumIndex)
            for noteTime, x in enumerate(xValues):
                text = self._measure.noteAt(noteTime, lineIndex)
                if text == DBConstants.EMPTY_NOTE:
                    painter.drawLine(x + 1, lineHeight,
                                     x + self._props.xSpacing - 1, lineHeight)
                else:
                    br = fontMetric.tightBoundingRect(text)
                    left = x + (self._props.xSpacing - br.width() + 2) / 2 - 2
                    offset = br.y() - (self._props.ySpacing - br.height()) / 2
                    painter.drawText(QtCore.QPointF(left, baseline - offset),
                                     text)
            baseline -= self._props.ySpacing

    def _paintHighlight(self, painter, xValues):
        noteTime, drumIndex = self._highlight
        baseline = (self.numLines() - drumIndex) * self._props.ySpacing
        countLine = (self.numLines() + 1) * self._props.ySpacing
        x = xValues[noteTime]
        painter.setPen(self.scene().palette().highlight().color())
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(x, baseline,
                         self._props.xSpacing - 1, self._props.ySpacing - 1)
        painter.drawRect(x, countLine,
                         self._props.xSpacing - 1,
                         self._props.ySpacing - 1)
        painter.setPen(self.scene().palette().text().color())

    def _paintBeatCount(self, painter, xValues):
        font = painter.font()
        fontMetric = QtGui.QFontMetrics(font)
        baseline = (self.numLines() + 1) * self._props.ySpacing
        for noteTime, count in enumerate(self._measure.count()):
            x = xValues[noteTime]
            br = fontMetric.tightBoundingRect(count)
            left = x + (self._props.xSpacing - br.width()) / 2 - 2
            offset = br.y() - (self._props.ySpacing - br.height()) / 2
            painter.drawText(QtCore.QPointF(left, baseline - offset), count)

    def _paintRepeatCount(self, painter, font):
        painter.setPen(self.scene().palette().text().color())
        repeatText = '%dx' % self._measure.repeatCount
        textWidth = QtGui.QFontMetrics(font).width(repeatText)
        textLocation = QtCore.QPointF(self.width() - textWidth,
                                      self._props.ySpacing)
        painter.drawText(textLocation, repeatText)
        if self._repeatCountRect is None:
            self._repeatCountRect = QtCore.QRectF(0, 0, 0, 0)
        self._repeatCountRect.setSize(QtCore.QSizeF(textWidth,
                                                    self._props.ySpacing))
        self._repeatCountRect.setTopRight(QtCore.QPointF(self.width(), 0))

    def _paintAlternate(self, painter, font):
        painter.setPen(self.scene().palette().text().color())
        painter.drawLine(0, 0, self.width() - 2, 0)
        painter.drawLine(0, 0, 0, self._props.ySpacing - 2)
        isItalic = font.italic()
        font.setItalic(True)
        painter.setFont(font)
        if self._alternate is None:
            self._alternate = QtCore.QRectF(0, 0, 0, 0)
        text = self._measure.alternateText
        textWidth = QtGui.QFontMetrics(font).width(text)
        self._alternate.setSize(QtCore.QSizeF(textWidth, self._props.ySpacing))
        bottomLeft = QtCore.QPointF(1, self._props.ySpacing - 1)
        self._alternate.setBottomLeft(bottomLeft)
        painter.drawText(1, self._props.ySpacing - 1, text)
        font.setItalic(isItalic)
        painter.setFont(font)

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.save()
        painter.setPen(QtCore.Qt.SolidLine)
        font = self._props.noteFont
        if font is None:
            font = painter.font()
        painter.setFont(font)
        xValues = [noteTime * self._props.xSpacing
                   for noteTime in range(0, len(self._measure))]
        self._paintNotes(painter, xValues)
        if self._props.beatCountVisible:
            self._paintBeatCount(painter, xValues)
        if self._highlight:
            self._paintHighlight(painter, xValues)
        if self._measure.isRepeatEnd() and self._measure.repeatCount > 2:
            self._paintRepeatCount(painter, font)
        else:
            self._repeatCountRect = None
        if self._measure.alternateText is not None:
            self._paintAlternate(painter, font)
        else:
            self._alternate = None
        painter.restore()

    def dataChanged(self, notePosition):
        if None not in (notePosition.noteTime, notePosition.drumIndex):
            self.update()
        else:
            self._setDimensions()
            self.update()
            self.parentItem().placeMeasures()

    def xSpacingChanged(self):
        self._setDimensions()
        self.update()

    def ySpacingChanged(self):
        self._setDimensions()
        self.update()

    def changeRepeatCount(self):
        repDialog = QRepeatCountDialog(self._measure.repeatCount,
                                       self._qScore.parent())
        if (repDialog.exec_()
            and self._measure.repeatCount != repDialog.getValue()):
            command = SetRepeatCountCommand(self._qScore,
                                            self._measurePosition(),
                                            self._measure.repeatCount,
                                            repDialog.getValue())
            self._qScore.addCommand(command)

    def _isOverNotes(self, point):
        return (1 <= (point.y() / self._props.ySpacing)
                < (1 + self.numLines()))

    def _isOverCount(self, point):
        return (point.y() / self._props.ySpacing) > self.numLines() + 1

    def _isOverRepeatCount(self, point):
        return (self._repeatCountRect is not None
                and self._repeatCountRect.contains(point))

    def _isOverAlternate(self, point):
        return (self._alternate is not None
                and self._alternate.contains(point))


    def _getMouseCoords(self, point):
        x = self._getNoteTime(point)
        y = self.numLines() - int(point.y() / self._props.ySpacing)
        return x, y

    def _getNotePosition(self, point):
        x, y = self._getMouseCoords(point)
        y = self.lineIndex(y)
        return x, y

    def _getNoteTime(self, point):
        return int(point.x() / self._props.xSpacing)

    def _hovering(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverNotes(point):
            newPlace = self._getMouseCoords(point)
            if newPlace != self._highlight:
                self._highlight = newPlace
                self.update()
                self.parentItem().setLineHighlight(newPlace[1])
        elif self._highlight != None:
            self._highlight = None
            self.parentItem().clearHighlight()
            self.update()
        if (self._isOverCount(point)
            or self._isOverRepeatCount(point)
            or self._isOverAlternate(point)):
            self.setCursor(QtCore.Qt.PointingHandCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)

    def hoverEnterEvent(self, event):
        self._hovering(event)

    def hoverMoveEvent(self, event):
        self._hovering(event)

    def hoverLeaveEvent(self, event_):
        self._highlight = None
        self.update()
        self.parentItem().clearHighlight()
        self.setCursor(QtCore.Qt.ArrowCursor)

    def toggleNote(self, noteTime, drumIndex, head = None):
        notePosition = self._makeNotePosition(noteTime, drumIndex)
        if head is None:
            head = self._props.head
        command = ToggleNote(self._qScore, notePosition, head)
        self._qScore.addCommand(command)

    def mousePressEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverNotes(point):
            noteTime, drumIndex = self._getNotePosition(point)
            self._notePressEvent(event, noteTime, drumIndex)
        else:
            event.ignore()

    def _notePressEvent(self, event, noteTime, drumIndex):
        menu = None
        if event.button() == QtCore.Qt.MiddleButton:
            event.ignore()
            menu = QMenuIgnoreCancelClick(self._qScore)
            for noteHead in self._props.allowedNoteHeads():
                def noteAction(nh = noteHead):
                    self.toggleNote(noteTime, drumIndex, nh)
                menu.addAction(noteHead, noteAction)
        elif event.button() == QtCore.Qt.RightButton:
            event.ignore()
            menu = QMeasureContextMenu(self._qScore, self,
                                       self._makeNotePosition(noteTime,
                                                              drumIndex),
                                       self._measure.noteAt(noteTime,
                                                            drumIndex),
                                       self._measure.alternateText)
        else:
            self._startClick = (noteTime, drumIndex)
        if menu is not None:
            menu.exec_(event.screenPos())

    def mouseReleaseEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverNotes(point):
            noteTime, drumIndex = self._getNotePosition(point)
            if (event.button() == QtCore.Qt.LeftButton and
                self._startClick == (noteTime, drumIndex)):
                self.toggleNote(noteTime, drumIndex)
            else:
                event.ignore()
        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        point = self.mapFromScene(event.scenePos())
        if self._isOverCount(point):
            self.editMeasureProperties()
        elif self._isOverRepeatCount(point):
            self.changeRepeatCount()
        elif self._isOverAlternate(point):
            self._setAlternate()
        else:
            event.ignore()

    def _makeNotePosition(self, noteTime, drumIndex):
        np = NotePosition(measureIndex = self._index,
                          noteTime = noteTime,
                          drumIndex = drumIndex)
        return self.parentItem().augmentNotePosition(np)

    def _measurePosition(self):
        np = NotePosition(measureIndex = self._index)
        return self.parentItem().augmentNotePosition(np)

    def editMeasureProperties(self):
        numTicks = len(self._measure)
        counter = self._measure.counter
        defBeats = self._props.beatsPerMeasure
        defCounter = self._props.beatCounter
        editDialog = QEditMeasureDialog(self._qScore.parent(),
                                        numTicks,
                                        counter,
                                        defBeats,
                                        defCounter)
        if editDialog.exec_():
            beats, newCounter = editDialog.getValues()
            newCounter = counterMaker(newCounter)
            newTicks = newCounter.beatLength * beats
            if (newCounter != counter
                or newTicks != numTicks):
                command = EditMeasurePropertiesCommand(self._qScore,
                                                       self._measurePosition(),
                                                       beats,
                                                       newCounter)
                self._qScore.addCommand(command)

    def setAlternate(self):
        altDialog = QAlternateDialog(self._measure.alternateText,
                                     self._qScore.parent())
        if (altDialog.exec_()
            and self._measure.alternateText != altDialog.getValue()):
            command = SetAlternateCommand(self._qScore, self._measurePosition(),
                                          altDialog.getValue())
            self._qScore.addCommand(command)
