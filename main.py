۱import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

QUESTIONS = [
    ("اگر همه گربه‌ها حیوان هستند و بعضی حیوان‌ها سفیدند، آیا حتماً بعضی گربه‌ها سفیدند؟",
     ["بله", "خیر", "اطلاعات کافی نیست"], "اطلاعات کافی نیست"),

    ("عدد بعدی چیست؟ 2، 4، 8، 16، ؟",
     ["24", "32", "30"], "32"),

    ("کدام مورد بیشتر به حافظه مربوط است؟",
     ["یادآوری اطلاعات", "دویدن", "تنفس"], "یادآوری اطلاعات"),

    ("اگر امروز دوشنبه باشد، 10 روز بعد چه روزی است؟",
     ["چهارشنبه", "پنجشنبه", "جمعه"], "پنجشنبه"),

    ("کدام گزینه نمونه‌ای از توجه انتخابی است؟",
     ["تمرکز روی صدای یک نفر در جمع شلوغ", "خوابیدن", "راه رفتن"],
     "تمرکز روی صدای یک نفر در جمع شلوغ"),

    ("عدد بعدی چیست؟ 1، 1، 2، 3، 5، ؟",
     ["7", "8", "9"], "8"),

    ("اگر 5 ماشین در 5 دقیقه، 5 قطعه تولید کنند، 1 ماشین در 5 دقیقه چند قطعه تولید می‌کند؟",
     ["1", "5", "25"], "1"),

    ("کدام کار بیشتر به حل مسئله کمک می‌کند؟",
     ["بررسی چند راه‌حل", "حدس زدن سریع", "نادیده گرفتن مشکل"],
     "بررسی چند راه‌حل"),

    ("وقتی قبل از پاسخ دادن مکث می‌کنی و جوانب موضوع را بررسی می‌کنی، بیشتر از کدام توانایی استفاده می‌کنی؟",
     ["تفکر و تصمیم‌گیری", "حافظه حرکتی", "شنوایی"],
     "تفکر و تصمیم‌گیری"),

    ("اگر همه Aها، B باشند و هیچ Bای C نباشد، آیا A می‌تواند C باشد؟",
     ["بله", "خیر", "همیشه مشخص نیست"], "خیر"),
]

user_data = {}


def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["🧠 آزمون امروز", "🎯 تمرین ذهنی"],
            ["🌱 خودشناسی", "✨ آگاهی"],
            ["📊 پیشرفت من", "📅 برنامه روزانه"],
        ],
        resize_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_data[user_id] = {
        "name": update.effective_user.first_name or "دوست من",
        "question": len(QUESTIONS),
        "score": 0,
        "answers": [],
    }

    await update.message.reply_text(
        "سلام رفیق 🌱\n\n"
        "به «آگاهی | خودشناسی و رشد ذهن» خوش آمدی.\n\n"
        "اینجا قرار نیست فقط یک عدد به تو بدهیم؛ "
        "هدف این است که به مرور، منطق، توجه، حافظه، تصمیم‌گیری "
        "و خودشناسی خودت را بهتر بشناسی.\n\n"
        "از منوی زیر شروع کن 👇",
        reply_markup=main_menu()
    )


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = user_data[user_id]
    index = data["question"]

    if index >= len(QUESTIONS):
        score = data["score"]
        total = len(QUESTIONS)

        if score <= 3:
            level = "نیاز به تمرین بیشتر 🌱"
        elif score <= 6:
            level = "در مسیر رشد 🧠"
        elif score <= 8:
            level = "عملکرد خوب ⭐"
        else:
            level = "عملکرد بسیار خوب 🔥"

        await update.message.reply_text(
            f"🎉 آزمون تمام شد!\n\n"
            f"امتیاز این دوره: {score} از {total}\n"
            f"ارزیابی فعلی: {level}\n\n"
            "این امتیاز IQ رسمی یا تشخیص روان‌شناختی نیست؛ "
            "فقط یک سنجش ساده از عملکرد همین آزمون است.",
            reply_markup=main_menu()
        )
        return

    question, options, _ = QUESTIONS[index]

    await update.message.reply_text(
        f"🧠 سؤال {index + 1} از {len(QUESTIONS)}\n\n{question}",
        reply_markup=ReplyKeyboardMarkup(
            [[option] for option in options],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_data:
        user_data[user_id] = {
            "name": update.effective_user.first_name or "دوست من",
            "question": 0,
            "score": 0,
            "answers": [],
        }

    user_data[user_id]["question"] = 0
    user_data[user_id]["score"] = 0
    user_data[user_id]["answers"] = []

    await send_question(update, context)


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data:
        await start(update, context)
        return

    data = user_data[user_id]

    # دکمه‌های منوی اصلی
    if data["question"] >= len(QUESTIONS):
        if text == "🧠 آزمون امروز":
            await start_test(update, context)

        elif text == "🎯 تمرین ذهنی":
            await update.message.reply_text(
                "🎯 تمرین امروز:\n\n"
                "از 100 شروع کن و هر بار 7 تا کم کن.\n"
                "هدف، دقت و تمرکز است؛ نه سرعت."
            )

        elif text == "🌱 خودشناسی":
            await update.message.reply_text(
                "🌱 سؤال امروز:\n\n"
                "اگر هیچ‌کس قرار نبود تو را قضاوت کند، "
                "چه تغییری در زندگی‌ات ایجاد می‌کردی؟"
            )

        elif text == "✨ آگاهی":
            await update.message.reply_text(
                "✨ تمرین آگاهی:\n\n"
                "دو دقیقه آرام بنشین و فقط نفس کشیدنت را مشاهده کن."
            )

        elif text == "📊 پیشرفت من":
            await update.message.reply_text(
                "📊 فعلاً اولین دوره را شروع کرده‌ایم.\n"
                "در نسخه بعدی روند چند دوره‌ای پیشرفت را ذخیره می‌کنیم."
            )

        elif text == "📅 برنامه روزانه":
            await update.message.reply_text(
                "📅 برنامه پیشنهادی امروز:\n\n"
                "🧘 10 دقیقه آرام‌سازی\n"
                "🧠 10 دقیقه تمرین ذهنی\n"
                "🌱 10 دقیقه خودشناسی\n"
                "📖 15 دقیقه مطالعه"
            )
        return

    # پاسخ آزمون
    index = data["question"]
    question, options, correct = QUESTIONS[index]

    if text not in options:
        await update.message.reply_text("لطفاً یکی از گزینه‌های نمایش‌داده‌شده را انتخاب کن.")
        return

    if text == correct:
        data["score"] += 1
        result = "✅ درست"
    else:
        result = f"❌ نادرست\nپاسخ درست: {correct}"

    data["answers"].append({
        "question": question,
        "answer": text,
        "correct": text == correct,
    })

    data["question"] += 1

    await update.message.reply_text(result)
    await send_question(update, context)

def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)
    )

    print("Aghahi Mind Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()

