from functools import wraps
import sys
from typing import Callable, Any, NoReturn
import matplotlib.pyplot as plt
import statistics


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
    """
    The RunGroup class stores informations about a bunch of experiments that shares 
    the sames parameters excepted the on_param parameter.
    """
    def __init__(self, df, on_param):
        """
        :param df: pandas Dataframe containg experiments scores and parameters
        :param on_param: The parameter that change across experiments
        """
        self.df = df
        self.on_param = on_param
        not_col = [self.on_param, "score", "experiment_name", "id_experiment"]
        # Add parameters as class attributes
        for column in self.df.columns:
            if column not in not_col:
                setattr(self, column, list(self.df[column])[0])

    def plot(self, show=True):
        """
        Plot the values of the desired score by on_param values
        :param show: Do show the plot or not
        """
        if len(self.df) < 2: return
        scores = self.df.score
        param = self.df[self.on_param]
        names = [self.on_param + "_" + p for p in param]
        sortedRes = sorted(zip(names, scores), key=lambda x: x[0])

        # Do mean if multiple score for same param        
        res_dict = {}
        for name, score in sortedRes:
            res_dict.setdefault(name, []).append(score)

        names = list(res_dict.keys())
        scores = [ statistics.mean(r) for r in list(res_dict.values())]

        p = plt.plot(names, scores)  
        plt.title(self._get_title())
        if show: plt.show()

    def _get_title(self):
        """
        Return a title containing all parameters value, used in the plot legend.
        """
        title = ""
        for i, (k, v) in enumerate(vars(self).items()):
            if k != "df" and k != "on_param":
                title += f"{k}: {v}, "
            if i % 3 == 0:
                title += "\n"
        return title