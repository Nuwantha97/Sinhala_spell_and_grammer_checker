from fastapi import APIRouter, HTTPException, Request
from app.services.spell_checker import check_sentence
from app.utils.utils import load_dictionary

router = APIRouter(
    prefix="/api/v1"
)


@router.get("/home")
def read_root():
    return {"message": "Hello World"}

@router.post("/check_spelling")
async def check_spelling(request: Request):
    # Load the Sinhala dictionary CSV
    sinhala_dictionary = load_dictionary("app/utils/sinhala_dict_with_ipa.csv")
    body = await request.json()
    print(body)
    return check_sentence(body["sentence"], sinhala_dictionary)