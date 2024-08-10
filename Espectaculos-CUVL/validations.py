from datetime import datetime

def validate_usuario(nombre, email):
    if not nombre or not email:
        return 'Todos los campos son obligatorios.'
    
    return None

def validate_espectaculo(nombre, descripcion, fecha, sala):
    if not nombre or not descripcion or not fecha or not sala:
        return 'Todos los campos son obligatorios.'
    
    if fecha <= datetime.now():
        return 'La fecha del espectáculo debe ser en el futuro.'
    return None

def validate_reserva(usuario_id, espectaculo_id):
    if not usuario_id or not espectaculo_id:
        return 'Debe seleccionar un usuario y un espectáculo.'
    return None
