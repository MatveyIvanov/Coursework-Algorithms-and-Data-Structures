import Stack, Queue, MinHeap, LinkedList
import sys


class UndirectedGraph:

    def __init__(self):
        self.adjacency_lists = LinkedList.LinkedList()

    # Find vertex with max value
    def max(self):
        if self.adjacency_lists.head != None:
            max_value = 0
            cur_list = self.adjacency_lists.head
            while cur_list != None:
                cur = cur_list
                while cur != None:
                    if cur.value > max_value:
                        max_value = cur.value
                    cur = cur.next
                cur_list = cur_list.next_list
            return max_value
        else:
            raise Exception("Graph is empty")
    
    # Number of vertices in the graph
    def vertices_count(self):
        result = 0
        cur_list = self.adjacency_lists.head
        while cur_list != None:
            result += 1
            cur_list = cur_list.next_list
        return result

    # Insert edge [vertex1, vertex2] with weight of edge_val into the graph
    def insert(self, vertex1, vertex2, edge_val):
        # If graph is empty
        if self.adjacency_lists.head == None:
            self.adjacency_lists.head = LinkedList.LinkedListNode(vertex1, edge_val)
            self.adjacency_lists.head.next = LinkedList.LinkedListNode(vertex2, edge_val)
            self.adjacency_lists.head.next_list = LinkedList.LinkedListNode(vertex2, edge_val)
            self.adjacency_lists.head.next_list.next = LinkedList.LinkedListNode(vertex1, edge_val)
        else: 
            cur_list = self.adjacency_lists.head
            while cur_list.next_list != None and cur_list.value != vertex1:
                cur_list = cur_list.next_list
            # If vertex1 already has adjacent vertices
            if cur_list.value == vertex1:
                cur = cur_list.next
                while cur.next != None:
                    if cur.value == vertex2: # If edge already exists
                        raise Exception("Edge already exists")
                    cur = cur.next
                if cur.value == vertex2: # If edge already exists
                    raise Exception("Edge already exists")
                else: # Add vertex2 to the list of adjacent vertices of vertex1
                    cur.next = LinkedList.LinkedListNode(vertex2, edge_val)
                cur_list = self.adjacency_lists.head
                # Insert edge [vertex2, vertex1]
                while cur_list.next_list != None and cur_list.value != vertex2:
                    cur_list = cur_list.next_list
                if cur_list.value == vertex2:
                    cur = cur_list.next
                    while cur.next != None:
                        cur = cur.next
                    cur.next = LinkedList.LinkedListNode(vertex1, edge_val)
                else:
                    cur_list.next_list = LinkedList.LinkedListNode(vertex2, edge_val)
                    cur_list.next_list.next = LinkedList.LinkedListNode(vertex1, edge_val)
            # If vertex1 does not have adjacent vertices
            else:
                cur_list.next_list = LinkedList.LinkedListNode(vertex1, edge_val)
                cur_list.next_list.next = LinkedList.LinkedListNode(vertex2, edge_val)
                cur_list = self.adjacency_lists.head
                while cur_list.next_list != None and cur_list.value != vertex2:
                    cur_list = cur_list.next_list
                if cur_list.value == vertex2:
                    cur = cur_list.next
                    while cur.next != None:
                        cur = cur.next
                    cur.next = LinkedList.LinkedListNode(vertex1, edge_val)
                else:
                    cur_list.next_list = LinkedList.LinkedListNode(vertex2, edge_val)
                    cur_list.next_list.next = LinkedList.LinkedListNode(vertex1, edge_val)


    # Remove edge [vertex1, vertex2] from the graph
    def remove(self, vertex1, vertex2):
        # If graph is not empty
        if self.adjacency_lists.head != None:
            cur_list = self.adjacency_lists.head
            # Search for list of adjacent vertices of vertex1
            while cur_list != None:
                if cur_list.value == vertex1:
                    break
                cur_list = cur_list.next_list
            # If that list is not found
            if cur_list == None:
                raise Exception("Edge does not exist")
            else:
                # Delete vertex2 from list
                if cur_list.next.value == vertex2:
                    cur_list.next = cur_list.next.next
                else:
                    cur = cur_list.next
                    while cur.next != None and cur.next.value != vertex2:
                        cur = cur.next
                    if cur.next == None:
                        raise Exception("Edge does not exist")
                    else:
                        temp = cur.next.next
                        cur.next = None
                        cur.next = temp
            # Do the same for edge [vertex2, vertex1]
            cur_list = self.adjacency_lists.head
            while cur_list.value != vertex2:
                cur_list = cur_list.next_list
            if cur_list.next.value == vertex1:
                cur_list.next = cur_list.next.next
            else:
                cur = cur_list.next
                while cur.next.value != vertex1:
                    cur = cur.next
                temp = cur.next.next
                cur.next = None
                cur.next = temp
        else: # If edge does not exist
            raise Exception("Edge does not exist")  

    # Dijkstra shortest path algorithm
    def dijkstra(self, start, end):
        cur_list = self.adjacency_lists.head
        start_found = False
        end_found = False
        # Check if start and end vertices are in the graph
        while cur_list != None and (start_found == False or end_found == False):
            if cur_list.value == start:
                start_found = True
            if cur_list.value == end:
                end_found = True
            cur_list = cur_list.next_list
        if start_found == True and end_found == True:
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
                cur_min = minHeap.extract_min() # Get minimal vertex with minimal distance from set of processed vertices
                cur_list = self.adjacency_lists.head
                while cur_list != None and cur_list.value != cur_min.vertex:
                    cur_list = cur_list.next_list
                # Loop through adjacent vertices of current minimal vertex and update their distances if it's needed
                if cur_list != None:
                    cur = cur_list.next
                    while cur != None:
                        if minHeap.isInMinHeap(cur.value) and distances[cur_min.vertex] != sys.maxsize and cur.edge_value + distances[cur_min.vertex] < distances[cur.value]:
                            distances[cur.value] = cur.edge_value + distances[cur_min.vertex] # Change distance
                            minHeap.decrease_key(cur.value, distances[cur.value]) # Change position in min heap
                        cur = cur.next
            return distances[end]
        else:
            raise Exception("Path does not exist")
    

    # Prim algorithm. Find minimal spanning tree
    def MST_prima(self, start):
        start_found = False
        cur_list = self.adjacency_lists.head
        # Check if start vertex in the graph
        while cur_list != None and start_found == False:
            if cur_list.value == start:
                start_found = True
            cur_list = cur_list.next_list
        if start_found == True:
            tree = UndirectedGraph() # Create new graph that will be returned as a result
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
                cur_min = minHeap.extract_min() # Get minimal vertex with minimal distance from set of processed vertices
                if cur_min.vertex != start:
                    tree.insert(cur_min.vertex, parent[cur_min.vertex], cur_min.distance)
                cur_list = self.adjacency_lists.head
                while cur_list != None and cur_list.value != cur_min.vertex:
                    cur_list = cur_list.next_list
                if cur_list != None:
                    # Loop through adjacent vertices of current minimal vertex and update their distances if it's needed
                    cur = cur_list.next
                    while cur != None:
                        if minHeap.isInMinHeap(cur.value) and distances[cur_min.vertex] != sys.maxsize and cur.edge_value < distances[cur.value]:
                            distances[cur.value] = cur.edge_value # Change distance
                            minHeap.decrease_key(cur.value, distances[cur.value]) # Change position in min heap
                            parent[cur.value] = cur_min.vertex # Add parent of minimal vertex
                        cur = cur.next
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
                self.stack.push(self.graph.adjacency_lists.head.value) # Push first vertex of adjacency list into the stack
            else:
                self.stack.push(start) # Push start vertex into the stack
            self.traversal_done = False
            self.graph_size = self.graph.vertices_count() # Number of vertices in the graph

        def __next__(self):
            if self.has_next():
                temp = self.stack.pop()
                if self.visited[temp] == True: # If vertex is already visited go to the next vertex in stack
                    return self.__next__()
                self.visited[temp] = True # Mark vertex as visited
                cur_list = self.graph.adjacency_lists.head
                while cur_list != None and cur_list.value != temp:
                    cur_list = cur_list.next_list
                if cur_list != None:
                    cur = cur_list.next
                    # Add not visited adjacent vertices into the stack
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.stack.push(cur.value)
                        cur = cur.next
                return temp # Return current vertex
            else:
                # Checking for other raw connectivity components
                self.traversal_done = True
                cur_list = self.graph.adjacency_lists.head
                while cur_list != None: # Find not visited vertex that has adjacent vertices
                    if self.visited[cur_list.value] == False:
                        self.stack.push(cur_list.value)
                        self.traversal_done = False
                        break
                    cur_list = cur_list.next_list
                if self.traversal_done == False: # If we found that vertex
                    temp = self.stack.pop()
                    self.visited[temp] = True # Mark vertex as visited
                    cur = cur_list.next
                    # Add not visited adjacent vertices into the stack
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.stack.push(cur.value)
                        cur = cur.next
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
                self.queue.enqueue(self.graph.adjacency_lists.head.value) # Insert first vertex of adjacency list into the queue
            else:
                self.queue.enqueue(start) # Insert start vertex into the queue
            self.traversal_done = False
            self.graph_size = self.graph.vertices_count() # Number of vertices in graph

        def __next__(self):
            if self.has_next():
                temp = self.queue.dequeue()
                if self.visited[temp] == True: # If vertex is already visited go to the next vertex in queue
                    return self.__next__()
                self.visited[temp] = True # Mark vertex as visited
                cur_list = self.graph.adjacency_lists.head
                while cur_list != None and cur_list.value != temp:
                    cur_list = cur_list.next_list
                if cur_list != None:
                    cur = cur_list.next
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.queue.enqueue(cur.value)
                        cur = cur.next
                return temp # Return current vertex
            else:
                # Checking for other raw connectivity components
                self.traversal_done = True
                cur_list = self.graph.adjacency_lists.head
                while cur_list != None: # Find not visited vertex that has adjacent vertices
                    if self.visited[cur_list.value] == False:
                        self.queue.enqueue(cur_list.value)
                        self.traversal_done = False
                        break
                    cur_list = cur_list.next_list
                if self.traversal_done == False: # If we found that vertex
                    temp = self.queue.dequeue()
                    self.visited[temp] = True # Mark vertex as visited
                    cur = cur_list.next
                    # Add not visited adjacent vertices into the queue
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.queue.enqueue(cur.value)
                        cur = cur.next
                    return temp # Return current vertex
                else:
                    raise StopIteration # Traversal is done

        def has_next(self):
            if self.queue.isEmpty():
                return False
            else:
                return True
