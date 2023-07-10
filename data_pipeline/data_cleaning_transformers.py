import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# Data cleaning transformers


class SqftColumnTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        X['sqft_basement'] = X['sqft_basement'].replace('?', np.NaN)
        # And we change the dtype of the column "sqft_basement" to float
        X['sqft_basement'] = X['sqft_basement'].astype(float)
        X.eval('sqft_basement = sqft_living - sqft_above', inplace=True)
        return X


class ViewColumnTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        # We replace Nan values in "view" with the most frequent expression (0)
        X['view'].fillna(0, inplace=True)
        return X


class WaterFrontColumnTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        # We replace Nan values in "waterfront" with the most frequent expression (0)
        X.waterfront.fillna(0, inplace=True)
        return X


class LastKnownChangeColumnTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        # We will create an empty list in which we will store values
        last_known_change = []

        # For each row in our data frame, we look at what is in the column "yr_renovated".
        for idx, yr_re in X.yr_renovated.items():
            # if "yr_renovated" is 0 or contains no value, we store the year of construction of the house in our empty listes ab
            if str(yr_re) == 'nan' or yr_re == 0.0:
                last_known_change.append(X.yr_built[idx])
            # if there is a value other than 0 in the column "yr_renovated", we transfer this value into our new list
            else:
                last_known_change.append(int(yr_re))
        # We create a new column and take over the values of our previously created list
        X['last_known_change'] = last_known_change

        return X


class DropExtraneousColumnsTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        # We delete the "yr_renovated" and "yr_built" columns
        X.drop("yr_renovated", axis=1, inplace=True)
        X.drop("yr_built", axis=1, inplace=True)
        return X
