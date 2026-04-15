from dataclasses import dataclass


@dataclass(slots=True)
class IntentResult:
    intent: str
    confidence: float


class IntentAgent:
    STYLE_KEYWORDS = {"образ", "стиль", "лук", "подбери", "минималист", "вечерин"}
    ORDER_KEYWORDS = {"корзин", "заказ", "добавь", "удали", "оформи"}
    SEARCH_KEYWORDS = {"найди", "покажи", "кожан", "до", "руб", "мужск", "женск"}

    def classify(self, message: str) -> IntentResult:
        text = message.lower()
        if any(word in text for word in self.ORDER_KEYWORDS):
            return IntentResult(intent="order_action", confidence=0.88)
        if any(word in text for word in self.STYLE_KEYWORDS):
            return IntentResult(intent="styling", confidence=0.85)
        if any(word in text for word in self.SEARCH_KEYWORDS):
            return IntentResult(intent="product_search", confidence=0.81)
        return IntentResult(intent="consultation", confidence=0.6)
