import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# Feature engineering transformers


class SqFtPriceColumnTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None) -> pd.DataFrame:
        # We create a new variable that gives us the price per square foot of living space
        X['sqft_price'] = (X.price/(X.sqft_living + X.sqft_lot)).round(2)
        return X


class CentreOfWealthColumnsTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None) -> pd.DataFrame:
        CENTRE_LATITUDE: np.float64 = 47.62774
        CENTRE_LONGITUDE: np.float64 = -122.24194
        RADIANS: np.float64 = 47.6219

        # Absolute difference of latitude between centre and property
        X['delta_lat'] = np.absolute(CENTRE_LATITUDE - X['lat'])
        # Absolute difference of longitude between centre and property
        X['delta_long'] = np.absolute(CENTRE_LONGITUDE - X['long'])
        # Distance between centre and property
        X['center_distance'] = pow((pow((X['delta_long'] * np.cos(np.radians(RADIANS))), 2)
                                    + pow(X['delta_lat'], 2)), 0.5) * 2 * np.pi * WaterDistanceColumnTransformer.NORMALISE_EARTH_CIRCUM
        return X


class WaterDistanceColumnTransformer(BaseEstimator, TransformerMixin):

    NORMALISE_EARTH_CIRCUM: np.float64 = 6378/360

    def fit(self, X, y=None):
        return self

    # This function helps us to calculate the distance between the house overlooking the seafront and the other houses.
    def dist(self, long: np.float64, lat: np.float64, ref_long: np.float64, ref_lat: np.float64) -> np.float64:
        '''dist computes the distance in km to a reference location. Input: long and lat of
        the location of interest and ref_long and ref_lat as the long and lat of the reference location'''
        delta_long = long - ref_long
        delta_lat = lat - ref_lat
        delta_long_corr = delta_long * np.cos(np.radians(ref_lat))
        result = pow((pow(delta_long_corr, 2) + pow(delta_lat, 2)), 0.5) * \
            2 * np.pi * WaterDistanceColumnTransformer.NORMALISE_EARTH_CIRCUM
        return result

    def transform(self, X, y=None) -> pd.DataFrame:
        water_distance = []
        water_list = X.query('waterfront == 1')

        # For each row in our data frame we now calculate the distance to the seafront
        for idx, lat in X.lat.items():
            ref_list = []
            for x, y in zip(list(water_list.long), list(water_list.lat)):
                ref_list.append(self.dist(X.long[idx], X.lat[idx], x, y).min())
            water_distance.append(min(ref_list))
        # wir erstellen eine neue Spalte und übernehmen die Werte unserer vorher erstellten Liste
        X['water_distance'] = water_distance
        return X
