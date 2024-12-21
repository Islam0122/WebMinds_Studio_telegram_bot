from aiogram import F, types, Router, Bot
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from filter.chat_types import ChatTypeFilter
from keyboard.inline import *

start_functions_private_router = Router()
start_functions_private_router.message.filter(ChatTypeFilter(['private']))

welcome_text = (
    "👋 Добро пожаловать в <b>WebMinds Studio</b>!\n\n"
    "🌐 Мы специализируемся на разработке современных сайтов и Telegram-ботов."
    "Наши <i>инновационные</i> и <i>интеллектуальные</i> решения помогут вам выделиться в цифровом пространстве💡.\n"
    "📖 Выберите интересующий вас раздел ниже:"
)


# Обработчик команды /start
@start_functions_private_router.message(CommandStart())
async def start_cmd(message: types.Message, ):
    """Обработчик команды /start"""
    await message.answer_photo(
        photo=types.FSInputFile('media/img/img.png'),
        caption=welcome_text,
        reply_markup=start_functions_keyboard()
    )


# Обработчик нажатия кнопки "Старт"
@start_functions_private_router.callback_query(F.data == "start")
async def start_main_menu(query: types.CallbackQuery, ):
    """Обработчик callback_query для основного меню"""
    await query.message.edit_caption(
        caption=welcome_text,
        reply_markup=start_functions_keyboard())

@start_functions_private_router.callback_query(F.data == "start_")
async def start_main_menu(query: types.CallbackQuery, ):
    """Обработчик callback_query для основного меню"""
    await query.message.delete()
    await query.message.answer_photo(
        photo=types.FSInputFile('media/img/img.png'),
        caption=welcome_text,
        reply_markup=start_functions_keyboard()
    )

@start_functions_private_router.callback_query(F.data == 'about_us')
async def about_us_command_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_functions_keyboard()
    caption_text = (
        "<b>WebMinds Studio</b> — студия, специализирующаяся на разработке современных сайтов 🌐 и Telegram-ботов 🤖. \n"
        "Мы предлагаем инновационные и интеллектуальные решения для цифрового пространства 💡.\n\n"
        "<b>Наша команда</b> — это специалисты с богатым опытом в области разработки и дизайна. \n"
        "Мы помогаем компаниям и стартапам достигать успеха в цифровом мире 🌟.\n\n"
        "<b>Наши услуги:</b>\n"
        "<b>🌐 Разработка сайтов</b> — создание современных и функциональных сайтов для вашего бизнеса.\n"
        "<b>🤖 Создание Telegram-ботов</b> — разработка удобных и эффективных ботов для различных целей.\n"
        "<b>🔍 SEO-оптимизация</b> — повышение видимости вашего сайта в поисковых системах.\n"
        "<b>⚙️ Индивидуальные решения</b> — разработка решений, которые идеально подходят под ваши задачи.\n"
        "<b>📈 Внедрение CRM-систем</b> — мы помогаем интегрировать CRM для оптимизации работы с клиентами и улучшения бизнес-процессов.\n"
        "<b>Свяжитесь с нами, чтобы узнать больше! 📩</b>"
    )

    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'our_services')
async def our_services_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_functions_keyboard()
    caption_text = (
        "<b>Наши услуги:</b>\n\n"
        "<b>🌐 Разработка сайтов</b> — создание современных и функциональных сайтов для вашего бизнеса.\n\n"
        "<b>🤖 Создание Telegram-ботов</b> — разработка удобных и эффективных ботов для различных целей.\n\n"
        "<b>🔍 SEO-оптимизация</b> — повышение видимости вашего сайта в поисковых системах.\n\n"
        "<b>⚙️ Индивидуальные решения</b> — разработка решений, которые идеально подходят под ваши задачи.\n\n"
        "<b>📈 Внедрение CRM-систем</b> — интеграция CRM для оптимизации работы с клиентами и улучшения бизнес-процессов.\n\n"
        "<b>Свяжитесь с нами, чтобы узнать больше! 📩</b>"
    )

    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'payment_terms')
async def payment_terms_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_functions_keyboard()

    caption_text = (
        "<b>Условия оплаты:</b>\n\n"
        "<b>💳 Способы оплаты:</b>\n"
        "• Банковские карты (Visa, MasterCard, Мир)\n"
        "• Электронные кошельки (Qiwi, WebMoney, Яндекс.Деньги)\n\n"

        "<b>📅 Сроки оплаты:</b>\n"
        "• Оплата должна быть произведена в течение 3 рабочих дней после подтверждения заказа.\n"
        "• В случае задержки оплаты заказ может быть отменен.\n\n"

        "<b>💡 Примечания:</b>\n"
        "• Все оплаты считаются окончательными и не подлежат возврату.\n"
        "• Мы предоставляем все необходимые документы для бухгалтерии по запросу.\n\n"

        "<b>🕒 Время работы:</b>\n"
        "• Понедельник — Пятница: 9:00 — 22:00\n"
        "• Воскресенье: выходной\n\n"

        "<b>Свяжитесь с нами для уточнения деталей! 📩</b>"
    )

    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'advantages')
