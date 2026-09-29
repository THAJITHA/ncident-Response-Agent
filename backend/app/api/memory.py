from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.hindsight_service import HindsightService

router = APIRouter(prefix="/api", tags=["memory"])


class MemorySearchRequest(BaseModel):
    query: str


@router.post("/memory/search")
def search_memory(payload: MemorySearchRequest, db: Session = Depends(get_db)):
    service = HindsightService(db)
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    memories = service.recall_memories(query)
    return {"query": query, "memories": memories}


@router.get("/memory/incidents")
def incident_memory(db: Session = Depends(get_db)):
    service = HindsightService(db)
    return {"memory": service.get_memories()}
