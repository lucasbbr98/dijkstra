from operator import attrgetter


# Sorry, I was too lazy to actually make this any better. It should be in a 'helper file' in larger projects
def are_values_unique(x):
    """ Asserts values are unique in a list """
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)


class Vertex:
    """ Represents a vertex, for instance: A, B, C ... """
    def __init__(self, label: str):
        self.label = label

        # Needed for Dijkstra's algorithm. Updated at the startup automatically
        self.is_origin = False
        self.is_destination = False
        self.min_cost = float("inf")
        self.coming_from = None
        self.ties = []
        self.has_visited = False
        self.neighbours = []

    @property
    def unvisited_neighbours(self) -> list:
        return [n for n in self.neighbours if not n.has_visited]

    def __repr__(self):
        return "Vertex {0}".format(self.label)


class Connection:
    """ Represents a Connection between two Vertex objects, with an associated weight """
    def __init__(self, vertex_one: Vertex, vertex_two: Vertex, weight: float):
        self.vertex_one = vertex_one
        self.vertex_two = vertex_two
        self.weight = weight

    def __repr__(self):
        return "Connection {0} - {1} - {2}".format(self.vertex_one.label, self.weight, self.vertex_two.label)


class Graph:
    """ Represents a whole Graph. It also facilitates developers to create them with helper functions """
    def __init__(self, vertexes=None, connections=None):
        if connections is None:
            connections = []
        if vertexes is None:
            vertexes = []
        self.vertexes = vertexes
        self.connections = connections
        self.__origin_index__ = None
        self.__destination_index__ = None

    def get_vertex_by_label(self, label: str) -> Vertex:
        if not label or not isinstance(label, str):
            raise ValueError("Label must be a string")

        vertex = None
        for v in self.vertexes:
            if v.label == label:
                vertex = v
                break
        return vertex

    def get_cost_from_to(self, v1: Vertex, v2: Vertex) -> float:
        distance = 0
        for c in self.connections:
            if (c.vertex_one == v1 and c.vertex_two == v2) or (c.vertex_one == v2 and c.vertex_two == v1):
                distance = c.weight
                break
        return distance

    @property
    def origin_vertex(self) -> Vertex:
        return self.vertexes[self.__origin_index__]

    @property
    def destination_vertex(self) -> Vertex:
        return self.vertexes[self.__destination_index__]

    @property
    def unvisited_vertexes(self) -> list:
        return [v for v in self.vertexes if not v.has_visited]

    def add_vertex(self, label: str):
        if label in [x.label for x in self.vertexes]:
            raise IndexError("Labels must be unique. We have found a duplicate in Vertex labeled: {0}".format(label))
        self.vertexes.append(Vertex(label=label.upper()))

    def add_vertexes(self, list_of_labels: list):
        if not all(isinstance(e, str) for e in list_of_labels):
            raise ValueError("List of vertexes labels must contain only strings")

        list_of_labels_upper = [x.upper() for x in list_of_labels]
        if not are_values_unique(list_of_labels_upper):
            raise IndexError("All values of vertexes labels must be unique. Please check again.")

        for label in list_of_labels_upper:
            self.add_vertex(label)

    def set_origin(self, origin_label: str):
        if origin_label is None or not isinstance(origin_label, str):
            raise ValueError("Origin label must be a string")

        if origin_label not in [x.label for x in self.vertexes]:
            raise IndexError("We could not find an index containing the following label: {0}".format(origin_label))

        origin_label = origin_label.upper()
        for index, vertex in enumerate(self.vertexes):
            if vertex.label == origin_label:
                if vertex.is_destination:
                    raise ValueError("Vertex {0} is already a destination and cant be an origin."
                                     "\nYou may reset the origin with the function "
                                     "Dijkstra.reset_origin()".format(vertex.label))
                vertex.is_origin = True
                vertex.min_cost = 0
                self.__origin_index__ = index
            else:
                vertex.is_origin = False

    def set_destination(self, destination_label: str):
        if destination_label is None or not isinstance(destination_label, str):
            raise ValueError("Destination label must be a string")

        if destination_label not in [x.label for x in self.vertexes]:
            raise IndexError("We could not find an index containing the following label: {0}".format(destination_label))

        destination_label = destination_label.upper()
        for index, vertex in enumerate(self.vertexes):
            if vertex.label == destination_label:
                if vertex.is_origin:
                    raise ValueError("Vertex {0} is already an origin and cant be a destination."
                                     "\nYou may reset the destination with the function "
                                     "Dijkstra.reset_destination()".format(vertex.label))
                vertex.is_destination = True
                self.__destination_index__ = index
            else:
                vertex.is_destination = False

    def reset_origin(self):
        for v in self.vertexes:
            v.is_origin = False
        self.__origin_index__ = None

    def reset_destination(self):
        for v in self.vertexes:
            v.is_destination = False
        self.__destination_index__ = None

    def add_connection(self, label_one: str, weight:float, label_two: str):
        if not label_one or not label_two or not isinstance(label_one, str) or not isinstance(label_two, str):
            raise ValueError("Connection labels must be of type string.")
        label_one = label_one.upper()
        label_two = label_two.upper()
        if label_one == label_two:
            raise ValueError("Connection labels cannot be identical."
                             "\nGot: {0} - {1} - {2}".format(label_one, weight, label_two))

        vertex_one = self.get_vertex_by_label(label=label_one)
        if not vertex_one:
            raise ValueError("A Vertex with label {0} was not found".format(label_one))
        vertex_two = self.get_vertex_by_label(label=label_two)
        if not vertex_two:
            raise ValueError("A Vertex with label {0} was not found".format(vertex_two))

        try:
            weight = float(weight)
        except ValueError:
            raise ValueError("Weight must be a number")

        if weight <= 0:
            raise ValueError("Weights must be positive and greater than 0")

        for c in self.connections:
            if (c.vertex_one == vertex_one and c.vertex_two == vertex_two) or (c.vertex_one == vertex_two and c.vertex_two == vertex_one):
                raise ValueError("You have assigned two weights for the same vertexes."
                                 "\nAssigned: {0} - {1} - {2}"
                                 "\nAttempted: {3} - {4} - {5}".format(c.vertex_one.label, c.weight, c.vertex_two.label,
                                                                       c.vertex_one.label, weight, c.vertex_two.label))

        self.connections.append(Connection(vertex_one=vertex_one, weight=weight, vertex_two=vertex_two))
        vertex_one.neighbours.append(vertex_two)
        vertex_two.neighbours.append(vertex_one)

    def add_connections(self, tuple_of_connections: list):
        for c in tuple_of_connections:
            self.add_connection(c[0], c[1], c[2])


