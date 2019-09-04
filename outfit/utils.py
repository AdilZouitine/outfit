from functools import wraps
import sys
from typing import Callable, Any, NoReturn
import matplotlib.pyplot as plt

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


class RunGroup:
    def __init__(self, df, on_param):
        self.df = df
        self.on_param = on_param
        self.not_col = [self.on_param, "score", "experiment_name", "id_experiment"]
        for column in self.df.columns:
            if column not in self.not_col:
                setattr(self, column, list(self.df[column])[0])

    def plot(self, show=True):
        scores = self.df.score
        exp_name = self.df.experiment_name
        param = self.df[self.on_param]
        names = [self.on_param + "_" + p for p in param]
        p = plt.bar(names, scores)
        if show: plt.show()
        return p