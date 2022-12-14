from aiogram import Router, types, Bot
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION


async def on_user_join(event: types.ChatMemberUpdated, bot: Bot):
    await bot.send_message(chat_id=event.chat.id,
                           text=f"Привет, {event.old_chat_member.user.full_name}!\n"
                                f"Ознакомься с <a href='#'>правилами</a>")


def register_handlers_group(router: Router):
    router.chat_member.register(on_user_join, ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    ))
