import asyncio
import os

from aiogram import F, Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from gtts import gTTS

from filter.chat_types import ChatTypeFilter
from handlers.ai_function import sent_prompt_and_get_response_2, sent_prompt_and_get_response_3
from keyboard.inline import start_functions_keyboard, get_cancel_keyboard, return_menu_functions_keyboard

create_music_private_router = Router()
create_music_private_router.message.filter(ChatTypeFilter(['private']))


class AiAssistanceState2(StatesGroup):
    WaitingForTheme = State()


@create_music_private_router.callback_query(F.data.startswith("create_music"))
async def create_music_callback_query(query: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для создания музыки. Пользователь отправляет тему, а бот придумывает музыку.
    """
    await state.clear()
    m = await query.message.edit_caption(
        caption=(
            "🎵 Мы готовы придумать музыку для вашей темы!\n\n"
            "Пожалуйста, отправьте тему, которая вдохновит нас. Например:\n"
            "— Любовь и дождь 🌧️❤️\n"
            "— Ветер и пустыня 🌬️🏜️\n"
            "— Рок и адреналин 🎸⚡"
        ),
        reply_markup=get_cancel_keyboard()
    )
    await state.update_data(message_id=m.message_id)
    await state.set_state(AiAssistanceState2.WaitingForTheme)
    await query.answer("Отправьте вашу тему, чтобы мы придумали музыку!")


@create_music_private_router.message(AiAssistanceState2.WaitingForTheme)
async def process_create_music(message: types.Message, state: FSMContext, bot: Bot):
    """
    Обработка темы для создания музыки.
    """
    # Получаем информацию о пользователе
    user_info = message.from_user.first_name or ""
    if message.from_user.last_name:
        user_info += f" {message.from_user.last_name}"
    if message.from_user.username:
        user_info += f" (@{message.from_user.username})"

    # Если пользователь отправил текст
    if message.text:
        # Отправляем сообщение с подтверждением
        processing_message = await message.answer(
            f"Запрос принят, {user_info}!\n💭 Ещё чуть-чуть, готовлю ответ..."
        )

        # Генерируем ответ с использованием ИИ
        generated_help = sent_prompt_and_get_response_3(message.text)

        # Создаём клавиатуру с кнопкой возврата
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text="🔊 Послушать ", callback_data='listen_music'))
        keyboard.add(InlineKeyboardButton(text="↩️ Вернуться", callback_data="return"))

        # Редактируем сообщение с результатом
        await bot.edit_message_text(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id,
            text=generated_help,
            reply_markup=keyboard.adjust(1,).as_markup(),
        )

        user_data = await state.get_data()
        message_id = user_data.get("message_id")
        if message_id:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")

        # Очищаем состояние
        await state.clear()

    else:
        await message.delete()
        m = await message.answer("Пожалуйста, отправьте текстовую тему для создания музыки!")
        await asyncio.sleep(5)
        await m.delete()


@create_music_private_router.callback_query(F.data.startswith("listen_music"))
async def listen_music(query: types.CallbackQuery, state: FSMContext) -> None:
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
