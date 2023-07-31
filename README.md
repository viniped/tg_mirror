TG_mirror


Introdução

Este script tem como finalidade raspar (ou extrair) mídias de um canal do Telegram e enviar essas mídias para outro canal ou grupo. Além disso, ele pode coletar e gerenciar metadados dos vídeos antes de enviá-los para o canal de destino. Esse script é util para usuários interessados em fazer cópias de conteúdo protegido de canais do telegram.
Atenção esse script serve apenas para salvar conteudo protegido

Funcionalidades
Autenticação no Telegram:

O script autentica o usuário no Telegram usando uma API ID e API Hash.
Os detalhes da sessão são armazenados para evitar autenticações repetidas.

Coleta de Metadados de Vídeos:

Antes de fazer o upload de qualquer vídeo, o script coleta metadados dos arquivos de vídeo em um diretório específico (por padrão, "downloads").
Esta funcionalidade usa o ffprobe para coletar informações, como duração do vídeo.

Download e Upload de Mídias:

O script raspa mídias (fotos, áudios, vídeos) de um canal específico do Telegram.
As mídias baixadas são então enviadas para outro canal ou grupo.
Para evitar downloads repetidos, o script mantém um registro de todas as mídias baixadas anteriormente em um arquivo JSON.
Suporte para Legendas:

Se uma mídia no canal de origem tiver uma legenda (texto associado à mídia), essa legenda será preservada e enviada junto com a mídia para o canal de destino.
Intervalo entre Transferências:

Para evitar limitações de taxa e garantir uma operação suave, o script espera 5 segundos entre o download e upload de cada mídia.


Configuração


Instale o Python

Acesse o site python.org e baixe a versão estável mais nova recomendo a versão 3.11.3 (usada nos testes de desenvolvimento)
Atualize as dependências
Execute o arquivo update_libs.bat para atualizar as dependências

Se aparecer uma mensagem falando sobre pip desatualizado, execute novamente o arquivo de update após executar o seguinte comando no terminal como administrador : python -m pip install --upgrade pip

Instale o ffmpeg

Instalando o FFmpeg no Windows: Um Guia Passo a Passo

O FFmpeg é uma solução completa e multiplataforma para gravar, converter e transmitir áudio e vídeo. Ele é composto por várias bibliotecas e programas de linha de comando para manipular conteúdo multimídia. Neste guia, ensinaremos como instalar o FFmpeg no Windows.

Passo 1: Baixar o FFmpeg
Vá para o site oficial do FFmpeg: https://ffmpeg.org/download.html.

Na seção "Windows", você encontrará links para builds do FFmpeg para Windows. Um dos lugares recomendados para baixar é o link "Windows builds gyan.dev". Clique nele.

Isso o redirecionará para uma página de download. Escolha a versão adequada para o seu sistema (32 ou 64 bits). Para a maioria dos sistemas modernos, você deve escolher a versão de 64 bits.

Baixe o pacote "ffmpeg-git-essentials.7z"

Passo 2: Extrair os Arquivos
Uma vez baixado, vá até o arquivo .zip e extraia-o. Você pode usar softwares como WinRAR ou 7-Zip

Extraia o arquivo para um local de fácil acesso. Para fins deste guia, vamos extrair para C:\.

Depois de extraído, você terá uma pasta chamada algo como "ffmpeg-xxxxxxxxx-essentials_build". Você pode renomeá-la para apenas "ffmpeg" para simplificar os próximos passos.

Passo 3: Adicionar FFmpeg ao PATH do Windows

Pressione a tecla Windows + X e escolha "Sistema".

No menu à esquerda, clique em "Configurações avançadas do sistema".

Clique no botão "Variáveis de ambiente" na parte inferior da nova janela que aparece.

Na seção "Variáveis de sistema", procure por uma variável chamada Path e clique em "Editar".

Na janela que se abre, clique em "Novo" e adicione o caminho para o diretório bin do FFmpeg. Se você extraiu o FFmpeg em C:\ffmpeg, o caminho seria C:\ffmpeg\bin.

Clique em "OK" para fechar todas as janelas.

Passo 4: Verificar a Instalação
Abra o Prompt de Comando (pressione a tecla Windows, digite "cmd" e pressione Enter).

Digite ffmpeg -version e pressione Enter.

Se tudo estiver configurado corretamente, você verá informações sobre a versão do FFmpeg.

