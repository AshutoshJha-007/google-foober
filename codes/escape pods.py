class Edge:
    def __init__(self, destination, capacity):
        self.destination = destination
        self.capacity = capacity
        self.remaining = capacity


class Node:

    def __init__(self, name, level=0, edges=None):
        self.name = name
        self.level = level
        if edges is None:
            self.edges = []

    def add_edge(self, destination, weight):
        self.edges.append(Edge(destination, weight))

    def get_children(self):
        res = []
        for edge in self.edges:
            res.append(edge.destination)
        return res

    def __str__(self):
        res = str(self.name) + " ({})".format(str(self.level))
        for edge in self.edges:
            res = res + " --> {} ({})".format(str(edge.destination), str(edge.remaining))
        return res


class Graph:
    nodes = []
    flow = []
    permanent_dead_ends = []
    levels = []

    def __init__(self, entrances, exits, matrix):
        self.entrances = entrances
        self.exits = exits
        self.matrix = matrix
        for i in range(0, len(self.matrix)):
            self.nodes.append(Node(i))

    def create(self):
        for i in range(0, len(self.matrix)):
            if self.nodes[i].name in self.exits:
                continue
            for j in range(0, len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    self.nodes[i].add_edge(j, self.matrix[i][j])

    def bfs(self):
        queue = self.entrances[:]
        seen = self.entrances[:]
        level = 0
        self.levels = [-1] * len(self.matrix)
        for entrance in self.entrances:
            self.nodes[entrance].level = level
            self.levels[entrance] = level
        while len(queue) > 0:
            to_remove = []
            i = queue.pop(0)
            level = self.nodes[i].level + 1
            for edge in self.nodes[i].edges:
                if edge.destination in self.permanent_dead_ends:
                    to_remove.append(edge)   # pruning permanent dead ends
                elif edge.remaining > 0:
                    if edge.destination not in seen:
                        self.nodes[edge.destination].level = self.levels[edge.destination] = level
                        queue.append(edge.destination)
                        seen.append(edge.destination)
                else:
                    to_remove.append(edge)
            for edge in to_remove:
                self.nodes[i].edges.remove(edge)

        #for node in self.nodes:
            #print(node)

        if self.is_finished():
            return False

        return True

    def is_finished(self):
        for ex in self.exits:
            if self.levels[ex] != -1:
                return False
        return True

    def choose_next_node(self, candidates, dead_ends):
        for i in candidates:
            previous_level = self.nodes[i].level
            for edge in self.nodes[i].edges:
                if (edge.remaining > 0) \
                        and (previous_level < self.nodes[edge.destination].level)\
                        and (edge.destination not in dead_ends):
                    return i, edge, edge.remaining
        return None, None, None

    def dfs(self):
        path = []
        capacities = []
        edges = []
        dead_ends = self.permanent_dead_ends[:]
        entr = self.entrances[:]
        current_node, edge, capacity = self.choose_next_node(entr, dead_ends)
        next_node = None
        if edge is not None:
            next_node = edge.destination
            edges.append(edge)
            path.append(current_node)
            if next_node in self.exits:
                path.append(next_node)
                capacities.append(capacity)
        else:
            return

        while next_node not in self.exits and len(path) > 0:
            if next_node != path[-1]:
                path.append(next_node)
                capacities.append(capacity)
            current_node, edge, capacity = self.choose_next_node([next_node], dead_ends)
            if edge is not None:
                next_node = edge.destination
                edges.append(edge)
                if next_node in self.exits:
                    path.append(next_node)
                    capacities.append(capacity)
            else:
                #print("dead-end reached: {}".format(path))
                if len(path) > 1:
                    dead_ends.append(path[-1])
                    path = path[:-1]
                    edges = edges[:-1]
                    next_node = path[-1]
                    capacities = capacities[:-1]
                else:
                    entr.remove(path[0])
                    path = []
                    capacities = []
                    current_node, edge, capacity = self.choose_next_node(entr, dead_ends)
                    next_node = None
                    if edge is not None:
                        next_node = edge.destination
                        edges.append(edge)
                        path.append(current_node)
                        if next_node in self.exits:
                            path.append(next_node)
                            capacities.append(capacity)
                    else:
                        return

        if len(path) < 1:
            #print("no path found!")
            return False

        capacity = min(capacities)
        #print("capacity: {}".format(capacity))
        self.flow.append(capacity)
        #print("path: {}".format(path))
        i = 0
        for edge in edges:
            edge.remaining -= capacity
            if edge.remaining == 0:
                self.nodes[path[i]].edges.remove(edge)
                if len(self.nodes[path[i]].edges) < 1:
                    self.permanent_dead_ends.append(self.nodes[path[i]].name)
                    #print("added permanent dead end: {}".format(self.nodes[path[i]].name))
            i += 1
        #for node in self.nodes:
            #print(node)

        return False


def solution(entrances, exits, matrix):
    graph = Graph(entrances,  exits, matrix)
    graph.create()
    while graph.bfs():
        #print("another BFS!")
        graph.dfs()
    #print("flow is: {}".format(graph.flow))
    return sum(graph.flow)