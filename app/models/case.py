from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import Text

from app.db.database import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    complaint_id = Column(
        Integer,
        ForeignKey(
            "complaints.id"
        )
    )

    client_id = Column(
        Integer,
        ForeignKey(
            "users.id"
        )
    )

    lawyer_id = Column(
        Integer,
        ForeignKey(
            "users.id"
        )
    )

    status = Column(
        String,
        default="Open"
    )

    hearing_date = Column(
        Date,
        nullable=True
    )

    notes = Column(
        Text,
        nullable=True
    )