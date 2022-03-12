import json
from typing import List

from kafka import KafkaConsumer

tweets: List[str] = []
likes: List[str] = []
time: List[str] = []
media: List[str] = []
tweet_cnt: int = 0


# if "extended_tweet" in data["retweeted_status"]:
#     text = data["retweeted_status"]["extended_tweet"].get("full_text", "")
#     media = (
#         data["retweeted_status"]["extended_tweet"]
#         .get("extended_entities", {"media": None})
#         .get("media", None)
#     )
#     if media:
#         media = media[-1].get("media_url", "")
# likes = data.get("favorite_count", "")
# time = data.get("created_at", "")

# if self.tweet_cnt % 10 == 0:
#     df = pd.DataFrame({"tweets": self.tweets, "likes": self.likes, "time": self.time, "media": self.media})
#     df.to_csv(
#         f"./at_{self.tweet_cnt}.csv",
#     )

# self.tweets.append(text)
# self.likes.append(likes)
# self.time.append(time)
# self.media.append(media)


if __name__ == "__main__":
    consumer = KafkaConsumer(
        "twitter",
        security_protocol="PLAINTEXT",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
    )

    print("Starting the comsumer")
    for msg in consumer:
        print(f"twitter: {json.loads(msg.value)}")
