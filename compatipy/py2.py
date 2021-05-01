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

class IntoObjectWriter(object):
    def __init__(self):
        pass
    
    @classmethod
    def write(self, data):
        output.append(data)

old_stdout = sys.stdout
sys.stdout = IntoObjectWriter

result = function.__dict__[method]()

sys.stdout = old_stdout

# A little workaround so strings are not interpreted as variables since shell output omits quotes
if isinstance(result, str):
    result = "str('%s')"%result

output = list(filter(lambda x: x and x != '\n' and x != '\r', output))

print "{'result': %s, 'output': %s}" % (result, str(output))