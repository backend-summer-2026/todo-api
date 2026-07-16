import json

import uvicorn
from fastapi import FastAPI, Query


app = FastAPI()
TASKS: list[dict] = list()
with open("tasks.json") as f:
    data = f.read()
    TASKS = json.loads(data)


# GET     /api/health   - message
@app.get("/api/health")
def health_view() -> dict:
    return {"message": "ok"}


# GET     /api/tasks    - task list
@app.get("/api/tasks")
def get_tasks_view(
    limit: int = Query(len(TASKS)),
) -> list[dict]:
    return TASKS[:limit]


# GET     /api/tasks/id - task detail
@app.get("/api/tasks/{task_id}")
def get_task_detail_view(task_id: int) -> dict:
    for task in TASKS:
        if task['id'] == task_id:
            return task
    return {'message': 'task not found'}


# POST    /api/tasks    - create task
@app.get("/api/tasks/")
def create_task_view(task_id) -> dict:
    return {'message': 'not implemented'}


# PUT     /api/tasks/id - create task
# PATCH   /api/tasks/id - mark as completed
# PATCH   /api/tasks/id - mark as incompleted
# DELETE  /api/tasks/id - delete task



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
