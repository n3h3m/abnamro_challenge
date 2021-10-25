from unittest import TestCase

from abn_amro.report_generator import ReportGenerator


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

    def test_get_names_success(self):
        actual = ReportGenerator.get_names(self.sample_config)
        expected = ["record_code", "client_type", "client_number", "account_number"]
        assert actual == expected

    def test_get_colspecs_emptylist(self):
        config = []
        actual = ReportGenerator.get_colspecs(config)
        expected = []
        assert actual == expected

    def test_get_names_emptylist(self):
        config = []
        actual = ReportGenerator.get_names(config)
        expected = []
        assert actual == expected

    def test_get_colspecs_one_key_missing_expect_AssertionError(self):
        config = [("record_code"), ("client_type", 4, 7), ("client_number", 8, 11), ("account_number", 12, 15)]
        with self.assertRaises(AssertionError):
            ReportGenerator.get_colspecs(config)

    def test_get_names_one_key_missing_expect_AssertionError(self):
        config = [("record_code"), ("client_type", 4, 7), ("client_number", 8, 11), ("account_number", 12, 15)]
        with self.assertRaises(AssertionError):
            ReportGenerator.get_names(config)

    def test_constructor_file_missing_expect_FileNotFoundError(self):
        with self.assertRaises(FileNotFoundError):
            ReportGenerator("a_none_existing_filename", "", self.sample_config)
