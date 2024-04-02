from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import func, select

from server.models import (
    Claim,
    ClaimCreate,
    ClaimOut,
    ClaimsOut,
    NetFeeClaimOut,
    Record,
)

from ..deps import SessionDep

router = APIRouter()


@router.get("/", response_model=ClaimsOut)
def read_claims(session: SessionDep, skip: int = 0, limit: int = 100) -> ClaimsOut:
    count_statement = select(func.count()).select_from(Claim)
    count = session.exec(count_statement).one()

    statement = select(Claim).offset(skip).limit(limit)
    claims = session.exec(statement).all()

    return ClaimsOut(data=claims, count=count)


@router.get("/{claim_id}", response_model=list[ClaimOut])
def read_claim(session: SessionDep, claim_id: int) -> ClaimOut:
    claim = session.get(Claim, id=claim_id)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found"
        )
    return claim


@router.post("/", response_model=ClaimOut, status_code=status.HTTP_201_CREATED)
def add_claim(session: SessionDep, claim_in: ClaimCreate) -> Any:
    new_claim = Claim()
    session.add(new_claim)
    session.commit()
    session.refresh(new_claim)
    records = [
        Record(**record.model_dump(), claim=new_claim) for record in claim_in.records
    ]
    session.add_all(records)
    session.commit()
    session.refresh(new_claim)
    return new_claim


@router.get("/top_net_fee", response_model=list[NetFeeClaimOut])
def read_top_net_fee(session: SessionDep) -> list[NetFeeClaimOut]:
    top_10_claims = session.query(Claim).order_by(Claim.total_net_fee).limit(10).all()

    return top_10_claims
