""" This file implements the ModelEvaluator that calculates up to 5 different
metrics to evaluate the performance of the time series predictions"""

import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


class ModelEvaluator(object):
    """
    This class
    """
    @staticmethod
    def _calc_r2(y_pred: np.array, y_true) -> float:
        """
        Calculates the r2 score / coefficient of determination
        :param y_pred: values predicted by the model
        :param y_true: actual values of the time-series data
        :return: r2 score / coefficient of determination
        """
        return r2_score(y_true, y_pred)

    @staticmethod
    def _calc_mae(y_pred: np.array, y_true: np.array) -> float:
        """
        Calculates the mean absolute error
        :param y_pred: values predicted by the model
        :param y_true: actual values of the time-series data
        :return: mean absolute error between the predicted y and the actual y
        """
        return mean_absolute_error(y_true, y_pred)

    @staticmethod
    def _calc_mse(y_pred: np.array, y_true: np.array) -> float:
        """
        Calculates the mean squared error
        :param y_pred: values predicted by the model
        :param y_true: actual values of the time-series data
        :return: mean squared error between the predicted y and the actual y
        """
        return mean_squared_error(y_true, y_pred)

    @staticmethod
    def _calc_mape(y_pred: np.array, y_true: np.array) -> float:
        """
        Calculates the mean absolute percentage error
        :param y_pred: values predicted by the model
        :param y_true: actual values of the time-series data
        :return: mean absolute percentage error between the predicted y and the
        actual y
        """
        mask = (y_pred != 0)  # prevents divisions by 0
        return (np.fabs(y_pred - y_true) / y_pred)[mask].mean()

    @staticmethod
    def _calc_smape(y_pred: np.array, y_true: np.array) -> float:
        """
        Calculates the symmetric mean absolute percentage error
        :param y_pred: values predicted by the model
        :param y_true: actual values of the time-series data
        :return: symmetric mean absolute percentage error between the predicted
        y and the actual y
        """
        smape = 100 / len(y_true) * np.sum(2 * np.abs(y_pred - y_true) /
                                           (np.abs(y_true) + np.abs(y_pred)))
        return smape

    def evaluate(self, y_pred: np.array, y_true: np.array,
                 eval_metrics: list = None) -> dict:
        """
        Calculates all requested metrics for evaluation
        :param y_pred: values predicted by the model
        :param y_true: actual values of the time-series data
        :param eval_metrics: list of requested metrics (all, r2, mae, mse, mape,
        smape)
        :return: scores_dict with the score of each requested metric
        """

        if eval_metrics is None:
            eval_metrics = ['all']

        scores_dict = dict()
        if 'r2' in eval_metrics or 'all' in eval_metrics:
            scores_dict["r2_score"] = self._calc_r2(y_pred, y_true)

        if 'mae' in eval_metrics or 'all' in eval_metrics:
            scores_dict["mae_score"] = self._calc_mae(y_pred, y_true)

        if 'mse' in eval_metrics or 'all' in eval_metrics:
            scores_dict["mse_score"] = self._calc_mse(y_pred, y_true)

        if 'mape' in eval_metrics or 'all' in eval_metrics:
            scores_dict["mape_score"] = self._calc_mape(y_pred, y_true)

        if 'smape' in eval_metrics or 'all' in eval_metrics:
            scores_dict["smape_score"] = self._calc_smape(y_pred, y_true)

        if not scores_dict:
            raise ValueError("Valid values for eval_metrics are: all, r2, mae, "
                             "mse, mape or smape.")

        return scores_dict
