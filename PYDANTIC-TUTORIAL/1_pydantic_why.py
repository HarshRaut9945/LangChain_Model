from pydantic import BaseModel
from typing import List,Dict,Optional


class Patient(BaseModel):
    name: str
    age: int
    weight:float
    married:bool
    allergies: Optional[List[str]]=None
    contact_details:Dict[str,str]



def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.contact_details)
    print('inserted')


patient_info = {
    'name': 'nitish',
    'age': 30,
    'weight': 12.5,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'email': 'abc@gmail.com',
        'phone': '1234678'
    }
}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)