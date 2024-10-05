from fastapi import APIRouter
from starlette import status

from app.api.dependencies.authentication import CurrentUser
from app.api.dependencies.services import TasksServiceDep, ProjectsServiceDep
from app.schemas.response import TodoistResponse, ListData
from app.schemas.tasks import TaskData, TaskToUpdate

router = APIRouter(
    prefix="/projects/{project_uid}/tasks",
    tags=["Tasks"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=TodoistResponse[ListData[TaskData]],
    name="Get all tasks for a project"
)
async def get_all_tasks(
        project_uid: str,
        projects_service: ProjectsServiceDep,
        tasks_service: TasksServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[ListData[TaskData]]:
    project = await projects_service.retrieve_project(current_user.id, project_uid)
    tasks = await tasks_service.retrieve_all_tasks(project.id)

    return TodoistResponse[ListData[TaskData]](
        success=True,
        data=ListData(
            count=len(tasks),
            items=[
                TaskData(
                    uid=task.uid,
                    content=task.content,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                    scheduled_at=task.scheduled_at,
                    is_finished=task.is_finished,
                ) for task in tasks
            ]
        )
    )


@router.get(
    "/{task_uid}",
    response_model=TodoistResponse[TaskData],
    name="Get a task for a project",
)
async def get_task(
        project_uid: str,
        task_uid: str,
        projects_service: ProjectsServiceDep,
        tasks_service: TasksServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[TaskData]:
    project = await projects_service.retrieve_project(current_user.id, project_uid)
    task = await tasks_service.retrieve_all_tasks(project.id)

    return TodoistResponse[TaskData](
        success=True,
        data=TaskData(
            uid=task.uid,
            content=task.content,
            created_at=task.created_at,
            updated_at=task.updated_at,
            scheduled_at=task.scheduled_at,
            is_finished=task.is_finished,
        )
    )

@router.delete(
    "/{task_uid}",
    response_model=TodoistResponse,
    name="Delete task for project",
)
async def delete_task(
        project_uid: str,
        task_uid: str,
        projects_service: ProjectsServiceDep,
        tasks_service: TasksServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[TaskData]:
    project = await projects_service.retrieve_project(current_user.id, project_uid)
    task = await tasks_service.delete_task(project.id, task_uid)

    return TodoistResponse[TaskData](
        success=True,
        data=TaskData(
            uid=task.uid,
            content=task.content,
            created_at=task.created_at,
            updated_at=task.updated_at,
            scheduled_at=task.scheduled_at,
            is_finished=task.is_finished,
        )
    )


@router.put(
    '/{task_id}',
    response_model=TodoistResponse[TaskData],
    name="tasks:update",
)
async def update_task(
        task_uid: str,
        task_to_update: TaskToUpdate,
        task_service: TasksServiceDep,
        current_user: CurrentUser,
) -> TodoistResponse[TaskData]:
    updated_task = await task_service.update_task(
        current_user, task_uid, task_to_update
    )
    return TodoistResponse[TaskData](
        success=True,
        data=updated_task,
    )
