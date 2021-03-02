import motor.motor_asyncio

from .. import DB_URI

# Client to connect to mongodb
mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)

db = mongodb_client.ultroid_userbot


class MongoDB:
    """Class for interacting with Bot database."""

    def __init__(self, collection) -> None:
        self.collection = db[collection]

    # Insert one entry into collection
    async def insert_one(self, document):
        result = await self.collection.insert_one(document)
        return repr(result.inserted_id)

    # Find one entry from collection
    async def find_one(self, query):
        result = await self.collection.find_one(query)
        if result:
            return result
        return False

    # Find entries from collection
    async def find_all(self, query={}):
        lst = []
        async for document in self.collection.find(query):
            lst.append(document)
        return lst

    # Count entries from collection
    async def count(self, query={}):
        return await self.collection.count_documents(query)

    # Delete entry/entries from collection
    async def delete_one(self, query):
        before_delete = await self.collection.count_documents({})
        await self.collection.delete_many(query)
        after_delete = await self.collection.count_documents({})
        return after_delete

    # Replace one entry in collection
    async def replace(self, query, new_data):
        old = await self.collection.find_one(query)
        _id = old["_id"]
        await self.collection.replace_one({"_id": _id}, new_data)
        new = await self.collection.find_one({"_id": _id})
        return old, new

    # Update one entry from collection
    async def update(self, query, update):
        result = await self.collection.update_one(query, {"$set": update})
        new_document = await self.collection.find_one(query)
        return result.modified_count, new_document

    # Close connection
    async def close():
        return mongodb_client.close()
