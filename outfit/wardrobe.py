import peewee

from .models import Experiment, Output, Parameter, Score, create_database


class Wardrobe:

    def __init__(self, db_path: str):
        pass

    def __call__(self):
        pass

    def add_experiement(self, comment: str):
        pass

    def add_output(self, **kwargs):
        pass

    def add_parameter(self, **kwargs):
        pass

    def add_score(self, **kwargs):
        pass

    def query(self, query):
        pass
    
    def get_best_scores(self, mode, on, n_best=10):
        pass 
