# Dijkstra

A Python implementation on Dijkstra's minimum algorithm

## Getting Started

Download, clone or copy the code from the repository into a .py file

```
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
    
    # Example on how to access Path object attributes
    origin = min_path.origin  # Vertex object representing the origin
    destination = min_path.destination  # Vertex object representing the final destination
    total_cost = min_path.total_cost  # The total minimum cost found from origin to destination
    path = min_path.path  # List of Vertex objects in order from origin to destination representing the optimal path
    other_paths = min_path.alternate_paths  # List of Vertex objects lists representing similar cost paths to optimal
    str_result = min_path.result  # A string representation, making it prettier: A -> B ... -> F [Total cost(X)]
    print(min_path)  # As I've overrided print() function on __str__, this actually does: print(min_path.result)

    # You may also check more information inside Vertex objects
   
    # Example on how to access Vertex object attributes
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
    
```

### Prerequisites

Python 3

## Running the tests

You can simply run the file to see the given output. The example is by the end of the file, and it starts on the function

```
if __name__ == '__main__':
```

## Contributing

Any contribution is very welcome to the project (Code, suggestions and even errors/bug reports). If you do wish to help, please contact me at: lucasbbr98@gmail.com


## Authors

* **Lucas Arruda Bonservizzi** - *Initial work* - [lucasbbr98](https://github.com/lucasbbr98)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Inspiration 1: I enjoyed an Operations Research class from professor Cleber Rocco at UNICAMP - FCA.
* Inspiration 2: Most Dijkstra's algorithm I have found were not flexible or simple enough
* Inspiration 3: Maybe my code can help someone around the world. 
* Feel free to contact me if you need any help at lucasbbr98@gmail.com.
