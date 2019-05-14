from newspaper import Article
from gtts import gTTS
from pygame import mixer
import time
from bs4 import BeautifulSoup
import requests

def init():
    print("|-------------------------------")
    print("|---- S P E A K   N E W S  -----")
    print("|-------------------------------")
    print("################################")
    print("#    1 - Categorias            #")
    print("#    2 - Pesquisa Direta       #")
    print("#    3 - Notícias Hoje         #")
    print("################################")
    print("\n")
    opcao = input( "#    - Categoria: ")
    if (int(opcao) > 0) & (int(opcao) < 4):
        menu(opcao)
    else:
        opcao = input("#    - Categoria: ")

def menu(opcaoEscolhida):
        if(opcaoEscolhida == "1"):
            categoria()
        elif(opcaoEscolhida == "2"):
            pesquisa()
        elif(opcaoEscolhida == "3"):
            print()



def categoria():
    print("|-------------------------------------------|")
    print("|---     1 - Esporte ")
    print("|---     1 - Esporte ")
    print("|---     1 - Esporte ")
    print("|---     1 - Esporte ")
    print("|---     0 - Outra ")
    print("|-------------------------------------------|")
    escolhido = input("|---       - Categoria: ")
    if(escolhido == "1"):
        categoriaEscolhida = "Esporte"



    return categoriaEscolhida;




def urlPesquisa(prePesquisa):
    print("|---- Digite sua pesquia: ")
    search = input("|---- ")
    url = 'https://news.google.com/search?q='+ prePesquisa + search + '&hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
    url = url.replace(' ', '%20')
    pesquisa(url)



def pesquisa(url):
    html_page = requests.get(url).text
    linkArray = []
    aux = []
    soup = BeautifulSoup(html_page, "lxml")
    for link in soup.findAll('a'):
        aux.append(link.get('href'))

    for x in aux:
        if "article" in x:
            linkArray.append(x)

    escolhePesquisa(0)


def escolhePesquisa(nLink):
    linkArray = []
    linkArray[nLink] = linkArray[nLink].replace(".", "")
    url = 'https://news.google.com' + linkArray[nLink]
    print('|---- URL DA NOTÍCIA')
    print('|---- ' + url)
    article = Article(url)
    a = Article(url)

    a.download()
    a.parse()

    print("|---- Título da Notícia:")
    print(a.title)
    voz = gTTS('Fonte :' + a.title, lang='pt')
    voz.save('noticia.mp3')
    print('Falando...')
    mixer.init()
    mixer.music.load('noticia.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        print('Continua falando...')
        time.sleep(1)

    print("################################")
    print("#    1 - Ler Pesquisa          #")
    print("#    2 - Próxima Pesquisa      #")
    print("#    3 - Cancelar Pesquisa     #")
    print("################################")
    option = input("#      - ")


    if (option == "1"):
        voz = gTTS(a.text, lang='pt')
        voz.save('noticia.mp3')
        mixer.init()
        mixer.music.load('noticia.mp3')
        mixer.music.play()

        while mixer.music.get_busy():
            print('Continua falando...')
            time.sleep(1)

    elif(option == "2"):
        escolhePesquisa(nLink+1)
    elif(option == "3"):
        init()
    else:
        print("#    -Repita por Favor")
        option = input("#      - ")



init()