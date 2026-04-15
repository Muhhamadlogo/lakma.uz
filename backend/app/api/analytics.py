from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import AnalyticsSummary
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def analytics_summary(db: Session = Depends(get_db)) -> AnalyticsSummary:
    return AnalyticsService(db).summary()
