# programa pega título, link é imagens de noticias, bem como as urls delas
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import datetime


class ParserHtml:
    """Faz parser do html"""
    def parse(self, url):
        self.url = url
        try:
            html = urlopen(self.url)
        except HTTPError:
            print('HTTP ERROR - 404 ou 500...')
        except URLError:
            print('URLERROR, verifique a URL')
        else:
            return BeautifulSoup(html.read(), 'html.parser')


class Crawler:
    """Encontra as tags"""
    def getTags(self, urlBase, tagTitulo, tagLink, tagImagem):
        self.urlBase = urlBase
        self.tagTitulo = tagTitulo
        self.tagLink = tagLink
        self.tagImagem = tagImagem
        self.bs1 = ParserHtml()
        self.bs2 = self.bs1.parse(self.urlBase)  # pega o html


        listaLink = []
        listaTitulo = []
        titulos = self.bs2.select(self.tagTitulo)
        for titulo in titulos:
            print(titulo.text)
            listaTitulo.append(titulo.text)
        links = self.bs2.select(self.tagLink)
        for link in links:
            if 'href' in link.attrs:
                listaLink.append(link.attrs['href'])
                print(link.attrs['href'])
        imagens = self.bs2.select(self.tagImagem)
        diretorio = 'imagensIFMG'
        contador_imagem = 0
        for imagem in imagens:
            if os.path.exists(diretorio):
                caminho = os.path.dirname(diretorio + '/') # da o local
                # grava os títulos e links da notícia
                with open(f'{caminho}/noticiasIFMG.txt', 'a') as f:
                    header = f.writelines(f'Notícia raspada em {datetime.now()}\n')
                    arquivo = f.writelines(f'{listaTitulo[contador_imagem]} : {listaLink[contador_imagem]}\n')
                # salva as imagens na pasta
                urlretrieve(imagem.attrs['src'], f'{caminho}/imagem{contador_imagem}.jpeg') # baixa a imagem
            else:
                os.mkdir(diretorio) # cria se não exitir
            contador_imagem += 1
        print('Concluído!As imagens foram baixadas para a pasta imagensIFMG')


url_tags = ['https://www.ifmg.edu.br/ourobranco/noticias', 'h2.tileHeadline','h2.tileHeadline a' , 'img.tileImage']
crawler = Crawler()
crawler.getTags(url_tags[0], url_tags[1], url_tags[2],  url_tags[3])
