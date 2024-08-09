import uuid

from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func


class UUIDMixin:
    """UUID миксин для ID моделей"""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)


class TimestampedMixin:
    """Миксин для даты создания и даты обновления"""

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class SerializerMixin:
    """Миксин для преобразования данных модели в словарь"""

    def to_dict(self, include_relationships=False, depth=1) -> dict:
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

        def serialize_value(value, include_relationships, depth):
            if isinstance(value, list):
                return [serialize_value(item, include_relationships, depth-1) for item in value]
            elif isinstance(value, SerializerMixin):
                return value.to_dict(include_relationships, depth-1)
            return value

        if include_relationships and depth > 0:
            for relationship in inspect(self).mapper.relationships:
                value = getattr(self, relationship.key)
                data[relationship.key] = serialize_value(value, include_relationships, depth)

        return data


class SoftDeleteMixin:
    """Миксин для мягкого удаления"""

    @declared_attr
    def deleted(cls):
        return Column(Boolean, default=False, nullable=False)

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True)

    def soft_delete(self, session: Session):
        self.deleted = True
        self.deleted_at = func.now()
        session.add(self)

    @classmethod
    def apply_soft_delete_filter(cls, query):
        return query.filter_by(deleted=False)

    @classmethod
    def restore(cls, session: Session, instance_id):
        record = session.query(cls).filter_by(id=instance_id, deleted=True).first()
        if record:
            record.deleted = False
            record.deleted_at = None
            session.add(record)
