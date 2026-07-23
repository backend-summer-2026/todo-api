from pydantic import BaseModel, Field


class TaskSchema(BaseModel):
    title: str = Field(min_length=3, max_length=128)
    description: str = ""
    status: bool = False
