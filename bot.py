import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# تفعيل اللوق (اختياري)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# جلب التوكن من Environment Variable
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("تأكد أنك وضعت TELEGRAM_TOKEN في Environment Variables!")

# قائمة أسئلة بسيطة كمثال
questions = [
    {"q": "أصل كلمة 'أردن' يعني:", "options": ["الأرض الخصبة", "القوة والانحدار", "الأرض المستوية", "الضفة المرتفعة"], "answer": 1},
    {"q": "أُعلن استقلال الأردن سنة:", "options": ["1946", "1952", "1939", "1960"], "answer": 0}
]

# دالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ابدأ الاختبار", callback_data='start_quiz')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحبا! اضغط للبدء:", reply_markup=reply_markup)

# التعامل مع الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "start_quiz":
        question = questions[0]
        keyboard = [
            [InlineKeyboardButton(opt, callback_data=str(i))] for i, opt in enumerate(question['options'])
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=question['q'], reply_markup=reply_markup)
    else:
        await query.edit_message_text(text=f"لقد اخترت الخيار {query.data}. شكرًا لك!")

# الدالة الرئيسية لتشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("البوت شغال...")
    app.run_polling()

if __name__ == '__main__':
    main()
