import jwt
import datetime

SECRET_KEY = "your-secret-key"  # Use the same key from jwt_utils.py

token = jwt.encode(
    {
        "sub": 1,  # Replace with your user ID from the database
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    },
    SECRET_KEY,
    algorithm="HS256"
)

print(token)