class Path:
    """ Represents an optimal path from Dijkstra algorithm, as well as similar cost paths """
    def __init__(self, main_path: list, alternate_paths=None):
        self.path = main_path
        if alternate_paths is None:
            self.alternate_paths = []
        else:
            self.alternate_paths = alternate_paths

    @property
    def total_cost(self) -> float:
        return self.path[-1].min_cost

    @property
    def origin(self) -> Vertex:
        return self.path[0]

    @property
    def destination(self) -> Vertex:
        return self.path[-1]

    @property
    def result(self) -> str:
        str_path = 'Main route: '
        last_index = len(self.path) - 1
        for index, v in enumerate(self.path):
            if index == last_index:
                str_path = str_path + v.label
            else:
                str_path = str_path + v.label + ' -> '
        str_path = str_path + ' [Total cost: ({0})]\n'.format(self.total_cost)

        for a_index, a in enumerate(self.alternate_paths):
            str_path = str_path + 'Alternate route {0}: '.format(a_index + 1)
            last_index = len(a) - 1
            for index, v in enumerate(a):
                if index == last_index:
                    str_path = str_path + v.label
                else:
                    str_path = str_path + v.label + ' -> '
            str_path = str_path + ' [Total cost: ({0})]\n'.format(self.total_cost)

        return str_path

    def __str__(self):
        """ Overrides print(Path) """
        return self.result


