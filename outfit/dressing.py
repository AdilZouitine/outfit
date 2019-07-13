import peewee

class Dressing:
    
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)

    def __call__(self):
        pass

    def add_comment(self, comment: str):
        pass

    def add_file(self, file):
        pass

    def add_parameter(self, file):
        pass

    def query(self, query):
        pass
    
    def get_best_scores(self, mode, on, n_best=10):
        pass 