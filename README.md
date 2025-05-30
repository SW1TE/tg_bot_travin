# 🐾 Telegram-бот: Тотемное животное | Московский зоопарк

Этот бот создан для Московского зоопарка. Он помогает пользователям пройти викторину и узнать своё **тотемное животное**, а также рассказывает о программе опеки животных.

## 🎯 Основной функционал

- 🦁 Викторина: 4 вопроса — 7 уникальных животных.
- 📷 Показ изображения животного и описание.
- 🔁 Перезапуск викторины.
- 📤 Поделиться результатом с друзьями.
- 🧾 Информация о программе опеки.
- ✍️ Оставить отзыв.
- 📩 Связь с сотрудником зоопарка.
- `/start` и `/help` — команды для запуска и справки.

## 🐍 Используемые технологии

- Python 3.11+
- [aiogram](https://github.com/aiogram/aiogram) (Telegram Bot API)
- SMTP (отправка отзывов на email через Yandex)

## 🚀 Как запустить

1. Установите зависимости:
   ```
   pip install aiogram
   ```

2. Убедитесь, что у вас есть `images/имя_животного.jpg` в папке рядом с `bot.py`

3. Запустите бота:
   ```
   python bot.py
   ```

4. Проверьте, что переменные API и SMTP корректны:
   - `API_TOKEN`
   - `SENDER_EMAIL`
   - `SENDER_PASSWORD`


## 🤝 Автор

- Telegram: [@v_tsukuyomi](https://t.me/v_tsukuyomi)
- При поддержке SkillFactory и Московского зоопарка

---

🧡 _Поддержите Зоопарк — узнайте своё тотемное животное и станьте опекуном!_

