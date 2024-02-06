from sqlalchemy import JSON, Boolean, Column, Date, ForeignKey, Integer, String, SmallInteger, Table
from sqlalchemy.orm import relationship, Mapped, registry, configure_mappers, mapped_column

from app.database import Base


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)

    providers = relationship(
        "Providers", secondary="providers_tags", back_populates="tags")

    def __str__(self):
        return f"Tag {self.name}"


class Providers(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=256), nullable=False)
    foundation_date = Column(Date, nullable=True)
    registration_date = Column(Date, nullable=False)
    rating = Column(SmallInteger, nullable=True, default=0)
    verified = Column(Boolean, nullable=False, default=False)
    location = Column(String, nullable=False)
    image_id = Column(Integer)

    tags = relationship("Tags", secondary="providers_tags",
                        back_populates="providers")

    def __str__(self):
        return f"Provider {self.name}"


class ProvidersTags(Base):
    __tablename__ = "providers_tags"

    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), primary_key=True)
