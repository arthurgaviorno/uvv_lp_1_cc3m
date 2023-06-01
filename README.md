 # Repositório utilizado para publicar os arquivos e questionário referentes ao PSET 1
 
### Aluno: Arthur Fornaciari Gaviorno
### Professor: Abrantes Araújo Silva Filho
### Turma: CC3M

----------------

# Confirmação dos Testes: 

![image](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/d2475059-b2e7-4c8e-a52a-ccf5b099ab4f)

-----------------
 
# Questionário: 

## Questão 1:
- O resultado após passar a imagem Imagem(1, 4, [29, 89, 136, 200]) pelo filtro de inversão é: Imagem(1, 4, [226, 166, 119, 55]), tendo em vista que as imagens ao serem invertidas são submetidas a passar pelo código:<br/> 
 ~~~~
def invertida(self):
        return self.aplicar_por_pixel(lambda c: 255 - c)
 ~~~~
       
## Questão 2: 

- Código usado para gerar a imagem invertida: 
 ~~~~
  imagem = Imagem.carregar('test_images/bluegill.png') <br/>
  invertida = imagem.invertida() <br/>
  Imagem.salvar(invertida, 'resultados_imagens/bluegill_invertida.png')
 ~~~~
 
- Antes: 

![bluegill](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/48d3f2ba-f33c-46d1-835e-c88dada9a1b8)

- Depois: 

![bluegill_invertida](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/fd8a982d-4504-4e61-83dd-06b27a722553)

## Questão 3: 

Na questão 3 seguindo a lógica, do que foi explicado no arquivo PDF e de acordo com a funcao "correlacao" criada no código, devemos com os dados do kernel, e com os dados da imagem dada na questão, prosseguir da seguinte forma: <br/>
- Agrupar o pixel selecionado e comparar com o kernel: 
  Pixel selecionado: <br/>
 ![image](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/7aa61a5b-64d7-47cb-92cf-27bbb2ef7d39)  <br/>
  
  Kernel: <br/>
  ~~~~
  0.00 -0.07 0.00 
  -0.45 1.20 -0.25 
  0.00 -0.12 0.00 
  ~~~~
 
- Multiplicar cada "coord" da imagem com o seu respectivo kernel: 
   ~~~~
   Ox, y =
   80 * 0 + 53 * -0,07 + 99 * 0 + 
   129 * -0,45 + 127 * 1,20 + 148 * -0,25 + 
   175 * 0 + 174 * -0,12 + 193 * 0 
   ~~~~
- O resultado será o resultado da conta acima "Ox, y": <br/>
  Resultado: 32,76 <br/>
  
## Questão 4: 
  
  - Código: 
  ~~~~
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
  ~~~~
- Antes: 

  ![pigbird](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/b98e5c89-917e-49f6-9520-12a5710c4af9)

- Depois: 

  ![pigbird_kernel](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/b618e71e-1430-4e88-8cdc-1fbb3d128d5e)
  
  
## Questão 5: 

- Nao sei explicar ao certo qual o kernel devo utilizar mas o resultado é a seguinte imagem: <br/>

![python_nitida](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/99d96c78-72fa-4aad-82a1-b84b7f555fc0)

Obs.: Imagem do gato borrada da sessão 5.1 <br/>
![cat_desfoque](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/9828b0d4-5a41-465c-941b-4c00badd0216)


## Questão 6: 

- O kernel Ky: 
~~~~
-1 -2 -1
 0  0  0
 1  2  1
~~~~
- Através do código: 
~~~~
imagem = Imagem.carregar('test_images/construct.png')
    apenasKy = imagem.correlacao(Ky)
    Imagem.salvar(apenasKy, 'resultados_imagens/construct_Ky.png')

~~~~
 É o responsável por fazer a detecção de bordas da imagem no eixo Y, sendo assim trará como resultado a seguinte imagem: 
 
 ![construct_Ky](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/b98297a2-51da-4f05-acfb-358db7eaed4f)

- O kernel Kx: 
~~~~
-1  0  1
-2  0  2
-1  0  1
~~~~
- Através do código: 
~~~~
imagem = Imagem.carregar('test_images/construct.png')
    apenasKx = imagem.correlacao(Kx)
    Imagem.salvar(apenasKx, 'resultados_imagens/construct_Kx.png')
~~~~

É o responsável por fazer a detecção de bordas da imagem no eixo X, sendo assim trará como resultado a seguinte imagem: 

![construct_Kx](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/b841ef72-5b70-44b8-9ed7-7e41232ca399)

Portanto se aplicarmos ambos os kernel para filtrar a imagem, teremos uma imagem com todas as bordas destacadas, tanto as de Ky, quanto as de Ky:

![construct_KxKy](https://github.com/arthurgaviorno/uvv_lp_1_cc3m/assets/103372834/8805918e-75d0-4c6e-8a3e-5d733c217c9f)

- Código utilizado para Kx e Ky simultaneamente:
~~~~
imagem = Imagem.carregar('test_images/construct.png')
    KxKy= imagem.bordas()
    Imagem.salvar(KxKy, 'resultados_imagens/construct_KxKy.png')

~~~~






 
