from collections import defaultdict, deque
import sqlite3
from datetime import datetime

class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path

def shortest_path(graph, origin, destination):
    if destination == origin:
        return int(0), origin
    else:
        visited, paths = dijkstra(graph, origin)
        full_path = deque()
        _destination = paths[destination]
        while _destination != origin:
            full_path.appendleft(_destination)
            _destination = paths[_destination]
        
        full_path.appendleft(origin)
        full_path.append(destination)
    
        return int(visited[destination]), list(full_path)
'''
def dodaj_zlecenie():
    print("Podaj skąd: ")
    skad = input()
    print("Podaj dokąd: ")
    dokad = input()
    print("Podaj masa: ")
    masa = input()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task = (skad, dokad, masa, now)
    sql = """ INSERT INTO Zlecenia(skad,dokad,masa,data_przyjscia) VALUES(?,?,?,?) """
    kursor.execute(sql, task)
    print(shortest_path(graph, skad, dokad))
    return kierowcy(skad)
'''
