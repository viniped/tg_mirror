## TG MIRROR 

# Introdução

Um script simples e e intuitivo para salvar seus conteúdos favoritos do Telegram 

# Pré requisitos 

Python 3.10.xx + 
ffmpeg
git

# Configuração

Para uma melhor experiencia recomendo instalar os pré requisitos usando um gerenciador de pacotes. Para essa instalação vamos usar o chocolatey.

O Chocolatey é como uma "loja de aplicativos" para computadores Windows, mas em vez de clicar em botões para instalar programas, você usa comandos em um terminal (uma janela onde você digita comandos para o computador executar).

Quando você quer instalar um programa no seu computador, normalmente você precisa:

1 - Procurar o programa na internet.
2 - Baixar o programa do site oficial.
3 - Clicar no arquivo baixado para começar a instalação.
3 - Seguir as instruções para instalar o programa.

Com o Chocolatey, você pode pular esses passos e simplesmente digitar um comando simples para instalar um programa.

Assim como explicado na [página de instalação](https://chocolatey.org/install) do chocolatey, abra o PowerShell do windows com privilégio de administrador e execute o comando abaixo:

`Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))`

Após a instalação do chocolatey você está pronto para preparar o ambiente para a instalção do 
python e ffmpeg para isso no mesmo no mesmo terminal aberto cole o seguinte comando:

'choco install git ffmpeg python --version 3.11.3 -y'

e aguarde a instalação.

# Baixando o script para a sua máquina e instalando as dependências

Com o git, python e ffmpeg instalados clone o repositorio do script para a sua máquina 

para isso abra o prompt de comando do seu computador como administrador e redirecione para a area de trabalho com o seguinte comando:

	'cd Desktop'
	
Após isso clone o repositorio do script:

	'git clone https://github.com/viniped/tg_mirror.git'
	
Com isso será criado na sua Área de Trabalho uma pasta tg_mirror

Acesse ela pelo terminal com o comando: 

	'cd tg_mirror'

Após isso vamos instalar as dependencias com o comando:

	'pip install -r requirements.txt --upgrade'

# Usando o script 

Após ter preparado o ambiente ao abrir a pasta do script você verá alguns arquivos porém somente 3 são interressantes para a sua utilizão na prática :

	'exec_download_module.bat' : Executa o script que faz o download de todo o conteúdo de um canal seja protegido ou não.

	'exec_forward_module.bat' : Executa o script que faz o encaminhamento de um canal para um canal só seu criando assim uma cópia particular	

	'exec_tg_mirror.bat' : Executa o script que baixa as mídias de um canal protegido e envia para um canal só seu.
	
#Suporte em caso de duvidas 

Caso tenha alguma dúvida entre nesse grupo :

	https://t.me/+uxnB4OwMYPhiNWMx
	
# Aviso Legal:

O script TG_MIRROR é fornecido "como está" e sem garantias. É sua responsabilidade garantir que você tenha os direitos e permissões necessários para realizar as operações propostas. O autor do script não assume nenhuma responsabilidade por qualquer uso indevido ou danos causados pelo uso deste script.	 		
		
			

 

