"""Project management tests."""

import pytest
from uuid import uuid4
from app.application.services import ProjectService
from app.domain.entities.project import ProjectEntity, ProjectStatus


@pytest.mark.asyncio
async def test_create_project():
    """Test creating a new project."""
    workspace_id = uuid4()
    user_id = uuid4()
    
    project_data = {
        "name": "New Project",
        "description": "Test project",
    }
    
    # Mock repository
    class MockProjectRepository:
        async def create(self, project):
            return project
    
    service = ProjectService(MockProjectRepository())
    
    # Create project
    project = await service.create_project(
        workspace_id=workspace_id,
        name=project_data["name"],
        description=project_data["description"],
        created_by=user_id,
    )
    
    # Verify
    assert project.name == project_data["name"]
    assert project.workspace_id == workspace_id
    assert project.created_by == user_id
    assert project.status == ProjectStatus.ACTIVE
