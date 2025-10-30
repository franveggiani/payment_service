from fastapi import FastAPI
from app import api
from app.rabbit_consumer import consume_payments
import asyncio

app = FastAPI()

app.include_router(api.router, prefix="/api", tags=["Api"])

@app.on_event("startup")
async def start_consumer():
    app.state.rabbit_task = asyncio.create_task(consume_payments())

@app.on_event("shutdown")
async def stop_consumer():
    app.state.rabbit_task.cancel()