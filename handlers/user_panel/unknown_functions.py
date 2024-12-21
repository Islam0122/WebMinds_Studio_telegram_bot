from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from filter.chat_types import ChatTypeFilter, IsAdmin

unknown_private_router = Router()
unknown_private_router.message.filter(ChatTypeFilter(['private']))


@unknown_private_router.message()
async def unknown_command(message: types.Message):
    await message.reply("Извините, я не понял вашего запроса. Пожалуйста, используйте доступные команды.")

