import re
from dataclasses import dataclass


@dataclass(slots=True)
class StyleRequest:
    budget: int | None
    material: str | None
    gender: str | None
    season: str | None


class StylistAgent:
    def parse_preferences(self, message: str) -> StyleRequest:
        text = message.lower()
        budget_match = re.search(r"до\s*(\d{3,6})", text)
        budget = int(budget_match.group(1)) if budget_match else None

        material = "кожа" if "кож" in text else None
        gender = "male" if "муж" in text else "female" if "жен" in text else None
        season = "autumn" if "осен" in text else "winter" if "зим" in text else None
        return StyleRequest(budget=budget, material=material, gender=gender, season=season)

    def explain(self, message: str) -> str:
        return "Я подобрал лаконичные позиции, которые соответствуют вашему запросу по стилю и бюджету."
