from fastapi import APIRouter
from database import SessionLocal
from models import Project
from services.project_service import process_project

router = APIRouter()

@router.post("/projects/")
def create_project(project: dict):
    db = SessionLocal()

    db_project = Project(**project)

    # 👇 BUSINESS LOGIC APPLIED HERE
    db_project = process_project(db_project)

    db.add(db_project)
    db.commit()

    return {"message": "Project created"}

@router.get("/projects/")
def get_projects():
    db = SessionLocal()
    return db.query(Project).all()


@router.put("/projects/{project_id}")
def update_project(project_id: int, updated_data: dict):
    db = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return {"error": "Project not found"}

    # Update fields
    for key, value in updated_data.items():
        setattr(project, key, value)

    # Apply business logic again
    project = process_project(project)

    db.commit()
    db.refresh(project)

    return {"message": "Project updated", "project": project}


@router.get("/projects/status/{status}")
def filter_projects(status: str):

    db = SessionLocal()

    projects = db.query(Project).filter(
        Project.status == status
    ).all()

    return projects


@router.delete("/projects/{project_id}")
def delete_project(project_id: int):
    db = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return {"error": "Project not found"}

    db.delete(project)
    db.commit()

    return {"message": "Project deleted"}


@router.get("/dashboard/")
def get_dashboard():

    db = SessionLocal()

    projects = db.query(Project).all()

    total_projects = len(projects)

    total_budget = sum(
        p.budget for p in projects
    )

    avg_progress = (
        sum(p.progress for p in projects) / total_projects
        if total_projects > 0 else 0
    )

    over_budget_projects = len([
        p for p in projects
        if p.status == "Over Budget"
    ])

    return {
        "total_projects": total_projects,
        "total_budget": total_budget,
        "avg_progress": round(avg_progress, 2),
        "over_budget_projects": over_budget_projects
    }