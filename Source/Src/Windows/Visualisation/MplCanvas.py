import sys
import matplotlib;
import netgraph

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from Data.MetricGraph import MyNetworkX
from Windows.Visualisation.MyEditableGraph import MyEditableGraph

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(MplCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)


        self.figure.set_tight_layout(True)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_adjustable('datalim')

        self.ax.patch.set_edgecolor('black')
        self.ax.patch.set_linewidth('1')

        self.graph = MyEditableGraph([(0, 1), (1, 2)], self.ax)



        self.networkGraph = MyNetworkX()


        print(self.graph.node_positions)
        print(self.graph.node_positions[0])
        print(self.graph.node_positions[0][0] + self.graph.node_positions[0][1])
        print(self.graph.edges)
