import datetime
import os.path
from typing import Any, Dict, List, NoReturn

import pandas as pd
import peewee
from tabulate import tabulate

from .models import (DatabaseUser, Experiment, Feature, Output, Parameter,
                     Score, create_database)


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
        self.feature = []

    def add_experiment(self,
                       experiment_name: str,
                       comment: str = None,
                       date_experiment: datetime.datetime = None) -> NoReturn:

        self.experiment = Experiment.create(
            experiment_name=experiment_name,
            comment=comment,
            date_experiment=date_experiment)

    def add_output(self, type_output: str, path_output: str) -> NoReturn:
        self.output.append(
            Output.create(
                type_output=type_output,
                path_output=path_output,
                experiment=self.experiment))

    def add_parameter(self, parameter_name: str, parameter: Any) -> NoReturn:

        self.parameter.append(
            Parameter.create(
                parameter_name=parameter_name,
                parameter=parameter,
                experiment=self.experiment))

    def add_score(self, type_score: str, score: float) -> NoReturn:
        self.score.append(
            Score.create(
                type_score=type_score, score=score,
                experiment=self.experiment))

    def add_feature(self, feature_name: str) -> NoReturn:
        self.feature.append(
            Feature.create(
                feature_name=feature_name, experiment=self.experiment))

    def add_dict_score(self, dict_score: Dict[str, float]) -> NoReturn:
        for key, value in dict_score.items():
            self.add_score(type_score=key, score=value)

    def add_dict_parameter(self, dict_parameter: Dict[str, Any]) -> NoReturn:
        for key, value in dict_parameter.items():
            self.add_parameter(parameter_name=key, parameter=value)

    def add_dict_output(self, dict_output: Dict[str, str]) -> NoReturn:
        for key, value in dict_output.items():
            self.add_output(type_output=key, path_output=value)

    def add_list_feature(self, list_feature: List[str]) -> NoReturn:
        for feature in list_feature:
            self.add_feature(feature_name=feature)

    def query(self, query):
        return Experiment.select()

    def get_best_scores(self,
                        mode: str,
                        on_score: str,
                        n_best=-1,
                        verbose=True) -> Dict[str, pd.DataFrame]:

        if mode == 'min':
            mode = Score.score.asc()
        elif mode == 'max':
            mode = Score.score.desc()
        else:
            raise ValueError(
                "mode only takes as value in input 'min' or 'max'")

        query = Score.select(Score.experiment).where(
            Score.type_score == on_score).order_by(mode).limit(n_best)

        for indice, val in enumerate(query.dicts()):

            best = {
                Experiment.__name__:
                self._query_to_dataframe(Experiment.select().where(
                    Experiment.id_experiment == val['experiment']))
            }

            best.update({
                table.__name__: self._query_to_dataframe(table.select().where(
                    table.experiment == val['experiment']))
                for table in [Parameter, Output, Score, Feature]
            })

            if verbose:
                self._verbose_best(best, indice + 1)

            yield best

    def tidy(self) -> NoReturn:
        self.experiment.insert()

        for list_row in [
                self.parameter, self.score, self.output, self.feature
        ]:
            if list_row:
                for row in list_row:
                    row.insert()
                list_row.clear()
        self.experiment = None

    @classmethod
    def _query_to_dataframe(cls, query: peewee.ModelSelect) -> pd.DataFrame:
        dict_query = {indice: row for indice, row in enumerate(query.dicts())}
        return pd.DataFrame.from_dict(dict_query, orient='index')

    @classmethod
    def _verbose_best(cls, dict_best: Dict[str, pd.DataFrame], indice: int):
        header = 'TOP {} EXPERIMENT'.format(indice)
        print('═' * (len(header) + 4))
        print("│ {} │".format(header))
        print('═' * (len(header) + 4))
        print('\n' * 2)

        for k, v in dict_best.items():
                print('Table : {} \n'.format(k))
                print(tabulate(v, headers='keys', tablefmt="fancy_grid"))
                print('\n')
