import logging
import numbers
import typing
from collections import deque

from ddalg.utils import get_boundary_margin, jaccard_coefficient
from ._interval import SimpleInterval
from ._node import IntervalNode, Interval


class IntervalTree:

    def __init__(self, intervals: typing.List[Interval]):
        self._head = IntervalNode(intervals)
        self._intervals = intervals
        self._in_sync = True
        self._size = len(intervals)
        self._logger = logging.getLogger(__name__)

    def build(self):
        if not self._in_sync:
            self._head = IntervalNode(self._intervals)
            self._in_sync = True
            self._size = len(self._intervals)

    def insert(self, interval: Interval):
        """
        Insert interval into the tree. The insert results in invalidation of the tree leading to lazy rebuild of
        the tree structure upon the next query.
        :param interval: interval to be inserted
        :return: None
        """
        self._intervals.append(interval)
        self._in_sync = False

    def search(self, position: numbers.Number) -> typing.List[Interval]:
        """
        Return intervals that overlap with given `position`.
        :param position: 1-based numeric position
        :return: list of overlapping intervals
        """
        self.build()  # make sure the tree is up-to-date
        return self._head.search(position)

    def get_overlaps(self, begin, end) -> typing.List[Interval]:
        """
        Get intervals that overlap with given query coordinates.
        :param begin: 0-based (excluded) begin position of query
        :param end: 0-based (included) end position of query
        :return: list with overlapping coordinates
        """
        self.build()  # make sure the tree is up-to-date
        return self._head.get_overlaps(begin, end)

    def fuzzy_query(self, begin, end, coverage=1.) -> typing.List[Interval]:
        """
        Get intervals that imperfectly overlap with given query coordinates, while covering at least `coverage` of
        the query.
        :param begin: 0-based (excluded) begin position of query
        :param end: 0-based (included) end position of query
        :param coverage: float in [0,1] specifying what fraction of query the interval needs to overlap with
        :return: list of overlapping intervals
        """
        if 0 < coverage > 1:
            raise ValueError("coverage must be within [0,1]")

        self.build()  # make sure the tree is up-to-date
        margin = get_boundary_margin(begin, end, coverage)

        # distal begin/end coordinates are defined as are query+-margin
        dist_begin, dist_end = begin - margin, end + margin
        prox_begin, prox_end = begin + margin, end - margin
        self._logger.debug("Returning intervals [{}+-{:.2f}, {}+-{:.2f}]".format(begin, margin, end, margin))

        # first get all intervals that overlap with [begin,end]
        # then filter to retain intervals with begin/end coordinates close to query
        return [interval for interval in self.get_overlaps(begin, end)
                if dist_begin <= interval.begin <= prox_begin
                and dist_end >= interval.end >= prox_end]

    def jaccard_query(self, begin, end, min_jaccard=1.):
        """
        Get intervals that imperfectly overlap with given query coordinates, while covering at least `coverage` of
        the query.
        :param begin: 0-based (excluded) begin position of query
        :param end: 0-based (included) end position of query
        :param min_jaccard: float in [0,1] specifying what fraction of query the interval needs to overlap with
        :return: list of overlapping intervals
        """
        if 0 < min_jaccard > 1:
            raise ValueError("min_jaccard must be within [0,1]")

        self.build()  # make sure the tree is up-to-date

        # first get all intervals that overlap with [begin,end]
        # then filter to retain intervals with begin/end coordinates close to query
        return [interval for interval in self.get_overlaps(begin, end)
                if jaccard_coefficient(interval, SimpleInterval.of(begin, end)) >= min_jaccard]

    def __len__(self):
        self.build()  # make sure the tree is up-to-date
        return self._size

    def __repr__(self):
        return "IntervalTree(size={})".format(len(self))

    def __iter__(self):
        self.build()  # make sure the tree is up-to-date
        return IntervalTreeIterator(self._head)

    def __bool__(self):
        return len(self) != 0


class IntervalTreeIterator:

    def __init__(self, root):
        self.initialized = False
        self.root = root
        self.node = None
        self.queue = None

    def has_next(self):
        if not self.initialized:
            if self.root:
                # find node with the smallest values and dump elements into a queue
                self.node = self.root.minimum()
                self.queue = self.node_to_queue(self.node)
                self.initialized = True
            else:
                # the tree is empty, no node
                return False

        if self.queue:
            return True
        else:
            # done iterating elements from the current node, try the next node
            self.node = self.successor(self.node)
            self.queue = self.node_to_queue(self.node)

        return len(self.queue) != 0

    def __next__(self):
        if self.has_next():
            return self.queue.popleft()
        else:
            raise StopIteration()

    @staticmethod
    def node_to_queue(node: IntervalNode) -> deque:
        queue = deque()
        if node:
            for interval in node.intervals:
                for item in node.intervals[interval]:
                    queue.append(item)
        return queue

    @staticmethod
    def successor(node: IntervalNode):
        if node.right:
            return node.right.minimum()
        y = node.parent
        while y and node == y.right:
            node = y
            y = y.parent
        return y
