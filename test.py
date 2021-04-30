import os

from compatipy import Compatible

test = Compatible('example1.test', path=os.path.join(os.path.dirname(__file__), 'examples'))

print(f'Executing test(): {test()}')
print(f'Executing test.output: {test.output}')
print(f'Executing test.all: {test.all}')