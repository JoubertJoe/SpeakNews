from newspaper import Article
from gtts import gTTS
from pygame import mixer
import time
from bs4 import BeautifulSoup
import requests
import speech_recognition as sr
#from subprocess import call
r = sr.Recognizer()



def reconhece():
    """
     Reconhece é uma função que serve para reconhecer os comandos de voz passados pelo usuário.
     A função utilizasse de uma api da google para reconhecimento de voz, que faz a ponte do microfone para o texto

    @return: Retorna aquilo que o usuário fala para o microfone
    """
    print("fale agora")
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        reconhecido = r.recognize_google(audio, language='pt')
        print("#      -" + reconhecido)
        return str(reconhecido).lower()
    except sr.UnknownValueError:
        print("Não consegui te entender")
        reconhece()

def fala(texto):
    """
    Uma função simples criada para falar o texto que o usuário deve ouvir
    Essa função também contem uma booleana que tem ultilidade de saber se ainda está sendo falado
    pois o audio poderia interferir no reconhecimento de voz.
    Utiliza-se gTTS (biblioteca google de sintetização de voz)
    @param texto: Texto a ser lido pela função
    @return: sem retorno
    """
    # Inicia-se a rotina de sintetização e reprodução
    voz = gTTS(texto, lang='pt')
    voz.save('fala.mp3')
    mixer.init()
    mixer.music.load('fala.mp3')
    mixer.music.get_busy()
    mixer.music.play()
    while mixer.music.get_busy():
        print('Continua falando...')
        time.sleep(1)

    #call(['espeak','-v','mb-br4','-s','140','-p','60', texto])
    print(texto)


# Inicia rotina do programa
def init():
    """
    Inicia a rotina do programa em sí, chamando o primeiro menu
    o programa foi modularizado de forma em que essa função, chama
    de forma respectiva todas as funções a serem usadas no processo
    de execução do programa.
    @return:
    """
    fala("Bem vindo ao Speak News, escolha uma opção: 1 categorias, 2 pesquisa direta, 3 notícias hoje")
    print("|-------------------------------")
    print("|---- S P E A K   N E W S  -----")
    print("|-------------------------------")
    print("################################")
    print("#    1 - Categorias            #")
    print("#    2 - Pesquisa Direta       #")
    print("#    3 - Notícias Hoje         #")
    print("################################")

    print("\n")
    # Pegando o Input do Usuário
    print("#    - Escolha: ")

    opcao = reconhece()

    # chamando a opção correspondente
    menu(opcao)
    print(opcao)


# Menu de funções
def menu(opcaoEscolhida):
    """
    Menu contendo opções a serem escolhidas no inicio da execução do programa
    aqui é possível escolher se a pesquisa será feita por categorias
    se será uma pesquisa direta, ou se simplesmente ouvirá as notícias do dia
    @param opcaoEscolhida: Essa opção é passado para outra função, ela que define qual função sera chamada a seguir
    @return: sem retorno
    """
    if (opcaoEscolhida == "1") or (opcaoEscolhida == "categorias"):
        fala("opção escolhida foi Categorias")

        categoria()
    elif (opcaoEscolhida == "2")or (opcaoEscolhida == "pesquisa direta"):
        fala("opção escolhida foi pesquisa direta")

        urlPesquisa("")
    elif (opcaoEscolhida == "3")or (opcaoEscolhida == "notícias hoje"):
        fala("opção escolhida foi Notícias hoje")

        pesquisa("https://news.google.com/?hl=pt-BR&gl=BR&ceid=BR:pt-419")
    else:
        init()


# Categorias para facilitar pesquisa do usuário
def categoria():
    """
    Caso seja escolhida o método de pesquisa categorizada essa função sera invocada
    ela serve para escolher a categoria que será pesquisada e adicioná-la na url
    url a qual será usada para pesquisar a notícia em sí.
    @return: sem retorno
    """
    print("|-------------------------------------------|")
    print("|---     1 - Esporte ")
    print("|---     2 - Jogos ")
    print("|---     3 - Politica ")
    print("|---     4 - Tv ")
    print("|---     0 - Outra ")
    print("|-------------------------------------------|")
    # recebendo Categoria
    print("|---       - Categoria: ")
    fala("Escolha uma categoria, 1 esporte, 2 jogos, 3 política, 4 tv, 0 outras")

    escolhido = reconhece()
    if( (escolhido == "1") or (escolhido == "esporte" )):
        fala("Categoria Esporte")
        urlPesquisa("Esporte")
    elif ((escolhido == "2") or (escolhido == "jogos" )):
        fala("Categoria Jogos")
        urlPesquisa("Jogos")
    elif ((escolhido == "3") or (escolhido == "política" )):
        urlPesquisa("Política")
        fala("Categoria Política")
    elif ((escolhido == "4")  or (escolhido == "tv" )):
        fala("Categoria TV")
        urlPesquisa("Tv")
    elif ((escolhido == "0") or (escolhido == "outro" )):
        fala("Diga a outra categoria a ser usada:")

        urlPesquisa(reconhece())




