import numbers
import typing
from collections import OrderedDict, defaultdict

import numpy as np

from ._interval import Interval


class IntervalNode:

    def __init__(self, intervals: typing.List[Interval], parent=None):
        """
        Create a node from given intervals.
        :param intervals: list with intervals
        """
        self.intervals = OrderedDict()
        self.parent = parent
        self.left = None
        self.right = None

        if len(intervals) == 0:
            return
        self._center = get_center(intervals)

        inner = defaultdict(list)
        left, right = [], []

        for interval in intervals:
            if interval.end < self._center:
                left.append(interval)
            elif interval.begin >= self._center:
                right.append(interval)
            else:
                inner[interval].append(interval)

        # make sure that the intervals are position sorted
        for interval in sorted(inner.keys()):
            self.intervals[interval] = []
            for item in inner[interval]:
                self.intervals[interval].append(item)

        if left:
            self.left = IntervalNode(left, parent=self)
        if right:
            self.right = IntervalNode(right, parent=self)

    def search(self, position: numbers.Number) -> typing.List[Interval]:
        """
        Return intervals that overlap with given `position`.
        :param position: 1-based numeric position
        :return: list of overlapping intervals
        """
        if not isinstance(position, numbers.Number):
            raise ValueError("Expected a number but `{}` is `{}`".format(position, type(position)))
        results = []
        for entry in self.intervals:
            if entry.contains(position):
                for item in self.intervals[entry]:
                    results.append(item)
            elif entry.begin > position:
                break

        if position < self._center and self.left:
            for item in self.left.search(position):
                results.append(item)
        elif position >= self._center and self.right:
            for item in self.right.search(position):
                results.append(item)
        return results

    def get_overlaps(self, begin: numbers.Number, end: numbers.Number) -> typing.List[Interval]:
        """
        Return intervals that overlap with given `begin` and `end` coordinates.
        :param begin: 0-based (excluded) begin coordinate
        :param end: 0-based (included) end coordinate
        :return: list of overlapping intervals
        """
        results = []

        for entry in self.intervals:
            if entry.intersects(begin, end):
                for item in self.intervals[entry]:
                    results.append(item)
            elif entry.begin >= end:
                break

        if begin <= self._center and self.left:
            for item in self.left.get_overlaps(begin, end):
                results.append(item)
        if end > self._center and self.right:
            for item in self.right.get_overlaps(begin, end):
                results.append(item)

        return results

    def min_value(self):
        return next(iter(self.intervals))

    def max_value(self):
        return next(reversed(self.intervals))

    def minimum(self):
        node = self
        while node.left:
            node = node.left
        return node

    def maximum(self):
        node = self
        while node.right:
            node = node.right
        return node

    # def __iter__(self):
    #     return IntervalNodeFwdIterator(self)

    def __eq__(self, other):
        return self.intervals == other.intervals \
               and self.left == other.left \
               and self.right == other.right

    def __len__(self):
        return len(self.intervals) if self.intervals else 0

    def __repr__(self):
        intstr = ','.join([str(key) for key in self.intervals.keys()])
        return "ITNode(intervals=[{}])".format(intstr)


# class IntervalNodeFwdIterator:
#
#     def __init__(self, root: IntervalNode):
#         self.initialized = False
#         self.root = root
#         self.next = None
#
#     def _has_next(self):
#         if not self.initialized:
#             if not self.root:
#                 return False
#             else:
#                 self.next = self.root.minimum()
#                 self.initialized = True
#
#         return self.next is not None
#
#     def __next__(self):
#         if self._has_next():
#             cur = self.next
#             self.next = self.successor(cur)
#             return cur
#         else:
#             raise StopIteration()
#
#     @staticmethod
#     def successor(node: IntervalNode):
#         if node.right:
#             return node.right.minimum()
#         y = node.parent
#         while y and node == y.right:
#             node = y
#             y = y.parent
#         return y
#
#
# class IntervalNodeRevIterator:
#     # Currently not used, perhaps in future
#     def __init__(self, root: IntervalNode):
#         self.initialized = False
#         self.root = root
#         self.next = None
#
#     def has_next(self):
#         if not self.initialized:
#             if not self.root:
#                 return False
#             else:
#                 self.next = self.root.maximum()
#                 self.initialized = True
#
#         return self.next is not None
#
#     def __next__(self):
#         if self.has_next():
#             cur = self.next
#             self.next = self.predecessor(cur)
#             return cur
#         else:
#             raise StopIteration()
#
#     @staticmethod
#     def predecessor(node: IntervalNode):
#         if node.left:
#             return node.left.maximum()
#         y = node.parent
#         while y and node == y.left:
#             node = y
#             y = y.parent
#         return y


def get_center(items: typing.Iterable[Interval]):
    positions = np.array(list(map(lambda x: (x.begin, x.end), items))).reshape(1, -1).flatten()
    sorted_positions = np.sort(np.unique(positions))
    return np.floor(np.median(sorted_positions))
