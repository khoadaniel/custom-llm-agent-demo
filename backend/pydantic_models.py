from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    quantity: int
    item: str


class ListItems(BaseModel):
    list_items: List[Item]


class PaymentMethod(BaseModel):
    payment_method: str
