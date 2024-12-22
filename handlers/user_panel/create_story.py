import os
import asyncio
from gtts import gTTS
from aiogram import F, types, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.ai_function import sent_prompt_and_get_response
from keyboard.inline import get_cancel_keyboard, return_menu_functions_keyboard
from filter.chat_types import ChatTypeFilter

story_functions_private_router = Router()
story_functions_private_router.message.filter(ChatTypeFilter(['private']))

class create_storyAiAssistanceState(StatesGroup):
    WaitingForReview = State()

@story_functions_private_router.callback_query(F.data.startswith("create_story"))
async def create_story_callback_query(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    m = await query.message.edit_caption(
        caption="💬 Напишите тему для сказки, и я помогу вам создать её!",
        reply_markup=get_cancel_keyboard()
    )
    await state.update_data(message_id=m.message_id)
    await query.answer("Ждем ваш запрос! 📝")
    await state.set_state(create_storyAiAssistanceState.WaitingForReview)

@story_functions_private_router.message(create_storyAiAssistanceState.WaitingForReview)
async def process_create_story_request(message: types.Message, state: FSMContext, bot: Bot):
    user_info = message.from_user.first_name or ""
    if message.from_user.last_name:
        user_info += f" {message.from_user.last_name}"
    if message.from_user.username:
        user_info += f" (@{message.from_user.username})"

    if message.text:
        processing_message = await message.answer(f"Запрос принят, {user_info}!\n💭 Ещё чуть-чуть, готовлю ответ...")
        story_theme = message.text
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text="🔊 Послушать сказку", callback_data='listen'))
        keyboard.add(InlineKeyboardButton(text="⏪ Вернуться в меню", callback_data='start_'))
        generated_story = sent_prompt_and_get_response(story_theme)
        # Генерация сказки с ИИ
        await bot.edit_message_text(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id,
            text=generated_story, reply_markup=keyboard.adjust(1).as_markup()
        )
        user_data = await state.get_data()
        message_id = user_data.get("message_id")

        if message_id:
            # Удаляем сообщение, которое мы редактировали ранее
            await bot.delete_message(message.chat.id, message_id)
        await state.clear()
    else:
        # Если сообщение пустое, удаляем его и отправляем новое сообщение
        await message.delete()
        m = await message.answer("Пожалуйста, напишите тему для сказки.")
        await asyncio.sleep(5)
        await m.delete()




@story_functions_private_router.callback_query(F.data.startswith("listen"))
async def listen_story(query: types.CallbackQuery, state: FSMContext) -> None:
    text = query.message.text
    user_id = query.from_user.id

    await query.message.edit_text(text, reply_markup=return_menu_functions_keyboard())

    wait_message = "Пожалуйста, подождите до трёх минут. Генерируется голос..."
    await query.message.answer(wait_message)
    tts = gTTS(text=text, lang='ru')

    file_path = f"{user_id}.mp3"
    tts.save(file_path)
    voice = types.FSInputFile(file_path)

    await query.message.answer_voice(voice)

    # Удаляем файл после отправки
    os.remove(file_path)

