import poundland
import waitrose
from classes import Item
from config import MAX_RESULT
from logger import logger
import tesco
import sains


def item_sort(elem: Item):
    return elem.price


def get_item_list(keyword: str, max_res: int = MAX_RESULT, en_tesco=True, en_sains=True, en_poundland=True,
                  en_waitrose=True):
    logger.info(f"Querying {keyword} item list")
    items = []
    if en_tesco:
        t = tesco.query(keyword)
        if t:
            items += t

    if en_sains:
        t = sains.query(keyword, max_res)
        if t:
            items += t

    if en_poundland:
        t = poundland.query(keyword)
        if t:
            items += t

    if en_waitrose:
        t = waitrose.query(keyword)
        if t:
            items += t
    logger.info(f"All queries completed, total result: {len(items)}")
    items.sort(key=item_sort)
    logger.info("Sort completed")

    return items[:max_res]


if __name__ == '__main__':
    kw = input("Input product name: ")
    items = get_item_list(kw, 100)
    for item in items:
        print(item)
