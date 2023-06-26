from sqlalchemy import create_engine
from base import Base

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)