class Dijkstra:
    def __init__(self, graph=None):
        if isinstance(graph, Graph):
            self.graph = graph
        else:
            self.graph = Graph()

        self.minimal_route = []

    def solve(self, origin: str, destination: str) -> Path:
        self.graph.set_origin(origin.upper())
        self.graph.set_destination(destination.upper())

        for v in self.graph.vertexes:
            vertex_has_connection = False
            for c in self.graph.connections:
                if v == c.vertex_one or v == c.vertex_two:
                    vertex_has_connection = True
                    break

            if not vertex_has_connection:
                raise AssertionError("FATAL ERROR: Vertex {0} was not found in any connections but added to the graph."
                                     .format(v.label))

        # Actual algorithm
        for _ in self.graph.vertexes:
            current_vertex = min(self.graph.unvisited_vertexes, key=attrgetter('min_cost'))
            current_vertex.has_visited = True
            current_neighbours = current_vertex.unvisited_neighbours
            for n in current_neighbours:
                cost_to_neighbour = self.graph.get_cost_from_to(current_vertex, n)
                current_cost = current_vertex.min_cost + cost_to_neighbour

                if current_cost < n.min_cost:
                    n.min_cost = current_cost
                    n.coming_from = current_vertex
                elif current_cost == n.min_cost:
                    n.ties.append(current_vertex)

                if n == self.graph.destination_vertex:
                    break

        # Reversing back to get the result
        min_path = [self.graph.destination_vertex]
        is_origin = False
        last_added = self.graph.destination_vertex
        while not is_origin:
            min_path.insert(0, last_added.coming_from)
            last_added = last_added.coming_from
            if last_added == self.graph.origin_vertex:
                is_origin = True

        alternate_paths = []
        for t in self.graph.destination_vertex.ties:
            min_path_alt = [t, self.graph.destination_vertex]
            is_origin = False
            last_added = t
            while not is_origin:
                min_path_alt.insert(0, last_added.coming_from)
                last_added = last_added.coming_from
                if last_added == self.graph.origin_vertex:
                    is_origin = True
            alternate_paths.append(min_path_alt)

        return Path(main_path=min_path, alternate_paths=alternate_paths)


if __name__ == '__main__':
    """ Example on how to setup and run the Dijkstra's algorithm """
    # Initiates an instance of Dijkstra's class
    d = Dijkstra()
    # Add vertexes with any custom Label
    d.graph.add_vertexes(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    # Adds connections between the vertexes. Labels must match with already added vertexes
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

    # Solves and returns a Path object, with all the information stored inside it
    min_path = d.solve(origin='A', destination='H')
    origin = min_path.origin  # Vertex object representing the origin
    destination = min_path.destination  # Vertex object representing the final destination
    total_cost = min_path.total_cost  # The total minimum cost found from origin to destination
    path = min_path.path  # List of Vertex objects in order from origin to destination representing the optimal path
    other_paths = min_path.alternate_paths  # List of Vertex objects lists representing similar cost paths to optimal
    str_result = min_path.result  # A string representation, making it prettier: A -> B ... -> F [Total cost(X)]
    print(min_path)  # As I've overrided print() function on __str__, this actually does: print(min_path.result)

    # You may also check more information inside Vertex objects
    # NOTE: Erase the triple quotes (''') on top and at the bottom to see it in action
    ''' < ERASE HERE FOR THE TUTORIAL
    
    print('Example on how to access Vertex attributes')
    v = min_path.destination
    print('Vertex Label: {0} -> str'.format(v.label))
    print('Is Route Origin? : {0} -> bool'.format(v.is_origin))
    print('Is Route Destination? : {0} -> bool'.format(v.is_destination))
    print('Minimum cost from origin: {0} -> float'.format(v.min_cost))
    print('Who should I come from?: {0} -> Vertex() object'.format(v.coming_from))
    print('Which other vertexes should I come from (That ties the minimum cost)?: {0} -> list'.format(v.ties))
    print('Did Dijkstra visit and calculate their neighbours minimum cost?: {0} -> bool'.format(v.has_visited))
    print('Neighbours: {0} -> list'.format(v.neighbours))
    print('Unvisited Neighbours: {0} -> list'.format(v.unvisited_neighbours))
    
    ERASE HERE FOR THE TUTORIAL >'''
