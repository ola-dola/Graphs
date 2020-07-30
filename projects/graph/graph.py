"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()
        else:
            raise Exception(f"Vertex with id {vertex_id} already exists")

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 == v2:
            raise Exception(
                "ERROR ADDING EDGE: You can't connecct a vetex to itself")

        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise Exception(
                f"Vertex {v2 if v1 in self.vertices else v1} does not exist")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        if starting_vertex not in self.vertices:
            raise Exception(
                "Error BFT: startting vertex not a member of the graph")

        qq = Queue()
        # Enqueue starting vet, in a list as path
        qq.enqueue([starting_vertex])
        # Keep track of visited nodes and all the path.
        # Final_path as a list neede cos sets don't keep track of order,
        # and lookup is time expensive in list
        visited = set()
        final_path = []

        while qq.size() > 0:
            path = qq.dequeue()

            if path[-1] not in visited:
                final_path.append(path[-1])
                print(path[-1])

                for neighbor in self.get_neighbors(path[-1]):
                    new_path = path.copy()
                    new_path.append(neighbor)

                    qq.enqueue(new_path)

                visited.add(path[-1])

        # print(final_path)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        stack = Stack()
        stack.push(starting_vertex)
        visited = set()

        while stack.size() > 0:
            current = stack.pop()

            if current not in visited:
                print(current)

                for neighbor in self.vertices[current]:
                    stack.push(neighbor)

                visited.add(current)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # Read up on why not to default to set().
        if visited is None:
            visited = set()

        # Explicit base case return. Could be left out, 
        # and use python's implicit return.
        if starting_vertex in visited:
            return

        visited.add(starting_vertex)
        print(starting_vertex)

        for neighbor in self.vertices[starting_vertex]:
            if neighbor not in visited:
                self.dft_recursive(neighbor, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        if starting_vertex not in self.vertices or destination_vertex not in self.vertices:
            raise Exception(
                "Error BFT: starting/destination vertex not a member of the graph")

        qq = Queue()
        # Enqueue starting vet, in a list as path
        qq.enqueue([starting_vertex])
        # Keep track of visited nodes and all the path.
        visited = set()

        while qq.size() > 0:
            path = qq.dequeue()

            if path[-1] == destination_vertex:
                return path

            if path[-1] not in visited:
                print(path[-1])

                for neighbor in self.get_neighbors(path[-1]):
                    new_path = path.copy()
                    new_path.append(neighbor)

                    qq.enqueue(new_path)

                visited.add(path[-1])

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        stack = Stack()
        visited = set()
        stack.push([starting_vertex])

        while stack.size() > 0:
            path = stack.pop()

            if path[-1] == destination_vertex:
                return path

            if path[-1] not in visited:
                for neighbor in self.vertices[path[-1]]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.push(new_path)

                visited.add(path[-1])


    def dfs_recursive(self, starting_vertex, destination_vertex,  visited=None, path=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if path is None:
            path = []

        if visited is None:
            visited = set()

        new_path = path + [starting_vertex]
        visited.add(starting_vertex)

        if starting_vertex == destination_vertex:
            return new_path

        for neighbor in self.get_neighbors(starting_vertex):
            if neighbor not in visited:
                neighbor_path = self.dfs_recursive(neighbor, destination_vertex, visited, new_path)
                if neighbor_path:
                    return neighbor_path


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
