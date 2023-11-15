from datetime import datetime, timedelta
import telebot
#from auth_data import token, openaiapi, dbconfig, connect
from telebot import types
import os
import openai
import requests
#from wizzair import get_wizzair_data
#from ivdkdk import get_ivdkdk_data

token = "" # тут ваш токен від телеграм бота
openaiapi = "" # тут ключ апі від чатGPT

bot = telebot.TeleBot(token)
openai.api_key = openaiapi

# 1. Обробник команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("--- нажали старт") 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Погода')
    item2 = types.KeyboardButton('Валюти')
    item3 = types.KeyboardButton('Івенти')
    item4 = types.KeyboardButton('Квітки')
    markup.add(item1, item2)
    markup.add(item3, item4)
    bot.reply_to(message, "Відправлена команда /start \n \n Привіт! Хочеш зіграти у вікторину. Готові почати? Напишіть /quiz", reply_markup=markup)

# Команда для вікторини
@bot.message_handler(commands=['quiz'])
def quiz(message):
    question = "Яка столиця України?"
    answers = ['Київ', 'Львів', 'Одеса', 'Харків']
    print("--- запущена вікторина") 

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for ans in answers:
        markup.add(ans)

    msg = bot.reply_to(message, question, reply_markup=markup)
    bot.register_next_step_handler(msg, process_answer)
    
# 2. Обробник текстових повідомлень    
@bot.message_handler(content_types=["text"])
def send_text(message):
    print("--- text findet")
    try:
        msg_thread_id = message.reply_to_message.message_thread_id
    except AttributeError:
        msg_thread_id = "General"  
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Погода')
    item2 = types.KeyboardButton('Валюти')
    item3 = types.KeyboardButton('Івенти')
    item4 = types.KeyboardButton('Квітки')
    markup.add(item1, item2)
    markup.add(item3, item4)
    if message.text.lower() == "погода":
        req = requests.get("https://api.open-meteo.com/v1/forecast?latitude=55.6759&longitude=12.5655&hourly=temperature_2m,apparent_temperature,precipitation_probability,visibility,windspeed_10m,windgusts_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,winddirection_10m_dominant&timezone=Europe%2FBerlin&forecast_days=1")
        response = req.json()
        temperaturamax = response["daily"]["temperature_2m_max"]
        temperaturamin = response["daily"]["temperature_2m_min"]
        new_markup = types.InlineKeyboardMarkup()
        new_btn = types.InlineKeyboardButton('Погода на сайті', url='https://weather.com/weather/tenday/l/5b11fc345f8675a6547f6a3b93eb2417a6090d2f04943161bdc96d05d0ac9bd7')
        new_markup.add(new_btn)
        bot.send_message(message.chat.id, f"Ось що я нарив про погоду: \nМаксимальна - {temperaturamax}\nМінімальна - {temperaturamin}", reply_to_message_id=message.message_id, reply_markup=new_markup)
        
    elif message.text.lower() == "валюти":
        req = requests.get("http://api.exchangeratesapi.io/v1/latest?symbols=DKK,USD,EUR,UAH&access_key=57825a04d29f2ee2a91aebdc578e52fc")
        response = req.json()
        rates = response['rates']
        dkk = round(rates['DKK'], 2)
        usd = round(rates['USD'], 2)
        eur = round(rates['EUR'], 2)  # Це може бути необхідним, якщо базова валюта може змінюватись
        uah = round(rates['UAH'], 2)
        dkkuah = round((uah / dkk), 2)
        usddkk = round((dkk / usd), 2)
        
        new_markup = types.InlineKeyboardMarkup()
        new_btn = types.InlineKeyboardButton('Курси валют на сайті', url='https://www.google.com/finance/markets/currencies')
        new_markup.add(new_btn)
        bot.send_message(message.chat.id, f"Ось що знаю про валюти: \nDKK={dkkuah} гривень, \nEUR={dkk} крон, \nUSD={usddkk} крон.", reply_to_message_id=message.message_id, reply_markup=new_markup)

        pass
    elif message.text.lower() == "івенти":
        new_markup = types.InlineKeyboardMarkup()
        new_btn = types.InlineKeyboardButton('Дивитись усі заходи на сайті ХАБу', url='https://hub.dkiv.dk/en/events')
        new_markup.add(new_btn)
        sent_message = bot.send_message(message.chat.id, 'Треба трохи зачекати, бо йде запрос на сервер...', reply_to_message_id=message.message_id, reply_markup=new_markup)
        #ivdkdk_data = get_ivdkdk_data()
        #response_message2 = '\n'.join(ivdkdk_data)
      
        #bot.edit_message_text(f"Ось що знаю про івенти: \n" + response_message2, chat_id=message.chat.id, message_id=sent_message.message_id, reply_markup=new_markup)

        pass
    elif message.text.lower() == "квитки":
        #wizzair_data = get_wizzair_data()
        #response_message2 = '\n'.join(wizzair_data)
        new_markup = types.InlineKeyboardMarkup()
        new_btn = types.InlineKeyboardButton('Дивитись сайт WizzAir', url='https://wizzair.com/en-gb/flights/fare-finder/copenhagen/anywhere')
        new_markup.add(new_btn)
        #bot.send_message(message.chat.id, f"Ось що знаю про квитки: \n" + response_message2, reply_to_message_id=message.message_id, reply_markup=new_markup)

        pass
    elif message.text.lower() == "asdasd":
        pass
    else:
        print("--- last text")
        # Виклик OpenAI GPT для генерації відповіді
        #try:
        new_markup = types.InlineKeyboardMarkup()
        new_btn = types.InlineKeyboardButton('кнопка', callback_data='button_clicked')
        new_markup.add(new_btn)
        sent_message = bot.send_message(message.chat.id, 'Треба трохи зачекати, бо йде запрос на сервер...', reply_to_message_id=message.message_id)
        chat_id=message.chat.id
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Цей чат для тих хто прийшов у ХАБ на воркшоп по чат ботам. сайт https://hub.dkiv.dk/"},
                    {"role": "user", "content": "Я можу сам створити бота ?"},
                    {"role": "assistant", "content": "Тобі краще звернутись до Андрія, компанія Бест Чоіс, він все зробить як надо. http://best-choice.dk/"},
                    {"role": "user", "content": "Що ти вмєш ?"},
                    {"role": "assistant", "content": "Я вмію все за допомогою свого творця - Андрія, тільки не забудь йому сказати що ти хочеш, щоб це працювало ;)"},
                    {"role": "user", "content": "Який лінк на фейсбук та лінкедін андрія ?"},
                    {"role": "assistant", "content": "https://www.facebook.com/andrii.denmark та https://www.linkedin.com/in/andrii-lynnyk"},
                    {"role": "user", "content": message.text}
                ],
                temperature=0.8,
                max_tokens=512,
                stop=["stop"]
            )
            response_te = response.choices[0].message['content'].strip()
            bot.edit_message_text(response_te, chat_id=message.chat.id, message_id=sent_message.message_id, reply_markup=new_markup)
        except Exception as ex:
            print(ex)
            bot.edit_message_text(
            "Щось не так... бот зараз не працює...",
            message_id=sent_message.message_id, chat_id=message.chat.id,
            reply_markup=new_markup
            )

