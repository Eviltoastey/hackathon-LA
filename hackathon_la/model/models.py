from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from hackathon_la.model import Base
from hackathon_la.model.mixin import IDMixin, DateMixin


class Car(Base, IDMixin, DateMixin):
    __tablename__ = 'car'

    fuel_level = Column(Integer, nullable=False)

    # current location
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    # parking spot location
    parking_spot_lat = Column(Float, nullable=False)
    parking_spot_lon = Column(Float, nullable=False)

    booking = relationship('Booking', uselist=True, back_populates='car')


class Booking(Base, IDMixin, DateMixin):
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    car_id = Column(ForeignKey('car.id'), nullable=False)
    car = relationship('Car', uselist=False, back_populates='booking')
