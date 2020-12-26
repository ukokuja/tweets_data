import csv
import re

import numpy
import pandas

#INPUT
INPUT_FILE_NAME = "tweets.csv"
TIMESTAMP = 'timestamp'
TEXT = 'text'

#OUTPUT
OUTPUT_FILE_NAME = "tweet-data.csv"
MONTH = "Month"
HASHTAG = "Hashtag"
MENTION = "Mention"
WEBSITE = "Website"
OUTPUT_HEADERS = [MONTH, HASHTAG, MENTION, WEBSITE]

#CONFIGURATION
INVALID_HASHTAGS = ["#bitcoin", "#bitcoins", "#btc"]
ENCODING = 'utf-8'


class TweetsSummary:
    """
        Module that summarize tweets from a csv and output it to csv.
    """
    def __init__(self, input_file_name=INPUT_FILE_NAME, output_file_name=OUTPUT_FILE_NAME, delimiter=";"):
        self.__texts_by_months = {}
        self.__max_by_months = []
        self.__input_file_name = input_file_name
        self.__output_file_name = output_file_name
        self.__delimiter = delimiter

    def compute_input(self):
        """
        The method creates a dictionary that computes every valid apparitions of hashtags,
         mentions and websites per month
        :return:
        """
        with open(self.__input_file_name, 'r', encoding=ENCODING) as file:
            csv_dict = csv.DictReader(file, delimiter=self.__delimiter)
            for row in csv_dict:
                month = row[TIMESTAMP][:7]
                self.__init_month(month)
                text = row[TEXT]
                self.__find_items(month, text, pattern=r"#[\w\d_-]+", data_type=HASHTAG,
                                  ignore_values=INVALID_HASHTAGS)
                self.__find_items(month, text, pattern=r"@[\w\d_-]+", data_type=MENTION)
                self.__find_items(month, text,
                                  pattern=r"(http|https)://(?P<Website>[\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
                                  data_type=WEBSITE, match_group=WEBSITE)

    def summarize_input(self):
        """
        The method creates a dictionary that summarize the previously computed dictionary
         indicating the most common value per month and category
        """
        sorted_items = sorted(self.__texts_by_months.items())
        for month, value in sorted_items:
            max_website = self.__get_max_by_key(value[WEBSITE])
            max_hashtag = self.__get_max_by_key(value[HASHTAG])
            max_mention = self.__get_max_by_key(value[MENTION])
            self.__max_by_months.append(
                {MONTH: month, HASHTAG: max_hashtag, MENTION: max_mention, WEBSITE: max_website})

    def output_summary(self):
        """
        The method outputs the previusly created summarized dictionary together with the headers
        :return:
        """
        with open(self.__output_file_name, 'w', newline='', encoding=ENCODING) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_HEADERS)
            writer.writeheader()
            for value in self.__max_by_months:
                writer.writerow(value)

    @staticmethod
    def __get_max_by_key(values_list):
        """
        The function returns the most common item in the list or 'None' if the list is empty
        :param values_list: list with string items
        :return: The most common item in list or 'None' if the list is empty
        """
        if values_list:
            return pandas.Series.mode(numpy.array(values_list)).iloc[0]
        return "None"

    def __init_month(self, month):
        """
        The function sets an empty dictionary with the categories in the computed dictionary, in the specified month,
        if the month was never initialized
        :param month: The month to initialize
        :return:
        """
        if month not in self.__texts_by_months:
            self.__texts_by_months[month] = self.__get_empty_dict()

    @staticmethod
    def __get_empty_dict():
        """
        :return: The function returns an empty dictionary with the categories
        """
        return {HASHTAG: {}, MENTION: {}, WEBSITE: {}}

    def __find_items(self, month, text, pattern, data_type, ignore_values=None, match_group=0):
        """
        The function searchs for a pattern in the given text and set it to the computed
         dictionary, if it's not an ignored value.
        :param month: input text month
        :param text: input text
        :param pattern: pattern to search
        :param data_type: one of the three categories (hashtag, mention, website)
        :param ignore_values: Values to ignore
        :param match_group: pattern group to match
        :return:
        """
        items = re.finditer(pattern, text)
        for item in items:
            item_text = item.group(match_group)
            if not ignore_values or item_text.lower() not in ignore_values:
                self.__start_item_count(data_type, month)
                self.__texts_by_months[month][data_type].append(item_text)

    def __start_item_count(self, data_type, month):
        """
        The function initialize a list on the indicated month and data_type if it does not exists
        :param data_type: one of the three categories (hashtag, mention, website)
        :param month: input text month
        :return:
        """
        if not self.__texts_by_months[month][data_type]:
            self.__texts_by_months[month][data_type] = []


if __name__ == '__main__':

    ts = TweetsSummary()
    ts.compute_input()
    ts.summarize_input()
    ts.output_summary()