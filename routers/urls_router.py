from fastapi import APIRouter, HTTPException, Depends

from utils import get_current_user
from ims_api_utils import (
    get_user_profile,
    get_bank_details,
    get_gpa_data,
    get_courses_data,
    get_attendance_data,
    get_attendance_for_course,
    get_leave_requests,
)

router = APIRouter()


@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]
    profile = get_user_profile(email)

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/bank_details")
async def get_bank_details_api(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]
    bank_details = get_bank_details(email)

    if bank_details is None:
        raise HTTPException(status_code=404, detail="Bank Details not found")
    return bank_details


@router.get("/transcript")
async def get_transcript(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]

    gpa_data = get_gpa_data(email)
    courses_data = get_courses_data(email)

    if gpa_data is None or courses_data is None:
        raise HTTPException(status_code=404, detail="Transcript not found")

    return {"gpa": gpa_data, "courses": courses_data}


@router.get("/courses")
async def get_courses_api(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]
    courses_data = get_courses_data(email)

    if courses_data is None:
        raise HTTPException(status_code=404, detail="Courses not found")
    return courses_data


@router.get("/attendance")
async def get_attendance_api(current_user: dict = Depends(get_current_user)):
    email = current_user["email"]
    attendance_data = get_attendance_data(email)

    if attendance_data is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance_data


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