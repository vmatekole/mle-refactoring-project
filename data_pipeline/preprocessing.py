import pandas as pd
from data_cleaning_transformers import (DropExtraneousColumnsTransformer,
                                        LastKnownChangeColumnTransformer,
                                        SqftColumnTransformer,
                                        ViewColumnTransformer,
                                        WaterFrontColumnTransformer)
from feature_enginneering_tranformers import (CentreOfWealthColumnsTransformer,
                                              SqFtPriceColumnTransformer,
                                              WaterDistanceColumnTransformer)
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


class PreprocessingSeattleHousing:

    def __init__(self):

        # Data cleaning Pipeline
        self.data_cleaning_pipeline = Pipeline(steps=[
            ('view', ViewColumnTransformer()),
            ('sqft_basement', SqftColumnTransformer()),
            ('waterfront', WaterFrontColumnTransformer()),
            ('last_known_change', LastKnownChangeColumnTransformer()),
            ('drop_extraneous_columns', DropExtraneousColumnsTransformer())
        ])
        # Feature Engineering
        self.feature_enginneering = Pipeline(steps=[
            ('sqft_price', SqFtPriceColumnTransformer()),
            ('center_of_wealth', CentreOfWealthColumnsTransformer()),
            ('water_distance', WaterDistanceColumnTransformer())
        ])

        self.preprocessor_pipe = Pipeline(steps=[
            ('data_cleaning', self.data_cleaning_pipeline),
            ('feature_enginneering', self.feature_enginneering)
        ])

    def preprocess_fit_transform(self, df):
        return self.preprocessor_pipe.fit_transform(df)

    def preprocess_transform(self, df):
        return self.preprocessor_pipe.transform(df)


def train(dataset):
    drop_lst = ['price', 'sqft_price', 'date', 'delta_lat', 'delta_long',]
    # we would like to consider all variables except the ones mentioned above
    all_features = [x for x in dataset.columns if x not in drop_lst]
    # X contains all descriptive variables defined above
    X = dataset[all_features]
    # we define y (our dependent variable): we take the price
    y = dataset['price']
    # We separate our data into train and test data. In the process, 30 % of the data is used for the subsequent testing of the prognostic quality.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

    # we can look at how much data is in each dataset
    print("X_train (features for the model to learn from): ", X_train.shape)
    print("y_train (labels for the model to learn from): ", y_train.shape)
    print("X_test (features to test the model's accuracy against): ", X_test.shape)
    print("y_test (labels to test the model's accuracy with): ", y_test.shape)
    # If we look at the first 5 lines of our training data, we see that the index is no longer sorted, it has been shuffled.
    X_train.head()


def drop_row(row_num, df_dataset):
    df_dataset.drop(row_num, axis=0, inplace=True)


def load_data(file_path):
    # Loading of the dataset via pandas
    df_dataset = pd.read_csv(file_path)
    return df_dataset


def main():
    RAW_DATASET = "./data/King_County_House_prices_dataset.csv"

    df_dataset = load_data(RAW_DATASET)
    drop_row(15856, df_dataset)

    pipeline = PreprocessingSeattleHousing()
    dataset = pipeline.preprocess_fit_transform(df_dataset)
    train(dataset)


if __name__ == "__main__":
    main()
