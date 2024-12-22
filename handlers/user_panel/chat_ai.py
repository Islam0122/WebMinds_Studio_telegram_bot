import asyncio

from aiogram import F, Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filter.chat_types import ChatTypeFilter
from handlers.ai_function import sent_prompt_and_get_response_2
from keyboard.inline import start_functions_keyboard, get_cancel_keyboard

ai_help_private_router = Router()
ai_help_private_router.message.filter(ChatTypeFilter(['private']))


class AiAssistanceState(StatesGroup):
    WaitingForReview = State()


@ai_help_private_router.callback_query(F.data.startswith("chat_ai"))
async def ai_help_callback_query(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    m = await query.message.edit_caption(
        caption="💬 Напишите свой вопрос, и я помогу вам!",
        reply_markup=get_cancel_keyboard()
    )
    await state.update_data(message_id=m.message_id)
    await query.answer("Ждем ваш вопрос! 📝")
    await state.set_state(AiAssistanceState.WaitingForReview)


@ai_help_private_router.message(AiAssistanceState.WaitingForReview)
async def process_help_request(message: types.Message, state: FSMContext, bot: Bot):
    user_info = message.from_user.first_name or ""
    if message.from_user.last_name:
        user_info += f" {message.from_user.last_name}"
    if message.from_user.username:
        user_info += f" (@{message.from_user.username})"

    if message.text:
        # Отправляем сообщение с подтверждением и сохраняем его
        processing_message = await message.answer(f"Запрос принят, {user_info}!\n💭 Ещё чуть-чуть, готовлю ответ...")

        # Генерируем ответ с ИИ
        generated_help = sent_prompt_and_get_response_2(message.text)
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='↩️ Вернуться', callback_data='return'))
        await bot.edit_message_text(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id,
            text=generated_help,
            reply_markup=keyboard.as_markup()
        )

        # Получаем и удаляем старое сообщение, если оно существует
        user_data = await state.get_data()
        message_id = user_data.get("message_id")

        if message_id:
            try:
                await bot.delete_message(message.chat.id, message_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")

        await state.clear()

    else:
        # Если сообщение пустое, удаляем его и отправляем новое сообщение
        await message.delete()
        m = await message.answer("Пожалуйста, задайте свой вопрос. Он не должен быть пустым.")
        await asyncio.sleep(5)
        await m.delete()
