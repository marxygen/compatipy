# compatipy

A library to use code for Python 2 in Python 3.

## Prerequisites

You need to have two versions of Python installed: Python 3 to run the main script, and Python 2 for older script you want to run from the newer one. If the older script uses some libraries, make sure they are installed for Python 2 as well.

## How to use

Suppose you have a Python 2 script in a file `script.py`, which contains a function that does something crucial and you absolutely need it for your project and for some reason cannot adapt to Python 3. Here is the example: <br><br>
Contents of `script.py`

```Python
def func():
    print 'This is the output'
    return 'This is something I return'
```

There is a Python 3 file **in the same directory** called `file.py`, where you want to use this function. Now, that's where my super duper very stupid crutch code comes into play:<br><br>
Contents of `file.py`

```Python
from compatipy import Compatible

func = Compatible('script.func')
print(func())
```

All you need to do is to instantiate a **Compatible** class and pass in the module and method name.

What will happen? Does the code break? I hope not. In fact, this is the output:

```IDLE
>>> This is something I return
```

Nice. So the code got executed even though it contains clearly Python-3-invalid `print` statement. But we also have something we printed out in the function that wasn't displayed anywhere. There is a special property for that:

```Python
func.output
```

It **runs** the function and returns a list of what was supposed to be printed out. Just in case.

```IDLE
>>> ['This is the output']
```

All data that was passed into `sys.stdout` is collected and returned as a list.

## Running Python 2 scripts from another directory

If you want to run a Python 2 script that is located in another directory, use `path` keyword argument. Make sure you use **absolute path**.

```Python
func = Compatible('example.func', path=os.path.join(os.path.dirname(__file__), 'directory'))
```

Yeah, we need absolute paths, cause under the hood this Frankenstein runs your script using another Python interpreter.

## Retrieving all information

If you for some reason want everything the function returned **and** printed out during execution, there is a method (but has to be used as a _property_) for that:

```Python
func.all
```

Output:

```IDLE
>>> {'result': 'This is something I return', 'output': ['This is the output']}
```
