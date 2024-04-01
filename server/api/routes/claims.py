from fastapi import APIRouter
from sqlmodel import func, select

from server.models import Claim, ClaimsOut

from ..deps import SessionDep

router = APIRouter()


@router.get("/", response_model=ClaimsOut)
def read_claims(
    claim: Claim, session: SessionDep, skip: int = 0, limit: int = 100
) -> ClaimsOut:
    count_statement = select(func.count()).select_from(Claim)
    count = session.exec(count_statement).one()

    statement = select(Claim).offset(skip).limit(limit)
    claims = session.exec(statement).all()

    return ClaimsOut(data=claims, count=count)


@app.get("/{claim_id}", response_model=list[Claim])
async def read_claim(claim_id: int, session: SessionDep):
    result = await session.get(Claim, claim_id)
    return result.scalars().first()


@app.post("/", response_model=Claim)
async def add_claim(claim: Claim, session: AsyncSession = Depends(get_session)):
    claim = Claim(**claim.model_dump())
    session.add(claim)
    await session.commit()
    await session.refresh(claim)
    return claim
