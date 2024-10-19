from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from models.base import Base

class Template(Base):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    client_uuid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    path = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
