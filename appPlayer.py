import flet as ft
import requests
import yt_dlp

# Definindo o caminho da pasta de músicas (sem usar os)
musica_folder = "musicas/"
titulo = []
capa = []
url_musica = []
control = 0
audio_player = None

def main(page: ft.Page):
    page.window.width = 400
    page.window.height = 600

    def reprodu():
        global titulo, capa, control, url_musica, audio_player
        page.controls.clear()  # Limpa os controles atuais
        
        img = ft.Image(src=capa[control])
        txt_tit = ft.Text(titulo[control])
        video_list = ft.Column()  # Cria uma coluna para a lista de vídeos

        # Cria botões para cada vídeo disponível
        for i in range(len(titulo)):
            btn = ft.ElevatedButton(titulo[i], on_click=lambda e, index=i: selecionar_video(index))
            video_list.controls.append(btn)

        # Botões para navegação entre vídeos
        btav = ft.ElevatedButton('>>', on_click=av)
        btvlt = ft.ElevatedButton('<<', on_click=vlt)
        
        # Botões de controle de áudio
        btn_play = ft.ElevatedButton('Play', on_click=play_audio)
        btn_pause = ft.ElevatedButton('Pause', on_click=pause_audio)

        # Adiciona o player de áudio
        if audio_player is None:
            audio_player = ft.Audio(src="", autoplay=False)
        
        # Define a fonte do áudio para o player após o download
        audio_player.src = f"{musica_folder}{titulo[control].replace('/', '-')}.mp3"  
        
        page.add(img, txt_tit, btav, btvlt, btn_play, btn_pause, audio_player, video_list)  
        page.update()

    def selecionar_video(index):
        global control
        control = index  # Atualiza o controle para o vídeo selecionado
        download_audio(index)  # Chama a função para baixar o áudio
        reprodu()  # Chama a função para reproduzir o vídeo selecionado

    def download_audio(index):
        global url_musica
        video_url = f"https://www.youtube.com/watch?v={url_musica[index]}"
        output_path = f"{musica_folder}{titulo[index].replace('/', '-')}.mp3"  # Define o caminho de saída

        # Configurações para o yt_dlp
        ydl_opts = {
            'ffmpeg_location': r'C:\ffmpeg\bin',  # Ajuste este caminho para o seu FFmpeg
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])  # Faz o download do vídeo

        print(f"Download concluído: {output_path}")

    def av(e):
        global control
        if control < len(titulo) - 1:  # Verifica se não é o último vídeo
            control += 1
            reprodu()  # Chama a função para reproduzir o próximo vídeo

    def vlt(e):
        global control
        if control > 0:  # Verifica se não é o primeiro vídeo
            control -= 1
            reprodu()  # Chama a função para reproduzir o vídeo anterior

    def play_audio(e):
        if audio_player:  # Verifica se o player de áudio existe
            audio_player.autoplay = True  # Ativa a reprodução automática
            audio_player.play()  # Inicia a reprodução da música

    def pause_audio(e):
        if audio_player:  # Verifica se o player de áudio existe
            audio_player.pause()  # Pausa a reprodução da música

    def busc(e):
        global artista, titulo, capa, url_musica
        artista = str(busca.value)
        API_KEY = 'AIzaSyBlr1x9Yg9r5nqV-d1pnyZg1bcaxszjVOI'
        SEARCH_QUERY = artista

        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': SEARCH_QUERY,
            'key': API_KEY,
            'type': 'video',  
            'maxResults': 5
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            titulo.clear()  
            capa.clear()
            url_musica.clear()

            for item in data['items']:
                titulo.append(item['snippet']['title'])
                capa.append(item['snippet']['thumbnails']['high']['url'])
                url_musica.append(item['id']['videoId']) 
                
            reprodu()  

        else:
            print(f"Erro na solicitação: {response.status_code}")

    busca = ft.TextField(label='Buscar artista:')
    bt = ft.ElevatedButton('Buscar', on_click=busc)

    page.add(busca, bt)
    page.update()

ft.app(target=main)
