"""Demo for using f451 Labs Uploader Module."""

import time
import sys
import asyncio
from pathlib import Path
from random import randint
import json

from f451_uploader.uploader import Uploader

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


# =========================================================
#                    D E M O   A P P
# =========================================================
def main():
    # Get app dir
    appDir = Path(__file__).parent

    # Initialize TOML parser and load 'settings.toml' file
    try:
        with open(appDir.joinpath("settings.toml"), mode="rb") as fp:
            config = tomllib.load(fp)
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        sys.exit("ERROR: Missing or invalid 'settings.toml' file")      

    iot = Uploader(config)
    feedName = 'TEST_FEED_' + str(time.time_ns())

    print("\n===== [Demo of f451 Labs Uploader Module] =====")
    print(f"Creating new Adafruit IO feed: {feedName}")
    feed = iot.aio_create_feed(feedName)

    dataPt = randint(1, 100)
    print(f"Uploading random value '{dataPt}' to Adafruit IO feed: {feed.key}")
    asyncio.run(iot.aio_send_data(feed.key, dataPt))

    print(f"Receiving latest from Adafruit IO feed: {feed.key}")
    data = asyncio.run(iot.aio_receive_data(feed.key, True))

    # Adafruit IO returns data in form of 'namedtuple' and we can 
    # use the '_asdict()' method to convert it to regular 'dict'.
    # We then pass the 'dict' to 'json.dumps()' to prettify before 
    # we print out the whole structure.
    pretty = json.dumps(data._asdict(), indent=4, sort_keys=True)
    print(pretty)

    print("=============== [End of Demo] =================\n")


if __name__ == "__main__":
    main()