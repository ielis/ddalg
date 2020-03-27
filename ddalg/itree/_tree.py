import numbers
import typing

from ddalg.utils import get_boundary_margin
from ._node import IntervalNode, Interval


class IntervalTree:

    def __init__(self, intervals: typing.List[Interval]):
        self._head = IntervalNode(intervals)
        self._intervals = intervals
        self._in_sync = True
        self._size = len(intervals)

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
        self.build()
        return self._head.search(position)

    def get_overlaps(self, begin, end) -> typing.List[Interval]:
        """
        Get intervals that overlap with given query coordinates.
        :param begin: 0-based (excluded) begin position of query
        :param end: 0-based (included) end position of query
        :return: list with overlapping coordinates
        """
        self.build()
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

        # make sure the tree is up-to-date
        self.build()
        margin = get_boundary_margin(begin, end, coverage)

        # distal begin/end coordinates are defined as are query+-margin
        dist_begin, dist_end = begin - margin, end + margin
        prox_begin, prox_end = begin + margin, end - margin

        # first get all intervals that are contained within the distal region
        # then filter to retain
        return [interval for interval in self.get_overlaps(dist_begin, dist_end)
                if interval.begin <= prox_begin and interval.end >= prox_end]

    def __len__(self):
        self.build()
        return self._size

    def __repr__(self):
        return "IntervalTree(size={})".format(len(self))

    def __iter__(self):
        return iter(self._head)

    def __bool__(self):
        return len(self) != 0
