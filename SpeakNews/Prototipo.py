from newspaper import Article
from gtts import gTTS
from pygame import mixer
import time
from bs4 import BeautifulSoup
import requests

print("|-------------------------------")
print("|---- S P E A K   N E W S  -----")
print("|-------------------------------")
print("\n\n\n|--------PROTOTIPO--------------")
print("|---- Digite sua pesquia: ")
search = input("|---- ")
url  = 'https://news.google.com/search?q='+search+'&hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
url = url.replace(' ', '%20')
html_page = requests.get(url).text
linkArray = []
aux = []
soup = BeautifulSoup(html_page, "lxml")
for  link in soup.findAll('a'):
    aux.append(link.get('href'))
    print(aux)
for x in aux:
    if x is None:
        x = "Nada"
    else:
        if './articles' in x:
            linkArray.append(x)
            print(x)

linkArray[0] = linkArray[0].replace(".", "")
url = 'https://news.google.com' + linkArray[0]
print('|---- URL DA NOTÍCIA')
print(url)
article = Article(url)
a = Article(url)

a.download()
a.parse()



print("Título:")
print(a.title)

voz = gTTS('Fonte :'+a.title, lang='pt')
voz.save('noticia.mp3')

print('Falando...')

mixer.init()
mixer.music.load('noticia.mp3')
mixer.music.play()

while mixer.music.get_busy():
    print('Continua falando...')
    time.sleep(1)

desejaOuvir = input("desejaOuvir? ")

if(desejaOuvir == "sim"):
    voz = gTTS(a.text, lang='pt')
    voz.save('noticia.mp3')
    mixer.init()
    mixer.music.load('noticia.mp3')
    mixer.music.play()

    while mixer.music.get_busy():
        print('Continua falando...')
        time.sleep(1)
else:
    print("PROTOTIPO ENCERRADO")






