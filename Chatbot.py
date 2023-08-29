import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Уровни разговора
START, RATING, COMMENT = range(3)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Добро пожаловать! Мы надеемся, что вы остались довольны нашим автосервисом. "
        "Пожалуйста, оцените нашу услугу по шкале от 1 до 5, где 1 - плохо, 5 - отлично."
    )
    return RATING

def collect_rating(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    rating = int(update.message.text)

    if rating < 1 or rating > 5:
        update.message.reply_text("Пожалуйста, введите оценку от 1 до 5.")
        return RATING

    context.user_data['rating'] = rating
    update.message.reply_text(
        "Спасибо за вашу оценку! Если у вас есть какие-либо комментарии или предложения, "
        "пожалуйста, напишите их."
    )
    return COMMENT

def collect_comment(update: Update, context: CallbackContext) -> int:
    comment = update.message.text
    user = update.message.from_user

    context.user_data['comment'] = comment
    update.message.reply_text("Спасибо за ваш отзыв! Ваше мнение очень важно для нас.")

    # Здесь вы можете сохранить оценку и комментарий в базе данных или файле

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Вы отменили диалог. Если у вас возникнут вопросы, вы всегда можете вернуться.")
    return ConversationHandler.END

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token="YOUR_BOT_TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            RATING: [MessageHandler(Filters.regex(r'^[1-5]$'), collect_rating)],
            COMMENT: [MessageHandler(Filters.text & ~Filters.command, collect_comment)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
