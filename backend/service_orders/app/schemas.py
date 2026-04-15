from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Dict

# УДАЛЯЕМ старый OrderItem и создаем новые схемы для дефектов

class OrderCreate(BaseModel):
    defect_description: str
    defect_location: str
    defect_type: str
    defect_priority: str
    responsible_person: str
    severity_level: int = 1

class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    defect_description: str
    defect_location: str
    defect_type: str
    defect_priority: str
    responsible_person: str
    severity_level: int
    status: str
    created_at: datetime
    updated_at: datetime

class OrderUpdate(BaseModel):
    status: str  
    # "created", "in_progress", "completed", "cancelled"