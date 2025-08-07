from sqlalchemy.orm import Session
from app.models.cuentas import Cuenta

async def notify_linked_clients(shipment: Shipment, db: Session, event_type: str):
    """
    Notifica por correo a los usuarios vinculados al cliente (vendor) del embarque,
    según sus preferencias de notificación y el tipo de evento.
    """
    # Buscar la cuenta del vendor
    cuenta = db.query(Cuenta).filter(Cuenta.nombre_cuenta == shipment.vendor).first()
    if not cuenta:
        print(f"No se encontró la cuenta para vendor: {shipment.vendor}")
        return

    # Buscar los usuarios vinculados a esta cuenta
    user_links = db.query(UserClient).filter(UserClient.client_id == cuenta.id).all()
    user_ids = [ul.user_id for ul in user_links]
    users = db.query(User).filter(User.id.in_(user_ids)).all()

    # Filtrar usuarios con preferencia activa para el evento
    recipients = [u for u in users if u.notifications and u.notifications.get(event_type)]
    if not recipients:
        print(f"No hay usuarios con notificación activa para '{event_type}' en la cuenta {cuenta.nombre_cuenta}")
        return

    # Diccionario para descripciones amigables de los eventos
    event_descriptions = {
        "end_trip": "Entrega Finalizada",
        "onroad_trip": "Embarque en ruta",
        "evidence_pf": "Carga de evidencia",
    }
    
    # Obtener descripción amigable o usar el event_type si no está definido
    event_desc = event_descriptions.get(event_type, event_type)

    # Preparar asunto y mensaje
    subject = f"Notificación de embarque: {event_desc}"
    # Importar enums
    from app.models.shipment import ShipmentStatus, ShipmentSubstatus
    from app.models.order import OrderStatus, order_Substatus

    def enum_to_str(val):
        if val is None:
            return ""
        # Si es instancia de Enum, usar su valor
        if isinstance(val, (ShipmentStatus, ShipmentSubstatus, OrderStatus, order_Substatus)):
            return val.value
        val_str = str(val)
        # Si es string igual a algún valor de los enums, devolver ese valor
        for enum_cls in [ShipmentStatus, ShipmentSubstatus, OrderStatus, order_Substatus]:
            try:
                for e in enum_cls:
                    if val_str == e.name or val_str == e.value or val_str == f"{enum_cls.__name__}.{e.name}":
                        return e.value
            except Exception:
                pass
        # Si no, devolver el string limpio
        if "." in val_str:
            return val_str.split(".")[-1]
        return val_str

    if event_type == "end_trip":
        # Construir detalle de órdenes en HTML
        ordenes_detalle = ""
        for orden in getattr(shipment, 'orders', []):
            estado_orden = enum_to_str(getattr(orden, 'Order_status', ''))
            ordenes_detalle += f"<li><b>Orden:</b> {getattr(orden, 'Order_number', '')}  | <b>Estado:</b> {estado_orden} | <b>Dirección:</b> {getattr(orden, 'address', '')}</li>"
        message = (
            f"<p><b>El embarque {shipment.reference} ha sido FINALIZADO.</b></p>"
            f"<p><b>Detalles del embarque:</b><br>"
            f"<b>Cliente:</b> {shipment.customer}<br>"
            f"<b>Destino:</b> {getattr(shipment, 'destination', '')}<br>"
            f"<b>Camión:</b> {shipment.Truck}<br>"
            f"<b>Chofer:</b> {getattr(shipment, 'driver', '')}<br>"
            f"<b>Subestado:</b> {enum_to_str(getattr(shipment, 'Substatus', ''))}</p>"
            f"<p><b>Órdenes entregadas:</b></p><ul>{ordenes_detalle}</ul>"
        )
    elif event_type == "onroad_trip":
        message = f"<p>El embarque <b>{shipment.reference}</b>, Truck <b>{shipment.Truck}</b> está <b>EN RUTA</b>.</p>"
    elif event_type == "evidence_pf":
        message = f"<p>Se ha subido una evidencia PDF al embarque <b>{shipment.reference}</b>, Identificador (Truck): <b>{shipment.Truck}</b></p>"
    else:
        message = f"<p>Actualización del embarque <b>{shipment.reference}</b>.</p>"

    # Enviar correo a todos los destinatarios
    for user in recipients:
        await send_email_with_attachment(
            recipient_email=user.email,
            subject=subject,
            message_body=message
        )
        print(f"Correo enviado a {user.email} para evento {event_type}")
