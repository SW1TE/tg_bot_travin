import smtplib
from email.mime.text import MIMEText
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '7648005239:AAERMWHzmb7z9v0n-ULfBXWBBE5PashIRUg'
SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 587
SENDER_EMAIL = "dan.brylev@yandex.ru"
SENDER_PASSWORD = "zozpgugjdvjpgify"
RECIPIENT_EMAIL = "dan.brylev@yandex.ru"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

quiz = [
    {
        "q": "Где ты чувствуешь себя комфортнее всего?",
        "a": [
            ("В горах", "баран"),
            ("В лесу", "медведь"),
            ("В одиночестве", "тигр"),
            ("Среди друзей", "слон"),
            ("В центре внимания", "попугай"),
            ("Там, где тепло и уютно", "альпака"),
            ("В стае", "волк")
        ]
    },
    {
        "q": "Как ты решаешь проблемы?",
        "a": [
            ("Логикой", "слон"),
            ("Напором", "тигр"),
            ("Советом с друзьями", "волк"),
            ("Терпеливо", "медведь"),
            ("С иронией", "попугай"),
            ("Уединяюсь", "баран"),
            ("Пью чай", "альпака")
        ]
    },
    {
        "q": "Какая еда тебе ближе?",
        "a": [
            ("Фрукты и зелень", "слон"),
            ("Мясо", "тигр"),
            ("Рыба", "медведь"),
            ("Морковка и травы", "альпака"),
            ("Злаки", "баран"),
            ("Орехи, семечки", "попугай"),
            ("Мясо (опять?)", "волк")
        ]
    },
    {
        "q": "Что для тебя важнее всего?",
        "a": [
            ("Семья", "слон"),
            ("Свобода", "тигр"),
            ("Команда", "волк"),
            ("Веселье", "попугай"),
            ("Спокойствие", "медведь"),
            ("Гармония", "альпака"),
            ("Тишина", "баран")
        ]
    }
]

user_answers = {}

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Ошибка отправки email: {e}")

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Пройти викторину 🐾"))
    await message.answer("Привет! 🐾 Добро пожаловать в Московский зоопарк!\n\nХочешь узнать своё тотемное животное?", reply_markup=keyboard)

@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer(
        "🦁 *Помощь по боту:*\n\n"
        "Этот бот поможет тебе узнать своё тотемное животное и познакомиться с программой опеки Московского зоопарка.\n\n"
        "📌 Просто нажми кнопку «Пройти викторину 🐾» и честно ответь на несколько вопросов.\n\n"
        "🐾 В конце ты узнаешь, кто ты в мире животных, сможешь узнать больше об опеке и поделиться результатом с друзьями!",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda msg: msg.text == "Пройти викторину 🐾")
async def start_quiz(message: types.Message):
    user_answers[message.from_user.id] = {"step": 0, "score": {}}
    await send_question(message.from_user.id)

async def send_question(user_id):
    data = user_answers.get(user_id)
    if not data:
        return
    step = data["step"]
    if step >= len(quiz):
        await show_result(user_id)
        return
    question = quiz[step]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for text, _ in question["a"]:
        keyboard.add(KeyboardButton(text))
    await bot.send_message(user_id, f"❓ {question['q']}", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "Пройти ещё раз")
async def restart_quiz(message: types.Message):
    user_answers[message.from_user.id] = {"step": 0, "score": {}}
    await send_question(message.from_user.id)

@dp.message_handler()
async def handle_answer(message: types.Message):
    data = user_answers.get(message.from_user.id)
    if not data:
        await message.answer("Напиши /start, чтобы начать викторину.")
        return
    step = data["step"]
    if step >= len(quiz):
        await show_result(message.from_user.id)
        return
    question = quiz[step]
    answer_text = message.text
    for text, animal in question["a"]:
        if text == answer_text:
            data["score"][animal] = data["score"].get(animal, 0) + 1
            data["step"] += 1
            await send_question(message.from_user.id)
            return
    await message.answer("Пожалуйста, выбери один из предложенных вариантов кнопками 👇")

async def show_result(user_id):
    data = user_answers.get(user_id)
    if not data or not data["score"]:
        await bot.send_message(user_id, "Что-то пошло не так... 😓 Попробуй ещё раз.")
        return
    scores = data["score"]
    top_animal = max(scores, key=scores.get)
    descriptions = {
        "слон": "🐘 Ты — азиатский слон! Мудрый и уравновешенный.",
        "альпака": "🦙 Ты — альпака! Добродушный, тёплый и немного дерзкий 😉",
        "попугай": "🦜 Ты — александрийский попугай! Яркий, шумный и харизматичный.",
        "тигр": "🐅 Ты — амурский тигр! Независимый, сильный и решительный.",
        "медведь": "🐻 Ты — бурый медведь! Терпеливый и надёжный, но можешь показать когти.",
        "баран": "🐏 Ты — голубой баран! Спокойный, выносливый и свободолюбивый.",
        "волк": "🐺 Ты — европейский волк! Умный, преданный и отличный командный игрок."
    }
    result_text = descriptions.get(top_animal, "🤔 Что-то пошло не так...")
    try:
        photo = InputFile(f"images/{top_animal}.jpg")
        await bot.send_photo(user_id, photo, caption=result_text)
    except Exception:
        await bot.send_message(user_id, result_text)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Узнать об опеке 🐾", url="https://moscowzoo.ru/about/guardianship"),
        InlineKeyboardButton("Пройти ещё раз 🔁", callback_data="restart"),
        InlineKeyboardButton("Оставить отзыв ✍️", callback_data="feedback"),
        InlineKeyboardButton("Связаться с сотрудником 📩", callback_data="contact"),
    )
    keyboard.add(
        InlineKeyboardButton("📤 Поделиться результатом", switch_inline_query="Хочу узнать своё тотемное животное! 🐾")
    )
    await bot.send_message(user_id, "👇 Выберите действие:", reply_markup=keyboard)
    user_answers[user_id] = {"step": 0, "score": {}}

@dp.callback_query_handler(lambda call: call.data == "restart")
async def restart_from_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_answers[callback_query.from_user.id] = {"step": 0, "score": {}}
    await send_question(callback_query.from_user.id)

@dp.callback_query_handler(lambda call: call.data == "feedback")
async def feedback_from_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.from_user.id not in user_answers:
        user_answers[callback_query.from_user.id] = {"step": 0, "score": {}}
    user_answers[callback_query.from_user.id]["waiting_feedback"] = True
    await bot.send_message(callback_query.from_user.id, "✍ Напишите свой отзыв одним сообщением.")

@dp.callback_query_handler(lambda call: call.data == "contact")
async def contact_from_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "📩 Наш сотрудник скоро свяжется с вами!\nИли пишите напрямую: @daniilbrylev")

@dp.message_handler(lambda message: user_answers.get(message.from_user.id, {}).get("waiting_feedback"))
async def receive_feedback(message: types.Message):
    user_answers[message.from_user.id]["waiting_feedback"] = False
    await bot.send_message(message.chat.id, "✅ Спасибо за ваш отзыв! Он отправлен сотруднику.")
    feedback_text = f"Отзыв от @{message.from_user.username or message.from_user.id}:\n\n{message.text}"
    send_email(subject="Новый отзыв из бота Московского зоопарка", body=feedback_text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)