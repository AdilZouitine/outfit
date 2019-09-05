import datetime
import os.path
from typing import Any, Dict, List, Tuple, NoReturn
import itertools as it
from functools import reduce
import pandas as pd
import peewee
from tabulate import tabulate
from .utils import RunGroup

from .models import (DatabaseUser, Experiment, Feature, Output, Parameter,
                     Score, create_database)


class Wardrobe:
    """The wardrobe allows you to insert your experimentations and to request them.

    Parameters:
        db_path (str): Path where the database is stored
        however if the file does not exist, it will be created.

    Example:

        ::

            >>> from outfit import Wardrobe, Experiment, Score, Output, Parameter, Feature
            >>> tidy = Wardrobe(':memory:')
            >>> tidy.add_experiment(experiment_name="Mnist", comment='Pytorch Resnet 18', date_experiment=None)
            >>> param = {'dropout': 0.20, 'kernel_size': '3x3', 'task': 'classification'}
            >>> tidy.add_dict_parameter(param)
            >>> # Do your training phase here.
            >>> score = {'acc': 0.90, 'loss': 0.1}
            >>> tidy.add_dict_score(score)
            >>> tidy.add_output(type_output='tensorboard', path_output='event.tb')
            >>> tidy.tidy() # commit your experiment in database
    """

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
                       date_experiment: datetime.datetime = None,
                       **kwargs) -> NoReturn:
        """Create a new database experiment.
        
        Parameters:
            experiment_name (str): Name of the experiment
            comment (str): Specific comment Defaults to `None`
            date_experiment (datetime.datetime): Date of the experimentation.
            I advise you to set in value `datetime.datetime.now()`.
            Defaults to `None`.

        """

        self.experiment = Experiment.create(
            experiment_name=experiment_name,
            comment=comment,
            date_experiment=date_experiment)

    def add_output(self, type_output: str, path_output: str) -> NoReturn:
        """Creates a new output in the database associated
        with the experimentation previously created.
        
        Parameters:
            type_output (str): The type of output file.
            path_output (str): The path of output file.

        """
        self.output.append(
            Output.create(
                type_output=type_output,
                path_output=path_output,
                experiment=self.experiment))

    def add_parameter(self, parameter_name: str, parameter: Any) -> NoReturn:
        """Creates a new parameter in the database associated
        with the experimentation previously created.
        
        Parameters:
            parameter_name (str): The parameter name.
            parameter (Any): The value of the parameter.

        """
        self.parameter.append(
            Parameter.create(
                parameter_name=parameter_name,
                parameter=parameter,
                experiment=self.experiment))

    def add_score(self, type_score: str, score: float) -> NoReturn:
        """Creates a new score in the database associated
        with the experimentation previously created.
        
        Parameters:
            type_score (str): The type of score.
            For example `val loss`.
            score {float} -- The value. For example `1.337`.
        """

        self.score.append(
            Score.create(
                type_score=type_score, score=score,
                experiment=self.experiment))

    def add_feature(self, feature_name: str) -> NoReturn:
        """Creates a new feature in the database associated
        with the experimentation previously created.
        
        Parameters:
            feature_name (str): The name of feature.
            For example `lag 7 day stock`.
        """

        self.feature.append(
            Feature.create(
                feature_name=feature_name, experiment=self.experiment))

    def add_dict_score(self, dict_score: Dict[str, float]) -> NoReturn:
        """Add many scores to the database in one method.
        
        Parameters:
            dict_score (Dict[str, float]): In key the `type_score` and in value the score.
            For example `{'train loss' : 0.42, 'train accuracy': 0.78, 'val loss': 1.336, 'val accuracy': 0.20}
        """
        for key, value in dict_score.items():
            self.add_score(type_score=key, score=value)

    def add_dict_parameter(self, dict_parameter: Dict[str, Any]) -> NoReturn:
        """Add many parameters to the database in one method.
        
        Parameters:
            dict_parameter (Dict[str, Any]): In key the `parameter_name` and in value the `parameter`.
            For example `{'dropout' : 0.1, 'TTA': True}
        """
        for key, value in dict_parameter.items():
            self.add_parameter(parameter_name=key, parameter=value)

    def add_dict_output(self, dict_output: Dict[str, str]) -> NoReturn:
        """Add many outputs to the database in one method.
        
        Parameters:
            dict_output (Dict[str, str]): In key the `type_output` and in value the `path_output`.
            For example `{'tensorboard' : '/result/event.tb', 'model': '/result/resnet18_fine_tune.pth'}
        """
        for key, value in dict_output.items():
            self.add_output(type_output=key, path_output=value)

    def add_list_feature(self, list_feature: List[str]) -> NoReturn:
        """Add many features to the database in one method.
        
        Parameters:
            list_feature {List[str]} -- List of feature name.
            For example `['phone_model','target_mean_by_phone_model','age']
        """
        for feature in list_feature:
            self.add_feature(feature_name=feature)

    def query(self, query: peewee.ModelSelect) -> dict:
        """Custom query, returns a generator that will return
        a dictionary (corresponding to a row).
        
        Parameters:
            query (peewee.ModelSelect) : Custom query.
        """
        for res in query.dicts():
            yield res

    def get_best_scores(self,
                        mode: str,
                        on_score: str,
                        n_best=-1,
                        verbose=True) -> Dict[str, pd.DataFrame]:
        """Returns a generator that returns the best experiments according to a criterion.
        
        Parameters:
            mode (str): 'min' => asc or 'max' => desc
            on_score (str): On what criteria will the method return the best experimentation.
            For example `val loss`.
            n_best (int): Returns `n_best` experiments. Defaults to `-1`.
            verbose (bool): Print in the console the information of each experiment. Defaults to `True`.
        
        Raises:
            ValueError: mode only takes as value in input 'min' or 'max'.
        """

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

    @classmethod
    def _query_to_dataframe(cls, query: peewee.ModelSelect) -> pd.DataFrame:
        dict_query = {indice: row for indice, row in enumerate(query.dicts())}
        return pd.DataFrame.from_dict(dict_query, orient='index')

    def tidy(self) -> NoReturn:
        """Commit the experiment.
        """

        self.experiment.insert()

        for list_row in [
                self.parameter, self.score, self.output, self.feature
        ]:
            if list_row:
                for row in list_row:
                    row.insert()
                list_row.clear()
        self.experiment = None

    ########################################
    ###### Methods for visualisation #######
    ########################################

    def _get_params(self, on_param: str) -> List[str]:
        """ 
        Fetch parameters list from Parameter Table, excepted on_param Parameter
        Parameters:
            on_param (str): Parameter to exclude from list.
        """
        query = Parameter.select(Parameter.parameter_name)
        df = self._query_to_dataframe(query)
        params = set(df.parameter_name)
        params.remove(on_param)
        params.remove('exp_name')
        return list(params)

    def _get_experiments_score(self, on_score: str) -> pd.DataFrame:
        """
        Fetch desired score for all experiments and parameters.
        Parameters:
            on_score (str): Score to select from Score table.
        """
        query = (Score.select(Score, Parameter, Experiment).join(
            Parameter, on=(Parameter.experiment == Score.experiment)).join(
                Experiment,
                on=(Experiment.id_experiment == Parameter.experiment_id
                    )).where(Score.type_score == on_score))
        res = self.query(query)
        df = pd.DataFrame(res)
        df = df[[
            'id_experiment', 'experiment_name', 'parameter_name', 'parameter',
            'score'
        ]]
        return df

    def _get_parameters_combinations(self, params:List[str]) -> Tuple:
        """
        Get all combination of parameters names and values.
        Parameters:
            params (List[str]): Parameters to combine.
        """
        # Query Parameters table to get all parameters values
        params_ = {}
        for p in params:
            query = Parameter.select(
                Parameter.parameter_name, Parameter.parameter).where(
                    Parameter.parameter_name == p).group_by(
                        Parameter.parameter)
            res = self.query(query)
            for val in res:
                params_.setdefault(val["parameter_name"],
                                   []).append(val['parameter'])

        # Produce parameters cominations
        allNames = sorted(params_)
        combinations = it.product(*(params_[n] for n in allNames))
        return combinations, allNames

    def _merge_df_from_combinations(self, df_list: List[pd.DataFrame],
                                    on_param: str) -> pd.DataFrame:
        """ 
        Given a dataframe list, merge all dataframes on the id_experiment column
        Query db to get the on_param value for each run
        Return a dataframe with all parameters and score values for each experiment.
        Parameters:
            df_list: List of dataframes to merge
            on_param (str): Parameter to add in df
        """
        # Merge row by exp name
        df_final = None
        for df in df_list:
            if df_final is None: df_final = df
            else:
                df_ = pd.merge(
                    df_final,
                    df,
                    on='id_experiment',
                    how='inner',
                    suffixes=('', '_y'))

                df_.drop([x for x in df_.columns if '_y' in x],
                         axis="columns",
                         inplace=True)

                for i, row in df_.iterrows():
                    query = (Experiment.select(
                        Parameter.parameter_name, Parameter.parameter).join(
                            Parameter,
                            on=Experiment.id_experiment == Parameter.experiment
                        ).where(Parameter.parameter_name == on_param).where(
                            Experiment.id_experiment == row.id_experiment))

                    res = self.query(query)
                    new_param = next(iter(res))
                    df_.at[i, new_param['parameter_name']] = new_param[
                        'parameter']
                    df_final = df_

        return df_final

    def plot_by_param(self, on_param: str, on_score: str):
        """
        Plot run that have all parameters identical excepted the on_param parameter.
        The value that is plotted is the on_score param.
        Parameters:
            on_param (str): Parameter to test
            on_score (str): Score to fetch as value for plot
        """
        # Get parameters names
        params = self._get_params(on_param=on_param)

        # Get all experiment with choosen score
        all_exp_df = self._get_experiments_score(on_score=on_score)

        # Get all parameters values
        combinations, allNames = self._get_parameters_combinations(params)

        # For every combination, filter experiment by parameters values and merge by exp
        for comb in combinations:
            dfs = []
            # Construct parameters dict
            pa = {allNames[i]: c for i, c in enumerate(comb)}

            # Select exp with params
            dfs = []
            for k, v in pa.items():
                df__ = all_exp_df[(all_exp_df['parameter_name'] == k)
                                  & (all_exp_df['parameter'] == v)]
                df__ = df__[['id_experiment', 'experiment_name', 'score']]
                df__[k] = v
                dfs.append(df__)

            # Merge all parameters
            merged_df = self._merge_df_from_combinations(
                df_list=dfs, on_param=on_param)
            yield RunGroup(merged_df, on_param=on_param)
