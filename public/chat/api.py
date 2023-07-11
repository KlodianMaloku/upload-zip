from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    return {"Message": "techdebtGPT root api"}


@router.get("/summary/{text}")
def read_item(text: str, q: str = None):
    return {"summary_for": text, "q": q}

