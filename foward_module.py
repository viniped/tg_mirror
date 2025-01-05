import os
import time
import json
from pyrogram import Client
from utils import Banner, show_banner, cache_path, authenticate

import pyrogram
pyrogram.utils.MIN_CHANNEL_ID = -1002999999999

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
    choices = input("\nInforme os conteúdos que deseja procesar separados por vírgula (ex: 1,3) < 0 para processar todos > : ").split(',')
    choices = [int(choice.strip()) for choice in choices]
    if 0 in choices:
        choices = [1, 2, 3, 4, 5, 6, 7]
    return choices

def extract_links_from_buttons(reply_markup):
    if not reply_markup or not hasattr(reply_markup, 'inline_keyboard') or not reply_markup.inline_keyboard:
        return ''

    link_texts = []
    for row in reply_markup.inline_keyboard:
        for button in row:
            link_texts.append(f"{button.text} ({button.url})")
    return ' '.join(link_texts)

def extract_text_links_from_caption(message):
    if not hasattr(message, 'caption_entities') or not message.caption_entities:
        return ''

    links = []
    for entity in message.caption_entities:
        if entity.type == "text_link":
            links.append(entity.url)
    return ' '.join(links)

def get_custom_caption():
    caption = input("Digite a legenda personalizada (deixe em branco para manter a legenda original): ")
    return caption #Ask user for a custom caption and return it

def get_caption(message, custom_caption=None):
    caption_texts = []
    
    if custom_caption:
        caption_texts.append(custom_caption)
  
    if message.caption:
        caption_texts.append(message.caption.markdown) # adicionar legenda tradicional ao texto final
    
    links_from_buttons = extract_links_from_buttons(message.reply_markup)
    if links_from_buttons:
        caption_texts.append(links_from_buttons)# Adicionar links dos botões
    
    links_from_caption = extract_text_links_from_caption(message)
    if links_from_caption:
        caption_texts.append(links_from_caption)# legenda com hiper-link (text_link), adicionamos ao texto final
    
    if message.text and not links_from_buttons and not links_from_caption:
        caption_texts.append(message.text)# mensagem puramente textual
    return ' '.join(caption_texts).strip()

def clean_filename(filename):
    unsupported_chars = '<>:"/\\|?#{}[]*'  
    for char in unsupported_chars:
        filename = filename.replace(char, '_')
    filename = filename.strip().strip('.')
    return filename    

def generate_progress_filename(channel_source, channel_target, chat_title):
    filename = f"{chat_title}_{channel_source}_{channel_target}.json"
    cleaned_filename = clean_filename(filename)
    return os.path.join("forward_task", cleaned_filename)

def save_progress(filename, last_message_id):
    with open(filename, 'w') as file:
        json.dump({'last_message_id': last_message_id}, file)

def get_previous_progress(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('last_message_id')
    return None        

def forward_message(client, message, channel_target, progress_file, custom_caption):
    try:
        links_from_buttons = extract_links_from_buttons(message.reply_markup)
        final_caption = get_caption(message, custom_caption)

        if message.photo:
            client.send_photo(channel_target, message.photo.file_id, caption=final_caption)
        elif message.audio:
            client.send_audio(channel_target, message.audio.file_id, caption=final_caption)
        elif message.video:
            client.send_video(channel_target, message.video.file_id, caption=final_caption)
        elif message.document:
            client.send_document(channel_target, message.document.file_id, caption=final_caption)
        elif message.text:
            text_with_links = message.text + ' ' + links_from_buttons
            client.send_message(channel_target, text_with_links.strip())
        elif message.sticker:
            client.send_sticker(channel_target, message.sticker.file_id)
        elif message.animation:
            client.send_animation(channel_target, message.animation.file_id, caption=final_caption)
          
        save_progress(progress_file, message.id)
        os.system('clear || cls')
        print(f"Message {message.id} forwarded")
    except Exception as e:
        print(f"Erro ao reenviar mensagem: {e}")  # Atualizando o 'task - progress' após encaminhar

def forward_messages_from_channel(choices, channel_source, channel_target, chat_title):
    custom_caption = get_custom_caption()  # Pegue a legenda personalizada do usuário
    with Client(session_name) as client:
        progress_file = generate_progress_filename(channel_source, channel_target, chat_title)
        last_processed_msg_id = get_previous_progress(progress_file)
        all_messages = list(client.get_chat_history(channel_source))
        
        if last_processed_msg_id:
            all_messages = [msg for msg in all_messages if msg.id > last_processed_msg_id]
        all_messages.reverse()

        for message in all_messages:
            
            if (1 in choices and message.photo) or \
               (2 in choices and message.audio) or \
               (3 in choices and message.video) or \
               (4 in choices and message.document) or \
               (5 in choices and message.text) or \
               (6 in choices and message.sticker) or \
               (7 in choices and message.animation):
                forward_message(client, message, channel_target, progress_file, custom_caption)
                time.sleep(10)
        print("Task complete sucessfully")        

if __name__ == "__main__":
    show_banner()
    authenticate()
    cache_path()
    channel_source, channel_target, chat_title = get_channels()
    choices = get_user_choices()
    forward_messages_from_channel(choices, channel_source, channel_target, chat_title)
