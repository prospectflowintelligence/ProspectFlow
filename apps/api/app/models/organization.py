import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OrgRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class Organization(Base):
    """Tenant root. Every tenant-owned object must trace back to one of these."""

    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    memberships: Mapped[list["OrganizationMembership"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )


class OrganizationMembership(Base):
    """Join table: which users belong to which org, and with what role.

    This is the enforcement point for tenant isolation — every
    tenant-scoped query in the service layer should filter through a
    user's memberships, never trust an org_id passed straight from the
    client without checking membership first.
    """

    __tablename__ = "organization_memberships"
    __table_args__ = (UniqueConstraint("user_id", "organization_id", name="uq_user_org"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[OrgRole] = mapped_column(Enum(OrgRole, name="org_role"), default=OrgRole.MEMBER, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="memberships")  # noqa: F821
    organization: Mapped["Organization"] = relationship(back_populates="memberships")
