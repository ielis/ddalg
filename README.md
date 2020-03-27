# ddalg
Algorithms and data structures for my Python projects.

## Interval tree

- implement your custom interval object while extending `Interval`. Two properties need to be overwritten:
  - `begin` - 0-based (excluded) begin coordinate of the interval
  - `end` - 0-based (included) end coordinate of the interval
    ```python
    from ddalg.itree import Interval
    
    class YourInterval(Interval):
    
      def __init__(self, begin: int, end: int):
        self._begin = begin
        self._end = end
        # anything else
    
      @property
      def begin(self):
        return self._begin
    
      @property
      def end(self):
        return self._end
   ``` 
- create a collection of your intervals and store them in the interval tree:
  ```python
  from ddalg.itree import IntervalTree
   
  itree = IntervalTree([YourInterval(0, 3), YourInterval(1, 4)])
  # ... 
  ```
- query `itree`:
  - either using *position*:
    ```python
    itree.stab(1)
    ```
    > returns `(0,3)`
  - or using half-open *interval coordinates*:
    ```python
    itree.query(0, 1) 
    ``` 
    > returns `(0,3)`, effectively the same query as above

