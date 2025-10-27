from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in environment variables. Please create a .env file.")

# --- Главное меню выбора тарифов ---
def tariff_selection_menu():
    text = "О каком тарифном плане хочешь узнать больше?"
    keyboard = [
        [InlineKeyboardButton("План B", callback_data="plan_b")],
        [InlineKeyboardButton("Для своих", callback_data="for_friends")]
    ]
    return text, InlineKeyboardMarkup(keyboard)

# --- Меню План B ---
def plan_b_menu():
    text = "👋 Узнай больше о тарифе План Б"
    keyboard = [
        [InlineKeyboardButton("📌 Топовая комбинация со скидкой", callback_data="combo")],
        [InlineKeyboardButton("💰 Обмен ГБ на золото", callback_data="gold_exchange")],
        [InlineKeyboardButton("📌 Все о тарифе План Б", callback_data="about")],
        [InlineKeyboardButton("📌 Совместимость с акциями", callback_data="promo")],
        [InlineKeyboardButton("📌 Механика подключения", callback_data="activation")],
        [InlineKeyboardButton("📌 Цены и другие условия", callback_data="prices")],
        [InlineKeyboardButton("📌 Просто вопросы", callback_data="faq")],
        [InlineKeyboardButton("Назад", callback_data="back_to_main")]
    ]
    return text, InlineKeyboardMarkup(keyboard)

# --- Меню "Для своих" ---
def for_friends_menu():
    text = "Дари промокоды близким, чтобы связь была выгодной!"
    keyboard = [
        [InlineKeyboardButton("где найти промокоды?", callback_data="for_friends_promo")],
        [InlineKeyboardButton("все о тарифе", callback_data="for_friends_about")],
        [InlineKeyboardButton("ограничения", callback_data="for_friends_limits")],
        [InlineKeyboardButton("Назад", callback_data="back_to_main")]
    ]
    return text, InlineKeyboardMarkup(keyboard)

# --- Старт ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text, reply_markup = tariff_selection_menu()
    await update.message.reply_text(text, reply_markup=reply_markup)

