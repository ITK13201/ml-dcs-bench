from datetime import datetime, timedelta
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer


class RunResultTask(BaseModel):
    name: str = ""
    success: bool = False
    started_at: datetime = None
    finished_at: datetime = None
    max_memory_usage: float = Field(alias="max_memory_usage [KiB]", default=-1)

    @field_serializer("started_at")
    def serialize_started_at(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("finished_at")
    def serialize_finished_at(self, value: datetime) -> str:
        return value.isoformat()

    @computed_field
    @property
    def duration(self) -> timedelta:
        return self.finished_at - self.started_at


class RunResult(BaseModel):
    started_at: datetime | None = None
    finished_at: datetime | None = None

    tasks: List[RunResultTask] = []

    model_config = ConfigDict()

    @field_serializer("started_at")
    def serialize_started_at(self, value: datetime) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat()

    @field_serializer("finished_at")
    def serialize_finished_at(self, value: datetime) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat()

    @computed_field
    @property
    def task_count(self) -> int:
        return len(self.tasks)

    @computed_field
    @property
    def task_success_count(self) -> int:
        success_count = 0
        for task in self.tasks:
            if task.success:
                success_count += 1
        return success_count

    @computed_field
    @property
    def task_failure_count(self) -> int:
        return self.task_count - self.task_success_count

    @computed_field
    @property
    def duration(self) -> Optional[timedelta]:
        if self.started_at and self.finished_at:
            return self.finished_at - self.started_at
        else:
            return None
