from LinkedList import LinkedList, LinkedListNode
import Stack, Queue


class DirectedGraph:

    def __init__(self):
        self.adjacency_lists = LinkedList()

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

    # Insert edge [vertex1, vertex2] into the graph
    def insert(self, vertex1, vertex2):
        # If graph is empty
        if self.adjacency_lists.head == None:
            self.adjacency_lists.head = LinkedListNode(vertex1)
            self.adjacency_lists.head.next = LinkedListNode(vertex2)
        else:
            cur_list = self.adjacency_lists.head
            # Check if vertex1 has adjacent vertices
            while cur_list.next_list != None and cur_list.value != vertex1:
                cur_list = cur_list.next_list
            # If vertex1 has adjacent vertices
            if cur_list.value == vertex1:
                if cur_list.next == None:
                    cur_list.next = LinkedListNode(vertex2)
                    return
                cur = cur_list.next
                while cur.next != None:
                    if cur.value == vertex2:
                        raise Exception("Edge already exists")
                    cur = cur.next
                cur.next = LinkedListNode(vertex2)
                return
            # If vertex1 does not have adjacent vertices
            else:
                cur_list.next_list = LinkedListNode(vertex1)
                cur_list = cur_list.next_list
                cur_list.next = LinkedListNode(vertex2)
                

    # Remove edge [vertex1, vertex2] from the graph
    def remove(self, vertex1, vertex2):
        cur_list = self.adjacency_lists.head
        while cur_list != None and cur_list.value != vertex1:
            cur_list = cur_list.next_list
        # If vertex1 has adjacent vertices
        if cur_list != None:
            cur = cur_list
            # Delete vertex2 from adjacency lists
            while cur.next != None and cur.next.value != vertex2:
                cur = cur.next
            if cur.next == None and cur.value != vertex2: # If vertex2 not in list of adjacent vertices of vertex1
                raise Exception("Edge does not exist")
            else:
                temp = cur.next.next
                cur.next = None
                cur.next = temp
        else: # If edge does not exist
            raise Exception("Edge does not exist")

    # Depth first traversal iterator
    class dftIterator:

        def __init__(self, graph, start=None):
            self.stack = Stack.Stack()
            self.graph = graph
            self.graph_size = self.graph.max() # Number of vertices in graph
            print(self.graph_size)
            self.visited = [False] * (self.graph_size + 1)
            if start is None:
                self.stack.push(self.graph.adjacency_lists.head.value) # Push first vertex of adjacency list into the stack
            else:
                self.stack.push(start) # Push start vertex into the stack
            self.traversal_done = False

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
                    # Add not visited adjacent vertices into the stack
                    cur = cur_list.next
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.stack.push(cur.value)
                        cur = cur.next
                return temp # Return current vertex
            else:
                # Checking for other unhandled strongly connected components
                self.traversal_done = True
                cur_list = self.graph.adjacency_lists.head
                # Check if there is not visited vertex in the graph
                while cur_list != None:
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


    # Breadth first traversal iterator
    class bftIterator:

        def __init__(self, graph, start=None):
            self.queue = Queue.Queue()
            self.graph = graph
            self.graph_size = self.graph.max() # Number of vertices in graph
            self.visited = [False] * (self.graph_size + 1)
            if start is None:
                self.queue.enqueue(self.graph.adjacency_lists.head.value) # Insert first vertex of adjacency list into the queue
            else:
                self.queue.enqueue(start) # Insert start vertex into the queue
            self.traversal_done = False 

        def __next__(self):
            if self.has_next():
                temp = self.queue.dequeue()
                if self.visited[temp] == True: # If vertex is already visited go to the next vertex in queue
                    return self.__next__()
                self.visited[temp] = True # Mark vertex as visited
                cur_list = self.graph.adjacency_lists.head
                while cur_list != None and cur_list.value != temp:
                    cur_list = cur_list.next_list
                # Add not visited adjacent vertices of current vertex if they exist
                if cur_list != None:
                    cur = cur_list.next
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.queue.enqueue(cur.value)
                        cur = cur.next
                return temp # Return current vertex
            else:
                # Checking for other unhandled strongly connected components
                self.traversal_done = True
                cur_list = self.graph.adjacency_lists.head
                # Check if there is not visited vertex in the graph
                while cur_list != None:
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
                    return temp
                else: # Traversal is done
                    raise StopIteration

        def has_next(self):
            if self.queue.isEmpty():
                return False
            else:
                return True
