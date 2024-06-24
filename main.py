from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from os import getenv

import routers.users_router as users_router
import routers.urls_router as urls_router

DEBUG = getenv("BACKEND_DEBUG", "False").lower() in ("true", "1", "t")
MIN_VERSION = getenv("MIN_VERSION", None)

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


@app.get(
    "/validate_version/{version}", tags=["General"], status_code=status.HTTP_200_OK
)
async def validate_version(version: str):
    if MIN_VERSION is None:
        return {"message": "No minimum version set"}

    pre = False
    if "pre" in version:
        pre = True

    split_version = list(version.split("."))
    if pre:
        if len(split_version) != 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid version format"
            )
        split_version = split_version[:3]
        # Move to last major version
        split_version[-1] = str(int(split_version[-1]) - 1)

    if len(split_version) != 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid version format"
        )

    split_min_version = MIN_VERSION.split(".")

    if int(split_version[0]) < int(split_min_version[0]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Old Version"
        )
    if int(split_version[0]) > int(split_min_version[0]):
        return {"message": "Valid Version", "pre": pre}

    if int(split_version[1]) < int(split_min_version[1]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Old Version"
        )
    if int(split_version[1]) > int(split_min_version[1]):
        return {"message": "Valid Version", "pre": pre}

    if int(split_version[2]) < int(split_min_version[2]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Old Version"
        )
    if int(split_version[2]) >= int(split_min_version[2]):
        return {"message": "Valid Version", "pre": pre}


# Mount the user router on the "/user" path
app.include_router(users_router.router, prefix="/user", tags=["User Management"])
app.include_router(
    urls_router.router, prefix="/data", tags=["Data Management and Retrieval"]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("__main__:app", host="0.0.0.0", port=80, reload=DEBUG)
