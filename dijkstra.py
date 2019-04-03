from collections import defaultdict, deque
import sqlite3
from datetime import datetime

db = sqlite3.connect('ASJW.db')
db.row_factory = sqlite3.Row
kursor = db.cursor()


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

graph = Graph()

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

kursor.execute(
        """
        SELECT miejscowosc_A, miejscowosc_B, czas FROM PUNKTY_MAPY
        """)
punkty = kursor.fetchall()
zbior = list()
z = list()
s = list()
t = list()
for PUNKTY_MAPY in punkty:
    z.append(PUNKTY_MAPY['miejscowosc_A'])
    s.append(PUNKTY_MAPY['miejscowosc_B'])
    t.append(PUNKTY_MAPY['czas'])
    zbior = z + s
        
for node in zbior:
    graph.add_node(node)

i = 0
while i < len(z):
    graph.add_edge(str(z[i]), str(s[i]), int(t[i]))
    i = i + 1

def kierowcy(y):
    kursor.execute(
        """
        SELECT id_samochodu, miejsce_przebywania FROM SAMOCHODY WHERE miejsce_przebywania IS NOT NULL
        """)
    kierowcy = kursor.fetchall()
    k = list()
    m = list()
    for SAMOCHODY in kierowcy:
        k.append(SAMOCHODY['miejsce_przebywania'])
        m.append(SAMOCHODY['id_samochodu'])
    
    if y in zbior:
        w = {}
        i = 0
        while i < len(k):
            w[m[i]] = shortest_path(graph, str(k[i]), y)
            i = i + 1
        lista=sorted(w.items(), key=lambda x: x[1])
        for elem in lista :
            print(elem[0] , "::", elem[1])
    else:
        return("Nie ma takiej miejscowości w bazie")

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
