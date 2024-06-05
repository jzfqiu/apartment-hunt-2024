import time
from common import Apartment
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from datetime import date, datetime
import re
from selenium.webdriver.support.wait import WebDriverWait


def _remove_non_numeric(text):
    text = text.replace("PH ", "")
    match = re.match(r"^\d+", text)
    return match.group(0) if match else ""


def _parse_date(date_str) -> str:
    if date_str == "Available Now":
        return date.today().isoformat()
    date_part = re.search(r"\b([a-zA-Z]+ \d+)(st|nd|rd|th)", date_str)
    if not date_part:
        raise RuntimeError(f"Cannot extract date from {date_str}")
    date_without_suffix = re.sub(r"(st|nd|rd|th)", "", date_part.group(1))

    date_object = datetime.strptime(date_without_suffix + " " + "2024", "%b %d %Y")
    return date_object.date().isoformat()


def get_montaje_apts(driver: Chrome) -> list[Apartment]:
    url = "https://livemontaje.com/floorplans/"

    driver.get(url)

    iframe = driver.find_element(By.ID, "embed-frame")

    wait = WebDriverWait(driver, timeout=10)
    wait.until(lambda d: iframe.is_displayed())

    time.sleep(2)

    driver.switch_to.frame(iframe)

    apts = []
    for floor in range(1, 19):
        floor_button = driver.find_element(By.ID, f"floor-item-{floor}")
        floor_button.click()
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if "list-item-" not in button.get_attribute("id"):
                continue
            apt_num_raw, layout_raw, price_raw, available_raw = button.text.splitlines()
            if "Studio" in layout_raw:
                layout = "Studio"
            elif "1 Bed" in layout_raw:
                layout = "1 Bed"
            elif "2 Bed" in layout_raw:
                layout = "2 Bed"
            else:
                layout = ">2 Bed"
            apt = Apartment(
                apt_name="Montaje",
                apt_num=_remove_non_numeric(apt_num_raw),
                layout=layout,
                price=int(price_raw.replace("$", "").replace(",", "")),
                available=_parse_date(available_raw),
            )
            apts.append(apt)
    return apts
