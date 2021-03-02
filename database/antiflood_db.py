from . import MongoDB


class AntiFlood:
    """Class for managing antiflood in groups."""

    def __init__(self) -> None:
        self.collection = MongoDB("antiflood")

    async def get_grp(self, chat_id: int):
        return await self.collection.find_one({"chat_id": chat_id})

    async def set_status(self, chat_id: int, status: bool = False):
        if await self.get_grp(chat_id):
            return await self.collection.update(
                {"chat_id": chat_id},
                {"status": status},
            )
        return await self.collection.insert_one({"chat_id": chat_id, "status": status})

    async def get_status(self, chat_id: int):
        z = await self.get_grp(chat_id)
        if z:
            return z["status"]
        return

    async def set_antiflood(self, chat_id: int, max_msg: int):
        if await self.get_grp(chat_id):
            return await self.collection.update(
                {"chat_id": chat_id},
                {"max_msg": max_msg},
            )
        return await self.collection.insert_one(
            {"chat_id": chat_id, "max_msg": max_msg},
        )

    async def get_antiflood(self, chat_id: int):
        z = await self.get_grp(chat_id)
        if z:
            return z["max_msg"]
        return

    async def set_action(self, chat_id: int, action: str = "kick"):

        if action not in ("kick", "ban", "mute"):
            action = "kick"  # Default action

        if await self.get_grp(chat_id):
            return await self.collection.update(
                {"chat_id": chat_id},
                {"action": action},
            )
        return await self.collection.insert_one({"chat_id": chat_id, "action": action})

    async def get_action(self, chat_id: int):
        z = await self.get_grp(chat_id)
        if z:
            return z["action"]
        return

    # Migrate if chat id changes!
    async def migrate_chat(self, old_chat_id: int, new_chat_id: int):
        old_chat = await self.collection.find_one({"chat_id": old_chat_id})
        if old_chat:
            return await self.collection.update(
                {"chat_id": old_chat_id},
                {"chat_id": new_chat_id},
            )
        return
