import Stack, Queue, MinHeap
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
            minHeap = MinHeap.Minheap() # Min heap for vertixes that are not processed yet
            minHeap.size = max_value + 1 # Min heap size
            # Add all vertices to the min heap
            for i in range(max_value + 1):
                minHeap.heap.append(minHeap.new_node(i, distances[i]))
                minHeap.pos.append(i)
            minHeap.pos[start] = start
            distances[start] = 0 # Distance from start vertex to itself is 0
            minHeap.decrease_key(start, distances[start]) # Change vertex position in heap according to it's new distance
            while minHeap.min_el() != end: # While distance from start to end is not found
                cur = minHeap.extract_min() # Get minimal vertex with minimal distance from set of processed vertices
                # Loop through adjacent vertices of current minimal vertex and update their distances if it's needed
                for i in range(len(self.adjacency_lists[cur.vertex])):
                    if minHeap.isInMinHeap(self.adjacency_lists[cur.vertex][i].value) and distances[cur.vertex] != sys.maxsize and self.adjacency_lists[cur.vertex][i].edge_value + distances[cur.vertex] < distances[self.adjacency_lists[cur.vertex][i].value]:
                        distances[self.adjacency_lists[cur.vertex][i].value] = self.adjacency_lists[cur.vertex][i].edge_value + distances[cur.vertex] # Change distance
                        minHeap.decrease_key(self.adjacency_lists[cur.vertex][i].value, distances[self.adjacency_lists[cur.vertex][i].value]) # Change position in min heap
            return distances[end]
        else:
            raise Exception("Path does not exist")
    

    # Prim algorithm. Find minimal spanning tree
    def MST_prima(self, start):
        if start in self.adjacency_lists.keys(): # If start vertex in the graph
            tree = UndirectedGraph() # Create new graph that will be returned as a result
            tree.adjacency_lists[start] = [] # Create list for adjacency vertices of start vertex
            max_value = self.max()
            distances = [sys.maxsize] * (max_value + 1) # Distances between adjacent vertices in graph
            parent = [-1] * (max_value + 1) # Parents of each vertex
            minHeap = MinHeap.Minheap() # Min heap for vertixes that are not processed yet
            minHeap.size = max_value + 1 # Min heap size
            # Add all vertices to the min heap
            for i in range(max_value + 1):
                minHeap.heap.append(minHeap.new_node(i, distances[i]))
                minHeap.pos.append(i)
            minHeap.pos[start] = start
            distances[start] = 0 # Distance from start vertex to itself is 0
            minHeap.decrease_key(start, distances[start]) # Change vertex position in heap according to it's new distance
            while minHeap.size > 1: # Until all vertices are processed
                cur = minHeap.extract_min() # Get minimal vertex with minimal distance from set of processed vertices
                if cur.vertex != start:
                    tree.insert(cur.vertex, parent[cur.vertex], cur.distance)
                # Loop through adjacent vertices of current minimal vertex and update their distances if it's needed
                for i in range(len(self.adjacency_lists[cur.vertex])):
                    if minHeap.isInMinHeap(self.adjacency_lists[cur.vertex][i].value) and distances[cur.vertex] != sys.maxsize and self.adjacency_lists[cur.vertex][i].edge_value < distances[self.adjacency_lists[cur.vertex][i].value]:
                        distances[self.adjacency_lists[cur.vertex][i].value] = self.adjacency_lists[cur.vertex][i].edge_value # Change distance
                        minHeap.decrease_key(self.adjacency_lists[cur.vertex][i].value, distances[self.adjacency_lists[cur.vertex][i].value]) # Change position in min heap
                        parent[self.adjacency_lists[cur.vertex][i].value] = cur.vertex # Add parent of minimal vertex
            return tree
        else:
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
