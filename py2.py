"""
This script accepts module and method name as the argument, executes the method and returns the result
"""
import sys, os
import imp

modulepath, method = sys.argv[1:3]
path, module = os.path.split(modulepath)
module = module.replace('.py', '')

function = imp.load_source(module+'.'+method, modulepath)
        
print function.__dict__[method]()

