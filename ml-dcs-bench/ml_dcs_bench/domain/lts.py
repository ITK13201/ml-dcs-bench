from typing import List

from pydantic import BaseModel, ConfigDict


class ControllerSpec(BaseModel):
    name: str
    safety: List[str] = []
    controllable: List[str] = []
    marking: List[str] = []
    nonblocking: bool = False

    model_config = ConfigDict()

    @property
    def nonblocking_str(self) -> str:
        if self.nonblocking:
            return "true"
        else:
            return "false"
