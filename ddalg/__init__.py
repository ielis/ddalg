import pkg_resources

__version__ = pkg_resources.get_distribution('ddalg').version

from . import itree
from . import metrics
from . import model
