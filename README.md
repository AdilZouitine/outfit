# :dress: Outfit [WIP]

Outfit is a lightweight library to **tidy up** your machine learning experiments in a simple way.

The idea of Outfit is to store in your `Wardrobe` your parameters, output file, scores and features in order to be able to make a request and find out which are your best experimentation according to a given criterion.

## How install outfit ?

Dev version: `pip install git+https://github.com/AdilZouitine/outfit --upgrade`

Pypi is comming.

## How outfit works ?

**notebook tutorials will be coming soon**

```python

import datetime

# Here import all the libraries you need for your experiment

from outfit import Wardrobe, getlog

wardrobe = Wardrobe(db_path='foo/bar/mnist.db')

exp = {
    'experiment_name': 'ResNet18',
    'comment': 'Use differential learning rate',
    'date_experiment': datetime.datetime.now()
}

wardrobe.add_experiment(**exp)

param = {
    'dropout': 0.20,
    'kernel_size': '3x3',
    'conv_block_1_lr': 0.01,
    'conv_block_2_lr': 0.001
   }

# Create the instance of your model here with your parameters
wardrobe.add_dict_parameter(param)


# Do your training phase here.
output = {'training log': '/result/training_log_resnet18.txt'}

@getlog(filepath=output['training log'])
def train_model(model, loaders, loss, lr_scheduler, n_epoch):
    ...

output.update({
    'tensorboard': '/result/event.tb',
    'model': 'diff_lr_resnet18.pth'
})

wardrobe.add_dict_output(output)

score = {
    'train acc': 0.96,
    'train loss': 0.430,
    'val acc': 0.94,
    'val loss': 0.460
     }
wardrobe.add_dict_score(score)


wardrobe.tidy() # commit your experiment in database

```

```python
# If you want to get the best experiments 

for exp in wardrobe.get_best_scores(mode='max',on_score='val acc'):
    '''
    Verbose is true by default and will print on the console 
    at each iteration the parameters, output file, 
    features and scores in a table format.

    Also returns in dictionary the parameters, output file, features and scores.
    '''
    ...

```
**Output**:
```
════════════════════
│ TOP 1 EXPERIMENT │
════════════════════



Table : Experiment 

╒════╤═════════════════╤═══════════════════╤════════════════════════════════╤════════════════════╕
│    │   id_experiment │ experiment_name   │ comment                        │ date_experiement   │
╞════╪═════════════════╪═══════════════════╪════════════════════════════════╪════════════════════╡
│  0 │               1 │ ResNet18          │ Use differential learning rate │                    │
╘════╧═════════════════╧═══════════════════╧════════════════════════════════╧════════════════════╛


Table : Parameter 

╒════╤════════════════╤══════════════════╤═════════════╤══════════════╕
│    │   id_parameter │ parameter_name   │ parameter   │   experiment │
╞════╪════════════════╪══════════════════╪═════════════╪══════════════╡
│  0 │              1 │ dropout          │ 0.2         │            1 │
├────┼────────────────┼──────────────────┼─────────────┼──────────────┤
│  1 │              2 │ kernel_size      │ 3x3         │            1 │
├────┼────────────────┼──────────────────┼─────────────┼──────────────┤
│  2 │              3 │ conv_block_1_lr  │ 0.01        │            1 │
├────┼────────────────┼──────────────────┼─────────────┼──────────────┤
│  3 │              4 │ conv_block_2_lr  │ 0.001       │            1 │
╘════╧════════════════╧══════════════════╧═════════════╧══════════════╛


Table : Output 

╒════╤═════════════╤═══════════════╤═══════════════════════════════════╤══════════════╕
│    │   id_output │ type_output   │ path_output                       │   experiment │
╞════╪═════════════╪═══════════════╪═══════════════════════════════════╪══════════════╡
│  0 │           1 │ training log  │ /result/training_log_resnet18.txt │            1 │
├────┼─────────────┼───────────────┼───────────────────────────────────┼──────────────┤
│  1 │           2 │ tensorboard   │ /result/event.tb                  │            1 │
├────┼─────────────┼───────────────┼───────────────────────────────────┼──────────────┤
│  2 │           3 │ model         │ diff_lr_resnet18.pth              │            1 │
╘════╧═════════════╧═══════════════╧═══════════════════════════════════╧══════════════╛


Table : Score 

╒════╤════════════╤══════════════╤═════════╤══════════════╕
│    │   id_score │ type_score   │   score │   experiment │
╞════╪════════════╪══════════════╪═════════╪══════════════╡
│  0 │          1 │ train acc    │    0.96 │            1 │
├────┼────────────┼──────────────┼─────────┼──────────────┤
│  1 │          2 │ train loss   │    0.43 │            1 │
├────┼────────────┼──────────────┼─────────┼──────────────┤
│  2 │          3 │ val acc      │    0.94 │            1 │
├────┼────────────┼──────────────┼─────────┼──────────────┤
│  3 │          4 │ val loss     │    0.46 │            1 │
╘════╧════════════╧══════════════╧═════════╧══════════════╛


Table : Feature 

```

## Other solution:

[mlflow](https://github.com/mlflow/mlflow) & [dvc](https://github.com/iterative/dvc).

These solutions are great, they also offer a user interface and have many more options than my library however for a simple use where you only want to organize your experimentation and make a simple query.
Both solutions seem to be overkill.

## TODO

- Finish the notebook tutorials
- Put outfit on Pypi
