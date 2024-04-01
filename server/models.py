from datetime import datetime

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


class ClaimBase(TimestampModel):
    claim_data: list["ClaimData"] = Relationship(back_populates="claim")


class Claim(ClaimBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ClaimOut(ClaimBase):
    id: int


class ClaimsOut(SQLModel):
    data: list[ClaimOut]
    count: int


class ClaimData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    claim_id: int | None = Field(default=None, foreign_key="claim.id")
    claim: Claim | None = Relationship(back_populates="claim_data")
    service_date: datetime
    submitter_procedure: str
    quadrant: str | None = None
    group_plan: str
    subscriber_id: int = Field(index=True)
    provider_npi: int
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float
