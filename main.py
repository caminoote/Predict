import telebot
import os
import time
from ultralytics import YOLO
from ftplib import FTP

ftp = FTP('')#Корпаративная информация
ftp.login(user='', passwd='')#Корпаративная информация
#print(ftp.pwd())
curdir=os.getcwd()
#print(curdir)

'''
files = ftp.nlst()
print(files[0])
os.chdir('D:/pythonProject/PredictModel/Directory')
my_file = open(files[0],'wb')  # Open a local file to store the downloaded file
ftp.retrbinary('RETR ' + files[0], my_file.write, 1024) # Enter the filename to download
os.chdir(curdir)
ftp.delete(files[0])
'''

def ftp_files():
    files = ftp.nlst()
    print(files[0])
    os.chdir('D:/pythonProject/PredictModel/Directory')
    my_file = open(files[0], 'wb')  # Open a local file to store the downloaded file
    ftp.retrbinary('RETR ' + files[0], my_file.write, 1024)  # Enter the filename to download
    os.chdir(curdir)
    ftp.delete(files[0])

def send_telegram(text: str, url: str):
    token = ''#Корпаративная информация
    bot = telebot.TeleBot(token)
    channel_id = ''#Корпаративная информация
    #bot.send_message(channel_id, text)
    bot.send_photo(channel_id, open(url,'rb'), caption=text)

def find_file():
    for root, dirs, files in os.walk('D:/pythonProject/PredictModel/Directory'):
        for file in files:
            if file.endswith('.jpg'):
                return os.path.join(root, file)

if __name__ == '__main__':
    kol = 0
    while 1:
        ftp_files()
        FilePath = find_file()
        if (FilePath != None):
            FileName = os.path.basename(FilePath)

            print("Имя изображения "+FileName)
            #Путь до изображения
            print("Путь изображения " +FilePath)

            model = YOLO("D:/pythonProject/PredictModel/UseModel/best.pt")
            results = model(FilePath)# ,save = True
            result = results[0]
            FileDir = "D:/pythonProject/PredictModel/AccessPhoto/"
            print("------------------")
            #считает количество найденных объектов
            print(len(result.boxes))
            if (len(result.boxes) > 1):
                send_telegram("На линии №3 возможно произведен брак,\n"
                              "проверьте углы ПВХ профиля", FilePath)
                os.replace(FilePath, FileDir+FileName)
                kol = kol+1
                print("Количество найденного брака:  "+str(kol))
            else:
                os.remove(FilePath)#Удаление обработанного файла
        time.sleep(10)
