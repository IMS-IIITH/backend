from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from utils.files_utils import (
    # get_encoded_url_file,
    # get_file_content,
    get_encoded_file,
    remove_file,
)
from utils.auth_utils import get_current_user
from utils.ims_api_utils import get_bank_details

router = APIRouter()


# @router.get("/encoded_file", response_class=FileResponse)
# async def get_encoded_file_api(
#     url: str,
#     background_tasks: BackgroundTasks,
#     current_user: dict = Depends(get_current_user),
# ):
#     encoded_url = get_encoded_url_file(url)
#     if encoded_url is None:
#         raise HTTPException(status_code=404, detail="File not found")

#     file_path = get_file_content(encoded_url)
#     if file_path is None:
#         raise HTTPException(status_code=404, detail="File not found")

#     background_tasks.add_task(remove_file, file_path)
#     return file_path


@router.get("/bank_file", response_class=FileResponse)
async def get_bank_details_api(
    background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user)
):
    email = current_user["email"]
    bank_details = get_bank_details(email)

    if bank_details is None:
        raise HTTPException(status_code=404, detail="Bank Details not found")

    has_bank_details = bank_details["hasBankDetails"]
    if not has_bank_details:
        raise HTTPException(status_code=404, detail="Bank Details not found")

    bank_details = bank_details["bankDetails"]
    fileurl = bank_details["fileurl"]

    file_path = get_encoded_file(fileurl)
    if file_path is None:
        raise HTTPException(status_code=404, detail="File not found")

    background_tasks.add_task(remove_file, file_path)
    return file_path
