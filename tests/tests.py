from unittest import TestCase

import pandas as pd
from mock import patch
from pandas._testing import assert_frame_equal

from report_generator import ReportGenerator

class TestReportGenerator(TestCase):
    def setUp(self):
        self.sample_config = [
            ("record_code", 1, 3),
            ("client_type", 4, 7),
            ("client_number", 8, 11),
            ("account_number", 12, 15),
        ]

    def teardown(self):
        pass

    def test_get_colspecs_success(self):
        actual = ReportGenerator.get_colspecs(self.sample_config)
        expected = [(0, 3), (3, 7), (7, 11), (11, 15)]
        assert actual == expected

    def test_get_colnames_success(self):
        actual = ReportGenerator.get_colnames(self.sample_config)
        expected = ["record_code", "client_type", "client_number", "account_number"]
        assert actual == expected

    def test_get_colspecs_emptylist(self):
        config = []
        actual = ReportGenerator.get_colspecs(config)
        expected = []
        assert actual == expected

    def test_get_colnames_emptylist(self):
        config = []
        actual = ReportGenerator.get_colnames(config)
        expected = []
        assert actual == expected

    def test_get_colspecs_one_key_missing_expect_AssertionError(self):
        config = [("record_code"), ("client_type", 4, 7), ("client_number", 8, 11), ("account_number", 12, 15)]
        with self.assertRaises(AssertionError):
            ReportGenerator.get_colspecs(config)

    def test_get_colnames_one_key_missing_expect_AssertionError(self):
        config = [("record_code"), ("client_type", 4, 7), ("client_number", 8, 11), ("account_number", 12, 15)]
        with self.assertRaises(AssertionError):
            ReportGenerator.get_colnames(config)

    def test_constructor_file_missing_expect_FileNotFoundError(self):
        with self.assertRaises(FileNotFoundError):
            ReportGenerator("a_none_existing_filename", "", self.sample_config)

    def test_generate_summary_report_success(self):
        input_columns = "client_type,client_number,account_number,subaccount_number,exchange_code,product_group_code,symbol,transaction_date,quantity_long,quantity_short".split(",")
        input_row = ['CL', 4321, 2, 1, 'SGX', 'FU', 'NK', '20100820', 1, 0]

        # Expected dataframe
        exp_columns = "client_type,client_number,account_number,subaccount_number,exchange_code,product_group_code,symbol,transaction_date,total_transaction_amount".split(",")
        exp_row = ['CL', 4321, 2, 1, 'SGX', 'FU', 'NK', '20100820', 1]

        # The __init__ can be mocked
        with patch.object(ReportGenerator, "__init__", lambda x: None):
            rg = ReportGenerator()
            rg.input_df = pd.DataFrame([input_row, ], columns=input_columns)
            rg.summary_report()
            expected_df = pd.DataFrame([exp_row, ], columns=exp_columns)
            assert_frame_equal(expected_df, rg.output_df)