async def advantages_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = return_functions_keyboard()

    caption_text = (
        "<b>Наши преимущества:</b>\n\n"
        "<b>🚀 Быстрая разработка:</b> Мы обеспечиваем высокую скорость выполнения проектов, не теряя в качестве.\n"
        "<b>💡 Инновационные решения:</b> Мы используем новейшие технологии и подходы для разработки уникальных решений.\n"
        "<b>🤖 Эксперты в Telegram-ботах:</b> Наша команда имеет большой опыт в создании ботов для любых целей.\n"
        "<b>🌐 Разработка сайтов:</b> Мы создаем современные, функциональные и адаптивные сайты для вашего бизнеса.\n"
        "<b>🔒 Безопасность:</b> Мы гарантируем безопасность ваших данных и защищаем ваши проекты от угроз.\n"
        "<b>🌍 Международный опыт:</b> Мы работаем с клиентами по всему миру, предоставляя качественные решения.\n"
        "<b>💬 Поддержка 24/7:</b> Мы всегда готовы помочь и поддерживать ваши проекты на всех этапах.\n\n"
        "<b>Свяжитесь с нами, чтобы узнать больше! 📩</b>"
    )

    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'faq')
async def faq_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = start_functions_keyboard()

    caption_text = (
        "<b>Часто задаваемые вопросы:</b>\n\n"
        "<b>❓ Как заказать?</b> Напишите нам через '📅 Связаться с нами'.\n"
        "<b>❓ Время разработки?</b> Обычно 1-4 недели.\n"
        "<b>❓ Как оплатить?</b> Банковский перевод или карта.\n"
    )

    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'our_projects')
async def our_projects_callback_query(query: types.CallbackQuery) -> None:
    keyboard_markup = our_projects_functions_keyboard()

    caption_text = (
        "<b>🚀 Наши проекты</b>\n\n"
        "<b>🔨 Проект 1: Sengoku — готов</b>\n"
        "Перейдите по кнопке ниже, чтобы узнать больше.\n\n"
        "<b>🔧 Проект 2 — в разработке</b>\n"
        "Ожидайте его запуск в ближайшее время!\n\n"
        "<b>🔨 Проект 3 — в разработке</b>\n"
        "Следите за обновлениями, мы скоро покажем его!\n\n"
        "Спасибо за интерес к нашим проектам! 🚀"
    )

    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == 'contact_us')
async def contact_us_callback_query(query: types.CallbackQuery) -> None:
    # Клавиатура с кнопками для связи
    keyboard_markup = contact_us_functions_keyboard()

    # Текст, который будет отображен при нажатии на кнопку
    caption_text = (
        "<b>📞 Свяжитесь с нами!</b>\n\n"
        "Если у вас есть вопросы или предложения, вы можете связаться с нами через следующие каналы:\n\n"
        "<b>WhatsApp</b> \n"
        "<b>Telegram</b> \n"
        "<b>Instagram</b> \n\n"
        "Нажмите кнопку ниже для связи с администратором."
    )

    # Отправка обновленного сообщения с кнопками
    await query.message.edit_caption(
        caption=caption_text,
        reply_markup=keyboard_markup
    )


@start_functions_private_router.callback_query(F.data == "contact_admin")
async def contact_admin_callback_query(query: types.CallbackQuery, bot: Bot):
    """Обработчик callback_query для записи на contact_admin"""

    # Клавиатура для возврата в главное меню
    keyboard_markup = return_functions_keyboard()

    # Сообщение, которое будет отправлено пользователю
    text = "Ваша заявка отправлена нашему менеджеру, он свяжется с вами в ближайшее время. 💬"

    # Обновляем сообщение с кнопками
    await query.message.edit_caption(
        caption=text,
        reply_markup=keyboard_markup
    )

    # Отправляем уведомление пользователю
    await query.answer(text=text)

    # Информация о пользователе
    user_info = f"📝 {query.from_user.first_name}"

    # Добавляем фамилию, если она есть
    if query.from_user.last_name:
        user_info += f" {query.from_user.last_name}"

    # Добавляем username, если он есть
    if query.from_user.username:
        user_info += f" (@{query.from_user.username})"

    # Отправка сообщения администратору
    await bot.send_message(
        chat_id=6316190199,  # ID чата с администратором
        text=(
            f"💬 <b>Новая заявка на связь с администратором</b>:\n\n"
            f"👤 <b>Информация о пользователе:</b>\n"
            f"📛 <b>Имя:</b> {user_info}\n"
            f"📲 <b>Контакт пользователя:</b> @{query.from_user.username or 'Не указан'}\n\n"
            f"🔑 <b>Ваши действия:</b>\n"
            f"1. Свяжитесь с пользователем для дальнейшего общения.\n"
        )
    )
