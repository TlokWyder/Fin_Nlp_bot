from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from BackEnd import NLP_faq_bot
from BackEnd.routers import catalog
from BackEnd.NLP_faq_bot import *

app = FastAPI(title="E-Commerce API", version="2.0.0")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=ALLOWED_ORIGINS,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(catalog.router, prefix="/catalog")
app.include_router(NLP_faq_bot.router, prefix="/chat")








