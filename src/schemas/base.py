from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        strict=True,
        str_min_length=1,
    )


class TimingDTO(BaseModel):
    created_at: datetime
    updated_at: datetime
