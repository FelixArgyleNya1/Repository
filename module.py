from .. import loader, utils

class UserInfoMod(loader.Module):
    """Get information about a user and their public chats"""
    strings = {"name": "UserInfo"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.owner
    async def usercmd(self, message):
        """Get user information and public chats"""
        args = utils.get_args(message)
        if len(args) != 1:
            await message.edit("<b>Usage: .user <user_id></b>")
            return

        user_id = args[0]

        # Get user information
        try:
            user_info = await self.client.get_users(user_id)
            user_info_str = (f"ID: {user_info.id}\n"
                             f"First Name: {user_info.first_name}\n"
                             f"Last Name: {user_info.last_name}\n"
                             f"Username: {user_info.username}\n"
                             f"Phone: {user_info.phone if user_info.phone else 'Not Available'}\n"
                             f"Bio: {user_info.bio if user_info.bio else 'Not Available'}")
        except Exception as e:
            user_info_str = f"Failed to get user info: {str(e)}"

        # Get public chats
        try:
            dialogs = await self.client.get_dialogs()
            public_chats = [dialog.name for dialog in dialogs if dialog.is_group]
            public_chats_str = "\n".join(public_chats) if public_chats else "No public chats found."
        except Exception as e:
            public_chats_str = f"Failed to get public chats: {str(e)}"

        # Send response
        response = f"User Info:\n{user_info_str}\n\nPublic Chats:\n{public_chats_str}"
        await message.reply(response)