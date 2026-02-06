from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from ..json.roles import RoleScheme


class Role(Base):

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)
    role_value = Column(Integer, nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow(),
                        nullable=False, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, default=None, nullable=True)

    def json_scheme(self) -> RoleScheme:
        scheme = RoleScheme(
            id=self.id,
            name=self.name,
            role_value=self.role_value,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at)

        return scheme
