from fastapi import APIRouter



from core.tickets import search

router = APIRouter(prefix='/test', tags=['Test'])

@router.get('/get', description="get ticket info")
async def get_ticket(
) -> dict:
    result = search('MAD','NYC','2024-10-01','1')
    return result