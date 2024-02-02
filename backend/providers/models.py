from sqlalchemy import JSON, Boolean, Column, Date, ForeignKey, Integer, String, SmallInteger, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


providers_tags = Table(
    "providers_tags",
    Base.metadata,
    Column("providers", ForeignKey("providers.id"), primary_key=True),
    Column("tags", ForeignKey("tags.id"), primary_key=True),
)

class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)

    prividers: Mapped[list["Providers"]] = relationship(secondary=providers_tags, back_populates="tags")

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

    tags: Mapped[list["Tags"]] = relationship(secondary=providers_tags, back_populates="providers")

    def __str__(self):
        return f"Provider {self.name}"
