#!/bin/bash

# Cores para o terminal
VERDE="\033[1;32m"
AZUL="\033[1;34m"
AMARELO="\033[1;33m"
VERMELHO="\033[1;31m"
MAGENTA="\033[1;35m"
CIANO="\033[1;36m"
RESET="\033[0m"

# Função para exibir o banner
mostrar_banner() {
    clear
    echo -e "${CIANO}"
    echo "░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░"
    echo "░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░"
    echo "░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░"
    echo "░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓██████▓▒░"
    echo "░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░"
    echo "░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░"
    echo " ░▒▓█████████████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░▒▓█▓▒░"
    echo -e "${RESET}"
    echo -e "${VERDE}𓃦 INSTALADOR DE REQUISITOS WOLF-Vitae 𓃦${RESET}"
    echo -e "${CIANO}==============================================${RESET}"
    echo -e "${AZUL}Este script instalará todos os requisitos necessários${RESET}"
    echo -e "${AZUL}para executar o Wolf-Vitae - Criador de Currículos${RESET}"
    echo -e "${CIANO}==============================================${RESET}"
    echo ""
}

# Função para verificar e instalar Python
instalar_python() {
    echo -e "${AZUL}Verificando a instalação do Python...${RESET}"
    
    if command -v python3 &>/dev/null; then
        echo -e "${VERDE}Python 3 já está instalado.${RESET}"
    else
        echo -e "${AMARELO}Python 3 não encontrado. Instalando...${RESET}"
        
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install python
        else
            echo -e "${VERMELHO}Sistema operacional não suportado. Instale o Python manualmente.${RESET}"
            exit 1
        fi
        
        if command -v python3 &>/dev/null; then
            echo -e "${VERDE}Python 3 instalado com sucesso!${RESET}"
        else
            echo -e "${VERMELHO}Falha ao instalar o Python 3.${RESET}"
            exit 1
        fi
    fi
}

# Função para instalar pacotes pip
instalar_pacotes_python() {
    echo -e "${AZUL}Instalando pacotes Python necessários...${RESET}"
    
    pacotes=(
        "reportlab"
        "pillow"
        "python-dateutil"
    )
    
    for pacote in "${pacotes[@]}"; do
        echo -e "${CIANO}Instalando $pacote...${RESET}"
        pip3 install --user "$pacote"
        if pip3 show "$pacote" &>/dev/null; then
            echo -e "${VERDE}$pacote instalado com sucesso!${RESET}"
        else
            echo -e "${VERMELHO}Falha ao instalar $pacote.${RESET}"
            exit 1
        fi
    done
    
    echo -e "${VERDE}Todos os pacotes Python foram instalados com sucesso!${RESET}"
}

# Função para instalar fontes (opcional)
instalar_fontes() {
    echo -e "${AZUL}Instalando fontes opcionais...${RESET}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "${CIANO}Instalando fontes Montserrat...${RESET}"
        sudo apt-get install -y fonts-montserrat
        echo -e "${VERDE}Fontes instaladas com sucesso!${RESET}"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${CIANO}Para instalar fontes no macOS, baixe-as manualmente:${RESET}"
        echo -e "${AZUL}https://fonts.google.com/specimen/Montserrat${RESET}"
    else
        echo -e "${AMARELO}Instalação de fontes não suportada para este sistema.${RESET}"
        echo -e "${AZUL}Baixe manualmente as fontes Montserrat se desejar.${RESET}"
    fi
}

# Função para criar diretórios necessários
criar_diretorios() {
    echo -e "${AZUL}Criando diretórios necessários...${RESET}"
    
    DIRETORIOS=(
        "./wolf_documentos"
        "./icones"
    )
    
    for dir in "${DIRETORIOS[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo -e "${VERDE}Diretório $dir criado com sucesso!${RESET}"
        else
            echo -e "${CIANO}Diretório $dir já existe.${RESET}"
        fi
    done
    
    # Baixar ícones padrão (opcional)
    echo -e "${AZUL}Baixando ícones padrão...${RESET}"
    ICONES=(
        "https://raw.githubusercontent.com/jottap/Wolf-Edit/main/icones/whatsapp.png"
        "https://raw.githubusercontent.com/jottap/Wolf-Edit/main/icones/gmail.png"
        "https://raw.githubusercontent.com/jottap/Wolf-Edit/main/icones/phone.png"
    )
    
    for icone in "${ICONES[@]}"; do
        nome_icone=$(basename "$icone")
        if [ ! -f "./icones/$nome_icone" ]; then
            wget "$icone" -P "./icones/" && \
            echo -e "${VERDE}Ícone $nome_icone baixado com sucesso!${RESET}" || \
            echo -e "${AMARELO}Falha ao baixar $nome_icone.${RESET}"
        else
            echo -e "${CIANO}Ícone $nome_icone já existe.${RESET}"
        fi
    done
}

# Função principal
main() {
    mostrar_banner
    
    # Verificar se é root
    if [ "$EUID" -eq 0 ]; then
        echo -e "${VERMELHO}Aviso: Não é recomendado executar este script como root.${RESET}"
        read -p "Deseja continuar mesmo assim? [s/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Ss]$ ]]; then
            exit 1
        fi
    fi
    
    # Atualizar lista de pacotes (Linux)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "${AZUL}Atualizando lista de pacotes...${RESET}"
        sudo apt-get update
    fi
    
    instalar_python
    instalar_pacotes_python
    instalar_fontes
    criar_diretorios
    
    echo -e "${CIANO}==============================================${RESET}"
    echo -e "${VERDE}Instalação concluída com sucesso!${RESET}"
    echo -e "${AZUL}Agora você pode executar o script Wolf-vitae.${RESET}"
    echo -e "${CIANO}==============================================${RESET}"
    echo ""
    
    # Mostrar mensagem final
    echo -e "${MAGENTA}Dica:${RESET} ${AMARELO}Certifique-se de que o script Wolf-Edit tenha permissão de execução:${RESET}"
    echo -e "  ${CIANO}chmod +x wolf-vitae.py${RESET}"
    echo -e "${AMARELO}E execute com:${RESET}"
    echo -e "  ${CIANO}python3 wolf-vitae.py${RESET}"
    echo ""
}

# Executar função principal
main