# 3. Обробник медіа-повідомлень (наприклад, фото)
@bot.message_handler(content_types=['photo'])
def handle_photo_messages(message):
    print("--- знайдено фото") 
    bot.send_message(message.chat.id, 'було знайдено фото у повідомлені', reply_to_message_id=message.message_id)
    pass


# 4. Обробник для документів
@bot.message_handler(content_types=['document'])
def handle_document_messages(message):
    print("--- знайден документ")
    bot.send_message(message.chat.id, 'був знайден документ у повідомлені', reply_to_message_id=message.message_id)
    pass


# 5. Обробник для аудіо-повідомлень
@bot.message_handler(content_types=['audio'])
def handle_audio_messages(message):
    print("--- знайдено аудіо")
    bot.send_message(message.chat.id, 'було знайдено аудіо у повідомлені', reply_to_message_id=message.message_id)
    pass


# 6. Обробник для відео-повідомлень
@bot.message_handler(content_types=['video'])
def handle_video_messages(message):
    print("--- video findet")
    bot.send_message(message.chat.id, 'було знайдено відео у повідомлені', reply_to_message_id=message.message_id)
    pass
            
            
# 7. Обробник для голосових повідомлень
@bot.message_handler(content_types=['voice'])
def handle_voice_messages(message):   
    print("--- voice findet")
    bot.send_message(message.chat.id, 'було знайдено голосове у повідомлені', reply_to_message_id=message.message_id)
    pass     


# 8. Обробник для стікерів
@bot.message_handler(content_types=['sticker'])
def handle_sticker_messages(message):
    print("--- stivker findet")
    bot.send_message(message.chat.id, 'було знайдено стікер у повідомлені', reply_to_message_id=message.message_id)
    pass


