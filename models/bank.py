from pydantic import BaseModel
from typing import Optional


class BankModel(BaseModel):
    rollNumber: int
    accountHolderName: str
    accountNumber: int
    bankName: str
    branchName: str
    ifscCode: str
    bankAddress: str
    remarks: Optional[str] = None
    base64Data: str

    class Config:
        json_schema_extra = {
            "example": {
                "rollNumber": 2022101005,
                "accountHolderName": "John Doe",
                "accountNumber": 9876543210,
                "bankName": "ABC Bank",
                "branchName": "Main Branch",
                "ifscCode": "QWERTY51656516",
                "bankAddress": "123 Main St, Cityville",
                "remarks": "Lorem ipsum dolor sit amet.",
                "base64Data": "base64_content_of_selected_file"
            }
        }
