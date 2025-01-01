from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/transport"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class TransportType(Base):
    __tablename__ = 'transport_types'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    average_speed = Column(Float, nullable=False)
    fuel_consumption = Column(Float, nullable=False)  
    vehicle_count = Column(Integer, nullable=False)  
    routes = relationship("Route", back_populates="transport_type")

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True, index=True)
    route_number = Column(String, nullable=False)
    daily_passenger_count = Column(Integer, nullable=False)
    fare = Column(Float, nullable=False) 
    vehicles_on_route = Column(Integer, nullable=False)  
    transport_type_id = Column(Integer, ForeignKey('transport_types.id'), nullable=False)
    transport_type = relationship("TransportType", back_populates="routes")
    path = relationship("Path", back_populates="route", uselist=False)

class Path(Base):
    __tablename__ = 'paths'
    id = Column(Integer, primary_key=True, index=True)
    start_point = Column(String, nullable=False)
    end_point = Column(String, nullable=False)
    stops_count = Column(Integer, nullable=False)  
    distance = Column(Float, nullable=False)  
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=False)
    route = relationship("Route", back_populates="path")
    
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
