""" This class implements a trivial model that always chooses the last
 known value as prediction """

import numpy as np
from typing import Any

from src.models.model_interface import BaseModel


class TrivialModel(BaseModel):
    """
    This class implements a trivial baseline model
    for the electricity price prediction task
    """

    def __init__(self, model_params: dict, name: str = 'trivial'):
        """
        Constructor for the trivial model setting the name field and
        the specific model parameters
        :param name: name of the used algorithm, 'trivial'
        :param model_params: Dictionary of parameters for the model
        """
        super().__init__(name, model_params)

    def train(self, dataset: Any, test_dataset: Any, model_params: dict) -> Any:  # pylint: disable=unused-argument
        """
        Trains the linear regression model with the provided data
        :param dataset: Training dataset in format tf.data.Dataset
            The dataset can be used as follows:
            for batch in dataset:
                x, y = batch
            Shapes: x -> (batch_size, window_size, 19(num_features));
                    y -> (batch_size,)
        :param test_dataset: test dataset -> Can not be used for training,
            only for printing test loss or similar
        :param model_params: dictionary which sets the relevant hyperparameters
            for the training procedure
        """
        # For this trivial model, training is not necessary
        pass

    def predict(self, test_dataset: Any) -> np.array:
        """
        Uses the trained model to make a prediction based on x_input
        :param test_dataset: Training dataset in format tf.data.Dataset
            The dataset can be used as follows:
            for batch in dataset:
                x, y = batch
            Shapes: x -> (batch_size, window_size, 19(num_features));
                    y -> (batch_size,)
        :return: np.array containing all predictions, shape: (n_test,)
        """
        prediction = np.empty(shape=(0, 1))
        for batch in test_dataset:
            x, _ = batch
            pred = np.asarray(x)[:, -1, 0].reshape((-1, 1))
            prediction = np.concatenate([prediction, pred], axis=0)

        return prediction.reshape((-1,))

    def save(self, path: str):
        """
        Saves the model at the given path with the given name
        For this model, no saving is necessary
        :param path: path and model name at location where model should be saved
        """
        pass

    def load(self, path: str):
        """
        Loads the model from the given path
        For this model, no loading is necessary
        :param path: path and model name at location where model should be
        loaded from
        """
        pass
