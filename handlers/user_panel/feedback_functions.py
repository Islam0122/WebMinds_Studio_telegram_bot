from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from keyboard.inline import start_functions_keyboard, get_cancel_keyboard, return_menu_functions_keyboard, \
    feedback_functions_keyboard, feedback_buttons
from handlers.user_panel.start_functions import welcome_text
from filter.chat_types import ChatTypeFilter, IsAdmin

feedback_private_router = Router()
feedback_private_router.message.filter(ChatTypeFilter(['private']))


class FeedbackState(StatesGroup):
    WaitingForReview = State()


# Обработчик callback запроса для кнопок
@feedback_private_router.callback_query(F.data.startswith("feedback"))
async def feedback_callback_query(query: types.CallbackQuery) -> None:
    # Создаем клавиатуру с кнопками
    keyboard_markup = feedback_functions_keyboard()

    # Текст для сообщения с эмодзи
    caption_text = (
        "<b>💬 Отзывы</b>\n\n"
        "Выберите действие, которое вы хотите выполнить:\n"
        "1. 📝 Оставить отзыв\n"
        "2. 👀 Посмотреть отзывы\n\n"
        "<i>Если хотите вернуться в главное меню, нажмите '🔙 Вернуться в главное меню'</i>"
    )

    # Отправляем обновленное сообщение с кнопками и текстом
    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=keyboard_markup
    )


comments = ({
               "comment_1": "<b>💻 WebMinds Studio разрабатывает сайт для нас!</b>\n\n"
                            "<i>\"Мы работаем с WebMinds Studio над созданием нового сайта. Команда профессионалов, всегда на связи, "
                            "предложили креативный и удобный дизайн. Все пожелания были учтены, а проект движется по плану. "
                            "Мы уверены, что результат превзойдет все ожидания!\"</i>\n\n"
                            "<b>— Клиент 1, компания скрытно</b>",

               "comment_2": "<b>🤖 WebMinds Studio разрабатывает бота для нас!</b>\n\n"
                            "<i>\"Мы заказали разработку Telegram-бота для нашего бизнеса. WebMinds Studio предложила решение, "
                            "которое идеально соответствует нашим потребностям. Все работает быстро и без сбоев. Бот стал незаменимым "
                            "инструментом для нашей команды!\"</i>\n\n"
                            "<b>— Клиент 2, компания скрытно</b>",

               "comment_3": "<b>🔧 WebMinds Studio создает функционал для сайта!</b>\n\n"
                            "<i>\"Наша компания работает с WebMinds Studio над улучшением функционала сайта. Все изменения были "
                            "внесены вовремя, а новый функционал оказался именно тем, что нам нужно. Отличная работа, мы очень довольны!\"</i>\n\n"
                            "<b>— Клиент 3, компания скрытно</b>"
           })
@feedback_private_router.callback_query(F.data.startswith("view_review"))
async def view_review_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = feedback_buttons()

    caption_text = (
        "<b>💬 Выберите комментарий для просмотра:</b>\n\n"
        "Выберите один из вариантов ниже, чтобы узнать мнение наших клиентов о наших проектах."
    )

    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=keyboard_markup
    )


@feedback_private_router.callback_query(F.data.in_(comments.keys()))
async def show_selected_comment(query: types.CallbackQuery) -> None:
    # Получаем выбранный комментарий
    selected_comment = comments[query.data]

    # Отправляем комментарий пользователю
    await query.message.edit_caption(
        caption=selected_comment,
        reply_markup=return_menu_functions_keyboard()
    )

@feedback_private_router.callback_query(F.data.startswith("leave_review"))
async def send_review_request_callback_query(query: types.CallbackQuery, state: FSMContext) -> None:
    caption_text = (
        "<b>💬 Оставьте свой отзыв</b>\n\n"
        "Пожалуйста, напишите ваш отзыв или предложение. Вы можете отправить текст или медиа.\n\n"
        "<i>Если хотите отменить, нажмите 'Отменить'</i>"
    )

    # Отправляем сообщение с запросом отзыва и сохраняем его ID в состоянии
    message = await query.message.edit_caption(
        caption=caption_text,
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(FeedbackState.WaitingForReview)
    await state.update_data(request_message_id=message.message_id)


@feedback_private_router.callback_query(F.data == "cancel")
async def cancel_feedback(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await query.answer("Действие отменено.")
    await query.message.edit_caption(
        caption=welcome_text,
        reply_markup=start_functions_keyboard()
    )


@feedback_private_router.message(FeedbackState.WaitingForReview)
async def process_review(message: types.Message, state: FSMContext, bot: Bot):
    group_id = -4553757993  # ID группы для получения отзывов

    # Получаем ID сообщения с запросом отзыва из состояния
    user_data = await state.get_data()
    request_message_id = user_data.get('request_message_id')

    # Проверка на содержание текста или медиа
    if message.text:
        # Если отзыв не пустой, отправляем его
        user_info = f"{message.from_user.first_name}"
        if message.from_user.last_name:
            user_info += f" {message.from_user.last_name}"
        if message.from_user.username:
            user_info += f" (@{message.from_user.username})"

        review_text = message.text
        review_message = f"💬 Отзыв от {user_info}:\n\n{review_text}"
        await state.clear()
        # Отправка отзыва в группу
        await bot.send_message(chat_id=group_id, text=review_message)
        await message.answer("Ваш отзыв успешно отправлен! Спасибо!",reply_markup=return_menu_functions_keyboard())

        # Удаляем сообщение с запросом отзыва из личного чата
        if request_message_id:
            try:
                await message.delete()
                await bot.delete_message(chat_id=message.chat.id, message_id=request_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
    elif message.photo or message.video or message.audio:
        # Если медиа, отправляем его как отзыв
        user_info = f"{message.from_user.first_name}"
        if message.from_user.last_name:
            user_info += f" {message.from_user.last_name}"
        if message.from_user.username:
            user_info += f" (@{message.from_user.username})"

        review_media_message = f"💬 Отзыв от {user_info}:\n\nОтправленное медиа:"
        await bot.send_message(chat_id=group_id, text=review_media_message)

        if message.photo:
            await bot.send_photo(chat_id=group_id, photo=message.photo[-1].file_id)
        elif message.video:
            await bot.send_video(chat_id=group_id, video=message.video.file_id)
        elif message.audio:
            await bot.send_audio(chat_id=group_id, audio=message.audio.file_id)

        await message.answer("Ваш медиа-отзыв успешно отправлен! Спасибо!",reply_markup=return_menu_functions_keyboard())

        # Удаляем сообщение с запросом отзыва из личного чата
        if request_message_id:
            try:
                await message.delete()
                await bot.delete_message(chat_id=message.chat.id, message_id=request_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
    else:
        # Удаляем сообщение с просьбой отправить текст или медиа
        await message.delete()
        # Попросим пользователя отправить отзыв
        await message.answer("Пожалуйста, отправьте текст или медиа для отзыва.")
