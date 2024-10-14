import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Пример расширенного словаря продуктов с URL изображений
PRODUCTS = {
    "Аниме": {
        "Фигурка Naruto": {
            "info": "Цена: 1500 руб.",
            "image": "https://example.com/naruto.jpg"
        },
        "Манга One Piece": {
            "info": "Цена: 800 руб.",
            "image": "https://example.com/one_piece.jpg"
        }
    },
    # Остальные категории аналогично...
}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Каталог", callback_data='catalog')],
        [InlineKeyboardButton("О нас", callback_data='about')],
        [InlineKeyboardButton("Контакты", callback_data='contacts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Добро пожаловать! Выберите опцию из меню ниже:",
        reply_markup=reply_markup
    )

# Обработчик нажатий кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == 'catalog':
        # Кнопки категорий
        keyboard = [
            [InlineKeyboardButton("Аниме", callback_data='category_Аниме')],
            [InlineKeyboardButton("Игры", callback_data='category_Игры')],
            [InlineKeyboardButton("Косплей", callback_data='category_Косплей')],
            [InlineKeyboardButton("Детали", callback_data='category_Детали')],
            [InlineKeyboardButton("Под заказ", callback_data='category_Под заказ')],
            [InlineKeyboardButton("Назад", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Выберите категорию:",
            reply_markup=reply_markup
        )

    elif data.startswith('category_'):
        category = data.split('_', 1)[1]
        products = PRODUCTS.get(category, {})
        if products:
            for product, details in products.items():
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=details.get("image"),
                    caption=f"**{product}**\n{details.get('info')}",
                    parse_mode='Markdown'
                )
            # После отправки всех продуктов, добавим кнопку "Назад к Каталогу"
            keyboard = [
                [InlineKeyboardButton("Назад к Каталогу", callback_data='catalog')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text=f"Товары в категории **{category}**:",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(
                text="В этой категории пока нет товаров.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Назад к Каталогу", callback_data='catalog')]
                ])
            )

    elif data == 'about':
        about_text = (
            "Мы предлагаем широкий ассортимент товаров в категориях Аниме, Игры, Косплей и многое другое. "
            "Наши продукты высокого качества и доступны по разумным ценам."
        )
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=about_text,
            reply_markup=reply_markup
        )

    elif data == 'contacts':
        contacts_text = (
            "Свяжитесь с нами:\n"
            "Телефон: +7 123 456-78-90\n"
            "Email: example@example.com\n"
            "Адрес: г. Нашичи, ул. Примерная, д. 1"
        )
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=contacts_text,
            reply_markup=reply_markup
        )

    elif data == 'back_to_menu':
        # Возврат к главному меню
        keyboard = [
            [InlineKeyboardButton("Каталог", callback_data='catalog')],
            [InlineKeyboardButton("О нас", callback_data='about')],
            [InlineKeyboardButton("Контакты", callback_data='contacts')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Выберите опцию из меню ниже:",
            reply_markup=reply_markup
        )

    else:
        await query.edit_message_text(text="Неизвестная команда.")

def main() -> None:
    # Вставьте ваш токен от BotFather
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

    # Создаем приложение
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
