from fastapi import APIRouter
from services.openai import generate_post, describe_image_gpt

router = APIRouter()

@router.get('/generate')
def generate():
    return {'output': generate_post()}

@router.get('/describe_img')
def describe(url: str):
    return {'output': describe_image_gpt(url)}