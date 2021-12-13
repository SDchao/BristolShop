import html
import json
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

import client
from classes import Item, UnitPrice
from logger import logger
from config import WARMUP_DURATION

warmup_time = datetime.fromtimestamp(0)

@logger.catch
def query(keyword: str) -> List[Item]:
    logger.debug(f"Querying {keyword} in tesco")
    # global warmup_time
    # delta_time = datetime.now() - warmup_time
    # if delta_time.total_seconds() > WARMUP_DURATION:
    #     client.get("https://www.tesco.com/")
    #     warmup_time = datetime.now()
    #     logger.info("Tesco warmed up")

    ret = client.get("https://www.tesco.com/groceries/en-GB/search", params={"query": keyword})

    res = []

    soup = BeautifulSoup(ret.content, "html.parser")
    j = html.unescape(soup.body.get("data-redux-state"))
    try:
        j = json.loads(j)
        data = j["results"]["pages"][0]["serializedData"]

        for d in data:
            try:
                item = Item()
                product = d[1]["product"]

                item.name = product["title"]
                item.image_url = product["defaultImageUrl"]
                item.url = "https://www.tesco.com/groceries/en-GB/products/" + product["id"]
                item.unit_price = UnitPrice(product["unitPrice"], product["unitOfMeasure"])
                item.price = product["price"]
                item.store = "Tesco"
                res.append(item)
            except KeyError as e:
                logger.warning("Unable to solve the following product")
                logger.warning(e)
                logger.warning(json.dumps(d))

    except json.JSONDecodeError:
        logger.error("Unable to solve json")
        return []

    # old html parsing
    # wrappers = soup.find_all("div", class_="product-tile-wrapper", limit=30)

    # for wrapper in wrappers:
    #     price_form = wrapper.find("form")
    #     if price_form:
    #         item = Item()
    #
    #         details_wrapper = price_form.div.div
    #         price_wrapper = details_wrapper.find("div", class_="price-control-wrapper")
    #         item.price = float(price_wrapper.find_all("span", attrs={"data-auto": "price-value"})[0].string)
    #
    #         unit_price_wrapper = details_wrapper.find("div", class_="price-per-quantity-weight")
    #         unit_price = float(unit_price_wrapper.find_all("span", attrs={"data-auto": "price-value"})[0].string)
    #         measure = unit_price_wrapper.find("span", class_="weight").string[1:]  # Remove '/' ahead
    #         item.unit_price = UnitPrice(unit_price, measure)
    #
    #         detail = wrapper.find("div", class_="product-details--wrapper")
    #         title_a = detail.find("h3").a
    #
    #         item.name = title_a.string
    #         item.url = "https://www.tesco.com" + title_a.get("href")
    #         item.store = "tesco"
    #         res.append(item)
    logger.debug(f"Tesco completed, total {len(res)}")
    return res


if __name__ == '__main__':
    res = query("milk")
    for r in res:
        print(r)
