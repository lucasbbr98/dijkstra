# dijkstra
An implementation of Dijkstra minimum path algorithm in plain Python

Example on how to setup and run the Dijkstra's algorithm:


1) Initiate an instance of Dijkstra's class
d = Dijkstra()


2) Add vertexes with any custom Label
d.graph.add_vertexes(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])


3) Adds connections between the vertexes. Labels must match with already added vertexes
d.graph.add_connections([
    ('A', 3, 'B'),
    ('A', 1, 'C'),
    ('B', 1, 'D'),
    ('B', 5, 'G'),
    ('C', 2, 'D'),
    ('C', 5, 'F'),
    ('D', 2, 'F'),
    ('D', 4, 'E'),
    ('E', 2, 'G'),
    ('E', 1, 'H'),
    ('F', 3, 'H')
])


4) Solve and get a Path object, with the results stored inside it
min_path = d.solve(origin='A', destination='H')


