"""
This script accepts module and method name as the argument, executes the method and prints what it returned so
it can be captured by subprocess
"""

import sys, os
import imp

modulepath, method = sys.argv[1:3]
path, module = os.path.split(modulepath)
module = module.replace('.py', '')

function = imp.load_source(module+'.'+method, modulepath)
    
output = []
errors = []
exceptions = []

class STDOUTWriter(object):
    def __init__(self):
        pass
    
    @classmethod
    def write(self, data):
        output.append(data)

class STDERRWriter(object):
    def __init__(self):
        pass
    
    @classmethod
    def write(self, data):
        errors.append(data)

old_stdout = sys.stdout
sys.stdout = STDOUTWriter

old_stderr = sys.stderr
sys.stderr = STDERRWriter

argv = ''.join(sys.argv[3:5])
args = None if argv == 'args=(None,)' else eval(argv.replace('args=', ''))

try:
    if args:
        result = function.__dict__[method](*args)
    else:
        result = function.__dict__[method]()
except Exception as e:
    result = []
    exceptions.append(e)

sys.stdout = old_stdout
sys.stderr = old_stderr

# A little workaround so strings are not interpreted as variables since shell output omits quotes
if isinstance(result, str):
    result = "str('%s')"%result

output = list(filter(lambda x: x and x != '\n' and x != '\r', output))

print "{'result': %s, 'output': %s, 'exceptions': %s}" % (result, str(output), str(exceptions))