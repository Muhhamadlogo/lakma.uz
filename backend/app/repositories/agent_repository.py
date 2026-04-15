from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models import AgentRun, AgentTrace, Artifact


class AgentRepository:
    def __init__(self, db: Session):
        self.db = db

    def start_run(self, user_id: int, agent_name: str, input_text: str, detected_intent: str) -> AgentRun:
        run = AgentRun(
            user_id=user_id,
            agent_name=agent_name,
            input_text=input_text,
            detected_intent=detected_intent,
            status="running",
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def add_trace(self, run_id: int, step_name: str, step_order: int, input_snapshot: dict[str, Any], output_snapshot: dict[str, Any]) -> AgentTrace:
        trace = AgentTrace(
            agent_run_id=run_id,
            step_name=step_name,
            step_order=step_order,
            input_snapshot=input_snapshot,
            output_snapshot=output_snapshot,
        )
        self.db.add(trace)
        self.db.commit()
        self.db.refresh(trace)
        return trace

    def add_artifact(self, run_id: int, artifact_type: str, content_json: dict[str, Any]) -> Artifact:
        artifact = Artifact(agent_run_id=run_id, artifact_type=artifact_type, content_json=content_json)
        self.db.add(artifact)
        self.db.commit()
        self.db.refresh(artifact)
        return artifact

    def finish_run(self, run: AgentRun, status: str = "completed") -> AgentRun:
        run.status = status
        run.finished_at = datetime.utcnow()
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run
