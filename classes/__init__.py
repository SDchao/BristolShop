class UnitPrice:
    price: float
    measure: str

    def __init__(self, price: float, measure: str, m_amount: float = 1.0):
        self.price = price / m_amount
        self.measure = measure


class Item:
    name: str
    image_url: str
    url: str
    unit_price: UnitPrice
    price: float
    rating: float
    store: str

    def __str__(self):
        return f"{self.name} - £ {self.price} - {self.store}"

    def to_dict(self):
        d = {"name": self.name, "imgurl": self.image_url, "url": self.url, "price": f"£{self.price}",
             "store": self.store,
             "unitprice": "- / -"}
        if hasattr(self, "unit_price"):
            d["unit_price"] = f"£{self.unit_price.price} / {self.unit_price.measure}"

        return d
