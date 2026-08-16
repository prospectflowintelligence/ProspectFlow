from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
    pass


# Import models here so Alembic's autogenerate can discover them via
# Base.metadata. Keep this list in sync with app/models/.
from app.models.organization import Organization, OrganizationMembership  # noqa: E402,F401
from app.models.user import User  # noqa: E402,F401
