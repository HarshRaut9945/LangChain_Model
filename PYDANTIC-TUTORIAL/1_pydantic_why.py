import re
from typing import List, Dict, Optional, Annotated

from pydantic import BaseModel, Field, ValidationError, field_validator,model_validator


class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='name of the patient', description='Give the name of the patient', examples=['Nitish', 'Amit'])]
    email: str = Field(..., description='Patient email address')
    age: int = Field(gt=0, lt=120)
    weight: float = Field(ge=0)
    married: Optional[bool] = Field(default=None, description='Is the patient married?')
    allergies: Optional[List[str]] = Field(default=None, max_length=5)
    contact_details: Dict[str, str]


    @field_validator('email')
    @classmethod
    def email_validator(cls, value: str) -> str:
        if not isinstance(value, str) or '@' not in value:
            raise ValueError('Email must be a valid string containing @')

        username, domain_name = value.rsplit('@', 1)
        valid_domains = ['hdfc.com', 'icici.com']
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if not re.match(email_regex, value):
            raise ValueError('Invalid email format')

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value.lower()
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value: str) -> str:
        return value.strip().title()
    

    @model_validator(mode='after')
    def validate_emergency_conntact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('patient older than 60 must have an emergency contact')
        
        return model




def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.weight)
    print(patient.contact_details)
    print('inserted')


if __name__ == '__main__':
    patient_info = {
        'name': 'nitish',
        'email': 'abc@hdfc.com',
        'age': 30,
        'weight': 12.5,
        'married': True,
        'allergies': ['pollen', 'dust'],
        'contact_details': {
            'email': 'abc@hdfc.com',
            'phone': '1234678'
        }
    }

    try:
        patient1 = Patient(**patient_info)
    except ValidationError as error:
        print('Validation failed:')
        print(error)
    else:
        insert_patient_data(patient1)