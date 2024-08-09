from fastapi import APIRouter, HTTPException, Depends

from models.bank import BankModel
from models.leave import LeaveApplicationModel

from utils.auth_utils import get_current_user
from utils.ims_api_utils import (
    get_user_profile,
    get_bank_details,
    update_bank_details,
    get_gpa_data,
    get_courses_data,
    get_attendance_for_course,
    get_leave_requests,
    new_leave_request,
    validate_new_leave,
)

router = APIRouter()


@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]
    profile = get_user_profile(email)

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    if (
        "aadhaarNumber" in profile["general"]
        and len(profile["general"]["aadhaarNumber"]) > 2
    ):
        profile["general"]["aadhaarNumber"] = (
            "X" * 10 + profile["general"]["aadhaarNumber"][-2:]
        )
    else:
        profile["general"]["aadhaarNumber"] = "Not Available"

    return profile


@router.get("/bank_details")
async def get_bank_details_api(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]
    bank_details = get_bank_details(email)

    if bank_details is None:
        raise HTTPException(status_code=404, detail="Bank Details not found")

    if (
        "accountNumber" in bank_details["bankDetails"]
        and len(bank_details["bankDetails"]["accountNumber"]) > 4
    ):
        bank_details["bankDetails"]["accountNumber"] = (
            "X" * (len(bank_details["bankDetails"]["accountNumber"]) - 4)
            + bank_details["bankDetails"]["accountNumber"][-4:]
        )
    else:
        bank_details["bankDetails"]["accountNumber"] = "Not Available"

    return bank_details


@router.post("/update_bank_details")
async def update_bank_details_api(
    bank_details: BankModel, current_user: dict = Depends(get_current_user)
):
    email = current_user["email"]
    bank_details_dict = bank_details.dict(by_alias=True)
    return_data = update_bank_details(email, bank_details_dict)

    if return_data is None:
        raise HTTPException(status_code=404, detail="Bank Details not updated")
    return return_data


@router.get("/transcript")
async def get_transcript(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]
    gpa_data = get_gpa_data(email)

    if gpa_data is None:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return gpa_data


@router.get("/courses")
async def get_courses_api(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]
    courses_data = get_courses_data(email)

    if courses_data is None:
        raise HTTPException(status_code=404, detail="Courses not found")
    return courses_data


@router.get("/attendance/{course_id}")
async def get_attendance_for_course_api(
    course_id: str,
    current_user: dict = Depends(get_current_user),
):
    email = current_user["email"]
    attendance_data = get_attendance_for_course(email, course_id)

    if attendance_data is None:
        raise HTTPException(
            status_code=404, detail=f"Attendance for course {course_id} not found"
        )
    return attendance_data


@router.get("/leave_requests")
async def get_leave_requests_api(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]
    leave_requests = get_leave_requests(email)

    if leave_requests is None:
        raise HTTPException(status_code=404, detail="Leave Requests not found")
    return leave_requests


@router.post("/new_leave_request")
async def new_leave_request_api(
    leave_request: LeaveApplicationModel, current_user: dict = Depends(get_current_user)
):
    email = current_user["email"]

    leave_request_dict = leave_request.dict(by_alias=True)
    validate_new_leave(email, leave_request_dict)

    return_data = new_leave_request(email, leave_request_dict)

    if return_data is None:
        raise HTTPException(status_code=404, detail="Leave Request not created")
    return return_data
