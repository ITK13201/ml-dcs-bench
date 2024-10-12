from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, field_serializer


class RunResultTask(BaseModel):
    name: str = ""
    success: bool = False
    started_at: datetime = None
    finished_at: datetime = None

    @field_serializer("started_at")
    def serialize_started_at(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("finished_at")
    def serialize_finished_at(self, value: datetime) -> str:
        return value.isoformat()


class RunResult(BaseModel):
    started_at: datetime = None
    finished_at: datetime = None

    tasks: List[RunResultTask] = []

    model_config = ConfigDict()

    @field_serializer("started_at")
    def serialize_started_at(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("finished_at")
    def serialize_finished_at(self, value: datetime) -> str:
        return value.isoformat()

    @property
    def task_count(self) -> int:
        return len(self.tasks)

    @property
    def task_success_count(self) -> int:
        success_count = 0
        for task in self.tasks:
            if task.success:
                success_count += 1
        return success_count

    @property
    def task_failure_count(self) -> int:
        return self.task_count - self.task_success_count
