from functools import wraps
import sys
from typing import Callable, Any, NoReturn


class Logger:
    '''Logger allowing to display on the console and write a message in a file
    at the same time.
    
    References :
    
     1. `<https://stackoverflow.com/questions/14906764/how-to-redirect-stdout-to-both-file-and-console-with-scripting/14906787>`_
    '''

    def __init__(self, filepath: str) -> NoReturn:
        self.terminal = sys.stdout
        self.logfile = open(filepath, "a")

    def write(self, message: str) -> NoReturn:
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass


def getlog(filepath: str) -> Callable:
    """Writes all console prints of the decorated function to a file.
    
    Parameters:
        filepath (str): Path of the file where the logs will be written.
    """
    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:

            sys.stdout = Logger(filepath)
            result = function(*args, **kwargs)
            sys.stdout.logfile.close()
            sys.stdout = sys.stdout.terminal
            return result

        return wrapper

    return decorator
