import os
import time
import json
from pyrogram import Client
from pathlib import Path
import subprocess
from tqdm import tqdm
from utils import Banner, show_banner, cache_path, authenticate

""" Global """
session_name = "user"

def get_channels():
    with Client(session_name) as client:
        channel_source = input("Forneça o @username ou ID do canal / grupo de origem: ")
        channel_target = input("Forneça o @username ou ID do canal de destino: ")
        channel_source = parse_channel_input(channel_source)
        channel_target = parse_channel_input(channel_target)
        chat_info = client.get_chat(channel_source)
        return channel_source, channel_target, chat_info.title

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
    print("Quais conteudos você deseja processar?:\n")
    options = ["Processar todos os Conteúdos", "Fotos", "Áudios", "Vídeos", "Arquivos", "Texto", "Sticker", "Animação - GIFs"]
    for i, option in enumerate(options):
        print(f"{i} - {option}")
    choices = input("\nInforme os conteúdos que deseja procesar separados por vírgula (ex: 1,3) < 0 para processar todos >  : ").split(',')
    choices = [int(choice.strip()) for choice in choices]
    if 0 in choices:
        choices = [1, 2, 3, 4, 5, 6, 7]
    return choices

def extract_thumbnail(video_path: str) -> str:
    thumbnail_path = video_path + ".jpg"

    # Extract frame from 00:00:01
    thumbnail_command = [
        'ffmpeg',
        '-i', video_path,
        '-ss', '00:00:01',
        '-vframes', '1',
        thumbnail_path
    ]
    try:
        subprocess.run(thumbnail_command)
        return thumbnail_path
    except Exception as e:
        print(f"Erro ao extrair miniatura: {e}")
        return ""

def collect_video_duration(video_path: str) -> int:
    try:
        ffprobe_command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        duration = subprocess.check_output(ffprobe_command).decode('utf-8').strip()
        return int(float(duration))
    except Exception as e:
        print(f"Erro ao coletar duração do vídeo: {e}")
        return 0  

def clean_filename(filename):
    unsupported_chars = '<>:"/\\|?#{}[]*'  
    for char in unsupported_chars:
        filename = filename.replace(char, '_')
    filename = filename.strip().strip('.')
    return filename    

def get_json_filename(channel_source, channel_target, chat_title):
    return f"downloaded_media_{chat_title}_{channel_source}_{channel_target}.json"

def get_json_filepath(channel_source, channel_target, chat_title):
    filename = f"downloaded_media_{chat_title}_{channel_source}_{channel_target}.json"
    cleaned_filename = clean_filename(filename)
    return os.path.join('download_tasks', cleaned_filename)

def download_and_upload_media_from_channel(choices, channel_source, channel_target, chat_title):
    downloaded_media = []
    last_processed_id = 0
    json_filepath = get_json_filepath(channel_source, channel_target, chat_title)

    if os.path.exists(json_filepath):
        with open(json_filepath, "r") as json_file:
            data = json.load(json_file)
            last_processed_id = data["last_processed_id"] if "last_processed_id" in data else 0
            print(f"Retomando do ID da próxima mensagem após a última processada: {last_processed_id + 1}")

    with Client(session_name) as client:
        all_messages = list(client.get_chat_history(channel_source))
        all_messages.reverse()
        start_processing = False

        for count, message in enumerate(all_messages):
            
            if start_processing or message.id > last_processed_id:
                start_processing = True
            else:
                continue
            file_name = None
            caption_text = message.caption
            duration = 0
            download_start_time = None
            last_update_time = None
            bytes_downloaded = 0
         
            def progress(current, total, operation="Downloading"):
                nonlocal download_start_time, last_update_time, bytes_downloaded
                if download_start_time is None:
                    download_start_time = time.time()
                    last_update_time = download_start_time
                else:
                    current_time = time.time()
                    elapsed_time = current_time - last_update_time
                    
                    if elapsed_time > 0.5:
                        speed_bps = (current - bytes_downloaded) / elapsed_time  # bytes por segundo
                        speed_mbps = (speed_bps * 8) / (10**6)  # megabits por segundo
                        bar.set_description(f"{operation} at {speed_mbps:.2f} Mbps")
                        bytes_downloaded = current
                        last_update_time = current_time
                bar.n = current
                bar.refresh()
           
            if 1 in choices and message.photo:
                file_size = message.photo.file_size
                bar = tqdm(total=file_size, desc="Downloading", leave=False)
                file_name = client.download_media(message.photo, progress=progress)
                client.send_photo(channel_target, file_name, caption=caption_text, progress=progress)        
           
            if 2 in choices and message.audio:
                #os.system('clear || cls')
                file_size = message.audio.file_size
                bar = tqdm(total=file_size, desc="Downloading", leave=False)                         
                file_name = client.download_media(message.audio, progress=lambda c, t: progress(c, t, "Downloading"))
                file_size = os.path.getsize(file_name)
                bar = tqdm(total=file_size, desc="Uploading ...", leave=False)
                client.send_audio(channel_target, file_name, caption=caption_text, progress=lambda c, t: progress(c, t, "Uploading"))
  
            if 3 in choices and message.video:
                #os.system('clear || cls')
                file_size = message.video.file_size
                bar = tqdm(total=file_size, desc="Downloading",unit = 'B', leave=False)
                file_name = client.download_media(message.video, progress=lambda c, t: progress(c, t, "Downloading"))
                duration = collect_video_duration(file_name)
                thumbnail_path = extract_thumbnail(file_name)
                
                if thumbnail_path:
                    file_size = os.path.getsize(file_name)
                    bar = tqdm(total=file_size, desc="Uploading ...", leave=False)
                    client.send_video(channel_target, file_name, caption=caption_text, duration=duration, thumb=thumbnail_path, progress=lambda c, t: progress(c, t, "Uploading"))

                    os.remove(thumbnail_path)  # Remove thumbnail file after uploads
                else:
                    file_size = os.path.getsize(file_name)
                    bar = tqdm(total=file_size, desc="Uploading ...", unit='B', leave=False)
                    client.send_video(channel_target, file_name, caption =caption_text, duration=duration, progress=progress)
               
            if 4 in choices and message.document:
                #os.system('clear || cls')
                file_size = message.document.file_size
                bar = tqdm(total=file_size, desc="Downloading", leave=False)
                file_name = client.download_media(message.document, progress=progress)
                client.send_document(channel_target, file_name, caption=caption_text, progress=progress)
                
            if 5 in choices and message.text:                
                client.send_message(channel_target, message.text)
                
            if 6 in choices and message.sticker:
                file_name = client.download_media(message.sticker)
                client.send_sticker(channel_target, file_name)
            if 7 in choices and message.animation:
                file_name = client.download_media(message.animation)
                client.send_animation(channel_target, file_name)
          
            if file_name:                            
                last_processed_id = message.id
                with open(json_filepath, "w") as json_file:
                    json.dump({"last_processed_id": last_processed_id}, json_file)
                    os.system('clear || cls')
                    print(f"Detalhes da mensagem {message.id} adicionados à lista e mídia / arquivo enviada ao canal de destino.")        
                os.remove(file_name)     
            # Intervalo de 5s para evitar abuso da API do Telegram
            time.sleep(5)
        print("Tarefa concluida e log salvo no arquivo JSON.")

if __name__ == "__main__":
    show_banner()
    cache_path()
    authenticate()
    channel_source, channel_target, chat_title = get_channels()
    choices = get_user_choices()
    download_and_upload_media_from_channel(choices, channel_source, channel_target, chat_title)
