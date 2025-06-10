import pygame
import random
import os
import math
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.funcoes import registrar_log
import json


def main():
    registrar_log("Sistema iniciado com sucesso.")
    print("Executando o programa...")

if __name__ == "__main__":
    main()
    
pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Iron Man do Marcão")
icone  = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
azul = (0, 0, 255)
vermelho = (255, 0, 0)
iron = pygame.image.load("assets/iron.png").convert_alpha() 
iron = pygame.transform.scale(pygame.image.load("assets/iron.png"), (300, 200))
fundoStart = pygame.image.load("assets/fundoStart.png")
fundoJogo = pygame.image.load("assets/fundoJogo.png")
fundoDead = pygame.image.load("assets/fundoDead.png")
missel = pygame.image.load("assets/missile.png").convert_alpha() 
circle = pygame.image.load("assets/circle.png").convert_alpha() 
fundoIntro = pygame.image.load("assets/fundoIntro.png")
objrandom = pygame.image.load("assets/objrandom.png").convert_alpha() 
missileSound = pygame.mixer.Sound("assets/missile.mp3")
explosaoSound = pygame.mixer.Sound("assets/explosao.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("assets/ironsound.mp3")
pygame.mixer.music.set_volume(0.2)


def jogar():
    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome 
        nome = entry_nome.get()  
        if not nome:  
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  
        else:
            root.destroy()  

    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    root.mainloop()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoIniciar.collidepoint(evento.pos):
                    esperando = False
        
        tela.blit(fundoIntro, (0,0))

        titulo = pygame.font.SysFont("arialblack", 70).render(f"Bem-vindo, {nome}!", True, vermelho)
        instrucoes = pygame.font.SysFont("arial", 35).render("Use o potente motor V8 do Lightning McQueen e desvie dos raios!", True, branco)
        iniciarTexto = pygame.font.SysFont("arial", 30).render("Clique aqui para iniciar", True, branco)

        tela.blit(titulo, (2, 2))
        tela.blit(instrucoes, (8,100))

        botaoIniciar = pygame.draw.rect(tela, azul, (8,180, 300, 50), border_radius=15)
        tela.blit(iniciarTexto, (4 + (300 - iniciarTexto.get_width()) // 2, 180 + (50 - iniciarTexto.get_height()) // 2))
        
        pygame.display.update()
        relogio.tick(60)

    posX_objrandom = random.randint(0, tamanho[0] - objrandom.get_width())
    posY_objrandom = random.randint(0, tamanho[1] - objrandom.get_height())
    velX_objrandom = random.choice([-2, -1, 1, 2])
    velY_objrandom = random.choice([-2, -1, 1, 2])
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    pygame.mixer.music.play(-1)
    pontos = 0

    pausado = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado  
                elif not pausado:
                    if evento.key == pygame.K_RIGHT:
                        movimentoXPersona = 15
                    elif evento.key == pygame.K_LEFT:
                        movimentoXPersona = -15
                    elif evento.key == pygame.K_UP:
                        movimentoYPersona = -15
                    elif evento.key == pygame.K_DOWN:
                        movimentoYPersona = 15
            elif evento.type == pygame.KEYUP and not pausado:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoXPersona = 0
                elif evento.key in [pygame.K_UP, pygame.K_DOWN]:
                    movimentoYPersona = 0
        if pausado:
            pause_text = pygame.font.SysFont("arial", 80).render("PAUSE", True, preto)
            tela.blit(pause_text, ((tamanho[0] - pause_text.get_width()) // 2, (tamanho[1] - pause_text.get_height()) // 2))
            pygame.display.update()
            relogio.tick(10)
            continue 
        
        if movimentoXPersona != 0:
            posicaoXPersona += movimentoXPersona
            movimentoYPersona = 0  
        elif movimentoYPersona != 0:
            posicaoYPersona += movimentoYPersona
            movimentoXPersona = 0  

        if posicaoXPersona < 0 :
            posicaoXPersona = 0
        elif posicaoXPersona >750:
            posicaoXPersona = 750
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 0
        elif posicaoYPersona > 540:
            posicaoYPersona = 540
        
        posX_objrandom += velX_objrandom
        posY_objrandom += velY_objrandom

        if posX_objrandom <= 0 or posX_objrandom >= tamanho[0] - objrandom.get_width():
            velX_objrandom = -velX_objrandom
        if posY_objrandom <= 0 or posY_objrandom >= tamanho[1] - objrandom.get_height():
            velY_objrandom = -velY_objrandom
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        tela.blit(objrandom, (posX_objrandom, posY_objrandom))
        tela.blit( iron, (posicaoXPersona, posicaoYPersona) )
    
        tempo = pygame.time.get_ticks() / 1000  
        escala = 1 + 0.1 * math.sin(tempo * 4)

        largura_original, altura_original = circle.get_size()
        nova_largura = int(largura_original * escala)
        nova_altura = int(altura_original * escala)
        circle_pulsando = pygame.transform.scale(circle, (nova_largura, nova_altura))

        pos_x = tamanho[0] - nova_largura - 20  
        pos_y = 20

        tela.blit(circle_pulsando, (pos_x, pos_y))
        posicaoYMissel = posicaoYMissel + velocidadeMissel
        if posicaoYMissel == 0:
            pygame.mixer.Sound.play(missileSound)
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(0,800)
            
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        
        pauseHint = fonteMenu.render("Press Space to Pause Game", True, preto)
        tela.blit(pauseHint, (150, 15))  

        mask_iron = pygame.mask.from_surface(iron)
        mask_missel = pygame.mask.from_surface(missel)

        offset = (posicaoXMissel - posicaoXPersona, posicaoYMissel - posicaoYPersona)
        colidiu = mask_iron.overlap(mask_missel, offset)

        if colidiu:
            escreverDados(nome, pontos)
            dead()
        else:
            print("Ainda Vivo")

        pygame.display.update()
        relogio.tick(60)


def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                     
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40

    try:
        with open("base.atitus", "r") as f:
            log_partidas = json.load(f)
    except:
        log_partidas = {}

    logs_formatados = []
    for chave in log_partidas:
        pontos = log_partidas[chave][0]
        data = log_partidas[chave][1]
        logs_formatados.append(f"{chave} - Pontos: {pontos} - Data: {data}")

    logs_formatados = logs_formatados[-10:]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit = 35

            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    quit()

        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))

        fonte_log = pygame.font.SysFont("arial", 24)
        subtitulo = pygame.font.SysFont("arial", 32).render("Últimos 5 Registros:", True, vermelho)

        x_subtitulo = tamanho[0] - subtitulo.get_width() - 20
        y_subtitulo = tamanho[1] - (len(logs_formatados) + 1) * 35 - 20 
        tela.blit(subtitulo, (x_subtitulo, y_subtitulo))

        y = y_subtitulo + 40
        for log in logs_formatados:
            linha = fonte_log.render(log, True, branco)
            x_linha = tamanho[0] - linha.get_width() - 20
            tela.blit(linha, (x_linha, y))
            y += 35

        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 12))

        quitButton = pygame.draw.rect(tela, branco, (10, 60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25, 62))

        pygame.display.update()
        relogio.tick(60)

start()