from pydantic import BaseModel, Field
from typing import Optional


class BankModel(BaseModel):
    selectBank: str 
    rollNumber: int
    accountHolderName: str
    accountNumber: str
    bankName: str = Field(None, alias="bankName")
    branchName: str = Field(None, alias="branchName")
    ifscCode: str = Field(None, alias="ifscCode")
    bankAddress: str = Field(None, alias="bankAddress")
    remarks: str  =  Field(None, alias="remarks")
    base64Data: str

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
                "base64Data": "base64_content_of_selected_file"
            }
        }
