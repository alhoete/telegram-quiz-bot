from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# حط هنا توكن البوت
TOKEN = "8244193609:AAElb8nuUA0WbfAdLrxKy1kbb8_oSC8p3Bo"

# بنك الأسئلة (مثال مبسط من الأسئلة اللي عطيتني)
QUESTIONS = [
    {
        "question": "أصل كلمة 'أردن' في اللغة الآرامية تعني:",
        "options": ["أ) الأرض الخصبة", "ب) القوة والانحدار", "ج) الأرض المستوية", "د) الضفة المرتفعة"],
        "answer": "ب"
    },
    {
        "question": "أطلقت تسمية الأردن قبل الميلاد على المنطقة المحاذية لـ:",
        "options": ["أ) نهر الفرات", "ب) نهر الأردن", "ج) نهر الزرقاء", "د) البحر الميت"],
        "answer": "ب"
    },
    {
        "question": "بعد الفتح الإسلامي أصبحت المنطقة الشرقية والغربية للنهر تُعرف باسم:",
        "options": ["أ) جند دمشق", "ب) جند الأردن", "ج) جند فلسطين", "د) جند حوران"],
        "answer": "ب"
    },
    # تقدر تضيف باقي الأسئلة بنفس التنسيق
]

# القيم اللي بتتخزن لكل مستخدم
user_data = {}

# دالة بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"score": 0, "index": 0}
    await send_question(update, context, user_id)

# دالة إرسال سؤال
async def send_question(update, context, user_id):
    index = user_data[user_id]["index"]
    if index >= len(QUESTIONS):
        score = user_data[user_id]["score"]
        await update.message.reply_text(f"انتهى الاختبار! نتيجتك: {score}/{len(QUESTIONS)}")
        return

    q = QUESTIONS[index]
    buttons = [
        [InlineKeyboardButton(opt, callback_data=opt[-1])] for opt in q["options"]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(q["question"], reply_markup=keyboard)

# دالة الرد على اختيار المستخدم
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    index = user_data[user_id]["index"]
    correct_answer = QUESTIONS[index]["answer"]

    if data == correct_answer:
        user_data[user_id]["score"] += 1

    user_data[user_id]["index"] += 1
    await send_question(query, context, user_id)

# تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
