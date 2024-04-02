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


# Unfortunately there is a bug currently in versions of SQLModel > 0.0.13 that prevents
# alias parameters from working. We can't go back as 0.0.13 will need to revert back
# to pydantic v1 syntax which will cause too many breaking changes.
# One solution for workaround was to manually override 2 resources FieldInfo and Field
# but that again requires some time to get right.
# Here are more details: https://github.com/tiangolo/sqlmodel/pull/774
# class RecordIn(RecordBase):
#     service_date: datetime = Field(validation_alias="service date")
#     submitted_procedure: str = Field(validation_alias="submitted procedure")
#     group_plan: str = Field(validation_alias="Plan/Group #")
#     subscriber_id: str = Field(validation_alias="Subscriber#")
#     provider_npi: str = Field(validation_alias="Provider NPI")
#     provider_fees: Float = Field(validation_alias="provider fees")
#     allowed_fees: Float = Field(validation_alias="Allowed fees")
#     member_coinsurance: Float = Field(validation_alias="member coinsurance")
#     member_copay: Float = Field(validation_alias="member copay")
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

    @field_validator("provider_npi", mode="before")
    @classmethod
    def validate_provider_npi(cls, v: Any):
        if not isinstance(v, str):
            raise ValidationError("provider_npi must be a string")
        if len(v) != 10:
            raise ValidationError("provider_npi must be 10 characters long")

        if v.isdigit():
            raise ValidationError("provider_npi string must contain only numbers")
        return v

    @field_validator("submitted_procedure", mode="before")
    @classmethod
    def validate_submitted_procedure(cls, v: Any):
        if not isinstance(v, str):
            raise ValidationError("submitted_procedure must be a string")
        if not v.startswith("D"):
            raise ValidationError("submitted_procedure must start with letter D")
        return v


class ClaimCreate(ClaimBase):
    records: list[RecordIn]
