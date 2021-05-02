from os import listdir, path
from os.path import isfile, join, dirname
from compatipy import Compatible
from tests import data

directory = join(dirname(__file__), 'tests')

for file in [f for f in listdir(directory) if isfile(join(directory, f)) and f != "__init__.py" and f != 'data.py' and 'pyc' not in f]:
    args = data.args.get(file, (None, ))
    func = Compatible(f'{file[:-3]}.test', path=join(directory, dirname(file)), args=args)
    try:
        result = func.all
        assert(result == data.data[file])
    except Exception as e:
        assert(str(e) == data.data[file])

