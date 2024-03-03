# import library yang kita butuhkan
import telebot
import yfinance as yf
import pandas as pd

#isikan token yang kita dapatkan
API_KEY = '7166054005:AAFKddSi1YDpuJpxxu1iIhqmXFHR7Bly5Og'
bot = telebot.TeleBot(API_KEY)

start_message = """Halo! Saya adalah StocksBotID.
Saya dapat membantu Anda dengan informasi saham dan data harga saham.
Silakan ketikkan perintah seperti:
- info [nama_ticker] untuk mendapatkan informasi saham.
- harga [nama_ticker] untuk mendapatkan data harga saham.
- download [nama_ticker] untuk mendownload data harga saham"""

@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message, start_message)

# Setiap kata yang kita masukkan menjadi parameter di "commands", yang kita ketikkan
# di bot akan menampilkan message sesuai dengan yang kita mau
# Ketika kita ketikkan /Salam di bot, maka akan muncul pesan otomatis
# "Halo, Saya StocksBotID siap membantu anda."
@bot.message_handler(commands=['Salam'])
def greet(message):
  bot.reply_to(message, "Halo, Saya StocksBotID siap membantu anda.")

@bot.message_handler(commands=['Halo'])
def hello(message):
  bot.send_message(message.chat.id, "Halo!")


# Fungsi ini untuk memberikan informasi saham setiap diketikkan kata "info" + ticker saham
# Karena ada banyak kriteria informasi saham, kita coba dengan memberikan yang biasa kita perlukan.
# jika kode ticker saham diketikkan dan diawali kata "info", makan fungsi akan menghasilkan True
# Ini berguna untuk filter kata penulisan yang kita harapkan untuk diketikkan ke dalam bot
# Jika diketikkan "info BBNI.JK", maka akan menghasilkan True dan lanjut ke fungsi dibawahnya
def stock_info(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "info":
        return False
    else:
        return True

@bot.message_handler(func=stock_info)
def send_info(message): 
    request = message.text.split()[1]
    ticker = yf.Ticker(request)
    
    # Mengambil informasi umum tentang saham
    info = ticker.info

    # Membuat pesan balasan dengan membatasi jumlah informasi yang ditampilkan
    response = "Informasi tentang saham:\n"
    keys_to_display = ['shortName', 'sector', 'country', 'marketCap', 'regularMarketPrice', 'earningsGrowth', 'revenueGrowth']
    for key in keys_to_display:
        if key in info:
            response += f"{key}: {info[key]}\n"

    # Mengirim pesan balasan kepada pengguna
    bot.send_message(message.chat.id, response)


# Ini adalah contoh fungsi untuk mendapatkan data harga saham
# jika kode ticker saham diketikkan dan diawali kata "harga", makan fungsi akan menghasilkan True
# Ini berguna untuk filter kata penulisan yang kita harapkan untuk diketikkan ke dalam bot
# Jika diketikkan "harga BBNI.JK", maka akan menghasilkan True dan lanjut ke fungsi dibawahnya
def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "harga":
    return False
  else:
    return True
  
# Kemudian harga saham ditarik dari fungsi ini, dengan interval 1 hari selama 5 hari terakhir
# Sayangnya, untuk yfinance hanya bisa menarik data saham dengan interval tercepat 1 hari.
@bot.message_handler(func=stock_request)
def send_price(message):
    request = message.text.split()[1]
    data = yf.download(tickers=request, period='5d', interval='1d')

    if data.size > 0:
        data["format_date"] = data.index.strftime('%m/%d %I:%M %p')
        response = data[['Close', 'format_date']].to_string(header=False)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Tidak ada data harga saham.")

    
# Sama seperti diatas, skrip ini untuk mendownload data harga saham
def stock_price(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() != "download":
        return False
    else:
        return True

@bot.message_handler(func=stock_price)
def download_price(message):
    request = message.text.split()[1]
    # Selama satu tahun dengan interval satu hari bursa
    data = yf.download(tickers=request, period='1y', interval='1d')

    if data.size > 0:
        filename = f"{request}_price.csv"
        data.to_csv(filename)
        bot.send_document(message.chat.id, open(filename, 'rb'))
    else:
        bot.send_message(message.chat.id, "Tidak ada data harga saham.")


# Eksekusi semua fungsi
bot.polling()