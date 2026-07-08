# LGP Tradutor — Língua Gestual Portuguesa 🖐️🤖

O **LGP Tradutor** é uma plataforma interativa baseada em inteligência artificial criada para a tradução em tempo real de dactilologia (alfabeto manual) e gestos da **Língua Gestual Portuguesa**. O processamento dos dados é executado inteiramente de forma local no navegador utilizando o **TensorFlow.js**, garantindo privacidade e rapidez.

A aplicação apresenta um design futurista premium baseado no estilo **Cybernetic HUD (Neon-Glass Brutalism)**, dispondo de duas interfaces otimizadas (Desktop e Mobile PWA).

---

## 🚀 Links Rápidos de Produção (Vercel):

*   **Versão Desktop:** [https://lgp-tradutor.vercel.app/](https://lgp-tradutor.vercel.app/)
*   **Versão Mobile (PWA):** [https://lgp-tradutor.vercel.app/mobile/](https://lgp-tradutor.vercel.app/mobile/)

---

## ✨ Funcionalidades Principais

*   **Tradução Local por IA:** Classificação em tempo real de gestos com a webcam utilizando TensorFlow.js e modelos pré-treinados do Teachable Machine.
*   **Design HUD Premium:** Interface fluida e responsiva com micro-animações néon, painéis estilo terminal e sem barra de scroll horizontal.
*   **Histórico Persistente (SQLite):** Área dedicada à construção de frases onde podes gravar frases traduzidas diretamente no servidor.
*   **Suporte PWA Mobile:** A versão telemóvel pode ser instalada diretamente no ecrã principal como uma aplicação nativa com suporte a modo offline.
*   **Logótipo e Favicon Personalizados:** Utilização do símbolo oficial recortado e transparente (`simbolo_only.png`) nos separadores do browser e ecrãs de boas-vindas.

---

## 🛠️ Arquitetura e Estrutura de Ficheiros

O projeto utiliza um servidor web leve em **Python (Flask)** para controlo de rotas e disponibilização dos endpoints REST de histórico.

```text
├── app.py                     # Servidor Flask principal (Rotas e API REST)
├── index.html                 # Página principal da versão Desktop
├── render.yaml                # Configuração de Blueprint para deploy no Render
├── requirements.txt           # Dependências do projeto (Flask, Gunicorn)
├── vercel.json                # Ficheiro de configuração de deploy na Vercel
├── history.db                 # Base de dados SQLite (gerada localmente em execução)
└── mobile/
    ├── index.html             # Página principal da versão Mobile
    ├── manifest.json          # Configuração de PWA (Mobile Install)
    ├── simbolo_only.png       # Logótipo oficial recortado (sem texto e transparente)
    └── icone_transparent.png  # Versão transparente com o texto completo
```

---

## 💾 Base de Dados SQLite Inteligente

O backend em `app.py` utiliza uma lógica de deteção dinâmica para o ficheiro de base de dados SQLite (`history.db`), permitindo que a aplicação corra em qualquer alojamento:
1.  **Render (Disco Persistente):** Deteta a pasta `/data` e monta a BD de forma permanente em `/data/history.db`.
2.  **Ambiente Local:** Cria o ficheiro na raiz do projeto (`history.db`).
3.  **Vercel (Serverless Grátis):** Grava de forma temporária na pasta `/tmp/history.db` permitindo a escrita correta sem erros de permissões (FileSystem de apenas-leitura da Vercel).

---

## 💻 Como Executar Localmente

### 1. Requisitos
Certifica-te de que tens o **Python 3** instalado.

### 2. Instalação de Dependências
Navega até ao diretório do projeto e instala as dependências listadas no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Iniciar o Servidor
Executa o ficheiro `app.py`:
```bash
python app.py
```
O servidor estará disponível localmente em: **`http://localhost:8000`**

---

## 🚀 Como Alojamento no Render (Grátis com Disco Persistente)

1.  Cria uma conta em **[Render.com](https://render.com/)** ligando a tua conta do **GitHub**.
2.  No painel do Render, clica em **New +** -> **Blueprint**.
3.  Seleciona o repositório **`Hack-4-Good`**.
4.  O Render lerá o ficheiro `render.yaml` e configurará automaticamente o servidor com o disco persistente necessário para o SQLite.
5.  Clica em **Apply** e em poucos minutos o teu tradutor estará online!