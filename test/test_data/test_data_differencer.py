""" Test the data differencer """

import pytest

from src.data.dataset_generator import DatasetGenerator
from src.data.data_differencer import DataDifferencer
from src.data.montel_data_getter import MontelDataGetter


def test_differencing():
    dataset = DatasetGenerator(['montel']).get_dataset('2021-01-01', '2021-01-10', 'T00')
    pseudo_dataset = DatasetGenerator(['montel']).get_dataset('2021-01-10', '2021-01-10', 'T16')
    differencer = DataDifferencer()
    pseudo_differencer = DataDifferencer()
    differenced_data = differencer.difference_data(dataset)
    pseudo_prediction = pseudo_differencer.difference_data(pseudo_dataset)
    pseudo_dataset.drop(pseudo_dataset.index[:1], inplace=True)
    pseudo_dataset.reset_index(drop=True, inplace=True)
    reverse_data = differencer.reverse_difference(pseudo_prediction)

    assert pseudo_dataset.drop('Time',axis=1).astype('float').equals(reverse_data.drop('Time', axis=1).astype('float'))

