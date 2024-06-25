from pydantic import BaseModel, Field
from typing import Optional


class BankModel(BaseModel):
    selectBank: str
    rollNumber: int
    accountHolderName: str
    accountNumber: str
    bankName: Optional[str] = Field(None)
    branchName: Optional[str] = Field(None)
    ifscCode: Optional[str] = Field(None)
    bankAddress: Optional[str] = Field(None)
    remarks: Optional[str] = Field(None)
    base64Data: str
    recordID: Optional[str] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "selectBank": "SBI",
                "rollNumber": 2022101005,
                "accountHolderName": "John Doe",
                "accountNumber": "9876543210",
                "bankName": "ABC Bank",
                "branchName": "Main Branch",
                "ifscCode": "QWERTY51656516",
                "bankAddress": "123 Main St, Cityville",
                "remarks": "Lorem ipsum dolor sit amet.",
                "base64Data": "base64_content_of_selected_file",
                "recordID": "ABCD123"
            }
        }
