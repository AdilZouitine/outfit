import peewee

database = peewee.SqliteDatabase(None)

class BaseModel(peewee.Model):
    class Meta:
        database = database


class Experiment(BaseModel):
    id_experiment =  peewee.AutoField()
    experiment_name = peewee.CharField()
    comment = peewee.CharField(null=True)
    date_experiement = peewee.DateField(null=True)


class Parameter(BaseModel):
    id_parameter =  peewee.AutoField()
    parameter_name = peewee.CharField(null=True)
    parameter = peewee.CharField(null=True)

    experiment = peewee.ForeignKeyField(Experiment, to_field="id_experiment")


class Output(BaseModel):
    id_output =  peewee.AutoField()
    type_output = peewee.CharField()
    path_output = peewee.CharField()

    experiment = peewee.ForeignKeyField(Experiment, to_field="id_experiment")


class Score(BaseModel):
    id_score =  peewee.AutoField()
    type_score = peewee.CharField()
    score = peewee.FloatField()

    experiment = peewee.ForeignKeyField(Experiment, to_field="id_experiment")


class DatabaseUser:
    """
    references:
        1. <https://stackoverflow.com/questions/41305870/how-can-i-dynamically-set-the-sqlite-database-file-in-peewee>
    """
    def __init__(self, db_path):
        database.init(db_path)

def create_database(db_path):
    DatabaseUser(db_path)
    database.create_tables([Experiment, Parameter, Output, Score])

