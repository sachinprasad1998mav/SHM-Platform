from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=list[schemas.Project])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectBase, db: Session = Depends(get_db)):
    db_project = models.Project(name=project.name, client_id=project.client_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.post("/zones")
def create_zone(name: str, project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_zone = models.Zone(name=name, project_id=project_id)
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone
