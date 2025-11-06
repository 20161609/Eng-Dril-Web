from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.schemas import ScoreReq, BatchReq, ScoreResp, BatchResp
from app.config import settings
from app.deps import get_current_user

router = APIRouter(prefix="/qe", tags=["qe"])

@router.post("/score", response_model=ScoreResp)
async def proxy_score(req: ScoreReq, user=Depends(get_current_user)):
    """
    Forward a single (src, mt) pair to the external QE model API
    with UTF-8 encoding enforced.
    """
    url = f"{settings.MODEL_API_BASE}/score"
    headers = {"Content-Type": "application/json; charset=utf-8"}

    # Optional API key forwarding
    if settings.MODEL_API_KEY:
        headers["Authorization"] = f"Bearer {settings.MODEL_API_KEY}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, json=req.model_dump(), headers=headers)
            if res.status_code != 200:
                raise HTTPException(status_code=res.status_code, detail=res.text)
            # force UTF-8 decode
            return res.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"QE model server unreachable: {e}")


@router.post("/score_batch", response_model=BatchResp)
async def proxy_score_batch(req: BatchReq, user=Depends(get_current_user)):
    """
    Forward multiple (src, mt) pairs to the QE model API for batch scoring.
    """
    url = f"{settings.MODEL_API_BASE}/score_batch"
    headers = {"Content-Type": "application/json; charset=utf-8"}

    if settings.MODEL_API_KEY:
        headers["Authorization"] = f"Bearer {settings.MODEL_API_KEY}"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(url, json=req.model_dump(), headers=headers)
            if res.status_code != 200:
                raise HTTPException(status_code=res.status_code, detail=res.text)
            return res.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"QE model server unreachable: {e}")
