class LinkedListNode:

    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:

    def __init__(self, val):
        self.head = LinkedListNode(val)
        self.last = self.head

    def push_back(self, val):
        new_node = LinkedListNode(val)
        if self.head == None:
            self.head = new_node
            self.last = self.head
        else:
            self.last.next = new_node
            self.last = self.last.next

    def pop_back(self):
        temp = self.head
        while(temp.next.next != None):
            temp = temp.next
        temp.next = None

    def remove(self, val):
        if self.head.value == val:
            self.head = None
            self.head = self.head.next
        else:
            cur = self.head
            while cur.next.value != val and cur != None:
                cur = cur.next
            temp = cur.next.next
            cur.next = None
            cur.next = temp
