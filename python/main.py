from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from parser.XML_parser import parse_recipi
from recipi.recipi import generate_recipi

class Ingredients(BaseModel):
    ingredients: list[str]

origins = [
    "http://localhost",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recipi")
def recipi(ingredeints: Ingredients):
    recipis_xml = generate_recipi(ingredeints.ingredients)
    recipis_json = parse_recipi(recipis_xml)
    return recipis_json
