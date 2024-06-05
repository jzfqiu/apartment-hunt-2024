from dataclasses import asdict
import json
import logging
import os
from selenium import webdriver

from common import Apartment
from montaje import get_montaje_apts
from telegram import send_message


logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)

if __name__ == "__main__":
    json_path = "apts.json"
    
    old_apts = []
    if os.path.exists(json_path):
        logging.info(f"Reading previous records from {json_path}...")
        with open(json_path) as f:
            old_apts = [Apartment(**d) for d in json.load(f)]
        logging.info(f"Read {len(old_apts)} records")
    else:
        logging.info(f"No previous record found at {json_path}")

    logging.info("Initiating driver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    logging.info("Driver initiated")
    
    new_apts: list[Apartment] = []
    logging.info("Getting Montaje apartments...")
    new_apts.extend(get_montaje_apts(driver))

    logging.info(f"Found {len(new_apts)} apartments. Sending messages...")
    for apt in new_apts:
        if apt not in old_apts and apt.meets_condition():
            send_message(str(apt))

    logging.info(f"Refreshing records at {json_path}")
    with open(json_path, "w") as f:
        json.dump([asdict(a) for a in new_apts], f, indent=4)
