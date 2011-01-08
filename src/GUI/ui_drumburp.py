# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\drumburp.ui'
#
# Created: Sat Jan 08 13:31:24 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DrumBurpWindow(object):
    def setupUi(self, DrumBurpWindow):
        DrumBurpWindow.setObjectName(_fromUtf8("DrumBurpWindow"))
        DrumBurpWindow.resize(800, 600)
        DrumBurpWindow.setAnimated(True)
        self.centralwidget = QtGui.QWidget(DrumBurpWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.scoreView = ScoreView(self.centralwidget)
        self.scoreView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.scoreView.setAcceptDrops(False)
        self.scoreView.setLineWidth(1)
        self.scoreView.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scoreView.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.scoreView.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.scoreView.setObjectName(_fromUtf8("scoreView"))
        self.gridLayout_2.addWidget(self.scoreView, 0, 0, 1, 1)
        DrumBurpWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DrumBurpWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        DrumBurpWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DrumBurpWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DrumBurpWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(DrumBurpWindow)
        self.toolBar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.toolBar.setMovable(True)
        self.toolBar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        DrumBurpWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.noteHeadDock = QtGui.QDockWidget(DrumBurpWindow)
        self.noteHeadDock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.noteHeadDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.noteHeadDock.setObjectName(_fromUtf8("noteHeadDock"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.defaultNoteHeadButton = RadioButtonTeller(self.dockWidgetContents)
        self.defaultNoteHeadButton.setChecked(True)
        self.defaultNoteHeadButton.setObjectName(_fromUtf8("defaultNoteHeadButton"))
        self.verticalLayout_4.addWidget(self.defaultNoteHeadButton)
        self.xNoteHeadButton = RadioButtonTeller(self.dockWidgetContents)
        self.xNoteHeadButton.setObjectName(_fromUtf8("xNoteHeadButton"))
        self.verticalLayout_4.addWidget(self.xNoteHeadButton)
        self.bigXNoteHeadButton = RadioButtonTeller(self.dockWidgetContents)
        self.bigXNoteHeadButton.setObjectName(_fromUtf8("bigXNoteHeadButton"))
        self.verticalLayout_4.addWidget(self.bigXNoteHeadButton)
        self.oNoteHeadButton = RadioButtonTeller(self.dockWidgetContents)
        self.oNoteHeadButton.setObjectName(_fromUtf8("oNoteHeadButton"))
        self.verticalLayout_4.addWidget(self.oNoteHeadButton)
        self.bigONoteHeadButton = RadioButtonTeller(self.dockWidgetContents)
        self.bigONoteHeadButton.setObjectName(_fromUtf8("bigONoteHeadButton"))
        self.verticalLayout_4.addWidget(self.bigONoteHeadButton)
        self.plusNoteHeadButton = RadioButtonTeller(self.dockWidgetContents)
        self.plusNoteHeadButton.setObjectName(_fromUtf8("plusNoteHeadButton"))
        self.verticalLayout_4.addWidget(self.plusNoteHeadButton)
        self.gNoteHeadButton = RadioButtonTeller(self.dockWidgetContents)
        self.gNoteHeadButton.setObjectName(_fromUtf8("gNoteHeadButton"))
        self.verticalLayout_4.addWidget(self.gNoteHeadButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.noteHeadDock.setWidget(self.dockWidgetContents)
        DrumBurpWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.noteHeadDock)
        self.diplayOptionsDock = QtGui.QDockWidget(DrumBurpWindow)
        self.diplayOptionsDock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.diplayOptionsDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.diplayOptionsDock.setObjectName(_fromUtf8("diplayOptionsDock"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.spacingLabel = QtGui.QLabel(self.dockWidgetContents_2)
        self.spacingLabel.setWordWrap(True)
        self.spacingLabel.setObjectName(_fromUtf8("spacingLabel"))
        self.verticalLayout_2.addWidget(self.spacingLabel)
        self.spaceSlider = QtGui.QSlider(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spaceSlider.sizePolicy().hasHeightForWidth())
        self.spaceSlider.setSizePolicy(sizePolicy)
        self.spaceSlider.setMaximum(100)
        self.spaceSlider.setProperty(_fromUtf8("value"), 0)
        self.spaceSlider.setTracking(False)
        self.spaceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.spaceSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.spaceSlider.setObjectName(_fromUtf8("spaceSlider"))
        self.verticalLayout_2.addWidget(self.spaceSlider)
        self.label = QtGui.QLabel(self.dockWidgetContents_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.verticalSlider = QtGui.QSlider(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider.sizePolicy().hasHeightForWidth())
        self.verticalSlider.setSizePolicy(sizePolicy)
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setTracking(False)
        self.verticalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.verticalSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.verticalLayout_2.addWidget(self.verticalSlider)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.lineSpaceSlider = QtGui.QSlider(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineSpaceSlider.sizePolicy().hasHeightForWidth())
        self.lineSpaceSlider.setSizePolicy(sizePolicy)
        self.lineSpaceSlider.setMaximum(100)
        self.lineSpaceSlider.setTracking(False)
        self.lineSpaceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.lineSpaceSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.lineSpaceSlider.setObjectName(_fromUtf8("lineSpaceSlider"))
        self.verticalLayout_2.addWidget(self.lineSpaceSlider)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.fixedWidthCheckBox = QtGui.QCheckBox(self.dockWidgetContents_2)
        self.fixedWidthCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.fixedWidthCheckBox.setChecked(True)
        self.fixedWidthCheckBox.setObjectName(_fromUtf8("fixedWidthCheckBox"))
        self.horizontalLayout_2.addWidget(self.fixedWidthCheckBox)
        self.widthSpinBox = QtGui.QSpinBox(self.dockWidgetContents_2)
        self.widthSpinBox.setMinimum(10)
        self.widthSpinBox.setMaximum(1000)
        self.widthSpinBox.setProperty(_fromUtf8("value"), 80)
        self.widthSpinBox.setObjectName(_fromUtf8("widthSpinBox"))
        self.horizontalLayout_2.addWidget(self.widthSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.widthLabel = QtGui.QLabel(self.dockWidgetContents_2)
        self.widthLabel.setObjectName(_fromUtf8("widthLabel"))
        self.verticalLayout_2.addWidget(self.widthLabel)
        self.fontComboBox = QtGui.QFontComboBox(self.dockWidgetContents_2)
        self.fontComboBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontComboBox.sizePolicy().hasHeightForWidth())
        self.fontComboBox.setSizePolicy(sizePolicy)
        self.fontComboBox.setEditable(False)
        self.fontComboBox.setMaxVisibleItems(20)
        self.fontComboBox.setFontFilters(QtGui.QFontComboBox.ScalableFonts)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("BatangChe"))
        font.setPointSize(10)
        self.fontComboBox.setCurrentFont(font)
        self.fontComboBox.setObjectName(_fromUtf8("fontComboBox"))
        self.verticalLayout_2.addWidget(self.fontComboBox)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.diplayOptionsDock.setWidget(self.dockWidgetContents_2)
        DrumBurpWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.diplayOptionsDock)
        self.songPropertiesDock = QtGui.QDockWidget(DrumBurpWindow)
        self.songPropertiesDock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.songPropertiesDock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.songPropertiesDock.setObjectName(_fromUtf8("songPropertiesDock"))
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.songNameLabel = QtGui.QLabel(self.dockWidgetContents_3)
        self.songNameLabel.setObjectName(_fromUtf8("songNameLabel"))
        self.gridLayout_3.addWidget(self.songNameLabel, 0, 0, 1, 1)
        self.songNameEdit = QtGui.QLineEdit(self.dockWidgetContents_3)
        self.songNameEdit.setObjectName(_fromUtf8("songNameEdit"))
        self.gridLayout_3.addWidget(self.songNameEdit, 0, 1, 1, 1)
        self.artistNameEdit = QtGui.QLineEdit(self.dockWidgetContents_3)
        self.artistNameEdit.setObjectName(_fromUtf8("artistNameEdit"))
        self.gridLayout_3.addWidget(self.artistNameEdit, 2, 1, 1, 1)
        self.tabberLabel = QtGui.QLabel(self.dockWidgetContents_3)
        self.tabberLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.tabberLabel.setObjectName(_fromUtf8("tabberLabel"))
        self.gridLayout_3.addWidget(self.tabberLabel, 2, 3, 1, 1)
        self.tabberEdit = QtGui.QLineEdit(self.dockWidgetContents_3)
        self.tabberEdit.setObjectName(_fromUtf8("tabberEdit"))
        self.gridLayout_3.addWidget(self.tabberEdit, 2, 4, 1, 1)
        self.artistNameLabel = QtGui.QLabel(self.dockWidgetContents_3)
        self.artistNameLabel.setObjectName(_fromUtf8("artistNameLabel"))
        self.gridLayout_3.addWidget(self.artistNameLabel, 2, 0, 1, 1)
        self.bpmLabel = QtGui.QLabel(self.dockWidgetContents_3)
        self.bpmLabel.setObjectName(_fromUtf8("bpmLabel"))
        self.gridLayout_3.addWidget(self.bpmLabel, 0, 3, 1, 1)
        self.bpmSpinBox = QtGui.QSpinBox(self.dockWidgetContents_3)
        self.bpmSpinBox.setMaximum(300)
        self.bpmSpinBox.setProperty(_fromUtf8("value"), 120)
        self.bpmSpinBox.setObjectName(_fromUtf8("bpmSpinBox"))
        self.gridLayout_3.addWidget(self.bpmSpinBox, 0, 4, 1, 1)
        self.songPropertiesDock.setWidget(self.dockWidgetContents_3)
        DrumBurpWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.songPropertiesDock)
        self.actionQuit = QtGui.QAction(DrumBurpWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionNew = QtGui.QAction(DrumBurpWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionLoad = QtGui.QAction(DrumBurpWindow)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        self.actionSave = QtGui.QAction(DrumBurpWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_As = QtGui.QAction(DrumBurpWindow)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.actionExport_ASCII = QtGui.QAction(DrumBurpWindow)
        self.actionExport_ASCII.setObjectName(_fromUtf8("actionExport_ASCII"))
        self.actionDisplayOptionsIsVisible = QtGui.QAction(DrumBurpWindow)
        self.actionDisplayOptionsIsVisible.setCheckable(True)
        self.actionDisplayOptionsIsVisible.setObjectName(_fromUtf8("actionDisplayOptionsIsVisible"))
        self.actionSongPropertiesIsVisible = QtGui.QAction(DrumBurpWindow)
        self.actionSongPropertiesIsVisible.setCheckable(True)
        self.actionSongPropertiesIsVisible.setObjectName(_fromUtf8("actionSongPropertiesIsVisible"))
        self.actionNoteHeadSelectorIsVisble = QtGui.QAction(DrumBurpWindow)
        self.actionNoteHeadSelectorIsVisble.setCheckable(True)
        self.actionNoteHeadSelectorIsVisble.setObjectName(_fromUtf8("actionNoteHeadSelectorIsVisble"))
        self.actionToolbarIsVisible = QtGui.QAction(DrumBurpWindow)
        self.actionToolbarIsVisible.setCheckable(True)
        self.actionToolbarIsVisible.setObjectName(_fromUtf8("actionToolbarIsVisible"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_ASCII)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuView.addAction(self.actionDisplayOptionsIsVisible)
        self.menuView.addAction(self.actionSongPropertiesIsVisible)
        self.menuView.addAction(self.actionNoteHeadSelectorIsVisble)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionToolbarIsVisible)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionLoad)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSave_As)
        self.toolBar.addAction(self.actionExport_ASCII)
        self.spacingLabel.setBuddy(self.spaceSlider)
        self.songNameLabel.setBuddy(self.songNameEdit)
        self.tabberLabel.setBuddy(self.tabberEdit)
        self.artistNameLabel.setBuddy(self.artistNameEdit)
        self.bpmLabel.setBuddy(self.bpmSpinBox)

        self.retranslateUi(DrumBurpWindow)
        QtCore.QObject.connect(self.fixedWidthCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.widthSpinBox.setEnabled)
        QtCore.QObject.connect(self.defaultNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.xNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.bigXNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.oNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.bigONoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.plusNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.gNoteHeadButton, QtCore.SIGNAL(_fromUtf8("emitValue(QString)")), self.scoreView.setNoteHead)
        QtCore.QObject.connect(self.spaceSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.scoreView.horizontalSpacingChanged)
        QtCore.QObject.connect(self.verticalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.scoreView.verticalSpacingChanged)
        QtCore.QObject.connect(self.lineSpaceSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.scoreView.systemSpacingChanged)
        QtCore.QObject.connect(self.fontComboBox, QtCore.SIGNAL(_fromUtf8("currentFontChanged(QFont)")), self.scoreView.setFont)
        QtCore.QObject.connect(self.actionDisplayOptionsIsVisible, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.diplayOptionsDock.setVisible)
        QtCore.QObject.connect(self.actionNoteHeadSelectorIsVisble, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.noteHeadDock.setVisible)
        QtCore.QObject.connect(self.actionSongPropertiesIsVisible, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.songPropertiesDock.setVisible)
        QtCore.QObject.connect(self.songPropertiesDock, QtCore.SIGNAL(_fromUtf8("visibilityChanged(bool)")), self.actionSongPropertiesIsVisible.setChecked)
        QtCore.QObject.connect(self.noteHeadDock, QtCore.SIGNAL(_fromUtf8("visibilityChanged(bool)")), self.actionNoteHeadSelectorIsVisble.setChecked)
        QtCore.QObject.connect(self.diplayOptionsDock, QtCore.SIGNAL(_fromUtf8("visibilityChanged(bool)")), self.actionDisplayOptionsIsVisible.setChecked)
        QtCore.QObject.connect(self.actionToolbarIsVisible, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.toolBar.setVisible)
        QtCore.QObject.connect(self.toolBar, QtCore.SIGNAL(_fromUtf8("visibilityChanged(bool)")), self.actionToolbarIsVisible.setChecked)
        QtCore.QMetaObject.connectSlotsByName(DrumBurpWindow)

    def retranslateUi(self, DrumBurpWindow):
        DrumBurpWindow.setWindowTitle(QtGui.QApplication.translate("DrumBurpWindow", "DrumBurp", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("DrumBurpWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("DrumBurpWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("DrumBurpWindow", "Tool Bar", None, QtGui.QApplication.UnicodeUTF8))
        self.noteHeadDock.setWindowTitle(QtGui.QApplication.translate("DrumBurpWindow", "Note Head", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "Default", None, QtGui.QApplication.UnicodeUTF8))
        self.xNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.xNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.bigXNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.bigXNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.oNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "o", None, QtGui.QApplication.UnicodeUTF8))
        self.oNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "o", None, QtGui.QApplication.UnicodeUTF8))
        self.bigONoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "O", None, QtGui.QApplication.UnicodeUTF8))
        self.bigONoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "O", None, QtGui.QApplication.UnicodeUTF8))
        self.plusNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.plusNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.gNoteHeadButton.setText(QtGui.QApplication.translate("DrumBurpWindow", "g", None, QtGui.QApplication.UnicodeUTF8))
        self.gNoteHeadButton.setProperty(_fromUtf8("buttonValue"), QtGui.QApplication.translate("DrumBurpWindow", "g", None, QtGui.QApplication.UnicodeUTF8))
        self.diplayOptionsDock.setWindowTitle(QtGui.QApplication.translate("DrumBurpWindow", "Display Options", None, QtGui.QApplication.UnicodeUTF8))
        self.spacingLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "Horizontal Spacing", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DrumBurpWindow", "Vertical Spacing", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DrumBurpWindow", "System Spacing", None, QtGui.QApplication.UnicodeUTF8))
        self.fixedWidthCheckBox.setText(QtGui.QApplication.translate("DrumBurpWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
        self.widthLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "Width", None, QtGui.QApplication.UnicodeUTF8))
        self.songPropertiesDock.setWindowTitle(QtGui.QApplication.translate("DrumBurpWindow", "Song Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.songNameLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.tabberLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "&Tabbed by", None, QtGui.QApplication.UnicodeUTF8))
        self.artistNameLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "&Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.bpmLabel.setText(QtGui.QApplication.translate("DrumBurpWindow", "&BPM", None, QtGui.QApplication.UnicodeUTF8))
        self.bpmSpinBox.setSuffix(QtGui.QApplication.translate("DrumBurpWindow", " bpm", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("DrumBurpWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setToolTip(QtGui.QApplication.translate("DrumBurpWindow", "Quit DrumBurp", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setStatusTip(QtGui.QApplication.translate("DrumBurpWindow", "Quit DrumBurp", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("DrumBurpWindow", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setIconText(QtGui.QApplication.translate("DrumBurpWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setToolTip(QtGui.QApplication.translate("DrumBurpWindow", "New Score", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setStatusTip(QtGui.QApplication.translate("DrumBurpWindow", "Create a new blank score", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("DrumBurpWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setText(QtGui.QApplication.translate("DrumBurpWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setToolTip(QtGui.QApplication.translate("DrumBurpWindow", "Load Score", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setStatusTip(QtGui.QApplication.translate("DrumBurpWindow", "Load a saved DrumBurp score", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setShortcut(QtGui.QApplication.translate("DrumBurpWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("DrumBurpWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setStatusTip(QtGui.QApplication.translate("DrumBurpWindow", "Save this DrumBurp score", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("DrumBurpWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("DrumBurpWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setStatusTip(QtGui.QApplication.translate("DrumBurpWindow", "Save this DrumBurp score with a new name", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_ASCII.setText(QtGui.QApplication.translate("DrumBurpWindow", "&Export ASCII", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_ASCII.setStatusTip(QtGui.QApplication.translate("DrumBurpWindow", "Write an ASCII representation of this score to a file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_ASCII.setShortcut(QtGui.QApplication.translate("DrumBurpWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDisplayOptionsIsVisible.setText(QtGui.QApplication.translate("DrumBurpWindow", "Display Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDisplayOptionsIsVisible.setToolTip(QtGui.QApplication.translate("DrumBurpWindow", "Change visibility of display options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDisplayOptionsIsVisible.setStatusTip(QtGui.QApplication.translate("DrumBurpWindow", "Change visibility of display options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSongPropertiesIsVisible.setText(QtGui.QApplication.translate("DrumBurpWindow", "Song Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSongPropertiesIsVisible.setIconText(QtGui.QApplication.translate("DrumBurpWindow", "Change visibility of song properties", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSongPropertiesIsVisible.setToolTip(QtGui.QApplication.translate("DrumBurpWindow", "Change visibility of song properties", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNoteHeadSelectorIsVisble.setText(QtGui.QApplication.translate("DrumBurpWindow", "Note Head Selector", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNoteHeadSelectorIsVisble.setToolTip(QtGui.QApplication.translate("DrumBurpWindow", "Change visibility of note head selector", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNoteHeadSelectorIsVisble.setStatusTip(QtGui.QApplication.translate("DrumBurpWindow", "Change visibility of note head selector", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToolbarIsVisible.setText(QtGui.QApplication.translate("DrumBurpWindow", "Tool Bar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToolbarIsVisible.setToolTip(QtGui.QApplication.translate("DrumBurpWindow", "Change visibility of tool bar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToolbarIsVisible.setStatusTip(QtGui.QApplication.translate("DrumBurpWindow", "Change visibility of tool bar", None, QtGui.QApplication.UnicodeUTF8))

from Widgets.ScoreView_plugin import ScoreView
from Widgets.RadioButtonTeller_plugin import RadioButtonTeller
