import unittest

import DirectedGraph, UndirectedGraph


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        self.graph = DirectedGraph.DirectedGraph()
        self.graph.insert(1, 2)
        self.graph.insert(1, 3)
        self.graph.insert(2, 3)
        self.graph.insert(2, 4)
        self.graph.insert(3, 5)
        self.graph.insert(3, 6)
        self.graph.insert(5, 6)
        self.graph.insert(6, 7)
        self.graph.insert(7, 5)
        self.graph.insert(6, 8)
        self.graph.insert(4, 9)
        self.graph.insert(4, 10)
        self.graph.insert(8, 9)
        self.graph.insert(8, 11)
        self.graph.insert(9, 10)
        self.graph.insert(10, 11)
        self.graph.insert(11, 9)

    def test_max(self):
        self.assertEqual(self.graph.max(), 11)

    def test_insert_vertex1_exists(self):
        self.graph.insert(2, 6)
        cur_list = self.graph.adjacency_lists.head
        while cur_list != None:
            if cur_list.value == 2:
                break
            cur_list = cur_list.next_list
        cur = cur_list.next
        while cur != None:
            if cur.value == 6:
                break
            cur = cur.next
        self.assertEqual(cur.value, 6)

    def test_insert_vertex1_doesnt_exist(self):
        self.graph.insert(12, 6)
        cur_list = self.graph.adjacency_lists.head
        while cur_list != None:
            if cur_list.value == 12:
                break
            cur_list = cur_list.next_list
        cur = cur_list.next
        while cur != None:
            if cur.value == 6:
                break
            cur = cur.next
        self.assertEqual(cur.value, 6)

    def test_insert_exception(self):
        try:
            self.graph.insert(11, 9)
        except Exception as e:
            self.assertEqual(str(e), "Edge already exists")

    def test_remove(self):
        self.graph.remove(1, 3)
        iterator = self.graph.dftIterator(self.graph, 1)
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, [1, 2, 4, 10, 11, 9, 3, 6, 8, 7, 5])

    def test_remove_exception_vertex1_doesnt_exist(self):
        try:
            self.graph.remove(12, 9)
        except Exception as e:
            self.assertEqual(str(e), "Edge does not exist")

    def test_remove_exception_vertex2_doesnt_exist(self):
        try:
            self.graph.remove(2, 6)
        except Exception as e:
            self.assertEqual(str(e), "Edge does not exist")

    def test_dft_iterator_default_start(self):
        iterator = self.graph.dftIterator(self.graph)
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, [1, 3, 6, 8, 11, 9, 10, 7, 5, 2, 4])

    def test_dft_iterator_set_start(self):
        iterator = self.graph.dftIterator(self.graph, 8)
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, [8, 11, 9, 10, 1, 3, 6, 7, 5, 2, 4])

    def test_dft_iterator_in_graph_with_some_strongly_connected_components(self):
        self.graph.remove(1, 3)
        self.graph.remove(2, 4)
        self.graph.remove(3, 6)
        self.graph.remove(6, 8)
        self.graph.remove(9, 10)
        self.graph.remove(5, 6)
        self.graph.remove(11, 9)
        iterator = self.graph.dftIterator(self.graph, 1)
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, [1, 2, 3, 5, 6, 7, 4, 10, 11, 9, 8])

    def test_bft_iterator_default_start(self):
        iterator = self.graph.bftIterator(self.graph)
        bft_result = []
        for _ in range(iterator.graph_size):
            bft_result.append(next(iterator))
        self.assertListEqual(bft_result, [1, 2, 3, 4, 5, 6, 9, 10, 7, 8, 11])

    def test_bft_iterator_set_start(self):
        iterator = self.graph.bftIterator(self.graph, 4)
        bft_result = []
        for _ in range(iterator.graph_size):
            bft_result.append(next(iterator))
        self.assertListEqual(bft_result, [4, 9, 10, 11, 1, 2, 3, 5, 6, 7, 8])

    def test_bft_iterator_in_graph_with_some_strongly_connected_components(self):
        self.graph.remove(1, 3)
        self.graph.remove(2, 4)
        self.graph.remove(3, 6)
        self.graph.remove(6, 8)
        self.graph.remove(9, 10)
        self.graph.remove(5, 6)
        self.graph.remove(11, 9)
        iterator = self.graph.bftIterator(self.graph, 1)
        bft_result = []
        for _ in range(iterator.graph_size):
            bft_result.append(next(iterator))
        self.assertListEqual(bft_result, [1, 2, 3, 5, 6, 7, 4, 9, 10, 11, 8])


