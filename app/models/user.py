from pydantic import BaseModel

class register(BaseModel):
    full_name: str
    dni : str
    password: str
    confirm_password: str

class login(BaseModel):
    dni: str
    password: str

class transferencias(BaseModel):
    numero_cuenta_enviar : str
    numero_cuenta_recibe : str
    cantidad_dinero : int

class historial(BaseModel):
    numero_cuenta : str