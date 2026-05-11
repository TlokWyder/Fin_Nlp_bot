# import os
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from BackEnd.routers import catalog, cart, orders, chat
#
# app = FastAPI(title="E-Commerce API", version="2.0.0")
#
# ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )
#
# app.include_router(catalog.router, prefix="/catalog")
# app.include_router(cart.router,    prefix="/cart")
# app.include_router(orders.router,  prefix="/orders")
# app.include_router(chat.router,    prefix="/chat")


import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from BackEnd import NLP_faq_bot
from BackEnd.routers import catalog  # только то что есть!
from BackEnd.NLP_faq_bot import *

app = FastAPI(title="E-Commerce API", version="2.0.0")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=ALLOWED_ORIGINS,
    allow_origins=["*"],  # Разрешаем ВСЕМ адресам стучаться к нам
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(catalog.router, prefix="/catalog")
app.include_router(NLP_faq_bot.router, prefix="/chat")
# cart, orders, chat добавим позже когда создадим файлы









