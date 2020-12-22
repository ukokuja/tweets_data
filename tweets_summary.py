import csv
import itertools
import re

import pandas as pd
import numpy as np
INPUT_FILE_NAME = "/Users/lucaskujawski/Projects/personal/tweets.csv"
OUTPUT_FILE_NAME = "tweet-data.csv"

MONTH = "Month"
HASHTAG = "Hashtag"
MENTION = "Mention"
WEBSITE = "Website"
TIMESTAMP = 'timestamp'
TEXT = 'text'
OUTPUT_HEADERS = [MONTH, HASHTAG, MENTION, WEBSITE]
DATA_EMPTY_DICT = {HASHTAG: ["None"], MENTION: ["None"], WEBSITE: ["None"]}
INVALID_HASHTAGS = ["#bitcoin", "#bitcoins", "#btc"]
ENCODING='utf-8'

class TweetsSummary:

    def __init__(self):
        self.texts_by_months = {}
        self.max_by_months = []
        start = time.time()
        self.compute_input()
        end = time.time()
        print("compute_input: {}".format(end - start))
        start = time.time()
        self.summarize_input()
        end = time.time()
        print("summarize_input: {}".format(end - start))
        start = time.time()
        self.output_summary()
        end = time.time()
        print("output_summary: {}".format(end - start))

    def compute_input(self):
        with open(INPUT_FILE_NAME, 'r', encoding=ENCODING) as file:
            csv_dict = csv.DictReader(file, delimiter=";")
            # csv_dict = itertools.islice(csv.DictReader(file, delimiter=";"), 1000*100)
            for row in csv_dict:
                month = row[TIMESTAMP][:7]
                self.init_month(month)
                self.find_items(month, row, pattern=r"#(\w+)", data_type=HASHTAG, ignore_values=INVALID_HASHTAGS)
                self.find_items(month, row, pattern=r"@(\w+)", data_type=MENTION)
                self.find_items(month, row,
                                pattern=r"(http|https)://(?P<website>[\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
                                data_type=WEBSITE, match_group='website')


    def summarize_input(self):
        sorted_items = sorted(self.texts_by_months.items())
        for month, value in sorted_items:
            max_website = self.get_max_by_key(WEBSITE, value)
            max_hashtag = self.get_max_by_key(HASHTAG, value)
            max_mention = self.get_max_by_key(MENTION, value)
            self.max_by_months.append({MONTH:month, HASHTAG: max_hashtag, MENTION: max_mention, WEBSITE: max_website})

    def get_max_by_key(self, metric, value):
        max_key = pd.Series.mode(value[metric])
        return max_key[0]

    def output_summary(self):
        with open(OUTPUT_FILE_NAME, 'w', newline='', encoding=ENCODING) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_HEADERS)

            writer.writeheader()
            for value in self.max_by_months:
                writer.writerow(value)

    def init_month(self, month):
        if month not in self.texts_by_months:
            self.texts_by_months[month] = DATA_EMPTY_DICT

    def find_items(self, month, row, pattern, data_type, ignore_values=None, match_group=0):
        items = re.finditer(pattern, row[TEXT])
        for item in items:
            item_text = item.group(match_group)
            if not ignore_values or item_text.lower() not in ignore_values:
                self.texts_by_months[month][data_type].append(item_text)

if __name__ == '__main__':
    import time

    start = time.time()
    ts = TweetsSummary()
    end = time.time()
    print(end - start)
