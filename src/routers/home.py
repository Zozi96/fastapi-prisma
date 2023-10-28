from fastapi import APIRouter

router = APIRouter()


@router.get("/index")
async def main():
    return {"message": "This is the main content"}
