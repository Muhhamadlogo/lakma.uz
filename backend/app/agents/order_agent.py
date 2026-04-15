from dataclasses import dataclass
import re


@dataclass(slots=True)
class OrderAction:
    action: str
    product_id: int | None
    quantity: int


class OrderAgent:
    def parse(self, message: str) -> OrderAction:
        text = message.lower()
        product_match = re.search(r"(?:товар|product|id)\s*(\d+)", text)
        quantity_match = re.search(r"(?:количеств[оа]|qty)\s*(\d+)", text)
        product_id = int(product_match.group(1)) if product_match else None
        quantity = int(quantity_match.group(1)) if quantity_match else 1

        if "удал" in text:
            return OrderAction(action="remove", product_id=product_id, quantity=0)
        if "офор" in text or "заказ" in text:
            return OrderAction(action="checkout", product_id=None, quantity=0)
        if "добав" in text:
            return OrderAction(action="add", product_id=product_id, quantity=quantity)
        return OrderAction(action="help", product_id=None, quantity=0)

    def explain(self, parsed: OrderAction) -> str:
        if parsed.action == "add":
            return "Товар добавлен в корзину."
        if parsed.action == "remove":
            return "Товар удален из корзины."
        if parsed.action == "checkout":
            return "Заказ оформлен на основе вашей корзины."
        return "Уточните действие: добавить товар, удалить товар или оформить заказ."
