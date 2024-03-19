import asyncio
import logging

from aiogram.types import Message, ChatJoinRequest, ForumTopicCreated
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, F
from tortoise import Tortoise
from db.models import User

from config_reader import config


bot = Bot(
    config.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


@dp.chat_join_request(F.chat.id == int(config.CHANNEL_ID.get_secret_value()))
async def chat_join_handler(request: ChatJoinRequest):
    await User.create(
        name=request.from_user.full_name, username=request.from_user.username
    )
    await request.approve()


@dp.message(F.chat.id.in_(config.CHAT_IDS))
async def message_handler(message: Message):
    # print(message.message_thread_id)
    if message.text != None:
        ...
        # print(message.text)
        # print(await message.bot.create_forum_topic(message.chat.id, "test"))
        # await message.answer()
        # await bot.send_message(message.chat.id,message_thread_id=8,text="hello")

async def on_startup() -> None:
    await Tortoise.init(
        db_url=config.DB_URL.get_secret_value(),
        modules={"models": ["db.models"]},
    )
    await Tortoise.generate_schemas()


async def on_shutdown() -> None:
    await Tortoise.close_connections()


async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


{
    "message_id": 39,
    "date": datetime.datetime(2024, 3, 19, 20, 25, 47, tzinfo=TzInfo(UTC)),
    "chat": Chat(
        id=-1002140514296,
        type="supergroup",
        title="Manager Chat 1",
        username=None,
        first_name=None,
        last_name=None,
        is_forum=True,
        photo=None,
        active_usernames=None,
        available_reactions=None,
        accent_color_id=None,
        background_custom_emoji_id=None,
        profile_accent_color_id=None,
        profile_background_custom_emoji_id=None,
        emoji_status_custom_emoji_id=None,
        emoji_status_expiration_date=None,
        bio=None,
        has_private_forwards=None,
        has_restricted_voice_and_video_messages=None,
        join_to_send_messages=None,
        join_by_request=None,
        description=None,
        invite_link=None,
        pinned_message=None,
        permissions=None,
        slow_mode_delay=None,
        unrestrict_boost_count=None,
        message_auto_delete_time=None,
        has_aggressive_anti_spam_enabled=None,
        has_hidden_members=None,
        has_protected_content=None,
        has_visible_history=None,
        sticker_set_name=None,
        can_set_sticker_set=None,
        custom_emoji_sticker_set_name=None,
        linked_chat_id=None,
        location=None,
    ),
    "message_thread_id": 8,
    "from_user": User(
        id=653327229,
        is_bot=False,
        first_name="No",
        last_name=None,
        username="Cotovnika",
        language_code="en",
        is_premium=None,
        added_to_attachment_menu=None,
        can_join_groups=None,
        can_read_all_group_messages=None,
        supports_inline_queries=None,
    ),
    "sender_chat": None,
    "sender_boost_count": None,
    "forward_origin": None,
    "is_topic_message": True,
    "is_automatic_forward": None,
    "reply_to_message": Message(
        message_id=8,
        date=datetime.datetime(2024, 3, 19, 20, 14, 42, tzinfo=TzInfo(UTC)),
        chat=Chat(
            id=-1002140514296,
            type="supergroup",
            title="Manager Chat 1",
            username=None,
            first_name=None,
            last_name=None,
            is_forum=True,
            photo=None,
            active_usernames=None,
            available_reactions=None,
            accent_color_id=None,
            background_custom_emoji_id=None,
            profile_accent_color_id=None,
            profile_background_custom_emoji_id=None,
            emoji_status_custom_emoji_id=None,
            emoji_status_expiration_date=None,
            bio=None,
            has_private_forwards=None,
            has_restricted_voice_and_video_messages=None,
            join_to_send_messages=None,
            join_by_request=None,
            description=None,
            invite_link=None,
            pinned_message=None,
            permissions=None,
            slow_mode_delay=None,
            unrestrict_boost_count=None,
            message_auto_delete_time=None,
            has_aggressive_anti_spam_enabled=None,
            has_hidden_members=None,
            has_protected_content=None,
            has_visible_history=None,
            sticker_set_name=None,
            can_set_sticker_set=None,
            custom_emoji_sticker_set_name=None,
            linked_chat_id=None,
            location=None,
        ),
        message_thread_id=8,
        from_user=User(
            id=653327229,
            is_bot=False,
            first_name="No",
            last_name=None,
            username="Cotovnika",
            language_code="en",
            is_premium=None,
            added_to_attachment_menu=None,
            can_join_groups=None,
            can_read_all_group_messages=None,
            supports_inline_queries=None,
        ),
        sender_chat=None,
        sender_boost_count=None,
        forward_origin=None,
        is_topic_message=True,
        is_automatic_forward=None,
        reply_to_message=None,
        external_reply=None,
        quote=None,
        reply_to_story=None,
        via_bot=None,
        edit_date=None,
        has_protected_content=None,
        media_group_id=None,
        author_signature=None,
        text=None,
        entities=None,
        link_preview_options=None,
        animation=None,
        audio=None,
        document=None,
        photo=None,
        sticker=None,
        story=None,
        video=None,
        video_note=None,
        voice=None,
        caption=None,
        caption_entities=None,
        has_media_spoiler=None,
        contact=None,
        dice=None,
        game=None,
        poll=None,
        venue=None,
        location=None,
        new_chat_members=None,
        left_chat_member=None,
        new_chat_title=None,
        new_chat_photo=None,
        delete_chat_photo=None,
        group_chat_created=None,
        supergroup_chat_created=None,
        channel_chat_created=None,
        message_auto_delete_timer_changed=None,
        migrate_to_chat_id=None,
        migrate_from_chat_id=None,
        pinned_message=None,
        invoice=None,
        successful_payment=None,
        users_shared=None,
        chat_shared=None,
        connected_website=None,
        write_access_allowed=None,
        passport_data=None,
        proximity_alert_triggered=None,
        boost_added=None,
        forum_topic_created=ForumTopicCreated(
            name="some", icon_color=7322096, icon_custom_emoji_id=None
        ),
        forum_topic_edited=None,
        forum_topic_closed=None,
        forum_topic_reopened=None,
        general_forum_topic_hidden=None,
        general_forum_topic_unhidden=None,
        giveaway_created=None,
        giveaway=None,
        giveaway_winners=None,
        giveaway_completed=None,
        video_chat_scheduled=None,
        video_chat_started=None,
        video_chat_ended=None,
        video_chat_participants_invited=None,
        web_app_data=None,
        reply_markup=None,
        forward_date=None,
        forward_from=None,
        forward_from_chat=None,
        forward_from_message_id=None,
        forward_sender_name=None,
        forward_signature=None,
        user_shared=None,
    ),
    "external_reply": None,
    "quote": None,
    "reply_to_story": None,
    "via_bot": None,
    "edit_date": None,
    "has_protected_content": None,
    "media_group_id": None,
    "author_signature": None,
    "text": "qwe",
    "entities": None,
    "link_preview_options": None,
    "animation": None,
    "audio": None,
    "document": None,
    "photo": None,
    "sticker": None,
    "story": None,
    "video": None,
    "video_note": None,
    "voice": None,
    "caption": None,
    "caption_entities": None,
    "has_media_spoiler": None,
    "contact": None,
    "dice": None,
    "game": None,
    "poll": None,
    "venue": None,
    "location": None,
    "new_chat_members": None,
    "left_chat_member": None,
    "new_chat_title": None,
    "new_chat_photo": None,
    "delete_chat_photo": None,
    "group_chat_created": None,
    "supergroup_chat_created": None,
    "channel_chat_created": None,
    "message_auto_delete_timer_changed": None,
    "migrate_to_chat_id": None,
    "migrate_from_chat_id": None,
    "pinned_message": None,
    "invoice": None,
    "successful_payment": None,
    "users_shared": None,
    "chat_shared": None,
    "connected_website": None,
    "write_access_allowed": None,
    "passport_data": None,
    "proximity_alert_triggered": None,
    "boost_added": None,
    "forum_topic_created": None,
    "forum_topic_edited": None,
    "forum_topic_closed": None,
    "forum_topic_reopened": None,
    "general_forum_topic_hidden": None,
    "general_forum_topic_unhidden": None,
    "giveaway_created": None,
    "giveaway": None,
    "giveaway_winners": None,
    "giveaway_completed": None,
    "video_chat_scheduled": None,
    "video_chat_started": None,
    "video_chat_ended": None,
    "video_chat_participants_invited": None,
    "web_app_data": None,
    "reply_markup": None,
    "forward_date": None,
    "forward_from": None,
    "forward_from_chat": None,
    "forward_from_message_id": None,
    "forward_sender_name": None,
    "forward_signature": None,
    "user_shared": None,
}
