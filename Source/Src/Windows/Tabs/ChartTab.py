import math
import sys
import matplotlib;
import netgraph
import networkx
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Qt5Agg")

from PyQt5 import QtWidgets, QtCore  # <- additional import
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from netgraph import EditableGraph
from Data.MetricGraph import MyNetworkX
from Windows.Visualisation.MyEditableGraph import MyEditableGraph
from Logic.Polynomials import *
from sympy import latex, Pow, Rational
from matplotlib import pyplot as plt
from itertools import combinations
import numpy as np
from matplotlib import animation
from sympy.ntheory.continued_fraction import continued_fraction_iterator

class ChartTab(FigureCanvasQTAgg):

    # Step 3. Implement the hover event to display annotations
    def motion_hover(self, event):
        annotation_visbility = self.annotation.get_visible()
        if event.inaxes == self.ax:
            is_contained, annotation_index = self.scat.contains(event)
            if is_contained:
                data_point_location = self.scat.get_offsets()[annotation_index['ind'][0]]
                self.annotation.xy = data_point_location

                text_label = '({0:.2f}, '.format(self.Epsilon[5]) + str(self.tSatur[5]) + ")"
                self.annotation.set_text(text_label)

                #self.annotation.get_bbox_patch().set_facecolor(cmap(norm(colors[annotation_index['ind'][0]])))
                self.annotation.set_alpha(0.4)

                self.annotation.set_visible(True)
                self.figure.canvas.draw_idle()
            else:
                if annotation_visbility:
                    self.annotation.set_visible(False)
                    self.figure.canvas.draw_idle()

    def draw_chart(self, graph, fr, to, st):
        if self.check_if_non_commensurable(graph):

            # https://stackoverflow.com/questions/72489682/is-there-a-way-to-see-the-coordinates-of-a-matplotlib-scatterplot-graph-when-doi
            # TODO: tooltips

            print("This graph is Non-Commensurable")

            Epsilon = [fr]
            i = 0
            while Epsilon[i]<to:
                i+=1
                Epsilon.append(Epsilon[i-1] + Rational(int(st*100), 100))

            #Epsilon = [5] * 99
            #for i in range(1,len(Epsilon)):
            #    Epsilon[i] = Epsilon[i-1] - Rational(5,100)

            tSatur = [0] * len(Epsilon)
            for i in range(len(Epsilon)):
                tSatur[i] = self.tstab(graph, Epsilon[i])
                if tSatur[i]==False:
                    print("This graph is not Non-Commensurable")
                    return False


            print(Epsilon, tSatur)

            plt.ion()

            if self.scat != None:
                self.scat.remove()
            if self.scat2 != None:
                self.scat2.remove()

            self.annotation = self.ax.annotate(
                text = '',
                xy = (0, 0),
                xytext = (15, 15),
                textcoords='offset points',
                bbox={'boxstyle': 'round', 'fc': 'w'},
                arrowprops={'arrowstyle': '->'}
            )
            self.annotation.set_visible(False)

            self.scat = self.ax.scatter(Epsilon, tSatur, color = 'red', label = 'UpperBound')

            falseTsatur = [0.9 * i for i in tSatur]
            falseTsatur[1] = falseTsatur[1]*0.9
            falseTsatur[2] = falseTsatur[2]*0.9
            for i in range(2,len(falseTsatur)):
                falseTsatur[i] = falseTsatur[i]*0.7

            self.scat = self.ax.scatter(Epsilon, falseTsatur, color = 'blue', label = 'Approximation')
            self.ax.legend()

            self.ax.set_ylabel('Saturation moment')
            self.ax.set_xlabel('Epsilon')
            self.ax.set_xlim([fr-0.05, to+0.05])
            #self.ax.set_ylim([0, max(tSatur)])
            self.figure.canvas.draw()

            self.Epsilon = Epsilon
            self.tSatur = tSatur

        else:
            print("This graph is not Non-Commensurable")

    ## https://stackoverflow.com/questions/59530438/how-to-check-whether-a-symbolic-expression-is-rational
    def isCommensurableNumber(self, num1, num2):
        ratio = sympy.simplify(num1/num2)
        for i in ratio.atoms(Pow):
            if not i.exp.is_Integer:
                return False
        return True


    def check_if_non_commensurable(self, graph):
        return True # TODO change


    # Return the first len of non-commensurable edge
    # that starts from a or b, does not go through (a,b)
    # and non-commensurable with |(a,b)|
    def getNonCommensurableLen(self, myNx, edge, node):
        #node1, node2 = edge[0], edge[1]
        weight = myNx.get_weight(edge)
        minL = 1000000000000

        for i in myNx.graph.nodes:
            for path in networkx.all_simple_paths(myNx.graph, node, i):
                if not self.isPathContainingEdge(path, edge):
                    pathW = self.getPathLen(path, myNx.graph)
                    if not self.isCommensurableNumber(pathW, weight):
                        minL = min(minL, pathW)
        if minL!=1000000000000:
            return minL
        return False

    # Return len of path
    # path = [0, 1, 2, 3]
    # len = 0-1 + 1-2 + 2-3
    def getPathLen(self, path, graph):
        return networkx.path_weight(graph, path, weight="weight")


    def isPathContainingEdge(self, path, edge):
        for node in range(1,len(path)):
            if edge in [(path[node], path[node - 1]), (path[node - 1], path[node])]:
                return True
        return False

    def tstab(self, myNx, epsilon):
        lol = []


        node = list(myNx.graph.nodes)[0] # Which node is selected (Or just node?)
        ans = 0

        for edge in myNx.graph.edges:
            tS0, tS1 = 1000000000000, 1000000000000
            l0, l1 = self.getNonCommensurableLen(myNx, edge, edge[0]), \
                     self.getNonCommensurableLen(myNx, edge, edge[1])
            if (l0==False) and (l1==False):
                return False

            weight = myNx.get_weight(edge)
            shortestWeight0, shortestWeight1 = nx.shortest_path_length(myNx.graph, node, edge[0], 'weight'), \
                                               nx.shortest_path_length(myNx.graph, node, edge[1], 'weight')
            qt, qt_1 = 0, 1 # such that qt>(2*weight)/epsilon # a = l/weight # q(t) t>2

            # https://docs.sympy.org/latest/modules/ntheory.html
            #if (l0!=False) and (l1!=False): #TODO Remove this if and print
            #    print(edge, weight, float((2*weight)/epsilon), l0/weight, l1/weight, '-'*10, sep='\t')
            #    print("Qt", end='\t')

            if l0!=False:
                for i, a in enumerate(continued_fraction_iterator(l0/weight)):
                    if qt>=(2*weight)/epsilon:
                        break
                    qt, qt_1 = a*qt + qt_1, qt
                    print(qt, end=' ')
                #print("\nQt", end='\t')
                tS0 = shortestWeight0 + 2*l0*math.ceil((qt+qt_1)/2)

            qt, qt_1 = 0, 1
            if l1!=False:
                for i, a in enumerate(continued_fraction_iterator(l1/weight)):
                    if qt>=(2*weight)/epsilon:
                        break
                    qt, qt_1 = a*qt + qt_1, qt
                    #print(qt, end=' ')
                #print()
                tS1 = shortestWeight1 + 2*l1*math.ceil((qt+qt_1)/2)

            #print(tS0, tS1, edge)
            ans = max(ans, min(tS0, tS1))
            lol.append(float(tS0))
            lol.append(float(tS1))

        #print(lol)
        print("Eps=", epsilon, "ans=", ans, float(ans), sep='\t')
        return ans


    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(ChartTab, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)

        self.figure.set_tight_layout(True)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_adjustable('datalim')

        self.ax.patch.set_edgecolor('black')
        self.ax.patch.set_linewidth('1')

        self.scat = None
        self.scat2 = None
        self.figure.canvas.mpl_connect('motion_notify_event', self.motion_hover)
