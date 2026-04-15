from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    total_users: int
    total_products: int
    total_orders: int
    total_revenue: float
    total_agent_runs: int
