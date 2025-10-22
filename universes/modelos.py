from sqlalchemy import (Column, Integer, String, Text, DateTime, func)
from sqlalchemy.orm import relationship
from database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    pass

class Universo(Base):
    __tablename__ = 'universos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False, unique=True)
    resumo = Column(Text)
    criado = Column(DateTime, default=func.now())
    alterado = Column(DateTime, default=func.now(), onupdate=func.now())
    textos =relationship('Texto', back_populates='universo')