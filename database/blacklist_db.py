from . import MongoDB


class Blacklist:
    """Class to manage database for blacklists for chats."""

    def __init__(self) -> None:
        self.collection = MongoDB("blacklists")

    async def add_blacklist(self, chat_id: int, trigger: str):
        curr = await self.collection.find_one({"chat_id": chat_id})
        if curr:
            triggers_old = curr["triggers"]
            triggers_old.append(trigger)
            triggers = list(dict.fromkeys(triggers_old))
            return await self.collection.update(
                {"chat_id": chat_id},
                {
                    "chat_id": chat_id,
                    "triggers": triggers,
                },
            )
        return await self.collection.insert_one(
            {
                "chat_id": chat_id,
                "triggers": [trigger],
                "action": "mute",
            },
        )

    async def remove_blacklist(self, chat_id: int, trigger: str):
        curr = await self.collection.find_one({"chat_id": chat_id})
        if curr:
            triggers_old = curr["triggers"]
            try:
                triggers_old.remove(trigger)
            except ValueError:
                return False
            triggers = list(dict.fromkeys(triggers_old))
            return await self.collection.update(
                {"chat_id": chat_id},
                {
                    "chat_id": chat_id,
                    "triggers": triggers,
                },
            )

    async def get_blacklists(self, chat_id: int):
        curr = await self.collection.find_one({"chat_id": chat_id})
        if curr:
            return curr["triggers"]
        return []

    async def count_blacklists_all(self):
        curr = await self.collection.find_all()
        num = 0
        for chat in curr:
            num += len(chat["triggers"])
        return num

    async def count_blackists_chats(self):
        curr = await self.collection.find_all()
        num = 0
        for chat in curr:
            if chat["triggers"]:
                num += 1
        return num

    async def set_action(self, chat_id: int, action: int):

        if action not in ("kick", "mute", "ban", "warn"):
            return "invalid action"

        curr = await self.collection.find_one({"chat_id": chat_id})
        if curr:
            return await self.collection.update(
                {"chat_id": chat_id},
                {"chat_id": chat_id, "action": action},
            )
        return await self.collection.insert_one(
            {
                "chat_id": chat_id,
                "triggers": [],
                "action": action,
            },
        )

    async def get_action(self, chat_id: int):
        curr = await self.collection.find_one({"chat_id": chat_id})
        if curr:
            return curr["action"] or "mute"
        await self.collection.insert_one(
            {
                "chat_id": chat_id,
                "triggers": [],
                "action": "mute",
            },
        )
        return "mute"

    async def rm_all_blacklist(self, chat_id: int):
        curr = await self.collection.find_one({"chat_id": chat_id})
        if curr:
            await self.collection.update(
                {"chat_id": chat_id},
                {"triggers": []},
            )
        return False

    # Migrate if chat id changes!
    async def migrate_chat(self, old_chat_id: int, new_chat_id: int):
        old_chat = await self.collection.find_one({"chat_id": old_chat_id})
        if old_chat:
            return await self.collection.update(
                {"chat_id": old_chat_id},
                {"chat_id": new_chat_id},
            )
        return
