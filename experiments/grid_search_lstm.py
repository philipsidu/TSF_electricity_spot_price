"""
This file shows an example grid search for the lstm model
"""

from src.data.dataset_generator import DatasetGenerator
from src.data.data_splitter import train_test_split
from src.data.data_transformer import DataTransformer
from src.grid_searcher import GridSearcher


if __name__ == '__main__':
    # define a parameter grid for each model
    lstm_param_grid = {
        'model_name': ['lstm'],
        'window_size': [168, 2*168, 4*168],
        'gap': [0, 23, 167],  # Prediction horizons (hour, day, week)
        'num_layers': [1, 2],
        'hidden_layer_size': [128, 256],
        'epochs': [100],
        'regularization': [0, 0.001]
    }

    trivial_param_grid = {
        'model_name': ['trivial']  # Add trivial model as baseline
    }

    # list of dicts containing the parameter grid for the every model
    all_model_param_grids = [lstm_param_grid,
                             trivial_param_grid]

    # CREATE TRAIN AND TEST DATASET #
    dg = DatasetGenerator(['all'])
    dataset = dg.get_dataset('2016-01-01', '2021-08-15', 'T23')
    train, test = train_test_split(dataset, 0.1)

    # Start the grid search
    grid_search = GridSearcher(all_model_param_grids)
    grid_search.run(train, test)

