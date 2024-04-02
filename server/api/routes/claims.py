from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import func, select

from server.models import Claim, ClaimCreate, ClaimOut, ClaimsOut

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


@router.post("/", response_model=ClaimOut)
def add_claim(session: SessionDep, claim_in: ClaimCreate) -> Any:
    claim = Claim.model_validate(claim_in)
    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim
