from LinkedList import LinkedList, LinkedListNode
import Stack, Queue


class DirectedGraph:

    def __init__(self):
        self.adjacency_lists = {}

    # Find vertex with max value
    def max(self):
        max_value = 0
        for key in self.adjacency_lists:
            if key > max_value:
                max_value = key
            cur = self.adjacency_lists[key]
            while cur is not None:
                if cur.value > max_value:
                    max_value = cur.value
                cur = cur.next
        return max_value

    # Insert edge [vertex1, vertex2] into the graph
    def insert(self, vertex1, vertex2):
        if vertex1 in self.adjacency_lists: # If vertex1 already in the graph
            cur = self.adjacency_lists[vertex1]
            while cur.next != None: # Search for the last element in the list
                if cur.value == vertex2: # If edge already exists
                    raise Exception("Edge already exists")
                cur = cur.next
            if cur.value == vertex2: # If edge already exists
                raise Exception("Edge already exists")
            else:
                new_node = LinkedListNode(vertex2)
                cur.next = new_node
        else: # If vertex1 not in the graph
            new_head = LinkedListNode(vertex2)
            self.adjacency_lists[vertex1] = new_head

    # Remove edge [vertex1, vertex2] from the graph
    def remove(self, vertex1, vertex2):
        if vertex1 in self.adjacency_lists: # If vertex1 in the graph
            cur = self.adjacency_lists[vertex1]
            # Delete vertex2 from adjacency lists
            if cur.value == vertex2: 
                self.adjacency_lists[vertex1] = cur.next
                del cur
                if self.adjacency_lists[vertex1] is None:
                    self.adjacency_lists.pop(vertex1)
            else:
                while cur != None:
                    if cur.next != None and cur.next.value == vertex2:
                        break
                    cur = cur.next
                if cur != None:
                    temp = cur.next.next
                    cur.next = None
                    cur.next = temp
                else: # If edge does not exist
                    raise Exception("Edge does not exist")
        else: # If edge does not exist
            raise Exception("Edge does not exist")

    # Depth first traversal iterator
    class dftIterator:

        def __init__(self, graph, start=None):
            self.stack = Stack.Stack()
            self.graph = graph
            self.graph_size = self.graph.max() # Number of vertices in graph
            self.visited = [False] * (self.graph_size + 1)
            if start is None:
                self.stack.push(list(graph.adjacency_lists.keys())[0]) # Push first vertex of adjacency list into the stack
            else:
                self.stack.push(start) # Push start vertex into the stack
            self.traversal_done = False

        def __next__(self):
            if self.has_next():
                temp = self.stack.pop()
                if self.visited[temp] == True: # If vertex is already visited go to the next vertex in stack
                    return self.__next__()
                self.visited[temp] = True # Mark vertex as visited
                if temp in self.graph.adjacency_lists.keys(): # If current vertex has adjacent vertices
                    # Add not visited adjacent vertices into the stack
                    cur = self.graph.adjacency_lists[temp]
                    while cur is not None:
                        if self.visited[cur.value] == False:
                            self.stack.push(cur.value)
                        cur = cur.next
                return temp # Return current vertex
            else:
                # Checking for other unhandled strongly connected components
                self.traversal_done = True
                for key in self.graph.adjacency_lists: # Find not visited vertex that has adjacent vertices
                    if self.visited[key] == False:
                        self.stack.push(key)
                        self.traversal_done = False
                        break
                if self.traversal_done == False: # If we found that vertex
                    temp = self.stack.pop()
                    self.visited[temp] = True # Mark vertex as visited
                    cur = self.graph.adjacency_lists[temp]
                    # Add not visited adjacent vertices into the stack
                    while cur is not None:
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
                self.queue.enqueue(list(graph.adjacency_lists.keys())[0]) # Insert first vertex of adjacency list into the queue
            else:
                self.queue.enqueue(start) # Insert start vertex into the queue
            self.traversal_done = False 

        def __next__(self):
            if self.has_next():
                temp = self.queue.dequeue()
                if self.visited[temp] == True: # If vertex is already visited go to the next vertex in queue
                    return self.__next__()
                self.visited[temp] = True # Mark vertex as visited
                if temp in self.graph.adjacency_lists.keys(): # If current vertex has adjacent vertices
                    # Add not visited adjacent vertices into the queue
                    cur = self.graph.adjacency_lists[temp]
                    while cur is not None:
                        if self.visited[cur.value] == False:
                            self.queue.enqueue(cur.value)
                        cur = cur.next
                return temp # Return current vertex
            else:
                # Checking for other unhandled strongly connected components
                self.traversal_done = True
                for key in self.graph.adjacency_lists: # Find not visited vertex that has adjacent vertices
                    if self.visited[key] == False:
                        self.queue.enqueue(key)
                        self.traversal_done = False
                        break
                if self.traversal_done == False: # If we found that vertex
                    temp = self.queue.dequeue()
                    self.visited[temp] = True # Mark vertex as visited
                    cur = self.graph.adjacency_lists[temp]
                    # Add not visited adjacent vertices into the queue
                    while cur is not None:
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
