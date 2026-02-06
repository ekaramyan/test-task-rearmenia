from datetime import datetime
from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Computed
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .roles import Role
from ..json.roles import RoleScheme
from ..json.users import UserScheme


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)

    photo = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    tg = Column(String, nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow(),
                        nullable=False, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, default=None, nullable=True)

    role = relationship(argument=Role, lazy='selectin')

    def json_scheme(self) -> UserScheme:
        role: Role = self.role

        scheme = UserScheme(
            id=self.id,
            role=RoleScheme(
                id=role.id,
                name=role.name,
                role_value=role.role_value,
                created_at=role.created_at,
                updated_at=role.updated_at,
                deleted_at=role.deleted_at) if role is not None else None,
            photo=self.photo,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            login=self.login,
            phone=self.phone,
            tg=self.tg,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at)

        return scheme