E pronto! Você instalou com sucesso o FFmpeg no seu sistema Windows e pode começar a usar seus recursos poderosos a partir do Prompt de Comando.


Com chocolatey é mais gostoso !!!


Você pode também instalar o ffmpeg via linha de comando, para isso siga o tutorial abaixo :


Chocolatey é um gerenciador de pacotes para Windows, similar ao apt-get do Ubuntu. Ele permite que você instale aplicativos e ferramentas de linha de comando com um único comando

Pórem aqui vamos abordar a instalação do python e ffmpeg

 1. Instalando o Chocolatey

1.1. Requisitos:

- Windows 7+ / Windows Server 2003+
- PowerShell v2+ (instalado por padrão em versões do Windows mais recentes)
- .NET Framework 4+ (o instalador tentará instalar o .NET 4.0 se você não tiver)

1.2. Processo de Instalação:

1. Abra o PowerShell como **administrador**. Você pode fazer isso pesquisando por "PowerShell" no menu Iniciar, clicando com o botão direito no ícone do Windows PowerShell e selecionando "Executar como administrador".

2. Copie e cole o seguinte comando no PowerShell e pressione Enter:


Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

3. Espere a instalação terminar. Após a instalação, feche o PowerShell.

2. Instalando o Python e FFmpeg usando Chocolatey

Após instalar o Chocolatey, instalar outros softwares se torna muito simples.

2.1. Instalando o Python:

1. Abra novamente o PowerShell como administrador.
  
2. Digite o seguinte comando para instalar o Python:


choco install python --version 3.11.3 -y


3. Aguarde a instalação terminar. O Python agora estará instalado e o comando `python` estará disponível no terminal.

2.2. Instalando o FFmpeg:

1. No mesmo PowerShell aberto como administrador, digite o seguinte comando para instalar o FFmpeg:


choco install ffmpeg -y


2. Aguarde a instalação terminar. O FFmpeg agora estará instalado e os comandos como `ffmpeg` e `ffprobe` estarão disponíveis no terminal.

3. Confirmando a Instalação:

Para confirmar que tudo foi instalado corretamente:

1. No PowerShell (não precisa ser como administrador), digite:


python --version

Isto deve mostrar a versão do Python que você instalou.

2. Ainda no PowerShell, digite:


ffmpeg -version


Isto deve mostrar a versão do FFmpeg que você instalou.

E é isso! Você instalou com sucesso o Python e o FFmpeg no seu sistema Windows usando o Chocolatey. Agora você pode aproveitar essas ferramentas poderosas sem ter que passar por processos de instalação complicados manualmente.

Você também pode aproveitar os recursos poderosos desse script no linux para isso use os comandos de instalação com sudo, para essa instalação vou abordar ubuntu e debian

os comandos devem ser 

sudo apt update --> atualizar a lista de pacotes do linux na máquina local 
sudo apt install python3 --> instalar o python3

Para instalar o gerenciador pip 

sudo apt install python3-pip

volto a repetir esse tutorial para linux serve apenas para ubuntu e debian 

se você usa outra distro linux se informe como fazer para a sua distro


Após preparar o ambiente você está pronto para usar esse poderoso script:

1 - Antes de usar o script esteja de posse da sua api_hash e api_id você pode obtê-las no site : https://my.telegram.org/auth

caso não souber pesquise a respeito 

2 - Após isso instale a biblioteca pyrogram na sua máquina para isso abra o prompt de comando como administrador e digite 

pip instal pyrogram

no linux a instalação é realizada com pip3 install pyrogram

3 - após isso execute o script para isso dentro da pasta onde você colocou o script na barra de caminho digite cmd e aperte enter 

Atenção : Esse script não requer privilégios elevados para ser executado

e digite o seguinte comando py tg_mirror.py 

4 - Na sua primeira execução ele irá pedir suas credenciais api_id e api_hash obtidas anteriormente autentique e siga os passos seguintes

5 Após autenticar o script pede para que você informe o @user_channel ou channel_id do canal que você quer copiar e o @user_channel ou channel_id do canal de destino. 

Após clonar sugiro que voce salve o Json criado com o nome do canal que você clonou em uma pasta dentro do script para clonar novamente 

Após ler esse tutorial e ainda tiver duvidas entre nesse grupo :

https://t.me/+uxnB4OwMYPhiNWMx

Esse script é disponibilizado como está e o desenvolvedor não se responsabiliza pelo mau uso do script 
