from dataclasses import asdict
import json
import os
from selenium import webdriver

from common import Apartment
from montaje import get_montaje_apts
from telegram import send_message



if __name__ == "__main__":
    json_path = "apts.json"
    
    old_apts = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            old_apts = [Apartment(**d) for d in json.load(f)]
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    
    new_apts: list[Apartment] = []
    new_apts.extend(get_montaje_apts(driver))

    for apt in new_apts:
        if apt not in old_apts and apt.meets_condition():
            send_message(str(apt))

    with open(json_path, "w") as f:
        json.dump([asdict(a) for a in new_apts], f, indent=4)
