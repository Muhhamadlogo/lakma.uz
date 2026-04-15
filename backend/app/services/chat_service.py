from dataclasses import asdict
from decimal import Decimal

from sqlalchemy.orm import Session

from app.agents.intent_agent import IntentAgent
from app.agents.order_agent import OrderAgent
from app.agents.stylist_agent import StylistAgent
from app.repositories.agent_repository import AgentRepository
from app.repositories.product_repository import ProductRepository
from app.services.cart_service import CartService
from app.services.order_service import OrderService
from app.schemas.chat import ArtifactRead, ChatResponse
from app.schemas.cart import CartItemCreate
from app.schemas.order import OrderCreate
from app.services.user_service import UserService


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.intent_agent = IntentAgent()
        self.stylist_agent = StylistAgent()
        self.order_agent = OrderAgent()
        self.agent_repo = AgentRepository(db)
        self.product_repo = ProductRepository(db)
        self.user_service = UserService(db)
        self.cart_service = CartService(db)
        self.order_service = OrderService(db)

    def process(self, user_id: int, message: str) -> ChatResponse:
        user = self.user_service.ensure_by_telegram(user_id)
        intent_result = self.intent_agent.classify(message)
        agent_name = {
            "styling": "StylistAgent",
            "order_action": "OrderAgent",
            "product_search": "CatalogRetrieval",
            "consultation": "IntentAgent",
        }[intent_result.intent]

        run = self.agent_repo.start_run(user.id, agent_name, message, intent_result.intent)
        self.agent_repo.add_trace(
            run.id,
            "intent_classification",
            1,
            {"message": message},
            {"intent": intent_result.intent, "confidence": intent_result.confidence},
        )

        products = []
        artifacts: list[ArtifactRead] = []

        if intent_result.intent == "styling":
            prefs = self.stylist_agent.parse_preferences(message)
            self.agent_repo.add_trace(run.id, "stylist_parse", 2, {"message": message}, asdict(prefs))
            candidates = self.product_repo.list_products(query=None, category_id=None)
            filtered = []
            for product in candidates:
                if prefs.material and (product.material or "").lower().find("кож") == -1 and (product.material or "").lower().find("leather") == -1:
                    continue
                if prefs.gender and (product.gender or "") != prefs.gender:
                    continue
                if prefs.season and (product.season or "") != prefs.season:
                    continue
                if prefs.budget and product.price > Decimal(prefs.budget):
                    continue
                filtered.append(product)
            products = filtered[:6]
            reply = self.stylist_agent.explain(message)
        elif intent_result.intent == "product_search":
            products = self.product_repo.list_products(query=message)[:6]
            reply = "Нашел релевантные товары по вашему запросу."
        elif intent_result.intent == "order_action":
            parsed = self.order_agent.parse(message)
            self.agent_repo.add_trace(run.id, "order_parse", 2, {"message": message}, asdict(parsed))

            if parsed.action == "add" and parsed.product_id:
                self.cart_service.add_item(CartItemCreate(user_id=user_id, product_id=parsed.product_id, quantity=parsed.quantity))
                products = [p for p in self.product_repo.list_products() if p.id == parsed.product_id][:1]
            elif parsed.action == "remove" and parsed.product_id:
                items = self.cart_service.get_cart(user_id)
                for item in items:
                    if item.product_id == parsed.product_id:
                        self.cart_service.remove_item(item.id)
                        break
            elif parsed.action == "checkout":
                self.order_service.create_order(OrderCreate(user_id=user_id))

            reply = self.order_agent.explain(parsed)
        else:
            reply = "Я помогу подобрать стиль, товары и оформить заказ. Уточните, что вам нужно."

        artifact_payload = {
            "title": "Результаты запроса",
            "items": [{"id": p.id, "name": p.name, "price": str(p.price)} for p in products],
        }
        artifact = self.agent_repo.add_artifact(run.id, "recommendation_cards", artifact_payload)
        artifacts.append(ArtifactRead(artifact_type=artifact.artifact_type, content_json=artifact.content_json))
        self.agent_repo.add_trace(run.id, "response_build", 3, {"products_count": len(products)}, {"reply": reply})
        self.agent_repo.finish_run(run, status="completed")

        return ChatResponse(
            intent=intent_result.intent,
            agent=agent_name,
            reply=reply,
            products=products,
            artifacts=artifacts,
            run_id=run.id,
        )
