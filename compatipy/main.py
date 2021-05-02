import subprocess
import os

class PortingException(BaseException):
    ...

class Compatible:
    def __init__(self, definition, *, args=(None,), path=os.path.dirname(__file__), old_version='2.7', command='python', prnt=True, raise_exceptions=True):
        """A class that tries to execute Python 2 code in a separate process (via subprocess) and capture the result and output

        Args:
            definition (str): Method of a module to be executed. Use the format: module.method
            args (tuple, optional): Arguments to be provided for the method. Defaults to (None,).
            path (str, optional): If the module to be executed is located in another directory, specify it. Make sure you use absolute path. Defaults to os.path.dirname(__file__).
            old_version (str, optional): What version of Python to use to run code for Python 2. Defaults to '2.7'.
            command (str, optional): What command to use to run code. Better leave alone. Defaults to 'python'.
            prnt (bool, optional): Defines if what the function prints must be printed out during its execution. Defaults to True
            raise_exceptions (bool, optional): Defines if the occurring exceptions will be raised in Python 3 script. Defaults to True
        Raises:
            PortingException: An exception if the script was unable to run the code due to some errors
        """
        self.path = path 
        self.module, self.method = *definition.split('.')[:-1], definition.split('.')[-1]
        self.old_version = old_version
        self.command = command
        self.args = args
        self.print = prnt
        self.raise_exceptions = raise_exceptions

        if not isinstance(args, tuple):
            raise PortingException(f'Arguments must be passed in as a tuple, not as {type(args)}')

        self.__check_file()
        self.__check_availabilty()
        self.__check_runcommand()

    def __check_file(self):
        """Checks that the module user requested exists"""
        if not os.path.exists(os.path.join(self.path, self.module+'.py')):
            raise PortingException(f'Module {os.path.join(self.path, self.module+".py")} cannot be accessed')

    def __check_availabilty(self):
        """Checks if the requested old_version is installed and available in PATH"""
        self.version_name = f'Python{self.old_version.replace(".", "")}'
        self.old_python_path = [entry for entry in os.environ['PATH'].split(';') if self.version_name in entry][0]
        if not self.old_python_path:
            raise PortingException(f'Python {self.old_version} is not added to PATH. Porting is not available')

    def __execute(self, cmd):
        """Executes given command in subprocess and returns output or error text if the latter is present

        Args:
            cmd (str): Command to be executed

        Raises:
            PortingException: Occurrs if the script was denied access to some resource (e.g. python executable)
        Returns:
            str: Output or error text resulting from command execution
        """
        cmd = cmd.split(' ')
        try:
            output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result =  output.stdout or output.stderr
            return result.decode('UTF-8')
        except PermissionError:
            raise PortingException('Couldn\'t execute a command due to insufficient privileges. Make sure this script has admin access')

    def __check_runcommand(self):
        """Checks if older version of python is run through specified command"""
        self.oldpy_command = os.path.join(self.old_python_path, self.command+".exe")
        result = self.__execute(f'{self.oldpy_command} -V')
        if not self.old_version in result:
            raise PortingException(f'Cannot run Python {self.old_version} via "{self.command}" command. Specify another command via "command" option on init')

    def __runfunc(self):
        py2dir = os.path.join(os.path.dirname(__file__), 'py2.py')
        module_dir = os.path.join(self.path, self.module) + '.py'
        result = self.__execute(f'{self.oldpy_command} {py2dir} {module_dir} {self.method} args={self.args}')
        try:
            result = eval(result)
            if result.get('exceptions') and self.raise_exceptions:
                raise result.get('exceptions')[0]
            return result
        except SyntaxError:
            raise PortingException('A SyntaxError occurred during file execution. It might be due to invalid file formatting (e.g. it\'s empty)')

    def __call__(self):
        """Returns what the function returned when it was executed (Ah, yes, the tautology)"""
        result = self.__runfunc()
        if self.print:
            [print(message) for message in result['output']]
        return result['result']

    @property
    def output(self):
        """Returns what the function printed out during its execution

        Returns:
            list: The list containing objects the function printed out during execution using print or sys.stdout
        """
        result = self.__runfunc()
        return result['output']

    @property
    def all(self):
        """Returns everything the function printed and returned

        Returns:
            dict: The dictionary with output and retured values of the function
        """
        return self.__runfunc()