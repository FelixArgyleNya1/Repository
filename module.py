from hikka import hikka, filters

@hikka.on_message(filters.command('user'))
async def user_info_command(client, message):
    try:
        user_id = int(message.text.split(' ', 1)[1])
    except (IndexError, ValueError):
        await message.reply("Будь ласка, вкажіть коректний ID користувача.")
        return

    try:
        user = await client.get_users(user_id)
        user_info = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'phone': user.phone if user.phone else "Немає",
            'bio': user.bio if user.bio else "Немає"
        }

        dialogs = await client.get_dialogs()
        public_chats = [dialog.name for dialog in dialogs if dialog.is_group]

        user_info_str = (f"ID: {user_info['id']}\n"
                         f"First Name: {user_info['first_name']}\n"
                         f"Last Name: {user_info['last_name']}\n"
                         f"Username: {user_info['username']}\n"
                         f"Phone: {user_info['phone']}\n"
                         f"Bio: {user_info['bio']}")

        public_chats_str = "\n".join(public_chats) if public_chats else "Не знайдено публічних чатів"

        await message.reply(f"User Info:\n{user_info_str}\n\nPublic Chats:\n{public_chats_str}")

    except Exception as e:
        await message.reply(f"Не вдалося отримати інформацію про користувача: {str(e)}")
