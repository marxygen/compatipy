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
        
result = function.__dict__[method]()

if isinstance(result, str):
    # A little workaround so strings are not interpreted as variables since shell output omits quotes
    result = "str('%s')"%result

print result