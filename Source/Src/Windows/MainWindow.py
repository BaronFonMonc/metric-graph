import copy
import sys
import matplotlib;
import sympy
from PyQt5.QtWidgets import QMessageBox
from netgraph._artists import NodeArtist

import Data.Utils
import Logic.Polynomials
from Windows.Tabs.ChartTab import ChartTab
from Windows.Visualisation.MyToolbar import MyToolbar

matplotlib.use("Qt5Agg")

from PyQt5 import QtWidgets, QtCore  # <- additional import
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from netgraph import EditableGraph
from Data.MetricGraph import MyNetworkX
from Windows.Visualisation.MyEditableGraph import MyEditableGraph
from Logic.Polynomials import *
from sympy import latex
from Windows.Visualisation.MplCanvas import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1072, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_3.sizePolicy().hasHeightForWidth())
        self.tab_3.setSizePolicy(sizePolicy)
        self.tab_3.setMinimumSize(QtCore.QSize(1024, 589))
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setObjectName("label_2")
        #self.verticalLayout.addWidget(self.label_2)
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser.setObjectName("textBrowser")
        #self.verticalLayout.addWidget(self.textBrowser)
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setObjectName("label_3")
        #self.verticalLayout.addWidget(self.label_3)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_2.setObjectName("textBrowser_2")
        #self.verticalLayout.addWidget(self.textBrowser_2)
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setObjectName("label_4")
        #self.verticalLayout.addWidget(self.label_4)
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_3.setObjectName("textBrowser_3")
        #self.verticalLayout.addWidget(self.textBrowser_3)
        #self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setObjectName("label_9")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setText("Substitute")

        self.qline_1 = QtWidgets.QLineEdit(self.tab_3)
        self.qline_1.setPlaceholderText("Y")
        self.qline_2 = QtWidgets.QLineEdit(self.tab_3)
        self.qline_2.setPlaceholderText("X")
        self.qline_3 = QtWidgets.QLineEdit(self.tab_3)
        self.qline_3.setPlaceholderText("Y")
        self.qline_4 = QtWidgets.QLineEdit(self.tab_3)
        self.qline_4.setPlaceholderText("T")
        self.qline_5 = QtWidgets.QLineEdit(self.tab_3)
        self.qline_5.setPlaceholderText("T")

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.qline_1, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.qline_2, 0, 2, 1, 1)
        self.gridLayout_3.addWidget(self.textBrowser, 1, 0, 1, 3)
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.qline_3, 2, 2, 1, 1)
        self.gridLayout_3.addWidget(self.textBrowser_2, 3, 0, 1, 3)
        self.gridLayout_3.addWidget(self.qline_4, 4, 2, 1, 1)
        self.gridLayout_3.addWidget(self.label_4, 4, 0, 1, 1)
        self.gridLayout_3.addWidget(self.textBrowser_3, 5, 0, 1, 3)
        self.gridLayout_3.addWidget(self.label_9, 6, 0, 1, 1)
        self.gridLayout_3.addWidget(self.qline_5, 6, 2, 1, 1)
        self.gridLayout_3.addWidget(self.textBrowser_4, 7, 0, 1, 3)
        self.gridLayout_3.addWidget(self.pushButton_5, 8, 2, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 8)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        #self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1) # TODO
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        #self.gridLayout.addWidget(self.pushButton_3, 1, 2, 1, 1) # TODO
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        #self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1) #TODO
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        #self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        #self.gridLayout.addWidget(self.doubleSpinBox_2, 4, 1, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        #self.gridLayout.addWidget(self.doubleSpinBox, 4, 0, 1, 1)
        self.doubleSpinBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.doubleSpinBox_3.addItem("Approximation")
        self.doubleSpinBox_3.addItem("Precise")
        self.doubleSpinBox_3.addItem("Counting points")
        #self.doubleSpinBox_3.setValue(0)
        self.doubleSpinBox_2.setValue(0.1) # delta T
        self.doubleSpinBox.setValue(0.5) # Epsilon
        #self.gridLayout.addWidget(self.doubleSpinBox_3, 4, 2, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setObjectName("horizontalSlider")
        #self.gridLayout.addWidget(self.horizontalSlider, 2, 3, 1, 1)
        #self.label = QtWidgets.QLabel(self.centralwidget)
        #self.label.setObjectName("label")
        #self.gridLayout.addWidget(self.label, 2, 4, 1, 1)
        #self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        #self.spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        #self.spinBox.setProperty("value", 5)
        #self.spinBox.setObjectName("spinBox")
        #self.gridLayout.addWidget(self.spinBox, 2, 6, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        #self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        #self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        #self.gridLayout.addWidget(self.pushButton_4, 2, 4, 1, 1) #TODO
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        #self.gridLayout.addWidget(self.label_8, 4, 4, 1, 1) #TODO
        self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1072, 26))
        self.menubar.setObjectName("menubar")

        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuSettings_2 = QtWidgets.QMenu(self.menubar)
        self.menuSettings_2.setObjectName("menuSettings_2")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")

        self.actionOpen_project = QtWidgets.QAction(MainWindow)
        self.actionOpen_project.setObjectName("actionOpen_project")
        self.actionSave_project = QtWidgets.QAction(MainWindow)
        self.actionSave_project.setObjectName("actionSave_project")
        self.actionRecent_projects = QtWidgets.QAction(MainWindow)
        self.actionRecent_projects.setObjectName("actionRecent_projects")
        self.actionCreate_graph_from_file = QtWidgets.QAction(MainWindow)
        self.actionCreate_graph_from_file.setObjectName("actionCreate_graph_from_file")
        self.actionSave_graph_to_file = QtWidgets.QAction(MainWindow)
        self.actionSave_graph_to_file.setObjectName("actionSave_graph_to_file")
        self.actionShow_coverage = QtWidgets.QAction(MainWindow)
        self.actionShow_coverage.setCheckable(True)
        self.actionShow_coverage.setObjectName("actionShow_coverage")
        self.actionDisable_animations = QtWidgets.QAction(MainWindow)
        self.actionDisable_animations.setCheckable(True)
        self.actionDisable_animations.setObjectName("actionDisable_animations")
        self.actionConfigure_graph = QtWidgets.QAction(MainWindow)
        self.actionConfigure_graph.setObjectName("actionConfigure_graph")
        self.actionConfigure_chart = QtWidgets.QAction(MainWindow)
        self.actionConfigure_chart.setObjectName("actionConfigure_chart")
        self.actionSympy_format = QtWidgets.QAction(MainWindow)
        self.actionSympy_format.setCheckable(True)
        self.actionSympy_format.setObjectName("actionSympy_format")
        self.actionLaTeX_format = QtWidgets.QAction(MainWindow)
        self.actionLaTeX_format.setCheckable(True)
        self.actionLaTeX_format.setObjectName("actionLaTeX_format")
        self.menuSettings.addAction(self.actionOpen_project)
        self.menuSettings.addAction(self.actionSave_project)
        self.menuSettings.addAction(self.actionRecent_projects)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionCreate_graph_from_file)
        self.menuSettings.addAction(self.actionSave_graph_to_file)
        self.menuSettings_2.addAction(self.actionShow_coverage)
        self.menuSettings_2.addAction(self.actionDisable_animations)
        self.menuSettings_2.addAction(self.actionConfigure_graph)
        self.menuSettings_2.addSeparator()
        self.menuSettings_2.addAction(self.actionConfigure_chart)
        self.menuSettings_2.addSeparator()
        self.menuSettings_2.addAction(self.actionSympy_format)
        self.menuSettings_2.addAction(self.actionLaTeX_format)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuSettings_2.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuSettings_2.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())


        self.pushButton_6 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setText("Confirm")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setText("Add")

        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setObjectName("label_10")
        self.label_10.setText("From")
        self.label_10.setAlignment(QtCore.Qt.AlignRight)
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setObjectName("label_11")
        self.label_11.setText("To")
        self.label_11.setAlignment(QtCore.Qt.AlignRight)
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setObjectName("label_12")
        self.label_12.setText("Step")
        self.label_12.setAlignment(QtCore.Qt.AlignRight)
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setObjectName("label_13")
        self.label_13.setText("Select algorithm")
        self.label_13.setAlignment(QtCore.Qt.AlignRight)

        self.qline_6 = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.qline_7 = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.qline_8 = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.qline_9 = QtWidgets.QComboBox(self.tab_2)
        #self.qline_9.setObjectName("doubleSpinBox_3")
        self.qline_9.addItem("Approximation")
        self.qline_9.addItem("Precise")
        self.qline_9.addItem("UpperBound")

        self.qline_6.setValue(0.1)
        self.qline_7.setValue(1)
        self.qline_8.setValue(0.1)
        #self.qline_9.setValue(0.5)

        ###############################################################################################################

        self.canvas = MplCanvas(MainWindow, width=5, height=4, dpi=100)
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        self.scat = None
        self.lines = None

        self.toolbar = MyToolbar(self.canvas, MainWindow)

        self.chartTab = ChartTab(MainWindow, width=5, height=4, dpi=100)
        layout2 = QtWidgets.QVBoxLayout(self.tab_2)

        layout2.addWidget(self.chartTab)

        horizontalLayout = QtWidgets.QHBoxLayout(self.tab_2)

        horizontalLayout.addWidget(self.label_10)
        horizontalLayout.addWidget(self.qline_6)
        horizontalLayout.addWidget(self.label_11)
        horizontalLayout.addWidget(self.qline_7)
        horizontalLayout.addWidget(self.label_12)
        horizontalLayout.addWidget(self.qline_8)
        horizontalLayout.addWidget(self.label_13)
        horizontalLayout.addWidget(self.qline_9)
        horizontalLayout.addWidget(self.pushButton_7)
        horizontalLayout.addWidget(self.pushButton_6)
        layout2.addLayout(horizontalLayout)
        #layout2.addWidget(self.pushButton_6)


        #layout = QtWidgets.QVBoxLayout(self.tab)
        #layout.addWidget(self.toolbar)
        #layout.addWidget(self.canvas)
        #layout.addWidget(self.pushButton)

        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")

        #layout.addLayout(self.gridLayout_4)

        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setText("Graph is not saturated")

        self.gridLayout_4.addWidget(self.toolbar, 0, 0, 1, 5)
        self.gridLayout_4.addWidget(self.canvas, 1, 0, 12, 5)

        self.gridLayout_4.addWidget(self.pushButton, 13, 0, 1, 1)
        self.gridLayout_4.addWidget(self.pushButton_2, 13, 1, 1, 1)
        self.gridLayout_4.addWidget(self.pushButton_3, 13, 2, 1, 1)
        self.gridLayout_4.addWidget(self.horizontalSlider, 13, 3, 1, 1)
        self.gridLayout_4.addWidget(self.pushButton_4, 15, 4, 1, 1)
        self.gridLayout_4.addWidget(self.label_5, 14, 0, 1, 1)
        self.gridLayout_4.addWidget(self.label_6, 14, 2, 1, 1)
        self.gridLayout_4.addWidget(self.label_7, 14, 1, 1, 1)
        self.gridLayout_4.addWidget(self.label_8, 13, 4, 1, 1)

        self.gridLayout_4.addWidget(self.doubleSpinBox, 15, 0, 1, 1)
        self.gridLayout_4.addWidget(self.doubleSpinBox_2, 15, 1, 1, 1)
        self.gridLayout_4.addWidget(self.doubleSpinBox_3, 15, 2, 1, 1)
        self.gridLayout_4.addWidget(self.label_14, 14, 4, 1, 1)


        self.__retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.__connectEvents()



        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _sympy_rational(self, fl):
        a = int(fl*100)
        res = sympy.Rational(a, 100)
        return res

    def prevState(self):
        self.current_i -= 1
        if self.current_i>=0:
            self.t = self.previous_states[self.current_i][0]
            self.label_8.setText("Time" + str(self.t))
            self.delta_t = self.previous_states[self.current_i][1]
            moving_points = self.previous_states[self.current_i][2]

            plt.ion()

            if self.horizontalSlider.value()>0:
                self.horizontalSlider.setValue(self.horizontalSlider.value() - 1)

            X, Y = [], []

            print("YOOOO", moving_points)
            for i in moving_points:
                left = i.edge[0]
                right = i.edge[1]
                if left == i.dir:
                    left, right = right, left
                x, y = Data.Utils.calc_pos(self.canvas.graph.node_positions[left],
                                           self.canvas.graph.node_positions[right],
                                           i.length,
                                           i.dist)
                X.append(x)
                Y.append(y)

            if self.scat != None:
                self.scat.remove()
            self.scat = self.canvas.ax.scatter(X, Y, zorder=5, color='blue')  # , s=220)

            self.canvas.draw_idle()
            if self.canvas.networkGraph.check_saturation(self.epsilon)[1]:
                self.label_14.setText("Graph is saturated!")
            else:
                self.label_14.setText("Graph is not saturated")
            print(self.t, self.delta_t, self.previous_states)



    # On presing "Next" button
    def nextState(self):

        if self.current_i < len(self.previous_states) - 1:
            self.current_i += 2
            self.prevState()
            return

        self.epsilon = self._sympy_rational(self.doubleSpinBox.value())
        self.delta_t = self._sympy_rational(self.doubleSpinBox_2.value())

        plt.ion()

        if self.horizontalSlider.value() == self.horizontalSlider.maximum():
            self.horizontalSlider.setMaximum(self.horizontalSlider.maximum()+5)
        self.horizontalSlider.setValue(self.horizontalSlider.value()+1)

        self.canvas.networkGraph.move_points_silly(self.delta_t)
        #moment = self.canvas.networkGraph.move_points_to_next_moment()

        self.previous_states.append([self.t, self.delta_t, copy.deepcopy(self.canvas.networkGraph.moving_points)])
        self.current_i = len(self.previous_states)-1
        #print(self.previous_states[self.current_i])

        #moment = self.canvas.networkGraph.get_points_next_moment()
        #self.canvas.networkGraph.move_points_to_next_moment()


        #print(self.canvas.networkGraph.moving_points)



        #self.canvas.ax.clear()
        #plt.show()

        #self.a = self.canvas.ax
        #self.b = self.canvas.figure

        #self.canvas.ax.axes.clear()

        #self.canvas.figure.canvas.ax.clear()
        #self.canvas.ax.cla()
        #self.canvas.draw_idle()

        #self.a = self.canvas.ax.scatter(self.canvas.graph.node_positions[0][0], self.canvas.graph.node_positions[0][1], color='blue')

        #scat.get_offset()
        #self.canvas.ax.plot_date(self.canvas.graph.node_positions[1][0], self.canvas.graph.node_positions[1][1], color='blue')
        #self.canvas.ax.plot_date(self.canvas.graph.node_positions[2][0], self.canvas.graph.node_positions[2][1], color='blue')

        #print(scat.get_offset())

        X,Y = [],[]



        for i in self.canvas.networkGraph.moving_points:
            left = i.edge[0]
            right = i.edge[1]
            if left==i.dir:
                left,right = right,left
            #print(self.canvas.graph.node_positions[left], self.canvas.graph.node_positions[right])
            x, y = Data.Utils.calc_pos(self.canvas.graph.node_positions[left],
                                       self.canvas.graph.node_positions[right],
                                       i.length,
                                       i.dist)
            #print(x,y)
            X.append(x)
            Y.append(y)

        if self.scat!=None:
            self.scat.remove()
        self.scat = self.canvas.ax.scatter(X, Y, zorder=5, color='red')#, s=220)

        #self.canvas.ax.cla()
        self.canvas.draw_idle()

        #self.canvas.networkGraph.check_saturation_between_moments(moment, self.epsilon)

        self.t += self.delta_t
        self.label_8.setText("Time" + str(self.t))
        #self.t += moment

        #print(self.t, moment, self.canvas.networkGraph.moving_points, self.canvas.networkGraph.check_saturation_between_moments(moment, self.epsilon))
        if self.canvas.networkGraph.check_saturation(self.epsilon)[1]:
            self.label_14.setText("Graph is saturated!")
        else:
            self.label_14.setText("Graph is not saturated")

        coverage = self.canvas.networkGraph.check_saturation(self.epsilon)[0]
        X, Y = [], []
        for i in coverage:
            left = i[0]
            right = i[1]
            #if left==i.dir:
            #    left,right = right,left
            x,y = None, None
            #print(self.canvas.graph.node_positions[left], self.canvas.graph.node_positions[right])
            for j in coverage[i]:
                print(j)
                x, y = Data.Utils.calc_pos(self.canvas.graph.node_positions[left],
                                           self.canvas.graph.node_positions[right],
                                           self.canvas.networkGraph.get_weight(i),
                                           j[0])
                x1, y1 = Data.Utils.calc_pos(self.canvas.graph.node_positions[left],
                                           self.canvas.graph.node_positions[right],
                                           self.canvas.networkGraph.get_weight(i),
                                           j[1])
            #print(x,y)
            if x != None and y != None:
                X.append(x)
                Y.append(y)
                X.append(x1)
                Y.append(y1)
        if self.lines!=None:
            for i in self.lines:
                self.canvas.ax.lines.pop(0)
            #self.scat_cov.remove()
        self.lines = []
        for i in range(0, len(X), 2):
            print(X[i], Y[i])
            #self.lines.append(self.canvas.ax.plot(X[i:i + 2], Y[i:i + 2], 'go-'))
        #self.scat_cov = self.canvas.ax.scatter(X, Y, zorder=5, color='green')#, s=220)


        #print(len(self.canvas.networkGraph.moving_points), self.t, self.canvas.networkGraph.check_saturation(self.epsilon))
        #print("!!!", self.canvas.networkGraph.moving_points)


    # On changing slider value
    def updateSlideMaximum(self, value):
        if self.horizontalSlider.value() == self.horizontalSlider.maximum():
            self.horizontalSlider.setMaximum(self.horizontalSlider.maximum()+10)

        if self.horizontalSlider.isSliderDown():# or self.horizontalSlider.is:
            if self.current_i < self.horizontalSlider.value():
                self.movePointsTo(self.current_i+1, False)
            elif self.current_i < len(self.previous_states):
                self.movePointsTo(self.current_i-1, True)
        else: # If you clicked
            self.showWarning()
            #if self.current_i < self.horizontalSlider.value():
            #    self.nextState()
            #elif self.current_i < len(self.previous_states) - 1:
            #    self.current_i += 2
            #    self.prevState()
            #else:
            #    self.nextState()
        #self.horizontalSlider.setMaximum(value)


    def calculateFrom(self, current_i, times):
        if current_i < len(self.previous_states) and times > 0:
            for i in range(current_i, current_i + times):
                self.movePointsTo(i, False)




    def showMovingPoints(self, moving_points, c='red'):
        X,Y = [],[]
        for i in moving_points:
            left = i.edge[0]
            right = i.edge[1]
            x, y = Data.Utils.calc_pos_dir(self.canvas.graph.node_positions[left],
                                       self.canvas.graph.node_positions[right],
                                       i.length, i.dist,
                                       i.dir, i.edge)
            X.append(x)
            Y.append(y)

        if self.scat!=None:
            self.scat.remove()
        self.scat = self.canvas.ax.scatter(X, Y, zorder=5, color=c)#, s=220)
        self.canvas.draw_idle()


    def showCoverage(self, coverage):
        X, Y = [], []
        for i in coverage:
            left = i[0]
            right = i[1]
            x,y = None, None
            for j in coverage[i]:
                print(j)
                x, y = Data.Utils.calc_pos(self.canvas.graph.node_positions[left],
                                           self.canvas.graph.node_positions[right],
                                           self.canvas.networkGraph.get_weight(i),
                                           j[0])
                x1, y1 = Data.Utils.calc_pos(self.canvas.graph.node_positions[left],
                                           self.canvas.graph.node_positions[right],
                                           self.canvas.networkGraph.get_weight(i),
                                           j[1])
            if x != None and y != None:
                X.append(x)
                Y.append(y)
                X.append(x1)
                Y.append(y1)
        if self.lines!=None:
            self.canvas.ax.lines = []
            #for i in self.lines:
            #    self.canvas.ax.lines.pop(0)
        self.lines = []
        for i in range(0, len(X), 2):
            print(X[i], Y[i])
            self.lines.append(self.canvas.ax.plot(X[i:i + 2], Y[i:i + 2], 'go-'))
        self.canvas.draw_idle()


    def movePointsTo(self, current_i, prev = False):
        if prev:
            self.t = self.previous_states[self.current_i][0]
            self.delta_t = self.previous_states[self.current_i][1]
            self.label_8.setText("Time" + str(self.t))
            prev = True
        else:
            self.delta_t = self._sympy_rational(self.doubleSpinBox_2.value())
            self.t += self.delta_t
            self.label_8.setText("Time" + str(self.t))

        self.current_i = current_i
        self.epsilon = self._sympy_rational(self.doubleSpinBox.value())
        plt.ion()


        print(self.doubleSpinBox_3.currentText())

        coverage = []

        if not prev:
            if (self.doubleSpinBox_3.currentText()=="Approximation"):
                self.canvas.networkGraph.move_points_silly(self.delta_t)
            elif (self.doubleSpinBox_3.currentText()=="Precise"):
                self.canvas.networkGraph.move_points_to_next_moment()

            coverage = self.canvas.networkGraph.check_saturation(self.epsilon)[0]
            self.previous_states.append([self.t, self.delta_t, copy.deepcopy(self.canvas.networkGraph.moving_points), coverage])
            self.showMovingPoints(self.canvas.networkGraph.moving_points)
        else:
            self.showMovingPoints(self.previous_states[current_i][2], 'blue')
            coverage = self.previous_states[current_i][3]

        if self.canvas.networkGraph.check_saturation(self.epsilon)[1]:
            self.label_14.setText("Graph is saturated!")
        else:
            self.label_14.setText("Graph is not saturated")

        self.showCoverage(coverage)


    def showWarning(self):
        msg = QMessageBox()
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Warning)
        msg.setText("You may lose your progress!")
        msg.setInformativeText('Are you sure you want to edit graph?')
        msg.setWindowTitle("Warning")
        msg.exec_()


    # On pressing "Confirm" button
    def printGraph(self):

        self.pushButton_4.setText(QtCore.QCoreApplication.translate("MainWindow", "Edit"))
        self.t = 0
        self.epsilon = self.doubleSpinBox.value()
        self.delta_t = self.doubleSpinBox_2.value()
        self.previous_states = [[0, self.delta_t, []]]
        self.current_i = 0

        weights = []
        for i in self.canvas.graph.edge_label_artists:
            weights.append(self.canvas.graph.edge_label_artists[i].get_text())

        print("Weights:", weights, "Nodes:", self.canvas.graph.nodes)

        nod = [self.canvas.graph._reverse_node_artists[artist] for artist in self.canvas.graph._selected_artists if
                 isinstance(artist, NodeArtist)]
        if len(nod)!=0:
            self.source = nod[0]
        else:
            self.source = 0

        ans = self.canvas.networkGraph.update(self.canvas.graph.edges, weights, nod)
        if ans == 1:
            print("Not enough weights")
        elif ans == 2:
            print("Cannot parse this edge")

        print(self.canvas.networkGraph.graph)

        print(tutte_polynomial(self.canvas.networkGraph.graph))
        print(critical_configuration_polynomial(self.canvas.networkGraph.graph))
        print(zonotope_polynomial(self.canvas.networkGraph.graph))

        self.textBrowser.setText(str(tutte_polynomial(self.canvas.networkGraph.graph)))
        self.textBrowser_2.setText(str(critical_configuration_polynomial(self.canvas.networkGraph.graph)))
        self.textBrowser_3.setText(str(zonotope_polynomial(self.canvas.networkGraph.graph)))


    def draw_chart(self):
        self.chartTab.draw_chart(self.canvas.networkGraph, float(self.qline_6.value()),
                                 float(self.qline_7.value()), float(self.qline_8.value()))


    def calculateNumberPolymials(self):
        x = sympy.Symbol("x")
        y = sympy.Symbol("y")
        t = sympy.Symbol("t")
        T = self.qline_5.text()
        print(T)
        #if len(T)>0:
            #T = int(T)
        number = Logic.Polynomials.getPointNumber_Todd(self.canvas.networkGraph, T, self.source)
        print(number)
        self.textBrowser_4.setText(str(number))# + "$\sqrt{2}$")
        Y1, X1 = self.qline_1.text(), self.qline_2.text()
        Y2 = self.qline_3.text()
        T2 = self.qline_4.text()
        if len(Y1)==0:
            Y1 = "y"
        #else:
        #    Y1 = int(Y1)
        if len(X1)==0:
            X1 = "x"
        #else:
        #    X1 = int(X1)
        if len(Y2)==0:
            Y2 = "y"
        #else:
        #    Y2 = int(Y2)
        if len(T2)==0:
            T2 = "t"
        #else:
        #    T2 = int(T2)
        self.textBrowser.setText(str(tutte_polynomial(self.canvas.networkGraph.graph).subs(x, X1).subs(y, Y1)))
        self.textBrowser_2.setText(str(critical_configuration_polynomial(self.canvas.networkGraph.graph).subs(y, Y2)))
        self.textBrowser_3.setText(str(zonotope_polynomial(self.canvas.networkGraph.graph).subs(t,T2)))


    # All events connect to their buttons, sliders etc.
    def __connectEvents(self):
        #self.spinBox.valueChanged['int'].connect(self.updateSlideMaximum)
        self.pushButton_4.pressed.connect(self.printGraph)
        self.pushButton_2.pressed.connect(self.nextState)
        self.pushButton_5.pressed.connect(self.calculateNumberPolymials)
        self.pushButton_6.pressed.connect(self.draw_chart)
        self.pushButton_3.pressed.connect(self.prevState)
        self.horizontalSlider.actionTriggered.connect(self.updateSlideMaximum)
        #self.horizontalSlider.dragLeaveEvent.connect(self.updateSlideMaximum)

    def __retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Metric Graph Tool"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.pushButton.setText(_translate("MainWindow", "Reset"))
        self.pushButton_3.setText(_translate("MainWindow", "Stop"))
        #self.label.setText(_translate("MainWindow", "Time Maximum"))
        self.pushButton_4.setText(_translate("MainWindow", "Confirm"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Metric Graph"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Chart"))
        self.label_2.setText(_translate("MainWindow", "Tutte Polynomial"))
        self.label_3.setText(_translate("MainWindow", "Critical configuration polynomial"))
        self.label_4.setText(_translate("MainWindow", "Ehrhart polynomial of the unimodular zonotope Z(D)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Polynomials"))

        self.label_7.setText(_translate("MainWindow", "Step t"))
        self.label_5.setText(_translate("MainWindow", "Epsilon"))
        self.label_6.setText(_translate("MainWindow", "Select Algorithm"))
        self.label_8.setText(_translate("MainWindow", "Time"))
        self.label_9.setText(_translate("MainWindow", "Number of points"))
        self.menuSettings.setTitle(_translate("MainWindow", "File"))
        self.menuSettings_2.setTitle(_translate("MainWindow", "Options"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))

        self.actionOpen_project.setText(_translate("MainWindow", "Open project"))
        self.actionSave_project.setText(_translate("MainWindow", "Save project"))
        self.actionRecent_projects.setText(_translate("MainWindow", "Recent projects"))
        self.actionCreate_graph_from_file.setText(_translate("MainWindow", "Create graph from file"))
        self.actionSave_graph_to_file.setText(_translate("MainWindow", "Save graph to file"))
        self.actionShow_coverage.setText(_translate("MainWindow", "Show coverage"))
        self.actionDisable_animations.setText(_translate("MainWindow", "Disable animations"))
        self.actionConfigure_graph.setText(_translate("MainWindow", "Configure graph"))
        self.actionConfigure_chart.setText(_translate("MainWindow", "Configure chart"))
        self.actionSympy_format.setText(_translate("MainWindow", "Sympy format"))
        self.actionLaTeX_format.setText(_translate("MainWindow", "LaTeX format"))



        #self.textBrowser_4.append('''
        #<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        #<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        #''')
        #self.textBrowser_4.append('''$$a = {F \over m}$$''')
        #self.textBrowser_4.append("<a href=http://google.com>Google</a>")
