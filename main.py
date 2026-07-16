import uvicorn
from fastapi import FastAPI, Query, Body, Path
from sqlalchemy.orm import Session

from models import engine, Tasks, Base


app = FastAPI()
Base.metadata.create_all(engine)


@app.get("/api/health")
def health_view() -> dict:
    return {"message": "ok"}


@app.get("/api/tasks")
def get_tasks_view(
    limit: int = Query(10),
    title: str = Query(''),
) -> list[dict]:
    with Session(engine) as session:
        tasks: list[Tasks] = session.query(Tasks).all()

    result = []
    for task in tasks:
        result.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        })

    if title:
        return [task for task in result if title.lower() in task["title"].lower()][:limit]
    return result[:limit]


# GET     /api/tasks/id - task detail
@app.get("/api/tasks/{task_id}")
def get_task_detail_view(task_id: int) -> dict:
    with Session(engine) as session:
        task: Tasks | None = session.query(Tasks).get(task_id)

    if task:
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        }
    return {'message': 'not found'}


# POST    /api/tasks    - create task
@app.post("/api/tasks")
def create_task_view(
    data: dict = Body()
) -> dict:
    task = Tasks(**data) # id=1, title="fsda"
    with Session(engine) as session:
        session.add(task)
        session.commit()

    return {'message': 'ok'}


# PUT     /api/tasks/id - create task
@app.put("/api/tasks/{task_id}")
def update_task_view(
    task_id: int = Path(),
    data: dict = Body()
) -> dict:
    pass

# PATCH   /api/tasks/id - mark as completed
# PATCH   /api/tasks/id - mark as incompleted
# DELETE  /api/tasks/id - delete task


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)
