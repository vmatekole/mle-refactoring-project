from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from fixtures import house_expected_output_file_path, house_input_file_path
from pandas.testing import assert_frame_equal
from preprocessing import PreprocessingSeattleHousing, load_data


class TestPreprocessingSeattleHousing:

    def test_preprocess_fit_transform(self, house_input_file_path, house_expected_output_file_path):
        preprocessor = PreprocessingSeattleHousing()

        input_data = load_data(house_input_file_path)
        expected_results_data = load_data(house_expected_output_file_path)

        transformed_X = preprocessor.preprocess_fit_transform(input_data)

        assert_frame_equal(transformed_X, expected_results_data)