# 10. Обробник для геолокації
@bot.message_handler(content_types=['location'])
def handle_location_messages(message):
    print("--- location findet")
    bot.send_message(message.chat.id, 'було знайдено локацію у повідомлені', reply_to_message_id=message.message_id)
    pass

# 11. Обробник для контактів        
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    print("--- contact findet")
    bot.send_message(message.chat.id, 'було знайдено контакт у повідомлені', reply_to_message_id=message.message_id)


# 12. Обробник для пересланих повідомлень
@bot.message_handler(func=lambda message: message.forward_from is not None)
def handle_forwarded_messages(message):
    print("--- forward findet")
    bot.send_message(message.chat.id, 'було знайдено переслане повідомлення у повідомлені', reply_to_message_id=message.message_id)
    pass


# 13. Обробник для повідомлень із вказаною локацією (геотегом)
@bot.message_handler(content_types=['venue'])
def handle_venue_messages(message):
    bot.send_message(message.chat.id, 'було знайдено геотег у повідомлені', reply_to_message_id=message.message_id)
    pass     


# 14. Обробник для обробки відповідей на повідомлення
@bot.message_handler(func=lambda message: message.reply_to_message is not None)
def handle_reply_messages(message):
    print("--- reply findet")
    bot.send_message(message.chat.id, 'було знайдено відповідь у повідомлені', reply_to_message_id=message.message_id)
    pass


# 15. Обробник для анімацій (GIF)
@bot.message_handler(content_types=['animation'])
def handle_animation_messages(message):
    print("--- gif findet")
    bot.send_message(message.chat.id, 'було знайдено гіф у повідомлені', reply_to_message_id=message.message_id)
    pass


# 16. Обробник для згадок користувачів
@bot.message_handler(func=lambda message: message.entities is not None and message.entities[0].type == "mention")
def handle_user_mention(message):
    print("--- mention findet")
    bot.send_message(message.chat.id, 'було знайдено згадування у повідомлені', reply_to_message_id=message.message_id)
    pass


# 17. Обробник для хештегів
@bot.message_handler(func=lambda message: message.entities is not None and message.entities[0].type == "hashtag")
def handle_hashtag_messages(message):
    print("--- hashtag findet")
    bot.send_message(message.chat.id, 'було знайдено хештег у повідомлені', reply_to_message_id=message.message_id)
    pass


# 18. Обробник для посилань
@bot.message_handler(func=lambda message: message.entities is not None and message.entities[0].type == "url")
def handle_url_messages(message):
    print("--- url findet")
    bot.send_message(message.chat.id, 'було знайдено посилання у повідомлені', reply_to_message_id=message.message_id)
    pass


# 20. Обробник для пінгованих повідомлень
@bot.message_handler(func=lambda message: message.pinned_message is not None)
def handle_pinned_messages(message):
    print("--- pinned findet")
    bot.send_message(message.chat.id, 'було знайдено закріпленє у повідомлені', reply_to_message_id=message.message_id)
    pass


# 21. Обробник для голосувань
@bot.message_handler(content_types=['poll'])
def handle_poll_messages(message):
    print("--- poll findet")
    bot.send_message(message.chat.id, 'було знайдено голосування у повідомлені', reply_to_message_id=message.message_id)
    pass


