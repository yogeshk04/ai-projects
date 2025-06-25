import re
from pydantic import BaseModel, Field, field_validator

class DateTimeModel(BaseModel):
    date: str = Field(description="Date format:", pattern=r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$")

    @field_validator("date")
    def validate_date(cls, value):
        if not re.match(r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$", value):
            raise ValueError("Date must be in the format DD-MM-YYYY HH:MM")
        return value
    
class DateModel(BaseModel):
    date: str = Field(description="Date format:", pattern=r"^\d{2}-\d{2}-\d{4}$")

    @field_validator("date")
    def validate_date(cls, value):
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", value): # ensure the date is in the correct format
            raise ValueError("Date must be in the format DD-MM-YYYY")
        return value
        
class IdentificationNumberModel(BaseModel):
    id: int = Field(description="Identification number must be a positive integer and 7 or 8 digits long", ge=1)
    @field_validator("id")
    def validate_id(cls, value):
        if not re.match(r"^\d{7,8}$", str(value)): # Convert to string before matching
            raise ValueError("ID must be a 7 or 8 digit positive integer")
        return value
            
            