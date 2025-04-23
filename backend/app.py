"""
File Name   : app.py
Author      : Bhanu Prakash Akepogu
Date        : 02/19/2025
Description : Initializes and runs the FastAPI app for the credit card fraud detection system.
              Sets up middleware, routes, DB lifecycle, and session management for OAuth.
Version     : 1.1.0
"""

import os

from database.db import close_db, init_db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
from routes.auth import router as auth_router
from routes.model import router as model_router
from routes.predict import router as predict_router
from routes.upload import router as upload_router
from starlette.middleware.sessions import SessionMiddleware

# Load environment variables
SESSION_SECRET = os.getenv("SESSION_SECRET", "super-secret-session-key")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Create FastAPI app instance
app = FastAPI(
    title="FRAUDetective",
    description="Credit Card Fraud Detection API with Auth",
    version="1.1.0",
)

# ------------------------
# Middleware Configuration
# ------------------------

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Middleware (Required for Google OAuth via Authlib)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
)

# ------------------------
# Database Lifecycle
# ------------------------


@app.on_event("startup")
async def startup():
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise HTTPException(status_code=500, detail="Database startup failed")


@app.on_event("shutdown")
async def shutdown():
    try:
        await close_db()
        logger.info("Database closed.")
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
        raise HTTPException(status_code=500, detail="Database shutdown failed")


# ------------------------
# Route Registration
# ------------------------

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(upload_router, tags=["CSV Upload"])
app.include_router(model_router, tags=["ML Training"])
app.include_router(predict_router, tags=["Predict"])

# ------------------------
# Entry Point (if run directly)
# ------------------------

if __name__ == "__main__":
    import uvicorn

    debug_mode = os.getenv("FASTAPI_DEBUG", "0") == "1"
    logger.info("FASTAPI APP IS RUNNING")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=debug_mode)
