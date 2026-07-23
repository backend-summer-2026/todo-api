from typing import Tuple
import json

import uvicorn
from fastapi import FastAPI, Query, Body, Path
from fastapi.responses import Response
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from sqlalchemy import select

from models import engine, Tasks, Base, async_engine
from schemas import TaskSchema


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.create_all(engine)

# client > request > server > response > client
# desializer vs serializer -> pydantic2


@app.get("/api/health")
async def health_view() -> dict:
    return {"message": "ok"}


@app.get("/api/tasks")
async def get_tasks_view(page: int = Query(1, ge=1), n: int = Query(4, ge=1)) -> list[dict]:
    offset = (page - 1) * n
    limit = n
    async_session = AsyncSession(async_engine)
    stmt = select(Tasks).order_by(desc(Tasks.id)).offset(offset).limit(limit)
    tasks = await async_session.execute(stmt)

    result = []
    for task in tasks:
        result.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
            }
        )

    return result


@app.get("/api/tasks/{task_id}")
async def get_task_detail_view(task_id: int = Path(ge=1)) -> Response:
    async_session = AsyncSession(async_engine)
    stmt = select(Tasks).where(Tasks.id==task_id)
    task: Tasks | None = await async_session.execute(stmt) # type: ignore

    if task:
        return Response(
            content=json.dumps(
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                }
            ),
            headers={"Content-Type": "application/json"},
        )
    return Response(
        content=json.dumps({"message": "task not found"}),
        status_code=status.HTTP_404_NOT_FOUND,
        headers={"Content-Type": "application/json"},
    )


@app.post("/api/tasks")
async def create_task_view(data: TaskSchema = Body()) -> Response:
    with Session(engine) as session:
        task = Tasks(title=data.title, description=data.description, status=data.status)
        session.add(task)
        session.commit()
        session.refresh(task)

    return Response(
        content=json.dumps(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
            }
        ),
        status_code=status.HTTP_201_CREATED,
        headers={"Content-Type": "application/json"},
    )


@app.put("/api/tasks/{task_id}")
async def update_task_view(task_id: int = Path(ge=1), data: dict = Body()) -> Response:
    with Session(engine) as session:
        task: Tasks | None = session.query(Tasks).get(task_id)
        if task:
            task.title = data["title"] if data.get("title") else task.title
            task.description = (
                data["description"] if data.get("description") else task.description
            )
            task.status = data["status"] if data.get("status") else task.status

            session.add(task)
            session.commit()

            return Response(
                content=json.dumps(
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "status": task.status,
                    }
                ),
                headers={"Content-Type": "application/json"},
            )

        return Response(
            content=json.dumps({"message": "task not found"}),
            status_code=status.HTTP_404_NOT_FOUND,
            headers={"Content-Type": "application/json"},
        )


@app.delete("/api/tasks/{task_id}")
async def delete_task_view(task_id: int = Path(ge=1)) -> Response:
    with Session(engine) as session:
        task: Tasks | None = session.query(Tasks).get(task_id)
        session.delete(task)
        session.commit()

        return Response(
            content=json.dumps({"message": "task has been deleted"}),
            status_code=status.HTTP_204_NO_CONTENT,
            headers={"Content-Type": "application/json"},
        )


@app.patch("/api/tasks/{task_id}/completed")
async def mark_as_comleted_view(task_id: int = Path(ge=1)) -> Response:
    with Session(engine) as session:
        task: Tasks | None = session.query(Tasks).get(task_id)
        if task:
            task.status = True

            session.add(task)
            session.commit()

            return Response(
                content=json.dumps(
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "status": task.status,
                    }
                ),
                headers={"Content-Type": "application/json"},
            )

        return Response(
            content=json.dumps({"message": "task not found"}),
            status_code=status.HTTP_404_NOT_FOUND,
            headers={"Content-Type": "application/json"},
        )


@app.patch("/api/tasks/{task_id}/incompleted")
async def mark_as_incomleted_view(task_id: int = Path(ge=1)) -> Response:
    with Session(engine) as session:
        task: Tasks | None = session.query(Tasks).get(task_id)
        if task:
            task.status = False

            session.add(task)
            session.commit()

            return Response(
                content=json.dumps(
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "status": task.status,
                    }
                ),
                headers={"Content-Type": "application/json"},
            )

        return Response(
            content=json.dumps({"message": "task not found"}),
            status_code=status.HTTP_404_NOT_FOUND,
            headers={"Content-Type": "application/json"},
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5001, reload=True)
