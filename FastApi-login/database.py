from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://devmultiproyectos:dYYCl1Ei0G4wi2JQ@devmongodb.kmyny.mongodb.net/"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.user_db
user_collection = database.get_collection("users")

# Helpers
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "hashed_password": user["hashed_password"],
    }
