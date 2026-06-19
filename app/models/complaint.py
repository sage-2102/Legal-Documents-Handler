from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    client_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    preferred_lawyer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    category = Column(
        String,
        nullable=False
    )

    urgency = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="Pending"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )