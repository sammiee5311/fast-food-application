import os

from dotenv import load_dotenv

ENV_PATH = os.path.join("config", ".env")


def load_env():
    load_dotenv(dotenv_path=ENV_PATH)
