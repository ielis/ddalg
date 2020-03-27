import abc
import numbers
import typing
from collections import OrderedDict, defaultdict

import numpy as np


class Interval(metaclass=abc.ABCMeta):
    """Class to be subclassed in order to play with IntervalTree."""

    @property
    @abc.abstractmethod
    def begin(self):
        pass

    @property
    @abc.abstractmethod
    def end(self):
        pass

    def contains(self, value) -> bool:
        return self.end >= value > self.begin

    def intersects(self, begin, end):
        return end > self.begin and begin < self.end

    def __lt__(self, other):
        if self.begin != other.begin:
            return self.begin < other.begin
        else:
            return self.end < other.end

    def __eq__(self, other):
        return self.begin == other.begin and self.end == other.end

    def __repr__(self):
        return '({},{})'.format(self.begin, self.end)

    def __hash__(self):
        return hash((self.begin, self.end))


def get_center(items: typing.Iterable[Interval]):
    positions = np.array(list(map(lambda x: (x.begin, x.end), items))).reshape(1, -1).flatten()
    sorted_positions = np.sort(np.unique(positions))
    return np.floor(np.median(sorted_positions))


class IntervalNode:

    def __init__(self, intervals: typing.Iterable[Interval]):
        """
        Create a node from given intervals.
        :param intervals: iterable with intervals
        """
        self._center = get_center(intervals)
        self.left = None
        self.right = None

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
        self._intervals = OrderedDict()
        for interval in sorted(inner.keys()):
            self._intervals[interval] = []
            for item in inner[interval]:
                self._intervals[interval].append(item)

        if left:
            self.left = IntervalNode(left)
        if right:
            self.right = IntervalNode(right)

    def stab(self, position: numbers.Number) -> typing.List[Interval]:
        """
        Return intervals that overlap with given `position`.
        :param position: 1-based numeric position
        :return: list of overlapping intervals
        """
        if not isinstance(position, numbers.Number):
            raise ValueError("Expected a number but `{}` is `{}`".format(position, type(position)))
        results = []
        for entry in self._intervals:
            if entry.contains(position):
                for item in self._intervals[entry]:
                    results.append(item)
            elif entry.begin > position:
                break

        if position < self._center and self.left:
            for item in self.left.stab(position):
                results.append(item)
        elif position >= self._center and self.right:
            for item in self.right.stab(position):
                results.append(item)
        return results

    def query(self, begin: numbers.Number, end: numbers.Number) -> typing.List[Interval]:
        """
        Return intervals that overlap with given `begin` and `end` coordinates.
        :param begin: 0-based (excluded) begin coordinate
        :param end: 0-based (included) end coordinate
        :return: list of overlapping intervals
        """
        results = []

        for entry in self._intervals:
            if entry.intersects(begin, end):
                for item in self._intervals[entry]:
                    results.append(item)
            elif entry.begin >= end:
                break

        if begin <= self._center and self.left:
            for item in self.left.query(begin, end):
                results.append(item)
        if end > self._center and self.right:
            for item in self.right.query(begin, end):
                results.append(item)

        return results

    def __len__(self):
        return len(self._intervals)

    def __repr__(self):
        return "ITNode(center={},n={},n_left={},n_right={})".format(self._center, len(self), len(self.left),
                                                                    len(self.right))


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

    def add(self, interval):
        self._intervals.append(interval)
        self._in_sync = False

    def stab(self, position):
        self.build()
        return self._head.stab(position)

    def query(self, begin, end):
        self.build()
        return self._head.query(begin, end)

    def __len__(self):
        self.build()
        return self._size

    def __repr__(self):
        return "IntervalTree(size={})".format(len(self))
