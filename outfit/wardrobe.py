import os.path
import typing

import peewee

from .models import DatabaseUser, Experiment, Output, Parameter, Score, create_database


class Wardrobe:
    def __init__(self, db_path: str):

        if not os.path.isfile(db_path):
            create_database(db_path)
        else:
            DatabaseUser(db_path)

        self.experiment = None
        self.parameter = []
        self.output = []
        self.score = []

    def __call__(self):
        pass

    def add_experiment(self, experiment_name: str, comment: str=None,
                       date_experiment=None) -> typing.NoReturn:

        self.experiment = Experiment.create(
            experiment_name=experiment_name,
            comment=comment,
            date_experiment=date_experiment)

    def add_output(self, type_output: str, path_output: str) -> typing.NoReturn:
        self.output.append(
            Output.create(
                type_output=type_output,
                path_output=path_output,
                experiment=self.experiment))

    def add_parameter(self, parameter_name: str, parameter) -> typing.NoReturn:

        self.parameter.append(
            Parameter.create(
                parameter_name=parameter_name,
                parameter=parameter,
                experiment=self.experiment))

    def add_score(self, type_score: str, score: float) -> typing.NoReturn:
        self.score.append(
            Score.create(
                type_score=type_score, score=score,
                experiment=self.experiment))

    def add_dict_score(self, dict_score:typing.Dict[str, float]) -> typing.NoReturn:
        for key, value in dict_score.items():
            self.add_dict_score(type_score=key,score=value)

    def add_dict_parameter(self, dict_parameter:typing.Dict[str, typing.Any]) -> typing.NoReturn:
        for key, value in dict_parameter.items():
            self.add_parameter(parameter_name=key, parameter=value)

    def add_dict_output(self, dict_output:typing.Dict[str, str]) -> typing.NoReturn:
        for key, value in dict_output.items():
            self.add_dict_output(type_output=key, path_output=value)

    def query(self, query):
        pass

    def get_best_scores(self,
                        on_experience: str,
                        mode: str,
                        on_score: str,
                        n_best=10):
        pass

    def commit(self) -> typing.NoReturn:
        self.experiment.insert()

        for list_row in [self.parameter, self.score, self.output]:
            if list_row:
                for row in list_row:
                    row.insert()
                list_row.clear()
        self.experiment = None