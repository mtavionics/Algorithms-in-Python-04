# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 17:08:05 2021
Project 5
@author: Mikhail Terentev

1)	Use and modify the textbook Code Fragment 9.1, 9.4, 9.5 and 9.7 
to implement a standard heap-sort algorithm. 
2)	Study the textbook section 9.3.2 and implement another in-place heap-sort algorithm. Note the heap here is defined as a maximum-oriented heap, with each position’s key being at least as large as its children. 

"""
import random
from time import time

# 9.1: A PriorityQueueBase class with a nested Item class that composes 
# a key and a value into a single object. For convenience, we provide a concrete
# implementation of is empty that is based on a presumed len impelementation.

class Empty(Exception):
    pass

class Full(Empty):
	pass
 
class PriorityQueueBase:
  """Abstract base class for a priority queue."""
 
  # nested _Item class 
  class _Item:
    """Lightweight composite to store priority queue items."""
    __slots__ = '_key', '_value'
 
    def __init__(self, k, v):
      self._key = k
      self._value = v
 
    def __lt__(self, other):
      return self._key < other._key    # compare items based on their keys
 
    def __repr__(self):
      return '({0},{1})'.format(self._key, self._value)
 
  # public behaviors
  def is_empty(self):                  # concrete method assuming abstract len
    """Return True if the priority queue is empty."""
    return len(self) == 0
 
  def __len__(self):
    """Return the number of items in the priority queue."""
    raise NotImplementedError('must be implemented by subclass')
 
  def add(self, key, value):
    """Add a key-value pair."""
    raise NotImplementedError('must be implemented by subclass')
 
  def min(self):
    """Return but do not remove (k,v) tuple with minimum key.
    Raise Empty exception if empty.
    """
    raise NotImplementedError('must be implemented by subclass')
 
  def remove_min(self):
    """Remove and return (k,v) tuple with minimum key.
    Raise Empty exception if empty.
    """

# 9.4 and 9.5: An implementation of a priority queue using an array-based heap.
 
class HeapPriorityQueue(PriorityQueueBase): # base class defines _Item
  """A min-oriented priority queue implemented with a binary heap."""
 
  # nonpublic behaviors
  def _parent(self, j):
    return (j-1) // 2
 
  def _left(self, j):
    return 2*j + 1   
    
  def _right(self, j):
    return 2*j + 2  
 
  def _has_left(self, j):
    return self._left(j) < len(self._data)     # index beyond end of list?
  
  def _has_right(self, j):
    return self._right(j) < len(self._data)    # index beyond end of list?
  
  def _swap(self, i, j):
    """Swap the elements at indices i and j of array."""
    self._data[i], self._data[j] = self._data[j], self._data[i]
 
  def _upheap(self, j):
    parent = self._parent(j)
    # if j > 0 and self._data[j] < self._data[parent]:
        # for maximum-oriented heap
    if j > 0 and self._data[j] > self._data[parent]:    
      self._swap(j, parent)
      self._upheap(parent)             # recur at position of parent
  
  def _downheap(self, j):
    if self._has_left(j):
      left = self._left(j)
      small_child = left               # although right may be smaller
      if self._has_right(j):
        right = self._right(j)
        #if self._data[right] < self._data[left]:
        # for maximum-oriented heap
        if self._data[right] > self._data[left]:
          small_child = right
      # if self._data[small_child] < self._data[j]:
          # for maximum-oriented heap
      if self._data[small_child] > self._data[j]:
        self._swap(j, small_child)
        self._downheap(small_child)    # recur at position of small child
 
  # public behaviors 
  def __init__(self):
    """Create a new empty Priority Queue."""
    self._data = []
 
  def __len__(self):    # 1 
    """Return the number of items in the priority queue."""
    return len(self._data)
 
  def add(self, key, value):   # 3
    """Add a key-value pair to the priority queue."""
    self._data.append(self._Item(key, value))
    self._upheap(len(self._data) - 1)            # upheap newly added position
  
  def min(self):         # 4 
    """Return but do not remove (k,v) tuple with minimum key.
    Raise Empty exception if empty.
    """
    if self.is_empty():
      raise Empty('Priority queue is empty.')
    item = self._data[0]
    return (item._key, item._value)
 
  def remove_min(self):   # 5
    """Remove and return (k,v) tuple with minimum key.
    Raise Empty exception if empty.
    """
    if self.is_empty():
      raise Empty('Priority queue is empty.')
    self._swap(0, len(self._data) - 1)           # put minimum item at the end
    item = self._data.pop()                      # and remove it from the list;
    self._downheap(0)                            # then fix new root
    return (item._key, item._value)

# 9.7    
def pq_sort(C):
    '''Sort a collection of elements stored in a positional list.'''
    n = len(C)
    P = HeapPriorityQueue()
    for j in range(n):
        #element = C.pop()
        element = C.delete(C.first())
        P.add(element,element)  # use element as key and value
    for j in range(n):
        (k,v) = P.remove_min()
        C.add_last(v)             # store smallest remaining element in C


# --- _DoublyLinkedBase
class _DoublyLinkedBase:
  """A base class providing a doubly linked list representation."""

  #-------------------------- nested _Node class --------------------------
  # nested _Node class
  class _Node:
    """Lightweight, nonpublic class for storing a doubly linked node."""
    __slots__ = '_element', '_prev', '_next'            # streamline memory

    def __init__(self, element, prev, next):            # initialize node's fields
      self._element = element                           # user's element
      self._prev = prev                                 # previous node reference
      self._next = next                                 # next node reference

  #-------------------------- list constructor --------------------------

  def __init__(self):
    """Create an empty list."""
    self._header = self._Node(None, None, None)
    self._trailer = self._Node(None, None, None)
    self._header._next = self._trailer                  # trailer is after header
    self._trailer._prev = self._header                  # header is before trailer
    self._size = 0                                      # number of elements

  #-------------------------- public accessors --------------------------

  def __len__(self):
    """Return the number of elements in the list."""
    return self._size

  def is_empty(self):
    """Return True if list is empty."""
    return self._size == 0

  #-------------------------- nonpublic utilities --------------------------

  def _insert_between(self, e, predecessor, successor):
    """Add element e between two existing nodes and return new node."""
    newest = self._Node(e, predecessor, successor)      # linked to neighbors
    predecessor._next = newest
    successor._prev = newest
    self._size += 1
    return newest

  def _delete_node(self, node):
    """Delete nonsentinel node from the list and return its element."""
    predecessor = node._prev
    successor = node._next
    predecessor._next = successor
    successor._prev = predecessor
    self._size -= 1
    element = node._element                             # record deleted element
    node._prev = node._next = node._element = None      # deprecate node
    return element                                      # return deleted element
# --- end


# 7.14-16
class PositionalList(_DoublyLinkedBase):

    class Position:
        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            return not (self == other)

    def _validate(self, p):
      #  if not isinstance(p, self.Positon):
       #     raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._next is None:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        if node is self._header or node is self._trailer:
            return None
        else:
            return self.Position(self, node)

    def first(self):
        return self._make_position(self._header._next)

    def last(self):
        return self._make_position(self.traier._prev)

    def before(self, p):
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self):
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def _insert_between(self, e, predecessor, successor):
        node = super()._insert_between(e, predecessor, successor)
        return self._make_position(node)

    def add_first(self, e):
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e):
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def add_before(self, p, e):
        original = self._validate(p)
        return self._insert_between(e, original._prev, original)

    def add_after(self, p, e):
        original = self._validate(p)
        return self._insert_between(e, original, original._next)

    def delete(self, p):
        original = self._validate(p)
        return self._delete_node(original)

    def replace(self, p, e):
        original = self._validate(p)
        old_value = original._element
        original._element = e
        return old_value


# main code:
def test(number):
    # floating number
    ilist = [ round(random.uniform(1,number+1),2)  for i in range(0,number)]

    print("Generated ", number, " floating numbers: ", ilist)

    # heap sort
    C = PositionalList()
    for item in ilist:
        C.add_last(item)

    start = time() 
    pq_sort(C)
    end = time()

    # print sorted numbers
    print("Sorted by heap: ")
    for item in C:
        if item:
            print(item)
    heap_time =  end - start

    print("Sort time was taken= ", heap_time)

def main():
    print("Heap sort") 

    while True:
        number = input("Enter the number (1000-10000) of random generated float data to be sorted (default: 1000) or 'q' for stop program: ")
        if number == 'q':
            break
        elif number == '':
            number = 1000
        else:
            number = int(number)
            if number < 1:
               print("Use the default number: 1000")
               number = 1000
        # for debugging

        test(number)

if __name__ == '__main__':
    main()