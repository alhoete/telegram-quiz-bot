import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== التوكن ==================
TOKEN = os.environ.get("TELEGRAM_TOKEN")  # ضع التوكن في Environment Variables على Render

# ================== الأسئلة ==================
questions = [
    {"q": "كلمة 'أردن' في أصلها الآرامي تعني:", "options": ["الأرض الخصبة", "القوة والانحدار", "الأرض المستوية", "الضفة المرتفعة"], "answer": 1},
    {"q": "أطلقت تسمية الأردن قبل الميلاد على المنطقة المحاذية لـ:", "options": ["نهر الفرات", "نهر الأردن", "نهر الزرقاء", "البحر الميت"], "answer": 1},
    {"q": "بعد الفتح الإسلامي أصبحت المنطقة الشرقية والغربية للنهر تُعرف باسم:", "options": ["جند دمشق", "جند الأردن", "جند فلسطين", "جند حوران"], "answer": 1},
    # ... أضف بقية الأسئلة بنفس الشكل ...
]

# ================== وظائف البوت ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["current_q"] = 0
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    q_index = user_data["current_q"]
    
    if q_index >= len(questions):
        await update.effective_chat.send_message("🎉 انتهت جميع الأسئلة!")
        return
    
    question = questions[q_index]
    buttons = [
        [InlineKeyboardButton(text=opt, callback_data=str(i))] 
        for i, opt in enumerate(question["options"])
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.effective_chat.send_message(
        text=f"❓ {question['q']}", reply_markup=reply_markup
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_data = context.user_data
    q_index = user_data.get("current_q", 0)
    
    if q_index >= len(questions):
        return
    
    question = questions[q_index]
    selected = int(query.data)
    
    if selected == question["answer"]:
        feedback = "✅ إجابة صحيحة!"
    else:
        feedback = f"❌ إجابة خاطئة! الإجابة الصحيحة: {question['options'][question['answer']]}"
    
    await query.edit_message_text(text=f"{question['q']}\n\n{feedback}")
    
    # انتقل للسؤال التالي
    user_data["current_q"] = q_index + 1
    await send_question(update, context)

# ================== بدء البوت ==================
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_answer))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
