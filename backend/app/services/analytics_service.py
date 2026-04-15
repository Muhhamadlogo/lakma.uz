from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AgentRun, Order, Product, User
from app.schemas.analytics import AnalyticsSummary


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def summary(self) -> AnalyticsSummary:
        total_users = self.db.scalar(select(func.count(User.id))) or 0
        total_products = self.db.scalar(select(func.count(Product.id))) or 0
        total_orders = self.db.scalar(select(func.count(Order.id))) or 0
        total_revenue = self.db.scalar(select(func.coalesce(func.sum(Order.total_amount), 0))) or 0
        total_agent_runs = self.db.scalar(select(func.count(AgentRun.id))) or 0
        return AnalyticsSummary(
            total_users=total_users,
            total_products=total_products,
            total_orders=total_orders,
            total_revenue=float(total_revenue),
            total_agent_runs=total_agent_runs,
        )
