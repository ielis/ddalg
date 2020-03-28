import abc


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

    def intersection(self, other):
        if self.end <= other.begin or other.end <= self.begin:
            return 0
        return max(min(self.end, other.end) - max(self.begin, other.begin), 1)

    def __lt__(self, other):
        if self.begin != other.begin:
            return self.begin < other.begin
        else:
            return self.end < other.end

    def __len__(self):
        return self.end - self.begin

    def __eq__(self, other):
        return self.begin == other.begin and self.end == other.end

    def __repr__(self):
        return '({},{})'.format(self.begin, self.end)

    def __hash__(self):
        return hash((self.begin, self.end))


class SimpleInterval(Interval):
    """Simple interval implementation for internal usage within the module."""

    def __init__(self, begin: int, end: int):
        self._begin = begin
        self._end = end

    @classmethod
    def of(cls, begin, end):
        return cls(begin, end)

    @property
    def begin(self):
        return self._begin

    @property
    def end(self):
        return self._end
