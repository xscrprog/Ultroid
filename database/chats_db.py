from . import MongoDB


class Chats:
    """Class to manage users for bot."""

    def __init__(self) -> None:
        self.collection = MongoDB("chats")

    async def remove_chat(self, chat_id: int):
        await self.collection.delete_one({"chat_id": chat_id})

    async def update_chat(self, chat_id: int, chat_name: str, user_id: int):
        curr = await self.collection.find_one({"chat_id": chat_id})
        if curr:
            return await self.collection.update(
                {"chat_id": chat_id},
                {"chat_id": chat_id, "chat_name": chat_name},
            )
        return await self.collection.insert_one(
            {"chat_id": chat_id, "chat_name": chat_name},
        )

    async def count_chats(self):
        return await self.collection.count()

    async def list_chats(self):
        chats = await self.collection.find_all()
        chat_list = []
        for chat in chats:
            chat_list.append(chat["chat_id"])
        return chat_list

    # Migrate if chat id changes!
    async def migrate_chat(self, old_chat_id: int, new_chat_id: int):
        old_chat = await self.collection.find_one({"chat_id": old_chat_id})
        if old_chat:
            return await self.collection.update(
                {"chat_id": old_chat_id},
                {"chat_id": new_chat_id},
            )
        return