# 22. Обробник для сервісних повідомлень (наприклад, вхід в групу)
@bot.message_handler(content_types=['new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
def handle_service_messages(message):
    print("--- service findet")
    bot.send_message(message.chat.id, 'Вітаємо нового користувача !', reply_to_message_id=message.message_id)
    pass


# 23. Обробник для готових опцій клавіатури (рядок кнопок під введенням тексту)
@bot.message_handler(func=lambda message: message.reply_markup is not None and isinstance(message.reply_markup, types.ReplyKeyboardMarkup))
def handle_keyboard_markup(message):
    print("--- button findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass
    
    
# 24. Обробник для відео-нотаток
@bot.message_handler(content_types=['video_note'])
def handle_video_note_messages(message):
    print("--- videonote findet")
    bot.send_message(message.chat.id, 'було знайдено відео у повідомлені', reply_to_message_id=message.message_id)

    pass
    
    
# 25. Обробник для повідомлень, що містять супергрупу
@bot.message_handler(func=lambda message: message.chat.type == 'supergroup')
def handle_supergroup_messages(message):
    print("--- supergroup findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass

    
# 26. Обробник для повідомлень в приватному чаті
@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_private_chat_messages(message):
    print("--- privatechat findet")
    bot.send_message(message.chat.id, 'ви з ботом спілкуєтесь у приватному чаті', reply_to_message_id=message.message_id)

    pass
    
    
# 27. Обробник для повідомлень в груповому чаті
@bot.message_handler(func=lambda message: message.chat.type == 'group')
def handle_group_chat_messages(message):
    print("--- groupchat findet")
    bot.send_message(message.chat.id, 'було знайдено повідомлення у групі', reply_to_message_id=message.message_id)

    pass
    
    
# 28. Обробник для повідомлень з каналу
@bot.message_handler(func=lambda message: message.chat.type == 'channel')
def handle_channel_messages(message):
    print("--- channelchat findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass
    
    
# 29. Обробник для повідомлень із згадкою бота
@bot.message_handler(func=lambda message: message.entities is not None and message.entities[0].type == "bot_command" and "@ukrainianhub_bot" in message.text)
def handle_bot_mention(message):
    print("--- tagbot findet")
    bot.send_message(message.chat.id, 'згадали бота', reply_to_message_id=message.message_id)

    pass
    
   
# 30. Обробник для повідомлень із кнопок inline клавіатури            
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    print("--- callback findet")
    if call.data == 'button_clicked':
        bot.answer_callback_query(call.id, 'Ви натиснули кнопку!')
        new_markup = types.InlineKeyboardMarkup()
        new_btn = types.InlineKeyboardButton('Нова кнопка', callback_data='button_clicked2')
        new_markup.add(new_btn)
        bot.edit_message_text('Текст було змінено.', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=new_markup)
    elif call.data == 'button_clicked2':
        bot.answer_callback_query(call.id, 'Знову натиснули кнопку!')
        new_markup = types.InlineKeyboardMarkup()
        new_btn = types.InlineKeyboardButton('Інша нова кнопка', callback_data='button_clicked')
        new_markup.add(new_btn)
        bot.edit_message_text('Текст ЗНОВУ було змінено.', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=new_markup)
                   
                        
# 31. Обробник для повідомлень з додатковими кнопками
@bot.message_handler(func=lambda message: message.reply_markup is not None and isinstance(message.reply_markup, types.InlineKeyboardMarkup))
def handle_inline_keyboard_markup(message):
    print("--- button2 findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass
    
    
# 32. Обробник для повідомлень з медіа-групою
@bot.message_handler(content_types=['media_group'])
def handle_media_group_messages(message):
    print("--- mediagroup findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass


# 33. Обробник для повідомлень із застосунками
@bot.message_handler(content_types=['game'])
def handle_game_messages(message):
    print("--- game findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass


# 34. Обробник для повідомлень із заголовками (веб-сайтів, посилань)
@bot.message_handler(func=lambda message: message.entities is not None and message.entities[0].type == "text_link")
def handle_text_link_messages(message):
    print("--- textlink findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass


# 35. Обробник для повідомлень із кодом
@bot.message_handler(func=lambda message: message.entities is not None and message.entities[0].type == "code")
def handle_code_messages(message):
    print("--- code findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass


# 36. Обробник для повідомлень із виділенням тексту
@bot.message_handler(func=lambda message: message.entities is not None and message.entities[0].type == "italic")
def handle_italic_text_messages(message):
    print("--- italic findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass

# 37. Обробник для повідомлень із жирним текстом
@bot.message_handler(func=lambda message: message.entities is not None and message.entities[0].type == "bold")
def handle_bold_text_messages(message):
    print("--- bold findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass


# 38. Обробник для повідомлень із посиланням на канал
@bot.message_handler(func=lambda message: message.entities is not None and message.entities[0].type == "channel_chat_created")
def handle_channel_chat_created_messages(message):
    print("--- link to channel findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass


# 39. Обробник для повідомлень із захардкодованим номером телефону
@bot.message_handler(func=lambda message: message.contact is not None and message.contact.phone_number is not None)
def handle_contact_phone_number_messages(message):
    print("--- telephone findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass


# 40. Обробник для повідомлень із датами
@bot.message_handler(func=lambda message: message.date is not None)
def handle_date_messages(message):
    print("--- date findet")
    bot.send_message(message.chat.id, 'було знайдено ... у повідомлені', reply_to_message_id=message.message_id)

    pass

                
# останній обробник                
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    print("-- станній обробник")
    bot.send_message(message.chat.id, 'станній обробник', reply_to_message_id=message.message_id)

    

def process_answer(message):
    if message.text == "Київ":
        bot.send_message(message.chat.id, "Вірно!", reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, "Невірно. Спробуйте ще раз!", reply_to_message_id=message.message_id)


bot.polling()
