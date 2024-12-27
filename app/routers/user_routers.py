from app.core.security import create_jwt_token, decode_jwt_token
from fastapi import APIRouter, HTTPException, Header, Depends
from app.models.user import register, login, transferencias, historial
from app.database.connection import get_db_connection
import bcrypt
import random
from datetime import datetime

router = APIRouter()

@router.post("/register")
async def register_user(register: register):
    if register.password != register.confirm_password:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    hashed_password = bcrypt.hashpw(register.password.encode('utf-8'), bcrypt.gensalt())

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE dni = ?", (register.dni,))
    existing_user = cursor.fetchone()

    if existing_user:
        raise HTTPException(status_code=400, detail="El DNI ya esta registrado")

    serie_fija = "009"  # Serie fija de 3 dígitos
    digitos_aleatorios = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # 6 dígitos aleatorios
    numero_cuenta = serie_fija + digitos_aleatorios

    try:
        cursor.execute("INSERT INTO usuarios (full_name, dni, password, numero_cuenta, cantidad_dinero) VALUES (?, ?, ?, ?, ?)", 
                      (register.full_name, register.dni, hashed_password, numero_cuenta, 0))
        connection.commit()
        return {"message": "Usuario registrado correctamente", "Su Numero De Cuenta Es ": numero_cuenta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

@router.post("/login")
async def login_user(login : login):
    dni = login.dni
    password = login.password
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM usuarios WHERE dni = ?", (dni,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        token = create_jwt_token(user['id'])
        return {"message": "Login exitoso", "token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado.")
    
    token = authorization.split(" ")[1]  # Formato "Bearer <token>"
    user_data = decode_jwt_token(token)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Token inválido o expirado.")
    
    return user_data  # Retorna el diccionario con datos del usuario, incluyendo el dni

@router.post("/transferencias")
async def transfer_funds(data: transferencias, authorization: str = Header(None), current_user: dict = Depends(get_current_user)):
    # Extraer la información del usuario autenticado (dni)
    user_dni = current_user["dni"]
    user_numero_cuenta = current_user["numero_cuenta"]
    
    if data.numero_cuenta_enviar != user_numero_cuenta:
        raise HTTPException(status_code=400, detail="No puedes realizar transferencias desde una cuenta que no es tuya.")
    
    # Conexión a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Verificar la cuenta que envía los fondos
        cursor.execute("SELECT id, numero_cuenta, cantidad_dinero FROM usuarios WHERE numero_cuenta = ?", (data.numero_cuenta_enviar,))
        user_data = cursor.fetchone()

        if not user_data:
            raise HTTPException(status_code=400, detail="Número de cuenta del remitente incorrecto.")
        
        user_id, user_numero_cuenta, user_cantidad_dinero = user_data

        if user_cantidad_dinero < data.cantidad_dinero:
            raise HTTPException(status_code=400, detail="Fondos insuficientes en la cuenta del remitente.")

        # Verificar la cuenta que recibe los fondos
        cursor.execute("SELECT id, numero_cuenta FROM usuarios WHERE numero_cuenta = ?", (data.numero_cuenta_recibe,))
        recibir_data = cursor.fetchone()

        if not recibir_data:
            raise HTTPException(status_code=400, detail="Número de cuenta del destinatario incorrecto.")

        recibir_id, recibir_numero_cuenta = recibir_data

        if data.numero_cuenta_enviar == data.numero_cuenta_recibe:
            raise HTTPException(status_code=400, detail="No puedes transferir fondos a la misma cuenta.")
        
        if data.cantidad_dinero <= 0:
            raise HTTPException(status_code=400, detail="No puedes transferir una cantidad de dinero igual o menor a 0")

        # Actualizar los saldos de ambas cuentas
        cursor.execute("UPDATE usuarios SET cantidad_dinero = cantidad_dinero - ? WHERE numero_cuenta = ?", (data.cantidad_dinero, data.numero_cuenta_enviar,))
        cursor.execute("UPDATE usuarios SET cantidad_dinero = cantidad_dinero + ? WHERE numero_cuenta = ?", (data.cantidad_dinero, data.numero_cuenta_recibe,))
        now = datetime.now()

        # Guardar fecha y hora en una sola variable
        fecha_y_hora = now.strftime("%Y-%m-%d %H:%M:%S") # Formato: YYYY-MM-DD HH:MM:SS
        cursor.execute("INSERT INTO historial (user_id, cuenta_usuario, cuenta_receptor, cantidad_dinero_enviada, fecha_enviado) VALUES (?, ?, ?, ?, ?)", 
                      (user_id, data.numero_cuenta_enviar, data.numero_cuenta_recibe, data.cantidad_dinero, fecha_y_hora,))
        connection.commit()

        return {"status": "Transferencia exitosa", "numero_cuenta_enviar": data.numero_cuenta_enviar, "numero_cuenta_recibe": data.numero_cuenta_recibe}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        connection.close()

@router.post("/historial")
async def check_history(data: historial, authorization: str = Header(None), current_user: dict = Depends(get_current_user)):
    # Extraer la información del usuario autenticado (dni)
    user_dni = current_user["dni"]
    user_numero_cuenta = current_user["numero_cuenta"]
    
    if data.numero_cuenta != user_numero_cuenta:
        raise HTTPException(status_code=400, detail="No Revisar El Historial De Otra Persona")
    
    # Conexión a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Verificar la cuenta que envía los fondos
        cursor.execute("SELECT numero_cuenta FROM usuarios WHERE numero_cuenta = ?", (data.numero_cuenta,))
        user_data = cursor.fetchone()

        if not user_data:
            raise HTTPException(status_code=400, detail="Número de cuenta No Encontrado.")
        
        user_numero_cuenta = user_data
        
        # Verificar la cuenta que envía los fondos
        cursor.execute("SELECT cuenta_usuario, cuenta_receptor, cantidad_dinero_enviada, fecha_enviado FROM historial WHERE cuenta_usuario = ?", (data.numero_cuenta,))
        history_data = cursor.fetchall()  # Cambiar fetchone a fetchall

        if not history_data:
            raise HTTPException(status_code=404, detail="No se encontró historial para esta cuenta.")

        # Crear una lista de resultados
        result = []
        for record in history_data:
            cuenta_usuario, cuenta_receptor, cantidad_dinero_enviada, fecha_enviado = record
            result.append({
                "Tu Cuenta": cuenta_usuario,
                "Numero De Cuenta Receptor": cuenta_receptor,
                "Cantidad De Dinero Enviada": cantidad_dinero_enviada,
                "Fecha Envio": fecha_enviado
            })

        return {"status": "Historiales Encontrados", "historial": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        connection.close()