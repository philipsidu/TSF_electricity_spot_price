""" Validate that the montel data getter works as expected """

import pytest
import os
import shutil
import pandas as pd

from src.data.montel_data_getter import *


def test_init():
    dg = MontelDataGetter("montel_test")
    path = dg.get_project_root()
    assert os.path.exists(
        os.path.join(path, 'data', 'montel_test')
    )
    assert dg.data_dir == os.path.join(path, 'data', 'montel_test')
    assert dg.name == "montel_test"
    assert dg._root_dir == path
    shutil.rmtree(dg.data_dir)


def test_show_all_datasets():
    dg = MontelDataGetter("montel_test")
    dg._show_available_datasets()
    shutil.rmtree(dg.data_dir)


def test_token_environment_variable():
    # Instantiate Montel Data Getter -> only works if token is valid
    dg = MontelDataGetter("montel_test")
    token = dg.token
    file_path = os.path.join(dg._root_dir, 'src', 'data',
                             'MONTEL_TOKEN.txt')
    os.remove(file_path)
    os.environ['MONTEL_TOKEN'] = token
    dg.get_token()  # Throws an error if token is invalid or not there


def test_get_and_process_data():
    dg = MontelDataGetter("montel_test")

    dg.get_data('2020-01-01', '2020-12-31', overwrite=True)

    assert os.path.exists(os.path.join(dg.data_dir, 'data.csv'))

    df = pd.read_csv(os.path.join(dg.data_dir, 'data.csv'))
    df.head()
    assert df.shape == (dg._get_num_days() * 24, 2)

    shutil.rmtree(dg.data_dir)


def test_check_data():
    dg = MontelDataGetter("montel_test")
    data = dict()
    data['Elements'] = [
        {
            'Date': '2020-01-01',
            'TimeSpans': list(range(26))
        }
    ]
    with pytest.raises(ValueError):
        dg._process_raw_data(data)

    dg.start_date = '2020-01-01'
    dg.end_date = '2020-01-31'
    raw_data = dg._get_raw_data()
    del raw_data['Elements'][3]

    processed_data = dg._process_raw_data(raw_data)
    assert len(processed_data) == 24 * 31
    for i in range(24):
        assert processed_data[72 + i]['SPOTPrice'] == \
            processed_data[48 + i]['SPOTPrice']


def test_loading():
    dg = MontelDataGetter("montel_test")

    data1 = dg.get_data('2020-01-01', '2020-12-31', overwrite=True)
    # Run again to check if loading the csv works correctly
    data2 = dg.get_data('2020-01-01', '2020-12-31')
    assert data1.equals(data2)

    assert os.path.exists(os.path.join(dg.data_dir, 'data.csv'))

    data3 = dg.get_data('2020-01-10', '2020-12-31')
    assert data1.iloc[9*24:, :].reset_index(drop=True).equals(data3)

    # Get older data than is downloaded
    data_4 = dg.get_data('2019-01-01', '2020-12-31')

    shutil.rmtree(dg.data_dir)


def test_loading_latest():
    dg = MontelDataGetter("montel_test")
    data = dg.get_data('2021-01-01', 'latest')
    data2 = dg.get_data('2021-01-01', '2021-06-01', 'T04')
    assert np.mod(len(data2.index), 24) == 5
    assert data.iloc[:len(data2.index), :].equals(data2)