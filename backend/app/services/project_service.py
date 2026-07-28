from uuid import UUID

from app.models.project import Project, ProjectStatus
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def create_project(
        self,
        *,
        user_id: UUID,
        data: ProjectCreate,
    ) -> Project:
        project = Project(
            user_id=user_id,
            name=data.name,
            description=data.description,
            tech_stack=(
                data.tech_stack.model_dump()
                if data.tech_stack
                else None
            ),
            status=ProjectStatus.ACTIVE,
        )

        return self.repository.create(project)

    def get_projects(
        self,
        *,
        user_id: UUID,
    ) -> list[Project]:
        return self.repository.get_all_by_user(user_id)

    def get_project(
        self,
        *,
        project_id: UUID,
        user_id: UUID,
    ) -> Project:
        project = self.repository.get_by_id(project_id)

        if project is None:
            raise ValueError("Project not found.")

        if project.user_id != user_id:
            raise PermissionError("Access denied.")

        return project

    def update_project(
        self,
        *,
        project_id: UUID,
        user_id: UUID,
        data: ProjectUpdate,
    ) -> Project:

        project = self.get_project(
            project_id=project_id,
            user_id=user_id,
        )

        update_data = data.model_dump(exclude_unset=True)

        if (
            "tech_stack" in update_data
            and update_data["tech_stack"] is not None
        ):
            update_data["tech_stack"] = (
                update_data["tech_stack"].model_dump()
            )

        for field, value in update_data.items():
            setattr(project, field, value)

        return self.repository.save(project)

    def delete_project(
        self,
        *,
        project_id: UUID,
        user_id: UUID,
    ) -> None:

        project = self.get_project(
            project_id=project_id,
            user_id=user_id,
        )

        self.repository.delete(project)