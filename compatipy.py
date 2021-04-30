import subprocess
import os

class PortingException(BaseException):
    ...

class Compatible:
    def __init__(self, definition, *, args=(None,), path=os.path.dirname(__file__), old_version='2.7', command='python'):
        self.path = path 
        self.module, self.method = *definition.split('.')[:-1], definition.split('.')[-1]
        self.old_version = old_version
        self.command = command

        if not isinstance(args, tuple):
            raise PortingException(f'Arguments must be passed in as a tuple, not as {type(args)}')

        self.__check_file()
        self.__check_availabilty()
        self.__check_runcommand()

    def __check_file(self):
        """Checks that the module user requested exists"""
        print(self.path)
        if not os.path.exists(os.path.join(self.path, self.module+'.py')):
            raise PortingException(f'Module {os.path.join(self.path, self.module+".py")} cannot be accessed')

    def __check_availabilty(self):
        """Checks if the requested old_version is installed and available in PATH"""
        self.version_name = f'Python{self.old_version.replace(".", "")}'
        self.old_python_path = [entry for entry in os.environ['PATH'].split(';') if self.version_name in entry][0]
        if not self.old_python_path:
            raise PortingException(f'Python {self.old_version} is not added to PATH. Porting is not available')

    def __execute(self, cmd):
        cmd = cmd.split(' ')
        try:
            output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result =  output.stdout or output.stderr
            return repr(result)
        except PermissionError:
            raise PortingException('Couldn\'t execute a command due to insufficient privileges. Make sure this script has admin access')

    def __check_runcommand(self):
        """Checks if older version of python is run through specified command"""
        self.oldpy_command = os.path.join(self.old_python_path, self.command+".exe")
        result = self.__execute(f'{self.oldpy_command} -V')
        if not self.old_version in result:
            raise PortingException(f'Cannot run Python {self.old_version} via "{self.command}" command. Specify another command via "command" option on init')

    def __call__(self):
        """Called when the function is referenced as f()"""
        py2dir = os.path.join(os.path.dirname(__file__), 'py2.py')
        module_dir = os.path.join(self.path, self.module) + '.py'
        result = self.__execute(f'{self.oldpy_command} {py2dir} {module_dir} {self.method}')
        print(result)