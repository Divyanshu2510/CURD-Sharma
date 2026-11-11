from sqlalchemy import Integer,String,Date,Enum
from sqlalchemy.orm import Mapped,mapped_column

from db import Base

class User(Base):
    __tablename__ ='user'
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    phone:Mapped[str]=mapped_column(String(100))