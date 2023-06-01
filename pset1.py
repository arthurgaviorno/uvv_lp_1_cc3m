# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Arthur Fornaciari Gaviorno
#    Matrícula: 202299628
#    Turma: CC3M
#    Email: arthurgaviorno@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.
#


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y): 
        return self.pixels[x + (y * self.largura)] #ja que os pixels nao estao em matriz, e preciso fazer com que haja apenas um valor dentro do array

    def set_pixel(self, x, y, c): 
        self.pixels[x + (y * self.largura)] = c #se aplica o mesmo caso do comentário de cima

    def aplicar_por_pixel(self, func): 
        resultado = Imagem.nova(self.largura, self.altura)
        nova_cor = ""
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x,y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)
        return resultado

    def invertida(self):
        return self.aplicar_por_pixel(lambda c: 255 - c) #corrigido de 256 para 255 como deveria ser

    def Kernel(self, n): #criando uma matriz em kernel
        kernel = []
        for x in range(n): #dois for para criar um kernel n x n, para o "blur box"
            lst = []
            for y in range(n):
                lst.append(1/(n**2))
            kernel.append(lst)
        return kernel

    def borrada(self, n):
        kernel = self.Kernel(n) #autoexplicativo, mas cria o kernel "n x n" 
        return self.correlacao(kernel).aplicar_por_pixel(lambda c: round(c)) #percorre e arredonda o resultado da correlação

    def focada(self, n):
        borrada = self.borrada(n) #borra a imagem segundo a equação: (S = 2*I - B)
        focada = Imagem.nova(self.largura, self.altura) #gera uma imagem zerada com as mesmas dimensões da imagem original
        for x in range(self.largura): #percorre os pixels das imagens nos dois eixos
            for y in range(self.altura):
                subtr = 2*self.get_pixel(x, y) - borrada.get_pixel(x, y) #realiza a equação para nitidez
                if subtr >=255: #verifica os limites de cores
                    subtr = 255
                elif subtr <= 0:
                    subtr = 0
                focada.set_pixel(x,y,subtr) #"seta" o novo pixel da nova imagem
        return focada

    def bordas(self):
        resultado = Imagem.nova(self.largura, self.altura)

        Kx = [[-1,0,1], [-2,0,2], [-1,0,1]]
        Ky = [[-1,-2,-1], [0,0,0], [1,2,1]] #setando o kernel para detectar as bordas nos dois eixos
       

        Ox = self.correlacao(Kx) #percorre a imagem Ox com o kernel Kx
        Oy = self.correlacao(Ky) #percorre a imagem Oy com o kernel Ky
        soma = 0

        for x in range(self.largura): #percorre os pixels de ambas as imagens
            for y in range(self.altura):
                soma = round(((Ox.get_pixel(x,y)**2)+(Oy.get_pixel(x,y)**2))**(1/2)) #equação para detecção de bordas
                if soma >=255: #verificando os limites da gama de cores
                    soma = 255
                resultado.set_pixel(x,y,soma) #seta o novo pixel como resultado da operação
        return resultado
    
    def limite(self, x, y): #verifica se na correlacao x e y ultrapassam x e y da imagem original
        if x >= self.largura: #Se ultrapassar "seta" as variáveis para o "limite"
            x = self.largura - 1
        elif x <= 0:
            x = 0
        if y >= self.altura:
            y = self.altura - 1
        elif y <= 0:
            y = 0
        return x, y 
    
    def correlacao(self, kernel): #Alogritmo para se utilizar a correlação
        resultado = Imagem.nova(self.largura, self.altura) #inicializa uma cópia zerada com os limites da imagem inicial
        altura_kernel, largura_kernel = len(kernel), len(kernel[0])                          
        for y in range(self.altura): #percorre a imagem nos dois eixos ou seja por inteiro
            for x in range(self.largura):
                soma = 0
                for ky in range(altura_kernel): #percorre a matriz nos dois eixos, ou seja por inteiro
                    for kx in range(largura_kernel):
                        imagemX = x + kx - (largura_kernel // 2) #identifica qual pixel da imagem será multiplicado pelo valor correspondente no kernel
                        imagemY = y + ky - (altura_kernel // 2)
                        imagemX, imagemY = self.limite(imagemX, imagemY) #verificação se ultrapassa os limites da imagem
                        coord = self.get_pixel(imagemX, imagemY) #coordenadas (x,y) específicas no qual será multiplicado e adicionado na variável "soma"
                        soma += coord * kernel[ky][kx] #realiza a multiplicação do pixel "coord" pelo valor "kernel[kx][ky]" e adiciona a soma
                resultado.set_pixel(x, y, soma) #seta o novo pixel como o resultado da soma

        return resultado

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.largura, event.altura), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.altura, width=event.largura)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.altura, width=e.largura))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.


    #Questão 1 (demonstrando uma maneira de obter por meio do codigo, sem ser pelo cálculo): 

    '''questao1 = Imagem(1, 4, 
                               [29, 89, 136, 200])
    resultado = questao1.invertida()
    print('Resultado Questão 1: ', resultado)'''


    ##Questão 2: 

    imagem = Imagem.carregar('test_images/bluegill.png')
    invertida = imagem.invertida()
    Imagem.salvar(invertida, 'resultados_imagens/bluegill_invertida.png')

    ##Questao 4: 

    kernel = [[0,0,0,0,0,0,0,0,0], 
              [0,0,0,0,0,0,0,0,0], 
              [1,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0]]
    
    imagem = Imagem.carregar('test_images/pigbird.png')
    correlacao = imagem.correlacao(kernel)
    Imagem.salvar(correlacao, 'resultados_imagens/pigbird_kernel.png')


    ##Questao 5

    
    imagem = Imagem.carregar('test_images/python.png')
    nitidez = imagem.focada(11)
    Imagem.salvar(nitidez, 'resultados_imagens/python_nitida.png')


    ##Imagem do gato pedida no decorrer da sessão 5 do PDF.
    ##5.1
    imagem = Imagem.carregar('test_images/cat.png')
    borrada = imagem.borrada(5)
    Imagem.salvar(borrada, 'resultados_imagens/cat_desfoque.png')


    ##Questão 6: 

    Kx = [[-1,0,1], [-2,0,2], [-1,0,1]]
    Ky = [[-1,-2,-1], [0,0,0], [1,2,1]]

    imagem = Imagem.carregar('test_images/construct.png')
    apenasKx = imagem.correlacao(Kx)
    Imagem.salvar(apenasKx, 'resultados_imagens/construct_Kx.png')

    imagem = Imagem.carregar('test_images/construct.png')
    apenasKy = imagem.correlacao(Ky)
    Imagem.salvar(apenasKy, 'resultados_imagens/construct_Ky.png')

    imagem = Imagem.carregar('test_images/construct.png')
    KxKy= imagem.bordas()
    Imagem.salvar(KxKy, 'resultados_imagens/construct_KxKy.png')



    pass

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
