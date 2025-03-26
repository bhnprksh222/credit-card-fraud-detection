"""
File Name   : config.py
Author      : Bhanu Prakash Akepogu
Date        : 02/19/2025
Description : This module loads environment variables and defines configuration settings
             for the credit card fraud detection web application. It utilizes environment
             variables for security-sensitive configurations such as database credentials
             and secret keys.
Version     : 1.0.0
"""

import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration with default settings."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    CORS_HEADERS: str = "Content-Type"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("DATABASE_URL")


# Select the configuration based on FASTAPI_ENV
configurations = {
    "development": DevelopmentConfig,
}

current_config = configurations[os.getenv("FASTAPI_ENV", "development")]
