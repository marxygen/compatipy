import os

from compatipy import Compatible

ten = Compatible('example1.ten', path=os.path.join(os.path.dirname(__file__), 'examples'))

print(f'Executing ten(): {ten()}')
print(f'Executing ten.output: {ten.output}')
print(f'Executing ten.all: {ten.all}')