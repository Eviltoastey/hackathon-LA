import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


class IDMixin:
    """
    Add a UUID primary key to a model inheriting this class.
    """

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class DateMixin:
    """
    Add two datetime columns to a model for date administration on create and
    update queries.
    """

    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())
