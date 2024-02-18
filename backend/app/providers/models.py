from sqlalchemy import JSON, Boolean, Column, Date, ForeignKey, Integer, String, SmallInteger, Table, true
from sqlalchemy.orm import relationship, Mapped, registry, configure_mappers, mapped_column

from app.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)

    providers = relationship(
        "Provider", secondary="providers_tags", back_populates="tags")

    def __str__(self):
        return f"Tag {self.name}"


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(length=256), nullable=False)
    foundation_date = Column(Date, nullable=True)
    registration_date = Column(Date, nullable=False)
    rating = Column(SmallInteger, nullable=True, default=0)
    verified = Column(Boolean, nullable=False, default=False)
    location = Column(String, nullable=False)
    image_id = Column(Integer)

    tags = relationship("Tag", secondary="providers_tags",
                        back_populates="providers")
    users = relationship("User", back_populates="providers")

    def __str__(self):
        return f"Provider {self.name}"


class ProviderTag(Base):
    __tablename__ = "providers_tags"

    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), primary_key=True)
