from typing import List

import simplejson

import client
from datetime import datetime
from config import WARMUP_DURATION, MAX_QUERY
from logger import logger
from classes import Item, UnitPrice
import json

warmup_time = datetime.fromtimestamp(0)


@logger.catch
def query(keyword: str, max_res=MAX_QUERY) -> List[Item]:
    logger.debug(f"Querying {keyword} in sains")
    # global warmup_time
    # delta_time = datetime.now() - warmup_time
    # if delta_time.total_seconds() > WARMUP_DURATION:
    #     client.get("https://www.sainsburys.co.uk/")
    #     warmup_time = datetime.now()
    #     logger.info("Sains warmed up")

    params = {"filter[keyword]": keyword, "include[PRODUCT_AD]": "citrus", "page_number": 1, "page_size": max_res,
              "sort_order": "FAVOURITES_FIRST"}

    ret = client.get("https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product", params=params)
    try:
        r_json = ret.json()
    except simplejson.JSONDecodeError:
        logger.error(f"Unable to query {keyword} from sains")
        logger.error(ret.text)
        return []

    res = []
    # JSON parse
    for product in r_json["products"]:
        try:
            if product["product_type"] == "CATCHWEIGHT":
                product["unit_price"] = product["catchweight"][0]["unit_price"]
                product["retail_price"] = product["catchweight"][0]["retail_price"]
            item = Item()
            item.name = product["name"]
            item.image_url = product["image"]
            item.url = product["full_url"]
            item.unit_price = UnitPrice(product["unit_price"]["price"], product["unit_price"]["measure"],
                                        product["unit_price"]["measure_amount"])
            item.price = float(product["retail_price"]["price"])
            item.rating = product["reviews"]["average_rating"]
            item.store = "Sainsbury"

            res.append(item)
        except KeyError as e:
            logger.warning("Unable to solve the following product")
            logger.warning(e)
            logger.warning(json.dumps(product))
    logger.debug(f"Sains completed, total {len(res)}")
    return res


if __name__ == '__main__':
    res = query("semi")
    for r in res:
        print(r)
