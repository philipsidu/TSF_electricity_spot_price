from linear_regression_model import LinearRegressionModel


class ModelFactory:
    """
    Factory for model instances
    """

    @staticmethod
    def get(model_name: str):
        """
        Get a model instance based on the name of the model/algorithm
        :param model_name: name of the model/algorithm
        :return: class instance of the model
        """

        if model_name == 'linear_regression':
            return LinearRegressionModel()

        elif model_name == 'prophet':
            pass

        elif model_name == 'rcnn':
            pass

        else:
            raise ValueError(f'The model with the name "{model_name}" '
                             f'does not exist!')