def urlPesquisa(prePesquisa):
    """
     urlPesquisa é uma função que define como será a pesquisa
     de notícias, anexando junto a URL de pesquisa os parâmetros
     necessários.
    @param prePesquisa: Caso seja escolhido categorias ou outros tipos de préparâmetros, eles podem ser adicionados aqui para se juntarem a url de pesquisa
    @return: sem retorno
    """

    # Colhendo a pesquisa do Usuário
    print("|---- Fale sua pesquia: ")
    fala("Diga sua pesquisa")

    search = reconhece()
    # preparando a URL para fazer a pesquisa
    url = 'https://news.google.com/search?q=' + prePesquisa + search + '&hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
    # Trocar os espaços em branco por %20 (que é usado pelo google para representar o mesmo)
    url = url.replace(' ', '%20')
    # Inicia a rotina de pesquisa
    pesquisa(url)



def pesquisa(url):
    """
    Aqui é efetivamente feito a pesquisa
    Essa função efetiva a pesquisa de Notícias e armazena-as em um array
    @param url: url a ser pesquisada
    @return: sem retorno
    """
    html_page = requests.get(url).text
    linkArray = []  # Array onde ficarão armazenados os links
    aux = []  # Array auxiliar dos links
    soup = BeautifulSoup(html_page, "lxml")
    for link in soup.findAll('a'):
        aux.append(link.get('href'))
    # estrutura de repetição para armazenar os links (não tratados)
    for x in aux:
        if x is None:
            x = "Nada"
        else:
            if './articles' in x:
                linkArray.append(x)
                #print(x)
    # Escolha do link de notícia
    # Paramêtro 0 começa do primeiro resultado
    print(linkArray)
    escolhePesquisa(0, linkArray)




def escolhePesquisa(nLink, link_array):
    """
    Função para escolher qual notícia ler (Préviamente pesquisado)
    @param nLink: Número do link que será lido
    @param link_array: Um array vindo da função anterior, onde estão armazenados os links, é usado para recursividade
    @return: sem retorno
    """
    # tratamnto de Link (Primeiro Passo)
    link_array[nLink] = link_array[nLink].replace(".", "")
    # Criando a URL da Notícia
    url = 'https://news.google.com' + link_array[nLink]
    print('|---- URL DA NOTÍCIA')
    print('|---- ' + url)
    # armazenando Notícia (artigo)
    article = Article(url)
    a = Article(url)

    # Download da Notícia, e tratamento de texto.
    a.download()
    a.parse()

    print("|---- Título da Notícia:")
    print(a.title)
    # Inicializando Sintetizador de Voz
    # Sintetizando a voz
    voz = gTTS('Título: ' + a.title, lang='pt')
    # Salvando a voz como arquivo MP3
    voz.save('noticia.mp3')
    print('Falando...')
    # Iniciando Reprodutor de áudio
    mixer.init()
    # Carregando arquivo de voz com o título da notícia
    mixer.music.load('noticia.mp3')
    # Reproduzindo
    mixer.music.play()
    while mixer.music.get_busy():
        print('Continua falando...')
        time.sleep(1)

    # Opções de escolha da Notícia
    fala("Escolha uma opção, 1 ouvir a pesquisa atual, 2 ouvir a próxima notícia, 3 cancelar sua pesquisa")
    print("################################")
    print("#    1 - Ler Pesquisa          #")
    print("#    2 - Próxima Pesquisa      #")
    print("#    3 - Cancelar Pesquisa     #")
    print("################################")

    option = reconhece()

    if (option == "1") or (option == "ler pesquisa"):
        # Caso escolha ouvir a notícia
        # Inicia-se a rotina de sintetização e reprodução
        voz = gTTS(a.text, lang='pt')
        voz.save('noticia.mp3')
        mixer.init()
        mixer.music.load('noticia.mp3')
        mixer.music.play()

        while mixer.music.get_busy():
            print('Continua falando...')
            time.sleep(1)

    elif (option == "2") or (option == "próxima pesquisa"):
        # Pula para o próximo Link da lista
        print(nLink)
        escolhePesquisa(nLink + 2,link_array)
    elif (option == "3") or (option == "cancelar"):
        # Recomeça o programa
        init()
    else:
        # Caso o input não seja reconhecido da forma esperada.
        print("#    -Repita por Favor")
        fala("Repita por favor")
        option = reconhece()


# Inicia a cadeia de execução.
init()
