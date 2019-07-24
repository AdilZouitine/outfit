# :dress: Outfit [WIP]

Outfit is a lightweight library to **tidy up** your machine learning experiments in a simple way.

The idea of Outfit is to store in your wardrobe your parameters, output file, scores and features in order to be able to make a request and find out which are your best experimentation according to a given criterion.

## How install outfit ?

Dev version: `pip install git+https://github.com/AdilZouitine/outfit --upgrade`

Pypi is comming.

## How outfit works ?

```python

import datetime

# Here import all the libraries you need for your experiment

from outfit import WardRobe, getlog

wardrobe = WardRobe(db_path='foo/bar/mnist.db')

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

# If you want to have the best experiments 

for exp in wardrobe.get_best_scores(mode='max',on_score='val acc'):
    '''
    At the default verbose and will print on the console 
    at each iteration the parameters, output file, 
    features and scores in a table format.

    Also returns in dictionary form the parameters, output file, features and scores.
    '''
    ...


```