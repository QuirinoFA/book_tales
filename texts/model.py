from ..database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from universes import Universo

class Texto(Base):
    __tablename__ = 'textos'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(255), nullable=False, unique=True)
    texto = Column(Text)
    criado = Column(DateTime, default=func.now())
    alterado = Column(DateTime, default=func.now(), onupdate=func.now())
    uni_id = Column(Integer, ForeignKey('universos.id'))
    universo = relationship('Universo', back_populates='textos')