# --- Обработчик кнопок ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = ""
    reply_markup = None

    if query.data == "back":
        # try to delete last sent document message
        last_mid = context.user_data.get("last_doc_mid")
        if last_mid:
            try:
                await context.bot.delete_message(chat_id=query.message.chat.id, message_id=last_mid)
            except TelegramError:
                pass
            finally:
                context.user_data.pop("last_doc_mid", None)
        text, reply_markup = plan_b_menu()
    
    elif query.data == "back_to_main":
        # try to delete last sent document message
        last_mid = context.user_data.get("last_doc_mid")
        if last_mid:
            try:
                await context.bot.delete_message(chat_id=query.message.chat.id, message_id=last_mid)
            except TelegramError:
                pass
            finally:
                context.user_data.pop("last_doc_mid", None)
        text, reply_markup = tariff_selection_menu()
    
    elif query.data == "plan_b":
        text, reply_markup = plan_b_menu()
    
    elif query.data == "for_friends":
        text, reply_markup = for_friends_menu()

    # --- Акция ---
    elif query.data == "combo":
        text = (
            "🔥 *Акция по тарифу «План Б.»*\n\n"
            "490 ₽/мес за комбинацию 50 ГБ и 200 мин на 3 месяца — для новых абонентов + 1ТБ в подарок \n\n"
            "*Условия:*\n"
            "— Только для подключения нового номера и активации SIM в период акции\n"
            "— Смена пакета или тарифа = скидка отключается\n"
            "— После 3 месяцев — абон. плата по тарифу филиала\n\n"
            "*За 490 ₽/мес абонент получает:*\n"
            "— 50 ГБ интернета каждый месяц\n"
            "— 200 минут на звонки любому оператору \n"
            "— 1 ТБ в подарок при подключении или 50 ГБ при переходе на тариф\n"
            "— Безлимитный интернет на 3 часа ежедневно\n"
            "— Telegram Premium 6 мес. бесплатно\n"
            "— Нейросети без VPN, до 100 запросов в день\n"
            "— Перенос остатков, гигабайты не сгорают\n"
            "— Обмен остатков на золото\n"
            "— Безлимит на популярные сервисы\n"
            "— Мини-приложение в Telegram для управления тарифом\n\n"
            "📄 Файл с памяткой и готовыми ответами на возражения — ниже:"
        )
        keyboard = [
            [InlineKeyboardButton("📄 Скачать памятку", callback_data="send_pdf")],
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data == "send_pdf":
        file_path = "planb.pdf"
        try:
            with open(file_path, "rb") as f:
                sent = await context.bot.send_document(
                    chat_id=query.message.chat.id,
                    document=f,
                    filename="PlanB.pdf",
                    caption="📄 Вот твоя памятка по тарифу План Б!"
                )
                # store message id for cleanup
                context.user_data["last_doc_mid"] = sent.message_id
        except FileNotFoundError:
            await query.message.reply_text("❌ Файл planb.pdf не найден. Помести его рядом с ботом.")
        return

    # --- Все о тарифе ---
    elif query.data == "about":
        text = (
            "план б - это больше, чем связь. Это тариф для тех, кто не боится расширять границы: нейросети, управление из мини-апп в тг, бонусы и компенсации\n\n"
            "Ты можешь выбрать разное наполнение:\n"
            "ИНТЕРНЕТ: 25 гб / 50 гб / 100 гб\n"
            "ЗВОНКИ: 0 мин / 200 мин / 400 мин\n\n"
            "в тариф уже включены безлимиты: у тебя будет безлимит на мессенджеры, соцсети (VK и Одноклассники), видео (Rutube, VK Видео, VK Клипы и TikTok) и музыку (Яндекс Музыка и Apple Music). только активируй их в приложении билайн\n\n"
            "также абонентам плана б билайн компенсирует подписку телеграм премиум, дает 100 запросов в день в топовых нейросетях, 3 часа безлимита каждый день и копит остатки минут и гб.\n\n"
            "узнать подробнее обо всем:"
        )
        keyboard = [
            [InlineKeyboardButton("⭐️ Компенсация премиума", callback_data="about_premium")],
            [InlineKeyboardButton("🤖 Нейросети", callback_data="about_ai")],
            [InlineKeyboardButton("📦 Копилка минут и ГБ", callback_data="about_rollover")],
            [InlineKeyboardButton("♾️ Безлимит", callback_data="about_unlim")],
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data == "about_premium":
        text = (
            "⭐️ *Компенсация премиума*\n\n"
            "Да — компенсируем по 299 ₽ в месяц, 6 месяцев. Эти деньги падают на бонусный баланс и автоматически списываются в счёт оплаты тарифа — потратить их на что-то другое не получится, зато связь будет выгоднее.\n\n"
            "Важно: нужно быть на Плане Б — плюшка действует только на нём."
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="about")]])

    elif query.data == "about_ai":
        text = (
            "🤖 *Нейросети*\n\n"
            "Работа с текстом, картинками, генерация изображений, оживление фото — ChatGPT, DeepSeek, Gemini, Claude, Flux и Runway, и всё без VPN."
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="about")]])

    elif query.data == "about_rollover":
        text = (
            "📦 *Копилка минут и ГБ*\n\n"
            "Всё, за что уплочено, должно быть проплочено! Все непотраченные ГБ и минуты остаются с тобой и переходят на следующий месяц — нужно только оплачивать План Б вовремя и держать баланс в плюсе. Работает только на Плане Б."
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="about")]])

    elif query.data == "about_unlim":
        text = (
            "♾️ *Безлимит*\n\n"
            "Каждый день ты можешь включать 3 часа безлимитного интернета: смотреть фильмы, слушать подкасты или играть не переживая за остаток ГБ — и это всё плюсом к другим безлимитам в тарифе."
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="about")]])

    # --- Акции ---
    elif query.data == "promo":
        text = (
            "🎁 *Совместимость с акциями*\n\n"
            "план б уникален, поэтому не совместим с классическими акциями билайна.\n\n"
            "Зато на замену им пришла акция \"Легкий старт\" — скидка первые 3 месяца на комбинации 100 ГБ/0 мин и 50 ГБ/200 мин.\n"
            "А также честный 1 ТБ в подарок при подключении и 50 ГБ при переходе на тариф"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="back")]])

    # --- Механика подключения ---
    elif query.data == "activation":
        text = (
            "⚡️ *Механика подключения Плана Б*\n\n"
            "1) После активации SIM-карты будет отправлена смс с ссылкой на мини-апп в Telegram.\n"
            "2) Необходимо запустить бота кнопкой /start\n"
            "3) Перейти в мини-апп, нажав на кнопку \"в мини-аппку\""
        )
        keyboard = [
            [InlineKeyboardButton("📩 Что делать, если не пришла SMS", callback_data="activation_nosms")],
            [InlineKeyboardButton("🤖 Для чего нужен мини-апп", callback_data="activation_app")],
            [InlineKeyboardButton("📱 У меня уже есть SIM Билайна — как перейти?", callback_data="activation_existing")],
            [InlineKeyboardButton("📖 Памятка для активации", callback_data="activation_pptx")],
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data == "activation_nosms":
        text = (
            "📩 *Если SMS не пришла*\n\n"
            "Если не пришла смс, то перейти в Telegram можно через мобильное приложение Билайн."
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="activation")]])

    elif query.data == "activation_app":
        text = (
            "🤖 *Для чего нужен мини-апп*\n\n"
            "Из уникального там доступ к нейронкам и компенсации TG Премиума. ГБ и минуты можно настроить и там, и в приложении Билайн — то же самое и с пополнением баланса."
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="activation")]])

    elif query.data == "activation_existing":
        text = (
            "📱 *Уже есть SIM?*\n\n"
            "В приложении Билайн — зайди в него со своим номером и выбери тариф План Б."
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="activation")]])

    elif query.data == "activation_pptx":
        file_path = "activation.pptx"
        try:
            with open(file_path, "rb") as f:
                sent = await context.bot.send_document(
                    chat_id=query.message.chat.id,
                    document=f,
                    filename="Activation.pptx",
                    caption="📖 Памятка для активации"
                )
                context.user_data["last_doc_mid"] = sent.message_id
        except FileNotFoundError:
            await query.message.reply_text("❌ Файл activation.pptx не найден.")
        return

    # --- Цены ---
    elif query.data == "prices":
        text = (
            "💰 *Цены и другие условия*\n\n"
            "цены на все комбинации ты можешь посмотреть на этой странице:\n"
            "https://beeline.ru/customers/products/mobile/tariffs/details/plan-b/\n\n"
            "❗ Проверь, что открылся твой регион!\n\n"
            "*Дополнительно:*\n"
            "исходящие SMS на местные номера всех операторов — 2,5 ₽/шт\n\n"
            "исходящие вызовы в страны СНГ, Грузию, Украину — 39 ₽/мин\n\n"
            "исходящие вызовы в Европу, США, Канаду, Вьетнам, Китай, Турцию — 60 ₽/мин\n\n"
            "исходящие вызовы в остальные страны — 85 ₽/мин\n\n"
            "исходящие SMS на международные номера — 8 ₽/шт\n\n"
            "пакет 1 ГБ с автопродлением: 1 ГБ / 120 ₽"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="back")]])

    # --- FAQ (новый блок с кнопками) ---
    elif query.data == "faq":
        text = "❓ *Частые вопросы*\n\nВыбери интересующий:"
        keyboard = [
            [InlineKeyboardButton("Это отдельный Билайн?", callback_data="faq_beeline")],
            [InlineKeyboardButton("Доступна ли семья?", callback_data="faq_family")],
            [InlineKeyboardButton("Что по безлимитам?", callback_data="faq_unlim")],
            [InlineKeyboardButton("А безопасность?", callback_data="faq_security")],
            [InlineKeyboardButton("А если уйду в минус?", callback_data="faq_minus")],
            [InlineKeyboardButton("Интернет можно шарить?", callback_data="faq_share")],
            [InlineKeyboardButton("Как компенсировать TG Premium?", callback_data="faq_premium")],
            [InlineKeyboardButton("Зачем TG мини-апп?", callback_data="faq_miniapp")],
            [InlineKeyboardButton("Как переносятся ГБ и минуты?", callback_data="faq_rollover")],
            [InlineKeyboardButton("Какие нейронки входят?", callback_data="faq_ai")],
            [InlineKeyboardButton("Ещё раз про плюшки", callback_data="faq_bonus")],
            [InlineKeyboardButton("Как купить SIM?", callback_data="faq_buy")],
            [InlineKeyboardButton("Электронная SIM", callback_data="faq_esim")],
            [InlineKeyboardButton("Перейти со своей SIM", callback_data="faq_switch")],
            [InlineKeyboardButton("Подробнее", callback_data="faq_more")],
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    # ответы на FAQ
    elif query.data == "faq_beeline":
        text = (
            "нет, это новый тариф, на котором доступен весь базовый билайн, — интернет по всей России (кроме Республики Крым, Севастополя, Анадыря и Норильска) и звонки на номера любых операторов России. роуминг, конечно, тоже есть, но нет семьи в билайне и домашнего интернета — по крайней мере, пока"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_family":
        text = "нет, семьи на плане б нет"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_unlim":
        text = (
            "всё есть — у тебя будет безлим на мессенджеры, соцсети (VK и Одноклассники), видео (Rutube, VK Видео, VK Клипы и TikTok) и музыку (Яндекс Музыка и Apple Music). только активируй их в приложении билайн"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_security":
        text = (
            "заботимся и о ней — предупредим о мошенниках и защитим от спама и нежелательных подписок. это всё можно настроить в приложении билайн"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_minus":
        text = (
            "мессенджеры, навигация и сервисы билайна будут работать 24 часа — нужно только подключить бесплатную поддержку при нуле в приложении билайн. ещё есть обещанный платёж — если сейчас баланс пополнить совсем не удобно"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_share":
        text = "да — если у твоего смартфона есть режим модема"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_premium":
        text = (
            "через тг мини-аппку. раз в месяц компенсируем по 299 ₽ — и так 6 раз. то есть ты можешь оплачивать премиум ежемесячно или купить сразу на год — просто заходи в мини-аппку и получай возврат. премиум должен быть оформлен на тот номер, на котором план б."
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_miniapp":
        text = (
            "из уникального там доступ к нейронкам и компенсации тг премиума. гб и минуты можно настроить и там, и в приложении билайн — то же самое и с пополнением баланса"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_rollover":
        text = (
            "автоматически — при условии, что вовремя оплачиваешь план б. и держишь баланс в плюсе. переносятся все гб и минуты, которые не потратишь в этом месяце"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_ai":
        text = (
            "ChatGPT, DeepSeek, Gemini, Claude, Flux, Suno, Runway, VEO 3 — все нужные для работы с текстом, картинками и видео. всё работает без впн, в день у тебя 100 запросов (в зависимости от выбранной модели)"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_bonus":
        text = (
            "окей, кратко. остатки гб и минут не сгорают и переносятся на следующий месяц — для этого нужно просто оплачивать тариф вовремя. комбодоступ к нейронкам для любых задач без впн. компенсация тг премиума. все преимущества самого билайна: безопасность, поддержка при нуле, качество связи"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_buy":
        text = (
            "можно зайти с паспортом в любой из наших офисов или оформить всё за пару минут на сайте или в приложении билайн"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_esim":
        text = (
            "конечно — главное, чтобы сам смартфон её поддерживал. ну и чтобы на ней был план б. ;) приходи в офис с паспортом или оформи всё в приложении билайн или на сайте"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_switch":
        text = (
            "в приложении билайн — зайди в него со своим номером и выбери тариф план б."
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    elif query.data == "faq_more":
        text = (
            "Подробнее: https://beeline.ru/customers/products/mobile/tariffs/details/plan-b/\n\n"
            "❗ Проверь, что открылся твой регион"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="faq")]])

    # --- Обмен ГБ на золото ---
    elif query.data == "gold_exchange":
        text = (
            "💰 *Обмен ГБ на золото*\n\n"
            "Абоненты тарифного плана \"План Б\" могут обменять накопленные ГБ на рубли!\n\n"
            "До 15.01.2026 все накопленные гигабайты можно обменять на золото, а затем конвертировать его в рубли по курсу ЦБ.\n\n"
            "*План такой:*\n"
            "— Подключаем тариф План Б\n"
            "— Вовремя оплачиваем связь и копим ГБ\n"
            "— Добываем золото в мини-апп по курсу: 1 ГБ = 1 мг золота\n"
            "— Выводим добытое золото на бонусный баланс по курсу ЦБ\n"
            "— Оплачиваем связь бонусными рублями и копим ГБ дальше\n\n"
            "*Важные условия:*\n"
            "— Накопленный остаток ГБ должен быть больше размера подключенного в тарифе пакета, не менее чем на 1 ГБ\n"
            "— Максимальное значение обмениваемых ГБ в календарном месяце не может быть больше 100 ГБ\n"
            "— Баланс должен быть положительным\n"
            "— Номер не должен находиться в адм. блокировке\n\n"
            "*Пример начисления бонусных рублей:*\n"
            "Абонент использовал за месяц 10 ГБ из 50, значит на следующий месяц у него в остатке уже 40 ГБ\n"
            "40 ГБ = 40 мг золота = 349 бонусных рублей по курсу 8 725 рублей за 1 г золота = второй месяц связи оплачен на 71%"
        )
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    # --- Обработчики для тарифа "Для своих" ---
    elif query.data == "for_friends_promo":
        text = (
            "Письмо с промокодами пришло сотрудникам Билайна 17.09.2025 на корпоративную почту.\n"
            "Его легко найти в поиске по отправителю: benefit@beeline.ru\n\n"
            "*Обрати внимание:*\n"
            "Промокоды для подключения тарифа существуют в единственном экземпляре — при утере их восстановление невозможно."
        )
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="for_friends")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data == "for_friends_about":
        text = (
            "На тарифе два выгодных пресета:\n\n"
            "500 минут, безлимитные ГБ — 300 руб\n\n"
            "1000 минут, безлимитные ГБ — 350 руб\n\n"
            "Безлимитные опции включены в абонентскую плату: мессенджеры, музыка, соцсети, видео, сервисы Яндекса.\n"
            "Безлимитные звонки на Билайн по РФ включены в абонентскую плату.\n\n"
            "Тариф доступен только при новых подключениях в собственных офисах или при переходе по MNP при наличии промокода.\n\n"
            "За продажу тарифа начисляется 0,2 УП.\n"
            "Для успешной продажи тарифа в чеке должна быть только одна сим-карта.\n\n"
            "*Обрати внимание:*\n"
            "Для жителей Норильска и Анадыря пресеты другие:\n\n"
            "500 минут, 60 ГБ — 490 руб\n\n"
            "1000 минут, 60 ГБ — 550 руб"
        )
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="for_friends")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif query.data == "for_friends_limits":
        text = (
            "Подключение доступно по MNP только в регионе подключения абонента.\n"
            "В других регионах переход по MNP недоступен по техническим причинам.\n\n"
            "На тарифе недоступны:\n\n"
            "Акция «Твоя выгода»\n\n"
            "Возможность делиться тарифом с дополнительными номерами («Дели все» или «Дели гига»)\n\n"
            "Акционные предложения и бонусы на оборудование\n\n"
            "Домашний интернет (пока не доступен, но находится в разработке)\n\n"
            "Тариф доступен только для новых подключений и только в собственных офисах."
        )
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="for_friends")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    else:
        text, reply_markup = tariff_selection_menu()

    try:
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")
    except TelegramError as e:
        # Handle stale callback queries (pressed on an old message)
        if "Query is too old" in str(e) or "query is too old" in str(e):
            fresh_text, fresh_markup = tariff_selection_menu()
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=fresh_text + "\n\n(Сообщение было устаревшим, показываю актуальное меню)",
                reply_markup=fresh_markup,
                parse_mode="Markdown",
            )
            return
        else:
            raise

# --- Запуск ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Бот План Б запущен! Ждем команду /start")
    app.run_polling()

if __name__ == "__main__":
    main()

