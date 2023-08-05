import os
import time
import json
from pyrogram import Client
from pathlib import Path
import subprocess
from utils import show_banner, cache_path, authenticate

def get_channel_title(client, channel_id_or_username):
    channel = client.get_chat(channel_id_or_username)
    return channel.title

def create_channel(client, title):
    channel = client.create_channel(title=title)
    return channel.id  

""" Global """
session_name = "user"        

def get_channels():
    with Client(session_name) as client:
        channel_source = input("Forneça o @username ou ID do canal / grupo de origem: ")
        channel_target = input("Forneça o @username ou ID do canal de destino: ")

        # Se o canal de origem foi especificado e o de destino foi deixado em branco
        if channel_source and not channel_target:
            source_title = get_channel_title(client, channel_source)
            channel_target_name = f"{source_title} - Cópia"
            channel_target = create_channel(client, channel_target_name)

    return channel_source, channel_target     

def parse_channel_input(channel_input: str):
    """Parse channel input to determine if it's an ID or username."""
    if channel_input.startswith("@"):
        return channel_input  
    else:
        try:
            return int(channel_input)  
        except ValueError:
            print("Entrada inválida. Por favor, forneça um ID ou nome de usuário válido.")
            exit()

def get_user_choices():
    print("Quais conteudos você deseja processar ?:\n")
    options = ["Processar todos os Conteúdos" , "Fotos","Áudios", "Vídeos", "Arquivos", "Texto", "Sticker", "Animação - GIFs"]
    for i, option in enumerate(options):
        print(f"{i} - {option}")
    choices = input("\nInforme os conteúdos que deseja procesar separados por vírgula (ex: 1,3) < 0 para processar todos > : ").split(',')
    choices = [int(choice.strip()) for choice in choices]
    if 0 in choices:  # Se o usuário escolher a opção 0
        choices = [1, 2, 3, 4, 5, 6, 7] 
    return choices            

def collect_video_metadata(directory: str) -> dict:
    videos_metadata = {}
    for video_file in os.listdir(directory):
        if video_file.endswith(('.mp4', '.mkv', '.avi')):  # você pode adicionar mais extensões conforme necessário
            video_path = os.path.join(directory, video_file)
            ffprobe_command = f"ffprobe -v quiet -print_format json -show_format -show_streams {video_path}"
            output = os.popen(ffprobe_command).read().strip()

            if output:
                try:
                    metadata = json.loads(output)
                    videos_metadata[video_file] = metadata
                except json.JSONDecodeError:
                    pass

    return videos_metadata

def download_and_upload_media_from_channel(choices, channel_source, channel_target):
    downloaded_media = []

    # Load task progress from Json file, if exists
    if os.path.exists("downloaded_media.json"):
        with open("downloaded_media.json", "r") as json_file:
            downloaded_media = json.load(json_file)
            print("Progresso anterior carregado do arquivo JSON.")

    downloaded_ids = [item["id"] for item in downloaded_media]

    with Client(session_name) as client:
         
        all_messages = list(client.get_chat_history(channel_source))
        all_messages.reverse()
        # Get 'duration' argument of videos before upload
        all_video_metadata = collect_video_metadata('downloads')
        
        for count, message in enumerate(all_messages):
            # Verify if media was downloaded before
            if message.id in downloaded_ids:
                os.system('clear || cls')
                print(f"Mensagem {message.id} já foi baixada anteriormente.")
                continue

            file_name = None
            caption_text = message.caption

            # Process and download content 
      
            if 1 in choices and message.photo:
                file_name = client.download_media(message.photo)
                client.send_photo(channel_target, file_name, caption=caption_text)
            if 2 in choices and message.audio:
                file_name = client.download_media(message.audio)
                client.send_audio(channel_target, file_name, caption=caption_text)
            if 3 in choices and message.video:
                file_name = client.download_media(message.video)
                client.send_video(channel_target, file_name, caption=caption_text)
            if 4 in choices and message.document:
                file_name = client.download_media(message.document)
                client.send_document(channel_target, file_name, caption=caption_text)
            if 5 in choices and message.text:
                client.send_message(channel_target, message.text)
            if 6 in choices and message.sticker:
                file_name = client.download_media(message.sticker)
                client.send_sticker(channel_target, file_name)
            if 7 in choices and message.animation:
                file_name = client.download_media(message.animation)
                client.send_animation(channel_target, file_name) 
                
                # Obter o argumento duração para os videos baixados antes do upload
                if file_name:
                    video_metadata = all_video_metadata.get(os.path.basename(file_name), {})
                    duration = video_metadata.get("format", {}).get("duration", "")

            # Depois de baixar e fazer o upload, adicione detalhes ao JSON
            if file_name:
                media_type = None
                if message.photo:
                    media_type = "photo"#1
                elif message.audio:
                    media_type = "audio"#2
                elif message.video:
                    media_type = "video"#3
                elif message.document:
                    media_type = "document"#4
                elif message.text:
                    media_type = "text"#5
                elif message.sticker:
                    media_type = "sticker"#6
                elif message.animation:
                    media_type = "animation"#7    
    
                downloaded_media.append({
                    "id": message.id,
                    "type": media_type,
                    "file_name": file_name
                })

                # Salvar detalhes da mídia baixada em um arquivo JSON após o upload
                with open("downloaded_media.json", "w") as json_file:
                    json.dump(downloaded_media, json_file, indent=4)
               
                # Remover arquivo baixado após o upload e atualizar o JSON
                os.remove(file_name)
                os.system('clear || cls')
                print(f"Detalhes da mensagem {message.id} adicionados à lista e mídia / arquivo enviada ao canal de destino.")
                

            # Intervalo de 10s para evitar abuso da API do Telegram
            time.sleep(10)

        print("Tarefa concluida e log salvo no arquivo JSON.")

if __name__ == "__main__":
    show_banner()
    cache_path()
    authenticate()
    channel_source, channel_target = get_channels()
    choices = get_user_choices()
    download_and_upload_media_from_channel(choices, channel_source, channel_target)

