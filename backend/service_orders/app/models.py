from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .database import Base


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID)
    # ЗАМЕНЯЕМ items на поля для дефектов
    defect_description = Column(String)
    defect_location = Column(String)
    defect_type = Column(String)
    defect_priority = Column(String)
    responsible_person = Column(String)
    status = Column(String, default="created")
    # Используем severity_level вместо total_amount
    severity_level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)