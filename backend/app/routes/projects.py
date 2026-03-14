from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=list[schemas.Project])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()
