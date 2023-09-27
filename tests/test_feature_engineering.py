import numpy as np
import pandas as pd
import pytest
from feature_enginneering_tranformers import (CentreOfWealthColumnsTransformer,
                                              SqFtPriceColumnTransformer,
                                              WaterDistanceColumnTransformer)
from pandas.testing import assert_frame_equal, assert_series_equal


class TestSqFtPriceColumnTransformer:

    @pytest.mark.parametrize("input_data, expected_output", [(
        pd.DataFrame({'price': [10000, 10900, 60000],
                      'sqft_living': [50, 65, 3000],
                      'sqft_lot': [500, 1000, 1500]}),
        pd.DataFrame({'price': [10000, 10900, 60000],
                      'sqft_living': [50, 65, 3000],
                      'sqft_lot': [500, 1000, 1500],
                      'sqft_price': [18.18, 10.23, 13.33]})
    )])
    
    def test_transform(self, input_data, expected_output):
        transformer = SqFtPriceColumnTransformer()
        transformed_X = transformer.transform(input_data)

        assert_series_equal(transformed_X['sqft_price'],
                            expected_output['sqft_price'])


class TestWaterDistanceColumnTransformer:

    @pytest.fixture
    def transformer(self):
        return WaterDistanceColumnTransformer()

    def test_dist(self, transformer):
        ref_long = 200.0
        ref_lat = 502.2

        # Test case 1: Check distance calculation for a specific location
        long = -122.238
        lat = 47.623
        expected_distance = 57999.37

        distance = transformer.dist(long, lat, ref_long, ref_lat)

        assert pytest.approx(distance, 0.001) == expected_distance

        # Test case 2: Check distance calculation for another location
        long = -122.245
        lat = 47.631
        expected_distance = 57998.89

        distance = transformer.dist(long, lat, ref_long, ref_lat)

        assert pytest.approx(distance, 0.001) == expected_distance


class TestCentreOfWealthColumnsTransformer:

    @pytest.mark.parametrize("input_data, expected_output", [(
        pd.DataFrame({
            'lat': [47.62774, 47.61905, 47.63232],
            'long': [-122.24194, -122.34568, -122.23314]
        }),
        pd.DataFrame({
            'lat': [47.62774, 47.61905, 47.63232],
            'long': [-122.24194, -122.34568, -122.23314],
            'delta_lat': [0.0, 0.00869, 0.00458],
            'delta_long': [0.0, 0.10374, 0.0088],
            'center_distance': [0.0, 7.843488549024477, 0.8341924729390267]
        })
    )])

    def test_centre_of_wealth_columns_transformer(self, input_data, expected_output):
        transformer = CentreOfWealthColumnsTransformer()

        transformed_X = transformer.transform(input_data)

        assert_frame_equal(transformed_X, expected_output)
