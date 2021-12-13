import poundland
from classes import Item
from config import MAX_RESULT
from logger import logger
import tesco
import sains


def item_sort(elem: Item):
    return elem.price


def get_item_list(keyword: str):
    logger.info(f"Querying {keyword} item list")
    items = []
    t = tesco.query(keyword)
    if t:
        items += t
    t = sains.query(keyword)
    if t:
        items += t
    t = poundland.query(keyword)
    if t:
        items += t
    logger.info(f"All queries completed, total result: {len(items)}")
    items.sort(key=item_sort)
    logger.info("Sort completed")

    return items[:MAX_RESULT]


if __name__ == '__main__':
    kw = input("Input product name: ")
    items = get_item_list(kw)
    for item in items:
        print(item)
