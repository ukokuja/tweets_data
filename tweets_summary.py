import csv
import itertools
import re

INPUT_FILE_NAME = "/Users/lucaskujawski/Projects/personal/tweets.csv"
OUTPUT_FILE_NAME = "tweet-data.csv"

MONTH = "Month"
HASHTAG = "Hashtag"
MENTION = "Mention"
WEBSITE = "Website"
TIMESTAMP = 'timestamp'
TEXT = 'text'
OUTPUT_HEADERS = [MONTH, HASHTAG, MENTION, WEBSITE]
DATA_EMPTY_DICT = {HASHTAG: {}, MENTION: {}, WEBSITE: {}}
INVALID_HASHTAGS = ["#bitcoin", "#bitcoins", "#btc"]


class TweetsSummary:

    def __init__(self):
        self.texts_by_months = {}
        self.max_by_months = []
        self.compute_input()
        self.summarize_input()
        self.output_summary()

    def compute_input(self):
        with open(INPUT_FILE_NAME, 'r') as file:
            csv_dict = csv.DictReader(file, delimiter=";")
            # csv_dict = itertools.islice(csv.DictReader(file, delimiter=";"), 10000*10000)
            for row in csv_dict:
                month = row[TIMESTAMP][:7]
                self.init_month(month)
                self.find_items(month, row, pattern=r"#(\w+)", data_type=HASHTAG, ignore_values=INVALID_HASHTAGS)
                self.find_items(month, row, pattern=r"@(\w+)", data_type=MENTION)
                self.find_items(month, row,
                                pattern=r"(http|https)://(?P<website>[\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
                                data_type=WEBSITE, match_group='website')


    def summarize_input(self):
        for month, value in self.texts_by_months.items():
            max_website = self.get_max_by_key(WEBSITE, value)
            max_hashtag = self.get_max_by_key(HASHTAG, value)
            max_mention = self.get_max_by_key(MENTION, value)
            self.max_by_months.append({MONTH:month, HASHTAG: max_hashtag, MENTION: max_mention, WEBSITE: max_website})

    def get_max_by_key(self, metric, value):
        max_value = max(value[metric].values())  # maximum value
        max_keys = sorted([k for k, v in value[metric].items() if v == max_value])
        max_key = None if len(max_keys) < 1 else max_keys[0]
        return max_key

    def output_summary(self):
        with open(OUTPUT_FILE_NAME, 'w', newline='') as csvfile:
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
                self.start_item_count(data_type, item_text, month)
                self.texts_by_months[month][data_type][item_text] += 1

    def start_item_count(self, data_type, item_text, month):
        if item_text not in self.texts_by_months[month][data_type]:
            self.texts_by_months[month][data_type][item_text] = 0


if __name__ == '__main__':
    import time

    start = time.time()
    ts = TweetsSummary()
    end = time.time()
    print(end - start)
