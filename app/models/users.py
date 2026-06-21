from app.core.database import Base

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class User(Base):
    __tablename__="users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False) 
    role = Column(String, default="member" )
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))