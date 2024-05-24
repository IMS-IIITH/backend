from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from os import getenv

import routers.users_router as users_router
import routers.urls_router as urls_router

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Backend Index Page - For checking purposes
@app.get("/", tags=["General"])
async def index():
    return {"message": "Backend Running!!"}


# Mount the user router on the "/user" path
app.include_router(users_router.router, prefix="/user", tags=["User Management"])
app.include_router(
    urls_router.router, prefix="/data", tags=["Data Management and Retrieval"]
)
