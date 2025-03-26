"""
File Name   : app.py
Author      : Bhanu Prakash Akepogu
Date        : 02/19/2025
Description : This script initializes and runs the FASTAPI application for
             the credit card fraud detection system. It loads configurations,
             sets up routes, and starts the application server.
Version     : 1.0.0
"""

import os

from database.db import close_db, init_db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
from routes.auth import router as auth_router

# FastAPI App
app = FastAPI(
    title="FRAUDetective",
    description="Credit Card Fraud Detection",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database Initialization
@app.on_event("startup")
async def startup():
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@app.on_event("shutdown")
async def shutdown():
    try:
        await close_db()
        logger.info("Database closed.")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")


# Register Routes (Equivalent to Flask Blueprints)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Run FastAPI Server
if __name__ == "__main__":
    import uvicorn

    debug_mode = os.getenv("FASTAPI_DEBUG", "0") == "1"
    logger.info("FASTAPI APP IS RUNNING")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=debug_mode)
