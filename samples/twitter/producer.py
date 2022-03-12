import json
import os
from time import sleep

from dotenv import load_dotenv
from kafka import KafkaProducer
from tweepy import OAuthHandler
from tweepy.streaming import Stream

ENV_PATH = ".env"
load_dotenv(dotenv_path=ENV_PATH)

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


producer = KafkaProducer(
    security_protocol="PLAINTEXT",
    bootstrap_servers=["localhost:9092"],
    value_serializer=json_serializer,
)


class KafkaStream(Stream):
    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True

    def process_data(self, raw_data):
        data = json.loads(raw_data)

        try:
            producer.send("twitter", data)
        except KeyError as e:
            print(e)
            return False
        sleep(2)

    def on_connection_error(self):
        self.disconnect()

    def on_request_error(self, status_code):
        if status_code == 420:
            return False


if __name__ == "__main__":
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = KafkaStream(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, max_retries=50)

    input_keyword = input("Type keywords. ex) python, django : ")
    keyword_list = input_keyword if "," not in input_keyword else input_keyword.split(",")

    stream.filter(track=keyword_list, languages=["en"])
