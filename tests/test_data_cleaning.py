import unittest

import numpy as np
import pandas as pd
import pytest
from data_cleaning_transformers import (DropExtraneousColumnsTransformer,
                                        LastKnownChangeColumnTransformer,
                                        SqftColumnTransformer,
                                        ViewColumnTransformer,
                                        WaterFrontColumnTransformer)
from pandas.testing import assert_frame_equal, assert_series_equal


class TestViewColumnTransformer:

    @pytest.mark.parametrize("input_data, expected_output", [
        (pd.DataFrame({'view': [1, np.nan, 3]}),
         pd.DataFrame({'view': [1.0, 0.0, 3.0]})),
    ])
    def test_transform(self, input_data, expected_output):
        transformer = ViewColumnTransformer()

        transformed_X = transformer.transform(input_data)

        assert_frame_equal(transformed_X, expected_output)


class TestWaterFrontColumnTransformer:

    @pytest.mark.parametrize("input_data, expected_output", [
        (pd.DataFrame({'waterfront': [1, np.nan, 0]}),
         pd.DataFrame({'waterfront': [1.0, 0.0, 0.0]})),
    ])
    def test_transform(self, input_data, expected_output):
        transformer = WaterFrontColumnTransformer()

        transformed_X = transformer.transform(input_data)

        assert_frame_equal(transformed_X, expected_output)


class TestLastKnownChangeColumnTransformer:

    @pytest.mark.parametrize("input_data, expected_output", [(
        pd.DataFrame({'yr_renovated': [0, np.nan, 2000],
                      'yr_built': [1980, 1990, 2010]}),
        pd.DataFrame({'yr_renovated': [0, np.nan, 2000],
                      'yr_built': [1980, 1990, 2010],
                      'last_known_change': [1980, 1990, 2000]})
    )])
    def test_transform(self, input_data, expected_output):
        transformer = LastKnownChangeColumnTransformer()
        transformed_X = transformer.transform(input_data)

        # Test case 1 - check yr_renovated remains null        

        assert_series_equal(transformed_X['yr_renovated'],
                            expected_output['yr_renovated'])

        # Test case 2 - check yr_renovated remains null and calculation of last_known_change is correct

        assert_frame_equal(transformed_X, expected_output)


class TestDropExtraneousColumnsTransformer:

    @pytest.mark.parametrize("input_data, expected_output", [(
        pd.DataFrame({'yr_renovated': [0, np.nan, 2000],
                      'yr_built': [1980, 1990, 2010],
                      'last_known_change': [1980, 1990, 2000]}),
        pd.DataFrame({'last_known_change': [1980, 1990, 2000]})
    )])
    def test_transform(self, input_data, expected_output):
        transformer = DropExtraneousColumnsTransformer()

        transformed_X = transformer.transform(input_data)

        assert_frame_equal(transformed_X, expected_output)


class TestSqftColumnTransformer:

    @pytest.mark.parametrize("input, expected_output", [(
        {'sqft_living': [1000, 1500, 1200],
         'sqft_above': [800, 1000, 900],
         'sqft_basement': ['200', '?', '300']},
        {'sqft_living': [1000, 1500, 1200],
         'sqft_above': [800, 1000, 900],
         'sqft_basement': [200, 500, 300]}
    )])
    def test_transform(self, input, expected_output):
        transformer = SqftColumnTransformer()
        results = transformer.transform(pd.DataFrame(input))

        assert_frame_equal(results, pd.DataFrame(
            expected_output), check_dtype=False)

        for value in results['sqft_basement']:
            assert type(value == np.float64)