class TestUndirectedGraph(unittest.TestCase):

    def setUp(self):
        self.graph = UndirectedGraph.UndirectedGraph()
        self.graph.insert(0, 1, 3)
        self.graph.insert(0, 3, 14)
        self.graph.insert(0, 8, 2)
        self.graph.insert(1, 7, 4)
        self.graph.insert(2, 3, 2)
        self.graph.insert(2, 7, 2)
        self.graph.insert(2, 5, 3)
        self.graph.insert(3, 4, 7)
        self.graph.insert(4, 8, 10)
        self.graph.insert(5, 6, 1)
        # Graph for MST
        self.graph_for_MST = UndirectedGraph.UndirectedGraph()
        self.graph_for_MST.insert(1, 4, 6)
        self.graph_for_MST.insert(1, 6, 9)
        self.graph_for_MST.insert(1, 2, 3)
        self.graph_for_MST.insert(2, 4, 4)
        self.graph_for_MST.insert(2, 3, 2)
        self.graph_for_MST.insert(3, 4, 2)
        self.graph_for_MST.insert(2, 6, 9)
        self.graph_for_MST.insert(4, 7, 9)
        self.graph_for_MST.insert(3, 7, 9)
        self.graph_for_MST.insert(3, 5, 8)
        self.graph_for_MST.insert(2, 5, 9)
        self.graph_for_MST.insert(6, 5, 8)
        self.graph_for_MST.insert(5, 7, 7)
        self.graph_for_MST.insert(7, 8, 4)
        self.graph_for_MST.insert(7, 9, 5)
        self.graph_for_MST.insert(8, 9, 1)
        self.graph_for_MST.insert(5, 9, 9)
        self.graph_for_MST.insert(6, 10, 18)
        self.graph_for_MST.insert(5, 10, 10)
        self.graph_for_MST.insert(8, 10, 4)
        self.graph_for_MST.insert(9, 10, 3)

    def test_max(self):
        self.assertEqual(self.graph.max(), 8)
        self.assertEqual(self.graph_for_MST.max(), 10)

    def test_insert_vertex1_exists(self):
        self.graph.insert(4, 5, 0)
        cur_list1 = self.graph.adjacency_lists.head
        while cur_list1.value != 4:
            cur_list1 = cur_list1.next_list
        cur1 = cur_list1.next
        while cur1.next != None:
            cur1 = cur1.next
        self.assertEqual(cur1.value, 5)
        cur_list2 = self.graph.adjacency_lists.head
        while cur_list2.value != 5:
            cur_list2 = cur_list2.next_list
        cur2 = cur_list2.next
        while cur2.next != None:
            cur2 = cur2.next
        self.assertEqual(cur2.value, 4)

    def test_insert_vertex1_doesnt_exist(self):
        self.graph.insert(14, 5, 0)
        cur_list1 = self.graph.adjacency_lists.head
        while cur_list1.value != 14:
            cur_list1 = cur_list1.next_list
        cur1 = cur_list1.next
        while cur1.next != None:
            cur1 = cur1.next
        self.assertEqual(cur1.value, 5)
        cur_list2 = self.graph.adjacency_lists.head
        while cur_list2.value != 5:
            cur_list2 = cur_list2.next_list
        cur2 = cur_list2.next
        while cur2.next != None:
            cur2 = cur2.next
        self.assertEqual(cur2.value, 14)

    def test_insert_exception(self):
        try:
            self.graph.insert(4, 3, 0)
        except Exception as e:
            self.assertEqual(str(e), "Edge already exists")

    def test_remove(self):
        self.graph.remove(2, 7)
        dft_result = []
        iterator = self.graph.dftIterator(self.graph)
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, [0, 8, 4, 3, 2, 5, 6, 1, 7])

    def test_remove_vertex1_doesnt_have_adjacent_vertices(self):
        try:
            self.graph.remove(9, 2)
        except Exception as e:
            self.assertEqual(str(e), "Edge does not exist")

    def test_remove_vertex2_not_adjacent_to_vertex1(self):
        try:
            self.graph.remove(3, 7)
        except Exception as e:
            self.assertEqual(str(e), "Edge does not exist")

    def test_dijkstra(self):
        self.assertEqual(self.graph.dijkstra(0, 3), 11)
        self.assertEqual(self.graph.dijkstra(8, 3), 13)

    def test_dijkstra_exception(self):
        try:
            self.graph.dijkstra(0, 9)
        except Exception as e:
            self.assertEqual(str(e), "Path does not exist")

    def test_prima_MST(self):
        MST = self.graph_for_MST.MST_prima(1)
        dft_result = []
        iterator = MST.dftIterator(MST, 1)
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, [1, 2, 3, 5, 6, 7, 8, 9, 10, 4])

    def test_prima_MST_exception(self):
        try:
            self.graph_for_MST.MST_prima(0)   
        except Exception as e:
            self.assertEqual(str(e), "Vertex does not exist")

    def test_dft_iterator_default_start(self):
        iterator = self.graph.dftIterator(self.graph)
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, [0, 8, 4, 3, 2, 5, 6, 7, 1])

    def test_dft_iterator_set_start(self):
        iterator = self.graph.dftIterator(self.graph, 2)
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, [2, 5, 6, 7, 1, 0, 8, 4, 3])

    def test_dft_iterator_in_graph_with_some_raw_connectivity_components(self):
        self.graph.remove(0, 8)
        self.graph.remove(1, 7)
        self.graph.remove(3, 4)
        self.graph.remove(2, 3)
        self.graph.remove(5, 6)
        dft_result = []
        iterator = self.graph.dftIterator(self.graph)
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, [0, 3, 1, 8, 4, 7, 2, 5, 6])

    def test_bft_iterator_default_start(self):
        iterator = self.graph.bftIterator(self.graph)
        bft_result = []
        for _ in range(iterator.graph_size):
            bft_result.append(next(iterator))
        self.assertListEqual(bft_result, [0, 1, 3, 8, 7, 2, 4, 5, 6])

    def test_bft_iterator_set_start(self):
        iterator = self.graph.bftIterator(self.graph, 2)
        bft_result = []
        for _ in range(iterator.graph_size):
            bft_result.append(next(iterator))
        self.assertListEqual(bft_result, [2, 3, 7, 5, 0, 4, 1, 6, 8])

    def test_bft_iterator_in_graph_with_some_raw_connectivity_components(self):
        self.graph.remove(0, 8)
        self.graph.remove(1, 7)
        self.graph.remove(3, 4)
        self.graph.remove(2, 3)
        self.graph.remove(5, 6)
        bft_result = []
        iterator = self.graph.bftIterator(self.graph)
        for _ in range(iterator.graph_size):
            bft_result.append(next(iterator))
        self.assertListEqual(bft_result, [0, 1, 3, 8, 4, 7, 2, 5, 6])


if __name__ == '__main__':
    unittest.main()
