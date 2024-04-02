from datetime import datetime
from typing import Annotated, Any

from pydantic import ValidationError, WrapValidator, field_validator
from sqlalchemy import text
from sqlmodel import Field, Relationship, SQLModel

# class UUIDModel(SQLModel):
#     uuid: uuid_pkg.UUID = Field(
#         default_factory=uuid_pkg.uuid4,
#         primary_key=True,
#         index=True,
#         nullable=False,
#         sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
#     )


class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)"),
        },
    )


class ClaimBase(SQLModel):
    pass


class Claim(TimestampModel, ClaimBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    records: list["Record"] = Relationship(back_populates="claim")


class RecordBase(SQLModel):
    service_date: datetime
    submitted_procedure: str
    quadrant: str | None = None
    group_plan: str
    subscriber_id: str = Field(index=True)
    provider_npi: str
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float


class Record(RecordBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    claim_id: int | None = Field(default=None, foreign_key="claim.id")
    claim: Claim | None = Relationship(back_populates="records")


class RecordOut(RecordBase):
    id: int
    claim_id: int


class ClaimOut(ClaimBase, TimestampModel):
    id: int
    records: list[RecordOut]


class ClaimsOut(SQLModel):
    data: list[ClaimOut]
    count: int


def validate_timestamp(v, handler):
    if isinstance(v, str):
        return float(v.strip().replace("$", ""))
    try:
        return handler(v)
    except ValidationError:
        # validation failed, in this case we want to return a default value
        return 0.0


Float = Annotated[float, WrapValidator(validate_timestamp)]


class RecordIn(RecordBase):
    provider_fees: Float
    allowed_fees: Float
    member_coinsurance: Float
    member_copay: Float

    @field_validator("service_date", mode="before")
    @classmethod
    def string_to_date(cls, v: Any):
        if isinstance(v, str):
            return datetime.strptime(v, "%m/%d/%y %H:%M")
        return v


class ClaimCreate(ClaimBase):
    records: list[RecordIn]
