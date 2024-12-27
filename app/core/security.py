from jose import JWTError, jwt
import datetime
from fastapi import HTTPException
from app.database.connection import get_db_connection

ALGORITHM = 'HS256'
SECRET_KEY = "tu_clave_secreta_aqui"  # Deberías mover esto a variables de entorno en producción

# Función para crear el token
def create_jwt_token(user_id: int):
    # Obtener información adicional del usuario desde la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Obtener DNI y número de cuenta
        cursor.execute("SELECT dni, numero_cuenta FROM usuarios WHERE id = ?", (user_id,))
        user_info = cursor.fetchone()
        
        if not user_info:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        dni = user_info['dni']
        numero_cuenta = user_info['numero_cuenta']
        
        # Crear payload con más información
        payload = {
            'user_id': user_id,
            'dni': dni,
            'numero_cuenta': numero_cuenta,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)  # Expiración del token
        }
        
        # Codificar el payload y devolver el token
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    
    finally:
        cursor.close()
        connection.close()

# Función para decodificar el token
def decode_jwt_token(token: str):
    try:
        # Decodificar el token y obtener el payload
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")