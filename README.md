## Alien Invasion — Jogo Arcade em Python
<p align="center">
  <img src="images/demo.gif" alt="Demonstração do Jogo Alien Invasion" width="600px">
</p>
[![Python](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-1d7032?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org/)

Um jogo arcade 2D estilo *Space Shooter* desenvolvido em Python utilizando a biblioteca **Pygame**. O jogador controla uma espaçonave que deve se defender de uma frota alienígena invasora.

---

##  Funcionalidades
- Movimentação fluida da espaçonave (esquerda e direita)
- Sistema de disparos de projéteis para destruir os inimigos
- Frota de aliens que se desloca pela tela e aumenta de dificuldade
- Tela de início, placar de pontuação máxima salvo em arquivo (`high_score.txt`) e gerenciamento de vidas

---

## Ferramentas
- **Python 3** (Linguagem principal)
- **Pygame** (Biblioteca para renderização gráfica e gerenciamento de eventos)

---

##  Como Rodar o Projeto no seu Computador

Siga os passos abaixo para clonar e executar o jogo localmente:

1. Clone o repositório:
git clone [https://github.com/thy-rodrygues/alien-invasion.git](https://github.com/thy-rodrygues/alien-invasion.git)

2. Acesse a pasta do projeto:
cd alien-invasion

3. Instale a biblioteca Pygame e Numpy:
pip install pygame
pip install numpy

4. Execute o jogo:
python alien_invasion.py

---

## Estrutura do Repositório

```text
alien-invasion/
├── images/              # Recursos visuais (sprites de naves e aliens)
├── sounds/              # Efeitos sonoros do jogo
├── alien.py             # Classe e movimentação dos inimigos
├── alien_bullet.py      # Lógica dos disparos dos inimigos
├── alien_invasion.py    # Arquivo principal que inicializa o jogo
├── bullet.py            # Lógica dos projéteis disparados pela nave
├── button.py            # Criação e tratamento de cliques nos botões
├── game_stats.py        # Gerenciamento de estatísticas e vidas
├── high_score.txt       # Armazenamento do recorde de pontuação
├── scoreboard.py        # Renderização do placar na tela
├── settings.py          # Configurações globais (cores, tela, velocidade)
├── ship.py              # Classe e lógica da espaçonave do jogador
└── README.md            # Documentação do projeto

