from uuid import UUID

from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def save(self, project: Project) -> Project:
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: UUID) -> Project | None:
        return (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

    def get_all_by_user(self, user_id: UUID) -> list[Project]:
        return (
            self.db.query(Project)
            .filter(Project.user_id == user_id)
            .all()
        )

    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()