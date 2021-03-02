from datetime import datetime

from . import MongoDB


class GBan:
    """Class for managing Gbans in bot."""

    def __init__(self) -> None:
        self.collection = MongoDB("gbans")

    async def check_gban(self, user_id: int):
        return bool(await self.collection.find_one({"user_id": user_id}))

    async def add_gban(self, user_id: int, reason: str, by_user: int):

        # Check if  user is already gbanned or not
        if await self.collection.find_one({"user_id": user_id}):
            return await self.update_gban_reason(user_id, reason)

        # If not already gbanned, then add to gban
        time_rn = datetime.now()
        return await self.collection.insert_one(
            {"user_id": user_id, "reason": reason, "by": by_user, "time": time_rn},
        )

    async def remove_gban(self, user_id: int):
        # Check if  user is already gbanned or not
        if await self.collection.insert_one({"user_id": user_id}):
            return await self.collection.delete_one({"user_id": user_id})
        return

    async def update_gban_reason(self, user_id: int, reason: str):
        return await self.collection.update(
            {"user_id": user_id},
            {"reason": reason},
        )

    async def count_gbans(self):
        return await self.collection.count()

    async def list_gbans(self):
        return await self.collection.find_all()
