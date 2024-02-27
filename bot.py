import telebot
import yfinance as yf

API_KEY = '7123140191:AAEL-SOG_2Vtnnjn6gfDFSKyGVTYY5vlO2c'
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['Salam'])
def greet(message):
  bot.reply_to(message, "Halo, Saya StocksBotID siap membantu anda.")

@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "Hello!")

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "cek":
    return False
  else:
    return True

@bot.message_handler(func=stock_request)
def send_price(message):
    request = message.text.split()[1]
    data = yf.download(tickers=request, period='5d', interval='1d')

    if data.size > 0:
        data["format_date"] = data.index.strftime('%m/%d %I:%M %p')
        response = data[['Close', 'format_date']].to_string(header=False)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "No data!?")

# @bot.message_handler(func=stock_request)
# def send_price_minutely(message):
#     request = message.text.split()[1]
#     data = yf.download(tickers=request, period='5m', interval='1m')

#     if data.size > 0:
#         data["format_date"] = data.index.strftime('%m/%d %I:%M %p')
#         response = data[['Close', 'format_date']].to_string(header=False)
#         bot.send_message(message.chat.id, response)
#     else:
#         bot.send_message(message.chat.id, "No data!?")




bot.polling()