import csv
import itertools
import re

INPUT_FILE_NAME = "/Users/lucaskujawski/Projects/personal/tweets.csv"
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
    def __init__(self, input_file_name=INPUT_FILE_NAME, output_file_name=OUTPUT_FILE_NAME):
        self.__texts_by_months = {}
        self.__max_by_months = []
        self.compute_input(input_file_name)
        self.summarize_input()
        self.output_summary(output_file_name)

    def compute_input(self, input_file_name):
        with open(input_file_name, 'r', encoding=ENCODING) as file:
            csv_dict = csv.DictReader(file, delimiter=";")
            # csv_dict = itertools.islice(csv.DictReader(file, delimiter=";"), 1000*100)
            for row in csv_dict:
                month = row[TIMESTAMP][:7]
                self.__init_month(month)
                text = row[TEXT]
                self.__find_items(month, text, pattern=r"#(\w+)", data_type=HASHTAG, ignore_values=INVALID_HASHTAGS)
                self.__find_items(month, text, pattern=r"@(\w+)", data_type=MENTION)
                self.__find_items(month, text,
                                  pattern=r"(http|https)://(?P<website>[\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
                                  data_type=WEBSITE, match_group='website')

    def summarize_input(self):
        sorted_items = sorted(self.__texts_by_months.items())
        for month, value in sorted_items:
            max_website = self.__get_max_by_key(WEBSITE, value)
            max_hashtag = self.__get_max_by_key(HASHTAG, value)
            max_mention = self.__get_max_by_key(MENTION, value)
            self.__max_by_months.append({MONTH: month, HASHTAG: max_hashtag, MENTION: max_mention, WEBSITE: max_website})

    def output_summary(self, output_file_name):
        with open(output_file_name, 'w', newline='', encoding=ENCODING) as csvfile:
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

    def __find_items(self, month, text, pattern, data_type, ignore_values=None, match_group=0):
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
    import time

    start = time.time()
    ts = TweetsSummary()
    end = time.time()
    print(end - start)
