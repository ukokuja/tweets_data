import unittest
import pandas as pd

from ex_2.tweets_summary import TweetsSummary


class TestTweetsSummary(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ts = None

    def get_case_outputs(self, case):
        self.ts = TweetsSummary(input_file_name="test_{}/input.csv".format(case),
                           output_file_name="test_{}/real_output.csv".format(case))
        self.ts.compute_input()
        self.ts.summarize_input()
        self.ts.output_summary()
        expected_output = pd.read_csv("test_{}/expected_output.csv".format(case), delimiter=",")
        real_output = pd.read_csv("test_{}/real_output.csv".format(case), delimiter=",")
        return expected_output, real_output


    def test_mention_none(self):
        expected_output, real_output = self.get_case_outputs(case=1)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_website_none(self):
        expected_output, real_output = self.get_case_outputs(case=2)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_hashtag_none(self):
        expected_output, real_output = self.get_case_outputs(case=3)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_complex_mention(self):
        expected_output, real_output = self.get_case_outputs(case=4)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_complex_hashtag(self):
        expected_output, real_output = self.get_case_outputs(case=5)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_composed_mention(self):
        expected_output, real_output = self.get_case_outputs(case=6)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_composed_hashtag(self):
        expected_output, real_output = self.get_case_outputs(case=7)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_complex_url(self):
        expected_output, real_output = self.get_case_outputs(case=8)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_hebrew_encoded_url(self):
        expected_output, real_output = self.get_case_outputs(case=9)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_hebrew_decoded_url(self):
        expected_output, real_output = self.get_case_outputs(case=10)
        pd.testing.assert_frame_equal(real_output, expected_output)

    def test_multiple_months(self):
        pass
    def test_timing_5k_rows(self):
        pass
    def test_timing_50k_rows(self):
        pass
    def test_timing_500k_rows(self):
        pass
    def test_timing_4M_rows(self):
        pass