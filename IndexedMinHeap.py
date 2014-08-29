__author__ = 'zaimmusa'
"""
Priority queue class with added methods for:
- changing key associated with index
- deleting arbitrary index from queue

Implemented using idea from Algorithms 4 Edition by Sedgewick and Wayne
"""
class IndexedMinHeap:
    def __init__(self, max_size):
        """
        Create heap of the defined size
        """
        if max_size <= 0:
            raise ValueError("size should be > 0")
        self.max_size = max_size
        self.pq = [-1] * (self.max_size + 1)
        self.qp = [-1] * (self.max_size + 1)
        self.keys = [None] * (self.max_size + 1)
        self.size = 0

    def insert(self, index, key):
        """
        Insert key indexed by index
        """
        if index > self.max_size or index <= 0:
            raise IndexError("Index should be in range 1 - " + str(self.max_size))
        self.size += 1
        self.qp[index] = self.size
        self.pq[self.size] = index
        self.keys[index] = key
        self._swim(self.size)

    def is_empty(self):
        """
        Check if heap is empty
        """
        return self.size == 0

    def contains(self, index):
        """
        Check if heap contains key with this index
        """
        if index > self.max_size or index <= 0:
            raise IndexError("Index should be in range 1 - " + str(self.max_size))
        return self.qp[index] != -1

    def _greater(self, position_1, position_2):
        return self.keys[self.pq[position_1]] > self.keys[self.pq[position_2]]

    def _exch(self, position_1, position_2):
        swap_temp = self.pq[position_1]
        self.pq[position_1] = self.pq[position_2]
        self.pq[position_2] = swap_temp

        self.qp[self.pq[position_1]] = position_1
        self.qp[self.pq[position_2]] = position_2

    def _swim(self, position):
        while (position > 1 and self._greater(position/2, position)):
            self._exch(position/2, position)
            position = position/2

    def _sink(self, position):
        while 2*position <= self.size:
            j = 2*position
            if j < self.size and self._greater(j, j + 1):
                j += 1
            if not self._greater(position, j):
                return
            self._exch(position, j)
            position = j

    def get_key(self, index):
        """
        Return key associated with this index
        """
        if index > 0 and index <= self.max_size:
            if self.contains(index):
                return self.keys[index]
            else:
                raise IndexError("Heap does not contain this index")
        else:
            raise IndexError("Index should be in range 1 - " + str(self.max_size))

    def min_key(self):
        """
        Return current minimum key without removing it
        """
        return self.keys[self.pq[1]]

    def del_min_key(self):
        """
        Remove current minimum key
        """
        min = self.pq[1]
        self._exch(1, self.size)
        self.size -= 1
        self._sink(1)
        self.qp[min] = -1
        self.keys[self.pq[self.size + 1]] = None
        self.pq[self.size + 1] = -1

    def pop_key(self):
        """
        Return and remove current minimum key
        """
        result = self.min_key()
        self.del_min_key()
        return result

    def pop_key_and_index(self):
        """
        Return and remove current minimum key and its index
        """
        index = self.pq[1]
        key = self.keys[self.pq[1]]
        self.del_min_key()
        return key, index

    def __str__(self):
        result = "pq :"
        for i in range(self.max_size + 1):
            result += str(self.pq[i]) + " "
        result += "\n"
        result += "keys :"
        for i in range(self.max_size + 1):
            result += str(i) + ": " + str(self.keys[i]) + " (" + str(self.qp[i]) + ") " + "\n"
        result += "\n"
        for i in range(self.max_size + 1):
            if self.pq[i] != -1:
                result += str(i) + ": " + self.keys[self.pq[i]].__str__() + "\n"
        return result

    def del_index(self, index):
        """
        Remove index and associated key from heap
        """
        if index <= 0 or index > self.max_size:
            raise IndexError("Index should be in range 1 - " + str(self.max_size))
        prev_position = self.qp[index]
        self._exch(self.size, self.qp[index])
        # print '_'*30
        # print self
        self.size -= 1
        self.pq[self.size + 1] = -1
        self._sink(prev_position)
        self.qp[index] = -1
        self.keys[index] = None

    def change_key(self, index, new_key):
        """
        Change key associated with index
        """
        if index <= 0 and index > self.max_size:
            raise IndexError("Index should be in range 1 - " + str(self.max_size))
        self.keys[index] = new_key
        self._swim(self.qp[index])
        self._sink(self.qp[index])


if __name__ == "__main__":
    # create heap
    heap = IndexedMinHeap(20)

    # insert some fruit with indexes
    heap.insert(15, "banana")
    heap.insert(3, "kiwi")
    heap.insert(11, "apple")
    heap.insert(14, "orange")
    heap.insert(7, "strawberry")
    heap.insert(9, "ananas")

    # pop minimum key
    print 'This should print ananas: ', heap.pop_key()

    # peek at the next minimum key
    print 'This should print apple:', heap.min_key()

    # change key of index 11
    heap.change_key(11, "pear")

    # peak at the new minimum key
    print 'This should print banana: ', heap.min_key()

    # remove banana key by index
    heap.del_index(15)

    # peak at the new minimum key
    print 'This should print kiwi: ',  heap.min_key()


