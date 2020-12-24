import csv
import re

INPUT_FILE_NAME = "/Users/lucaskujawski/Projects/personal/tweets.csv"
from datetime import datetime

# INPUT_FILE_NAME = "tweets.csv"
OUTPUT_FILE_NAME = "tweet-data.csv"

MONTH = "Month"
HASHTAG = "Hashtag"
MENTION = "Mention"
WEBSITE = "Website"
TIMESTAMP = 'timestamp'
TEXT = 'text'
OUTPUT_HEADERS = [MONTH, HASHTAG, MENTION, WEBSITE]
INVALID_HASHTAGS = ["#bitcoin", "#bitcoins", "#btc"]
ENCODING = 'utf-8'


class TweetsSummary:
    def __init__(self, input_file_name=INPUT_FILE_NAME, output_file_name=OUTPUT_FILE_NAME, delimiter=";",
                 date_format="%Y-%m-%d %H:%M:%S+00"):
        self.__texts_by_months = {}
        self.__max_by_months = []
        self.__input_file_name = input_file_name
        self.__output_file_name = output_file_name
        self.__delimiter = delimiter
        self.__date_format = date_format

    def compute_input(self):
        with open(self.__input_file_name, 'r', encoding=ENCODING) as file:
            csv_dict = csv.DictReader(file, delimiter=self.__delimiter)
            for row in csv_dict:
                # month = self.__get_month(row[TIMESTAMP])
                month = row[TIMESTAMP][:7]
                self.__init_month(month)
                text = row[TEXT]
                self.__find_items(month, text, pattern=r"(\s|^)+(#[\w\d_-]+)+", data_type=HASHTAG,
                                  ignore_values=INVALID_HASHTAGS)
                self.__find_items(month, text, pattern=r"(\s|^)+(@[\w\d_-]+)+", data_type=MENTION)
                self.__find_items(month, text,
                                  pattern=r"(http|https)://(?P<Website>[\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
                                  data_type=WEBSITE, match_group=WEBSITE)

    def __get_month(self, timestamp):
        parsed_date = datetime.strptime(timestamp, self.__date_format)
        return parsed_date.strftime("%Y-%m")

    def summarize_input(self):
        sorted_items = sorted(self.__texts_by_months.items())
        for month, value in sorted_items:
            max_website = self.__get_max_by_key(WEBSITE, value)
            max_hashtag = self.__get_max_by_key(HASHTAG, value)
            max_mention = self.__get_max_by_key(MENTION, value)
            self.__max_by_months.append(
                {MONTH: month, HASHTAG: max_hashtag, MENTION: max_mention, WEBSITE: max_website})

    def output_summary(self):
        with open(self.__output_file_name, 'w', newline='', encoding=ENCODING) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_HEADERS)
            writer.writeheader()
            for value in self.__max_by_months:
                writer.writerow(value)

    @staticmethod
    def __get_max_by_key(metric, value):
        if value[metric]:
            max_value = max(value[metric].values())  # maximum value
            max_keys = sorted([k for k, v in value[metric].items() if v == max_value])
            max_key = max_keys[0]
            return max_key
        return "None"

    def __init_month(self, month):
        if month not in self.__texts_by_months:
            self.__texts_by_months[month] = self.__get_empty_dict()

    @staticmethod
    def __get_empty_dict():
        return {HASHTAG: {}, MENTION: {}, WEBSITE: {}}

    def __find_items(self, month, text, pattern, data_type, ignore_values=None, match_group=2):
        items = re.finditer(pattern, text)
        for item in items:
            item_text = item.group(match_group)
            if not ignore_values or item_text.lower() not in ignore_values:
                self.__start_item_count(data_type, item_text, month)
                self.__texts_by_months[month][data_type][item_text] += 1

    def __start_item_count(self, data_type, item_text, month):
        if item_text not in self.__texts_by_months[month][data_type]:
            self.__texts_by_months[month][data_type][item_text] = 0


if __name__ == '__main__':
    # import time

    # start = time.time()
    ts = TweetsSummary()
    ts.compute_input()
    ts.summarize_input()
    ts.output_summary()
    # end = time.time()
    # print(end - start)

#TODO: Add readme
#TODO: Add documentation