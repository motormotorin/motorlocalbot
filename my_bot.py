import telebot
import parser
import datetime
import urllib.request
from bs4 import BeautifulSoup


#main variables
TOKEN = "869560890:AAG6ux0oE_PD5yzpYF412qglgpWPTP_7mbY"
bot = telebot.TeleBot(TOKEN)

now = datetime.datetime.now()

@bot.message_handler(commands=['start', 'go'])
def start(message):
    
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Ну, давай посмеемся! Напиши что-нибудь, что ли')
    
@bot.message_handler(content_types=['text'])
def main_func(message):
    chat_id = message.chat.id
    text = message.text.lower()
    print(text)
    if text == "погода":
        print('all_ok')
        bot.send_message(chat_id, 'Ща, погодь! Перекинусь словечком с метеорологами...')
        output = ''
        try:
            html = urllib.request.urlopen('https://yandex.ru/pogoda/vladivostok').read()
        except urllib.error.HTTPError:
            print('Error 404 Not Found')
        soup = BeautifulSoup(html, 'html.parser')
        degree = soup.find('span', class_ = 'temp__value')
        degree = degree.get_text()
        print(degree)
        region = soup.find('span', class_ = 'header-title__title-wrap')
        region = region.get_text()
        print(region)
        cloud = soup.find('div', class_ = 'link__condition day-anchor i-bem')
        cloud = cloud.get_text()
        print(cloud)
        msg = bot.send_message(chat_id, "Исходя из данных Яндекса, " + str(region) + " примерно такая: \r\n \r\n" + "Температура воздуха: " + degree + " \r\n \r\n" + "А если посмотреть на небо, то там : \r\n \r\n" + cloud)
    
    elif text == "10":
        print('all_ok')
        print(now.day)
        bot.send_message(chat_id, 'Нужно немного подождать. Пока ты ждешь, можешь подумать о чем-угодно. Узнаю погоду во Владивостоке на 10 дней...')
        output = ''
        out = ''
        try:
            html = urllib.request.urlopen('https://yandex.ru/pogoda/vladivostok/details?via=ms').read()
        except urllib.error.HTTPError:
            print('Error 404 Not Found')
        soup = BeautifulSoup(html, 'html.parser')
        cloud = soup.find_all('td', class_ = 'weather-table__body-cell weather-table__body-cell_type_condition')
        temp_10 = soup.find_all('div', class_ = 'weather-table__temp')
        print(now.strftime("%B"))
        u = 0
        i = 0
        j = 0
        now_day = now.day
        for i in temp_10:
            i = i.get_text()
            if j==0: 
                
                output += (now.strftime("%B") + '   ' + str(now_day) + '\n' + 'Преимущественно '+ cloud[u].get_text().lower() +'\n' +'Утром:     ' + i + '\n')
                j = j + 1
                u = u + 4
            elif j==1: 
                output += ('Днем:      ' + i + '\n')
                j = j + 1
            elif j==2:
                output += ('Вечером:  ' + i + '\n')
                j = j + 1
            elif j==3:
                if now_day >= 31: 
                    now_day = 1
                    j = 0
                    output += ('Ночью:     ' + i + '\n \n')
                else:
                    output += ('Ночью:     ' + i + '\n \n')
                    now_day = now_day + 1
                    j = 0

        msg = bot.send_message(chat_id, output )

        
        
        
        
        
def getWeater(value = 'weather'):
    output = ''
    try:
        html = urllib.request.urlopen('https://yandex.ru/pogoda/').read()
    except urllib.error.HTTPError:
        print('Error 404 Not Found')
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('a', class_ = 'temp__value')
    title = title.get_text()
    return title
    
    
bot.polling(none_stop = True)