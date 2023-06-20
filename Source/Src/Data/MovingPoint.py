class MovingPoint:

    # edge - is edge moving point is currently located
    # length - is length of edge
    # pos - is position on canvas. [0.1, 0.2]
    # dist - distance from start of edge.
    # dir - direction:
    #   1 means its moving from somewhere to 1
    def __init__(self, edge, length, dir, dist):
        self.edge = edge
        self.length = length
        self.old_pos = [0, 0]
        self.mid_pos = None
        self.pos = [0, 0]
        self.dist = dist
        self.dir = dir

    def __str__(self):
        return "Edge: " + str(self.edge) + \
               " Length: " + "{0:0.2f}".format(float(self.length)) + \
               " Distance: " + "{0:0.2f}".format(float(self.dist)) + \
               " Moving towards: " + str(self.dir)
    # " Old_pos: " + self.old_pos + \
    # " Mid_pos: " + self.mid_pos + \
    # " Pos: " + self.pos + \

    def __repr__(self):
        return "Edge: " + str(self.edge) + \
               " Length: " + "{0:0.2f}".format(float(self.length)) + \
               " Distance: " + "{0:0.2f}".format(float(self.dist)) + \
               " Moving towards: " + str(self.dir)
    # " Old_pos: " + str(self.old_pos) + \
    # " Mid_pos: " + str(self.mid_pos) + \
    # " Pos: " + str(self.pos) + \

    def __eq__(self, other):
        return self.edge == other.edge \
               and self.length == other.length \
               and self.dist == other.dist \
               and self.dir == other.dir

    def __hash__(self):
        return hash(self.edge) ^ hash(self.dist) ^ hash(self.length) ^ hash(self.dir)