import Stack, Queue
import sys


class GraphNode:

    def __init__(self, value, edge_value = 0):
        self.value = value
        self.edge_value = edge_value


class UndirectedGraph:

    def __init__(self):
        self.adjacency_lists = {}

    # Find vertex with max value
    def max(self):
        max_value = 0
        for key in self.adjacency_lists:
            if key > max_value:
                max_value = key
            for i in range(len(self.adjacency_lists[key])):
                if self.adjacency_lists[key][i].value > max_value:
                    max_value = self.adjacency_lists[key][i].value
        return max_value

    # Insert edge [vertex1, vertex2] with weight of edge_val into the graph
    def insert(self, vertex1, vertex2, edge_val):
        if vertex1 in self.adjacency_lists.keys(): # If vertex1 in adjacency list
            # Check if edge already exists
            for i in range(len(self.adjacency_lists[vertex1])):
                if self.adjacency_lists[vertex1][i].value == vertex2:
                    raise Exception("Edge already exists")
            new_node = GraphNode(vertex2, edge_val) # Create vertex2 node
            self.adjacency_lists[vertex1].append(new_node) # Add new node to adjacency vertices of vertex1
            if vertex2 in self.adjacency_lists.keys(): # If vertex2 in adjacency list
                new_node = GraphNode(vertex1, edge_val) # Create vertex1 node
                self.adjacency_lists[vertex2].append(new_node) # Add new node to adjacency vertices of vertex2
            else:
                self.adjacency_lists[vertex2] = [] # Add vertex2 to the adjacency list
                new_node = GraphNode(vertex1, edge_val) # Create vertex1 node
                self.adjacency_lists[vertex2].append(new_node) # Add new node to adjacency vertices of vertex2
        else:
            self.adjacency_lists[vertex1] = [] # Add vertex1 to the adjacency list
            new_node = GraphNode(vertex2, edge_val) # Create vertex2 node
            self.adjacency_lists[vertex1].append(new_node) # Add new node to adjacency vertices of vertex1
            if vertex2 in self.adjacency_lists.keys(): # If vertex2 in adjacency list
                new_node = GraphNode(vertex1, edge_val) # Create vertex1 node
                self.adjacency_lists[vertex2].append(new_node) # Add new node to adjacency vertices of vertex2
            else:
                self.adjacency_lists[vertex2] = [] # Add vertex2 to the adjacency list
                new_node = GraphNode(vertex1, edge_val)  # Create vertex1 node
                self.adjacency_lists[vertex2].append(new_node)  # Add new node to adjacency vertices of vertex2

    # Remove edge [vertex1, vertex2] from the graph
    def remove(self, vertex1, vertex2):
        if vertex1 in self.adjacency_lists: # If vertex1 in adjacency list
            for i in range(len(self.adjacency_lists[vertex1])): # Delete vertex2 from list of adjacency vertices of vertex1
                if self.adjacency_lists[vertex1][i].value == vertex2:
                    del self.adjacency_lists[vertex1][i]
                    break
            else: # If vertex2 not found in list of adjacency vertices of vertex1 then edge does not exist
                raise Exception("Edge does not exist")
            for i in range(len(self.adjacency_lists[vertex2])): # Delete vertex1 from list of adjacency vertices of vertex2
                if self.adjacency_lists[vertex2][i].value == vertex1:
                    del self.adjacency_lists[vertex2][i]
                    break
        else: # Edge does not exist
            raise Exception("Edge does not exist")    

    
    # Dijkstra shortest path algorithm
    def dijkstra(self, start, end):
        if start in self.adjacency_lists.keys() and end in self.adjacency_lists.keys(): # If start and end vertices in the adjacency list
            max_value = self.max() # Max value in the graph
            distances = [sys.maxsize] * (max_value + 1) # Distances from start to vertex[i]
            known = [False] * (max_value + 1) # Set of processed vertices (marked as True)
            distances[start] = 0 # Distance from start vertex to itself is 0
            cur = start
            while cur != end: # While distance from start to end is not found
                min_vertex = -1 # Current minimal vertex
                min_distance = sys.maxsize # Current minimal distance to minimal vertex
                # Find minimal edge coming out of set of processed vertices
                for i in range(max_value + 1): # Loop throught all vertices
                    if distances[i] < min_distance and known[i] == False:
                        min_distance = distances[i]
                        min_vertex = i
                known[min_vertex] = True # Add minimal vertex to the set of processed vertices
                # Add new edges coming out of set of processed vertices if the are smaller than existing distances
                for i in range(len(self.adjacency_lists[min_vertex])): 
                    if known[self.adjacency_lists[min_vertex][i].value] == False and distances[min_vertex] + self.adjacency_lists[min_vertex][i].edge_value < distances[self.adjacency_lists[min_vertex][i].value]:
                        distances[self.adjacency_lists[min_vertex][i].value] = distances[min_vertex] + self.adjacency_lists[min_vertex][i].edge_value
                cur = min_vertex 
            return distances[end] # Return shortest path value from start to end
        else: # Path does not exist
            raise Exception("Path does not exist")
    
    # Prima algorithm. Find minimal spanning tree
    def MST_prima(self, start):
        if start in self.adjacency_lists.keys(): # If start vertex in the graph
            tree = UndirectedGraph() # Create new graph that will be returned as a result
            tree.adjacency_lists[start] = [] # Create list for adjacency vertices of start vertex
            max_value = self.max()
            distances = [sys.maxsize] * (max_value + 1) # Distances between adjacent vertices in graph
            known = [False] * (max_value + 1) # Set of processed vertices (marked as True)
            parent = [-1] * (max_value + 1) # Parents of each vertex
            distances[start] = 0 # Distance from start vertex to itself is 0
            while len(tree.adjacency_lists.keys()) != len(self.adjacency_lists.keys()): # Until all vertices are processed
                min_vertex = -1 # Current minimal vertex
                min_edge = sys.maxsize # Current minimal edge
                # Find minimal edge coming out of set of processed vertices
                for i in range(max_value + 1): # Loop throught all vertices
                    if distances[i] < min_edge and known[i] == False:
                        min_edge = distances[i]
                        min_vertex = i
                known[min_vertex] = True # Add minimal vertex to the set of processed vertices
                if min_vertex != start: # If current minimal vertex isn't a start vertex
                    tree.insert(min_vertex, parent[min_vertex], min_edge) # Add edge [min_vertex, min_vertex parent] into the tree
                # Add new edges coming out of set of processed vertices if the are smaller than existing distances
                for i in range(len(self.adjacency_lists[min_vertex])):
                    if known[self.adjacency_lists[min_vertex][i].value] == False and self.adjacency_lists[min_vertex][i].edge_value < distances[self.adjacency_lists[min_vertex][i].value]:
                        distances[self.adjacency_lists[min_vertex][i].value] = self.adjacency_lists[min_vertex][i].edge_value
                        parent[self.adjacency_lists[min_vertex][i].value] = min_vertex # Add parent of minimal vertex
            return tree # Return MST
        else: # Start vertex does not exist
            raise Exception("Vertex does not exist")

        
    # Depth first traversal iterator      
    class dftIterator:

        def __init__(self, graph, start=None):
            self.stack = Stack.Stack()
            self.graph = graph
            self.visited = [False] * (graph.max() + 1) # Visited vertices
            if start is None:
                self.stack.push(list(graph.adjacency_lists.keys())[0]) # Push first vertex of adjacency list into the stack
            else:
                self.stack.push(start) # Push start vertex into the stack
            self.traversal_done = False
            self.graph_size = len(graph.adjacency_lists.keys()) # Number of vertices in the graph

        def __next__(self):
            if self.has_next():
                temp = self.stack.pop()
                if self.visited[temp] == True: # If vertex is already visited go to the next vertex in stack
                    return self.__next__()
                self.visited[temp] = True # Mark vertex as visited
                if temp in self.graph.adjacency_lists.keys(): # If current vertex has adjacent vertices
                    # Add not visited adjacent vertices into the stack
                    for i in range(len(self.graph.adjacency_lists[temp])):
                        if self.visited[self.graph.adjacency_lists[temp][i].value] == False:
                            self.stack.push(self.graph.adjacency_lists[temp][i].value)
                return temp # Return current vertex
            else:
                # Checking for other raw connectivity components
                self.traversal_done = True
                for key in self.graph.adjacency_lists: # Find not visited vertex that has adjacent vertices
                    if self.visited[key] == False:
                        self.stack.push(key)
                        self.traversal_done = False
                        break
                if self.traversal_done == False: # If we found that vertex
                    temp = self.stack.pop()
                    self.visited[temp] = True # Mark vertex as visited
                    # Add not visited adjacent vertices into the stack
                    for i in range(len(self.graph.adjacency_lists[temp])):
                        if self.visited[self.graph.adjacency_lists[temp][i].value] == False:
                            self.stack.push(self.graph.adjacency_lists[temp][i].value)
                    return temp # Return current vertex
                else:
                    raise StopIteration # Traversal is done

        def has_next(self):
            if self.stack.isEmpty():
                return False
            else:
                return True


    class bftIterator:

        def __init__(self, graph, start=None):
            self.queue = Queue.Queue()
            self.graph = graph
            self.visited = [False] * (graph.max() + 1)
            if start is None:
                self.queue.enqueue(list(graph.adjacency_lists.keys())[0]) # Insert first vertex of adjacency list into the queue
            else:
                self.queue.enqueue(start) # Insert start vertex into the queue
            self.traversal_done = False
            self.graph_size = len(graph.adjacency_lists.keys()) # Number of vertices in graph

        def __next__(self):
            if self.has_next():
                temp = self.queue.dequeue()
                if self.visited[temp] == True: # If vertex is already visited go to the next vertex in queue
                    return self.__next__()
                self.visited[temp] = True # Mark vertex as visited
                if temp in self.graph.adjacency_lists.keys(): # If current vertex has adjacent vertices
                    # Add not visited adjacent vertices into the queue
                    for i in range(len(self.graph.adjacency_lists[temp])):
                        if self.visited[self.graph.adjacency_lists[temp][i].value] == False:
                            self.queue.enqueue(self.graph.adjacency_lists[temp][i].value)
                return temp # Return current vertex
            else:
                # Checking for other raw connectivity components
                self.traversal_done = True
                for key in self.graph.adjacency_lists: # Find not visited vertex that has adjacent vertices
                    if self.visited[key] == False:
                        self.queue.enqueue(key)
                        self.traversal_done = False
                        break
                if self.traversal_done == False: # If we found that vertex
                    temp = self.queue.dequeue()
                    self.visited[temp] = True # Mark vertex as visited
                    # Add not visited adjacent vertices into the queue
                    for i in range(len(self.graph.adjacency_lists[temp])):
                        if self.visited[self.graph.adjacency_lists[temp][i].value] == False:
                            self.queue.enqueue(self.graph.adjacency_lists[temp][i].value)
                    return temp # Return current vertex
                else:
                    raise StopIteration # Traversal is done

        def has_next(self):
            if self.queue.isEmpty():
                return False
            else:
                return True
