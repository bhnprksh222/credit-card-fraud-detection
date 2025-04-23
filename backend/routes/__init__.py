from .auth import router as auth_router
from .model import router as model_router
from .upload import router as upload_router

__all__ = ["auth_router", "upload_router", "model_router"]
