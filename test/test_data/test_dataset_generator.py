import pytest

from src.data.dataset_generator import DatasetGenerator
from src.data.montel_data_getter import MontelDataGetter
from src.data.weather_data_getter import WeatherDataGetter


def test_init():
    dg = DatasetGenerator()
    assert dg.datasets == ['montel', 'entsoe', 'weather', 'weather_hamburg']
    dg = DatasetGenerator(['all'])
    assert dg.datasets == ['montel', 'entsoe', 'weather', 'weather_hamburg']
    dg = DatasetGenerator(['montel', 'montel'])
    assert dg.datasets == ['montel', 'montel']
    assert len(dg.data_getters) == 2
    for getter in dg.data_getters:
        assert isinstance(getter, MontelDataGetter)
    dg = DatasetGenerator(['weather', 'weather'])
    assert dg.datasets == ['weather', 'weather']
    assert len(dg.data_getters) == 2
    for getter in dg.data_getters:
        assert isinstance(getter, WeatherDataGetter)

    with pytest.raises(ValueError):
        _ = DatasetGenerator(['invalid'])


def test_dataset_generation():
    dg = DatasetGenerator()
    _ = dg.get_dataset('2021-01-01', 'latest', '')


def test_merging_datasets():
    dg = DatasetGenerator(['montel', 'montel'])
    dataset = dg.get_dataset('2020-01-01', '2020-01-10', 'T16')
    assert dataset.shape == (9 * 24 + 17, 3)
    for index in range(9 * 24 + 17):
        assert dataset.iloc[index, 1] == dataset.iloc[index, 2]
