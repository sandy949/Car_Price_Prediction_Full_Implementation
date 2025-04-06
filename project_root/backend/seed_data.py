import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import SessionLocal
from project_root.backend.db_models import Car

dummy_cars = [
    {
        "year": 2013,
        "manufacturer": "ford",
        "model": "f-150 xlt",
        "condition": "excellent",
        "cylinders": "6 cylinders",
        "fuel": "gas",
        "odometer": 128000.0,
        "transmission": "automatic",
        "drive": "rwd",
        "size": "full-size",
        "type": "truck",
        "paint_color": "black"
    },
    {
        "year": 2015,
        "manufacturer": "toyota",
        "model": "corolla",
        "condition": "good",
        "cylinders": "4 cylinders",
        "fuel": "gas",
        "odometer": 89000.0,
        "transmission": "automatic",
        "drive": "fwd",
        "size": "compact",
        "type": "sedan",
        "paint_color": "white"
    }
]

db = SessionLocal()

for car_data in dummy_cars:
    car = Car(**car_data)
    db.add(car)

db.commit()
db.close()
