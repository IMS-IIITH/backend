from fastapi import FastAPI
from os import getenv
import routers.users_router as users_router

DEBUG = getenv("BACKEND_DEBUG", "False").lower() in ("true", "1", "t")

# FastAPI instance
if DEBUG:
    app = FastAPI(
        debug=DEBUG,
        title="IMS App Backend",
        description="TODO: Add Description",
    )
else:
    app = FastAPI(
        debug=DEBUG,
        title="IMS App Backend",
        description="TODO: Add Description",
        docs_url=None,
        redoc_url=None,
    )

# Backend Index Page - For checking purposes
@app.get("/", tags=["General"])
async def index():
    return {"message": "Backend Running!!"}

# Mount the user router on the "/user" path
app.include_router(users_router.router, prefix="/user", tags=["User Management"])
