import re
from typing import List

import simplejson

import client
from classes import Item, UnitPrice
from config import MAX_RESULT
from logger import logger


def query(kw: str, max_res: int = MAX_RESULT) -> List[Item]:
    logger.debug(f"Querying {kw} in waitrose")
    p_j = {"customerSearchRequest": {
        "queryParams": {
            "size": max_res,
            "searchTerm": kw,
            "sortBy": "RELEVANCE",
            "searchTags": [],
            "filterTags": [],
            "orderId": "0",
            "categoryLevel": 1
        }
    }
    }
    ret = client.post("https://www.waitrose.com/api/content-prod/v2/cms"
                      "/publish/productcontent/search/-1?clientType=WEB_APP",
                      j=p_j, headers={"authorization": "Bearer unauthenticated"})
    try:
        j = ret.json()
    except simplejson.JSONDecodeError:
        logger.error("Unable to solve json in waitrose")
        logger.error(ret.text)
        return []

    res = []
    for product in j["componentsAndProducts"]:
        if "searchProduct" not in product:
            continue
        try:
            detail = product["searchProduct"]
            item = Item()
            item.name = detail["name"]
            item.image_url = detail["thumbnail"]
            item.url = "https://www.waitrose.com/ecom/products/" + re.sub(r"\W+", "-", item.name.lower()) + "/" + \
                       detail["id"]
            c_unit_price = detail["currentSaleUnitPrice"]
            item.price = float(c_unit_price["price"]["amount"])
            item.unit_price = UnitPrice(item.price, c_unit_price["quantity"]["uom"],
                                        c_unit_price["quantity"]["amount"])

            item.rating = detail["reviews"]["averageRating"]
            item.store = "waitrose"
            res.append(item)
        except KeyError as e:
            logger.warning("Unable to solve following product")
            logger.warning(e)
            logger.warning(product)
    logger.debug(f"Waitrose completed, total {len(res)}")
    return res


if __name__ == '__main__':
    for i in query("chicken", 100):
        print(i)
