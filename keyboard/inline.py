from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_functions_keyboard():
    """Функция для создания клавиатуры."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="📖 О нас", callback_data="about_us"))

    keyboard.add(InlineKeyboardButton(text="💼 Наши проекты", callback_data="our_projects"))
    keyboard.add(InlineKeyboardButton(text="⭐ Отзывы клиентов", callback_data="feedback"))

    keyboard.add(InlineKeyboardButton(text="🛠️ Наши услуги", callback_data="our_services"))

    keyboard.add(InlineKeyboardButton(text="💳 Оплата и условия", callback_data="payment_terms"))

    keyboard.add(InlineKeyboardButton(text="💬 Часто задаваемые вопросы (FAQ)", callback_data="faq"))

    keyboard.add(InlineKeyboardButton(text="📈 Наши преимущества", callback_data="advantages"))

    keyboard.add(InlineKeyboardButton(text="📅 Связаться с нами", callback_data="contact_us"))

    keyboard.add(InlineKeyboardButton(text="✨ Полезные функции от нас", callback_data="useful_features"))
    return keyboard.adjust(1, 2, 1, 1, 1, 1, ).as_markup()


def return_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="📅 Связаться с нами", callback_data="contact_us"))
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start"))
    return keyboard.adjust(1, ).as_markup()


def our_projects_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔗 Перейти к проекту Sengoku", url="https://t.me/sengokukg_bot"))
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start"))
    return keyboard.adjust(1, ).as_markup()


def get_cancel_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel"))
    return keyboard.adjust(1).as_markup()


def return_menu_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start_"))
    return keyboard.adjust(1, ).as_markup()


# Функция для создания клавиатуры с кнопками
def feedback_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    # Кнопка для оставления отзыва с эмодзи
    keyboard.add(InlineKeyboardButton(text="💬 Оставить отзыв", callback_data="leave_review"))
    # Кнопка для просмотра отзывов с эмодзи
    keyboard.add(InlineKeyboardButton(text="👀 Посмотреть отзыв", callback_data="view_review"))
    # Кнопка для возвращения в главное меню с эмодзи
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start_"))

    # Возвращаем клавиатуру с оптимизацией для отображения
    return keyboard.adjust(1).as_markup()


def feedback_buttons():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Комментарий о сайте", callback_data="comment_1"),
        InlineKeyboardButton(text="Комментарий о боте", callback_data="comment_2"),
        InlineKeyboardButton(text="Комментарий о функционале", callback_data="comment_3"),
    )
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start_"))
    return keyboard.adjust(1, ).as_markup()


def contact_us_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Напишите нам в WhatsApp", url="https://api.whatsapp.com/send/?phone=996509968969"),
        InlineKeyboardButton(text="Напишите нам в Telegram", url="https://t.me/DJSUAIDA"),
        InlineKeyboardButton(text="Напишите нам в Instagram", url="https://www.instagram.com/web_mind_studio/"),
        InlineKeyboardButton(text="📩 Связаться с администратором", callback_data="contact_admin"),
        # Кнопка для связи с администратором
        InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start")
    )
    return keyboard.adjust(1, ).as_markup()


def useful_features_functions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="🤖 Чат с ИИ", callback_data="chat_ai"),
        InlineKeyboardButton(text="🎵 Создать музыку", callback_data="create_music"),
        InlineKeyboardButton(text="📖 Создать сказку", callback_data="create_story"),
        InlineKeyboardButton(text="🔙 Вернуться в главное меню", callback_data="start")
    )
    return keyboard.adjust(1, 1, 1, 1).as_markup()
