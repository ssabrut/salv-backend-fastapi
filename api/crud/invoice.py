from sqlalchemy.orm import Session
from db.models import invoice as InvoiceModel
import uuid


async def create(user_id: str, order_id: str, amount: int, db: Session):
    _uuid = str(uuid.uuid4())
    data = {"id": _uuid, "user_id": user_id, "order_id": order_id, "amount": amount}
    db_invoice = InvoiceModel.Invoice(**data)
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
