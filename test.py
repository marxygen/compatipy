import os

from compatipy import Compatible

ten = Compatible('example1.ten', path=os.path.join(os.path.dirname(__file__), 'examples'))

ten()