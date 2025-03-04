# YouTube Downloader 🎬

Um aplicativo em Python para baixar vídeos e playlists do YouTube através de uma interface gráfica (GUI) desenvolvida com Tkinter.  
Ideal para quem deseja uma solução prática e eficiente para salvar seus vídeos favoritos.

## 🖥️ Captura de Tela
![Screenshot do HashCheck](https://raw.githubusercontent.com/HermesRoot/youtube-downloader/main/screenshot.jpg
)

## 🚀 Funcionalidades

- ✅ Download de vídeos e playlists completos do YouTube.
- ✅ Interface gráfica moderna inspirada no Windows 11.
- ✅ Barra de progresso em tempo real.
- ✅ Integração com FFmpeg para conversão automática para MP4.
- ✅ Salvamento do último diretório usado.
- ✅ Log de atividades gerado automaticamente.

## 🛠️ Requisitos

- Python 3.8 ou superior
- [FFmpeg](https://ffmpeg.org/) instalado no caminho:


- Bibliotecas Python:
- `yt-dlp`
- `ttkthemes`

## 📦 Instalação

1. Clone o repositório:

  ```bash
  git clone https://github.com/HermesRoot/youtube-downloader.git
  ```

2. Instale as dependências:

  ```bash
  pip install -r requirements.txt
  ```

3. Certifique-se de que o FFmpeg está instalado e disponível em `C:/ffmpeg/bin`.

## 🎮 Como usar

1. Execute o programa:

  ```bash
  python src/youtube-downloader.py
  ```

2. Na interface:
 - Cole a URL do vídeo ou playlist.
 - Escolha o diretório de destino.
 - Clique em **Download** e acompanhe o progresso.

## ⚠️ Observações

- Apenas URLs válidas do YouTube são aceitas.
- Caso o FFmpeg não seja detectado no diretório indicado, o download não será iniciado.
- O progresso pode variar de acordo com a velocidade da internet e tamanho do conteúdo.

## 📝 Licença

Este projeto está licenciado sob a licença **MIT** — veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

Desenvolvido por **HermesRoot**.  
