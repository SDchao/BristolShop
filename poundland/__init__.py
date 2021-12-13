import client
from classes import Item
from logger import logger
from bs4 import BeautifulSoup


@logger.catch()
def query(keyword: str):
    logger.debug(f"Querying {keyword} in poundland")
    ret = client.get("https://www.poundland.co.uk/catalogsearch/result/",
                     params={"q": keyword, "product_list_limit": 36})
    res = []
    soup = BeautifulSoup(ret.content, "html.parser")
    infos = soup.find_all("div", class_="c-product__inner-container product-item-info")

    for info in infos:
        item = Item()
        img_div = info.div

        p_infos = info.find("div", class_="c-product__info-meta").find_all("p")
        item.name = p_infos[0].string
        item.price = float(p_infos[1].string[1:])

        item.url = img_div.a.get("href")
        item.image_url = img_div.a.img.get("data-src")
        item.store = "Poundland"
        res.append(item)

    logger.debug(f"Poundland completed, total {len(res)}")
    return res


if __name__ == '__main__':
    for i in query("chocolate"):
        print(i)
