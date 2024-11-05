import pygame

# Inicializar
pygame.init()

tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)
titulo = pygame.display.set_caption("Block Breaker")

tamanho_bola = 15
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)

tamanho_jogador = 100
jogador = pygame.Rect(0, 750, tamanho_jogador, 15)

qtde_blocos_linha = 8
qtde_linhas_blocos = 5
qtde_total_blocos = qtde_blocos_linha * qtde_linhas_blocos

def criar_blocos(qtde_blocos_linha, qtde_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / 8 - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10

    blocos = []
    # Criar os blocos
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas, largura_bloco, altura_bloco)
            blocos.append(bloco)
    return blocos

cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0)
}

fim_jogo = False
pontuacao = 0
movimento_bola = [1, -1]

def desenhar_inicio_jogo():
    tela.fill(cores["preta"]) 
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["branca"], bola)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)

def movimentar_jogador(evento):
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_RIGHT:
            if jogador.x + tamanho_jogador < tamanho_tela[0]:
                jogador.x += 1
        if evento.key == pygame.K_LEFT:
            if jogador.x > 0:
                jogador.x -= 1

def movimentar_bola(bola):
    movimento = movimento_bola
    bola.x += movimento[0]
    bola.y += movimento[1]

    if bola.x <= 0 or bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = -movimento[0]
    if bola.y <= 0:
        movimento[1] = -movimento[1]
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        movimento = None

    if jogador.collidepoint(bola.x, bola.y):
        movimento[1] = -movimento[1]
    for bloco in blocos:
        if bloco.collidepoint(bola.x, bola.y):
            blocos.remove(bloco)
            movimento[1] = -movimento[1]
    return movimento

def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", 1, cores["amarela"])
    tela.blit(texto, (0, 780))
    return pontuacao >= qtde_total_blocos

# Função para desenhar a tela de GAME OVER
def desenhar_game_over():
    fonte = pygame.font.Font(None, 50)
    texto_game_over = fonte.render("GAME OVER", 1, cores["amarela"])
    tela.fill(cores["preta"])
    tela.blit(texto_game_over, (tamanho_tela[0] // 2 - texto_game_over.get_width() // 2, tamanho_tela[1] // 2 - 50))
    pygame.display.flip()

# Função para desenhar a tela de VITÓRIA
def desenhar_win():
    fonte = pygame.font.Font(None, 50)
    texto_win = fonte.render("YOU WIN", 1, cores["amarela"])
    tela.fill(cores["preta"])
    tela.blit(texto_win, (tamanho_tela[0] // 2 - texto_win.get_width() // 2, tamanho_tela[1] // 2 - 50))
    pygame.display.flip()

blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)

# Loop principal do jogo
while not fim_jogo:
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    
    # Verificar a condição de vitória ou derrota
    pontuacao = qtde_total_blocos - len(blocos)
    if pontuacao >= qtde_total_blocos:
        desenhar_win()  # O jogador venceu
        fim_jogo = True
    elif bola.y + tamanho_bola >= tamanho_tela[1]:
        desenhar_game_over()  # O jogador perdeu
        fim_jogo = True
    
    # Atualizar a pontuação
    atualizar_pontuacao(pontuacao)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True
        movimentar_jogador(evento)
    
    if fim_jogo:  # Se o jogo acabou, não move mais a bola
        continue
    
    movimento_bola = movimentar_bola(bola)
    
    if not movimento_bola:
        fim_jogo = True
        
    pygame.time.wait(1)
    pygame.display.flip()

pygame.quit()
