import os
import re
import json
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage, ImageDraw

# Configurações iniciais
CORES_NOMES = {
    "preto": "#000000", "branco": "#FFFFFF", "vermelho": "#e74c3c", "verde": "#27ae60",
    "azul": "#3498db", "amarelo": "#f1c40f", "laranja": "#e67e22", "cinza": "#7f8c8d",
    "roxo": "#8e44ad", "rosa": "#fd79a8", "marrom": "#8d5524", "bege": "#f5f5dc",
    "dourado": "#ffd700", "prata": "#c0c0c0", "ciano": "#00bcd4", "violeta": "#9b59b6",
    "azul claro": "#5dade2", "azul escuro": "#2980b9", "verde claro": "#2ecc71",                     
    "verde escuro": "#145a32", "vermelho escuro": "#c0392b", "amarelo claro": "#fff9c4",
    "black": "#000000", "white": "#FFFFFF", "red": "#e74c3c", "green": "#27ae60",
    "blue": "#3498db", "yellow": "#f1c40f", "orange": "#e67e22", "gray": "#7f8c8d",
    "grey": "#7f8c8d", "purple": "#8e44ad", "pink": "#fd79a8", "brown": "#8d5524",
    "beige": "#f5f5dc", "gold": "#ffd700", "silver": "#c0c0c0", "cyan": "#00bcd4",
    "violet": "#9b59b6", "lightblue": "#5dade2", "darkblue": "#2980b9",
    "lightgreen": "#2ecc71", "darkgreen": "#145a32", "darkred": "#c0392b", "lightyellow": "#fff9c4"
}

pasta_curriculos = "/sdcard/wolf_documentos"
pasta_icones = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icones")
os.makedirs(pasta_curriculos, exist_ok=True)
os.makedirs(pasta_icones, exist_ok=True)

# Registrar fontes (se disponíveis)
try:
    pdfmetrics.registerFont(TTFont('Montserrat', 'Montserrat-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Montserrat-Bold', 'Montserrat-Bold.ttf'))
except:
    pass

# Banner do programa
BANNER = """
\033[1;36m


 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣄⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣡⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠙⣦⡙⢦⡀⠀⠀⠀⠀⠀⠀⡀⣄⡀⠀⡴⠸⣄⠀⣠⠎⢦⠀⢀⣠⢀⠀⠀⠀⠀⠀⠀⢀⡴⢋⣴⠏⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠘⢯⣦⣉⡳⠦⣄⡾⠶⠄⠛⢄⠉⣙⠁⣆⣌⠶⢃⣰⠈⢛⠉⠠⠚⠢⠶⠿⣠⠤⠞⣋⢴⡿⠋⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢠⠀⠈⢻⡻⣽⣶⣦⣄⠠⣄⠕⣤⣢⣞⣷⡜⣿⣶⣿⢧⣾⣷⣗⣤⠪⢀⠄⣠⣴⣶⣟⣟⡟⠁⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⡸⡂⠀⠀⠓⠘⢦⠀⠁⠁⠘⣦⢪⢿⣿⣿⠻⣿⣿⣿⠟⣿⣿⣿⡵⣴⠃⠘⠉⠐⡵⠋⠞⠀⠀⢀⢇⣻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣧⡀⠀⠀⠀⠄⠘⣧⠀⠀⠀⠸⣿⣿⣿⣿⣇⠘⣿⠃⣸⣿⣿⣿⣿⠇⠀⠀⠀⣼⠃⠀⠀⠀⠀⠘⢼⡸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⢿⡳⠀⠀⠀⠀⠀⠘⣧⡘⣦⣷⣻⢿⡿⣿⣿⣧⠀⣰⣿⣿⢿⡿⣿⣼⣴⣇⣼⠃⠀⠀⠀⠀⢀⠞⣿⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⢸⡀⡈⢷⠄⠀⠀⠄⣲⣶⣾⡿⠿⢝⠿⢷⡕⠸⡿⣿⢷⣿⣯⡏⢪⡾⠫⣻⠿⢿⣷⣶⣖⠢⠀⠀⠀⡾⢃⠀⡇⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢯⡛⠁⠘⠀⠀⠀⠀⡴⣖⣚⣿⣧⣄⠠⡀⠀⠹⣆⢳⠉⠀⠉⡞⣠⠏⠀⢀⠄⣠⣼⣿⣓⣒⠦⠀⠀⠀⠀⠂⡈⠛⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⢋⣤⣤⡖⠋⠁⠀⣠⣴⣟⢿⡿⣿⣿⣽⣦⣄⠈⠎⠣⠀⠘⠱⠁⢠⣴⣯⣿⣿⢿⡿⣿⣦⣄⠀⠈⠛⣶⣦⣄⡘⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢟⡖⢀⣤⡤⠔⠂⠠⠼⢿⡡⠌⠁⠈⡀⠻⣝⣿⣿⣆⡆⠀⠀⠀⢠⣴⣿⣿⢿⠟⢁⠁⠈⠀⢉⡿⠷⠄⠐⠢⠤⣤⡀⢲⡛⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠐⡻⠉⠀⠀⠀⠀⣀⡬⠀⠀⡤⡀⠻⣦⡀⠙⣿⡿⠇⠀⠀⠀⠸⢿⣿⠃⢁⣴⡟⢀⣤⠀⠀⢥⣄⠀⠀⠀⠀⠉⢝⠂⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢇⣼⣧⢾⣽⡂⢠⣾⠿⢿⣿⣧⣝⣿⣦⣄⠀⠀⠀⠀⠠⣴⣀⣦⡤⠀⠀⠀⠀⣀⣴⣟⣫⣴⣿⣿⠿⣷⣄⢀⢮⡷⢮⣧⡘⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡚⠉⠐⣩⡯⠖⢀⣤⢆⡀⠀⠉⠛⢻⡭⠀⠀⠲⢮⣽⣦⠸⣿⠏⣴⣏⡽⠖⠀⠀⢹⡟⠛⠋⠀⠀⡰⣤⡄⠰⢽⣍⠂⠉⢛⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⣠⠀⢚⡭⠂⠀⢉⣾⡿⠉⠀⠀⠀⢠⡶⢿⣷⣿⣦⠸⠿⠳⠉⠞⠿⠏⣴⣿⣾⡿⢶⣄⠀⠀⠀⠨⢿⣷⡍⠀⠐⢮⡓⠄⣄⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⡴⢋⣔⠄⠀⠀⡟⠀⡴⣾⠀⠀⡏⠀⢰⣿⢿⡇⠐⠊⠻⣿⠟⠉⠂⢹⣿⣿⡞⠀⠸⡄⠀⢳⢦⠀⢻⠀⠀⠠⡢⡙⢦⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠟⡀⢸⣿⠊⠀⠀⠃⠀⠁⡏⡆⠀⠀⠐⢌⠻⣟⣧⡀⠀⠀⠀⠀⠀⢀⣼⣳⡟⡡⠂⠀⠀⢰⢿⠈⠂⠈⠀⠀⠑⣽⡇⢀⠻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢸⡧⠀⠀⡀⠀⠀⠀⠁⢟⣆⠀⠀⠠⡓⢽⡿⡗⠆⠀⠀⠀⠠⢾⢟⡿⢊⠅⠀⢠⣸⡻⠈⠀⠀⠀⢀⠀⠀⢾⡇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠈⣠⡎⣾⠄⠰⡁⠄⠀⠀⠈⢻⡀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡀⠀⢀⡾⠁⠀⠀⠀⣀⠆⠀⣳⢰⣄⠁⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣰⠋⣧⠟⢀⢀⣿⡔⢰⠇⠀⠀⠁⠀⠀⣿⠀⡇⢰⢠⠀⡆⡆⢸⠀⣷⠁⠀⠈⠀⠀⠐⡆⢢⣻⡀⡀⠻⣸⠙⣆⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠇⠀⠸⡄⡾⣆⠻⡇⠘⠀⢀⠀⠀⠀⢀⠹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠏⠀⠀⠀⠀⡀⠀⠃⢸⠟⣰⣿⢀⠏⠀⠸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠁⣿⠀⣴⠀⢸⢺⠀⠀⠀⠘⠀⢸⠀⠀⠀⠀⠀⠀⠀⡇⠀⡇⠀⠀⠀⢳⡄⠀⣶⠀⢹⠈⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡜⠹⠳⣌⣿⡄⠀⠀⢇⠀⢻⢠⠀⠀⠀⠀⠀⡄⡯⠀⢰⠀⠀⢠⣿⢡⠞⠏⢧⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠈⠫⢳⣔⢠⠀⠀⡌⠈⠋⠃⠂⠘⠉⠁⢁⠀⠀⡄⣤⡞⠝⠁⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢶⡆⣦⠈⠓⠒⠒⠒⠒⠒⠚⠁⣰⢠⣵⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠘⢧⡈⢾⣴⣾⣦⠶⢃⡼⠃⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡈⠛⢃⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀by:jottap_62⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀©⠀Wolf-edit
insta📷:@jottap_62

░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░                                                                             
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░                                                                                    
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░                                                                                    
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓██████▓▒░                                                                               
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░                                                                                    
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░                                                                                    
 ░▒▓█████████████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░▒▓█▓▒░                                                                                    
                                                                                                                                         
\033[1;31m
 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓████████▓▒░▒▓██████▓▒░   
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
   ░▒▓██▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ 
                                                           
                                                           
                                                                                                                                                                                                                                                                                                                                                                                                                         
\033[0m
"""
class Cores:
    VERDE = '\033[1;32m'
    AZUL = '\033[1;34m'
    AMARELO = '\033[1;33m'
    VERMELHO = '\033[1;31m'
    MAGENTA = '\033[1;35m'
    CIANO = '\033[1;36m'
    RESET = '\033[0m'

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_banner():
    limpar_tela()
    print(BANNER)
    print(f"{Cores.CIANO}{'='*60}{Cores.RESET}")
    print(f"{Cores.VERDE}𓃦CRIADOR DE CURRÍCULOS PROFISSIONAIS 𓃦 by:jottap&&wolf-edit{Cores.RESET}")
    print(f"{Cores.CIANO}{'='*60}{Cores.RESET}\n")

def validar_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def validar_data(data):
    return re.match(r'^\d{2}/\d{2}/\d{4}$', data)

def validar_telefone(tel):
    return re.match(r'^\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4}$', tel)

def pedir_input(msg, obrigatorio=True, validar=None):
    while True:
        valor = input(msg).strip()
        if obrigatorio and not valor:
            print(f"{Cores.VERMELHO}Este campo é obrigatório!{Cores.RESET}")
            continue
        if validar and not validar(valor):
            print(f"{Cores.VERMELHO}Formato inválido!{Cores.RESET}")
            continue
        return valor

def traduz_cor(cor):
    cor = cor.strip().lower()
    if cor in CORES_NOMES:
        return CORES_NOMES[cor]
    if re.match(r"^#([A-Fa-f0-9]{6})$", cor):
        return cor
    return "#000000"  # padrão preto

def pedir_cor(msg, cor_padrao):
    while True:
        cor = input(msg + f" (ex: azul, blue, #3498db) [{cor_padrao}]: ").strip().lower()
        if not cor:
            return cor_padrao
        cor_hex = traduz_cor(cor)
        if cor_hex:
            return cor_hex
        print(f"{Cores.VERMELHO}Cor inválida! Digite nome da cor ou código hexadecimal.{Cores.RESET}")

def obter_foto():
    while True:
        opcao = input(f"\n{Cores.AZUL}Deseja adicionar uma foto? (s/n): {Cores.RESET}").strip().lower()
        if opcao in ('s', 'n'):
            break
        print(f"{Cores.VERMELHO}Opção inválida! Digite 's' ou 'n'.{Cores.RESET}")
    if opcao == 'n':
        return None
    while True:
        caminho = input(f"{Cores.AMARELO}Digite o caminho completo da foto (jpg, jpeg, png): {Cores.RESET}").strip()
        if caminho and os.path.isfile(caminho) and caminho.lower().endswith(('.jpg', '.jpeg', '.png')):
            return caminho
        print(f"{Cores.VERMELHO}Arquivo não encontrado ou formato inválido. Tente novamente.{Cores.RESET}")

def obter_lista(titulo):
    print(f"\n{Cores.AZUL}{titulo}{Cores.RESET}")
    print(f"{Cores.AMARELO}(digite 'fim' para terminar){Cores.RESET}")
    itens = []
    while True:
        item = input(f"{Cores.VERDE}• {Cores.RESET}").strip()
        if item.lower() == 'fim':
            break
        if item:
            itens.append(item)
    return itens

def obter_issp_completo():
    """Implementação completa do ISSP"""
    print(f"\n{Cores.AZUL}INFORMAÇÕES SOCIAIS E SOCIOPROFISSIONAIS (ISSP){Cores.RESET}")
    print(f"{Cores.AMARELO}(Preencha com informações relevantes){Cores.RESET}")

    issp = {
        "origem_social": input(f"{Cores.VERDE}• Origem Social/Familiar: {Cores.RESET}").strip(),
        "trajetoria_educacional": obter_lista("Trajetória Educacional"),
        "experiencias_profissionais": obter_lista("Experiências Profissionais"),
        "participacao_social": obter_lista("Participação Social"),
        "habilidades_sociais": obter_lista("Habilidades Sociais"),
        "conquistas": obter_lista("Principais Conquistas"),
        "objetivos_sociais": input(f"{Cores.VERDE}• Objetivos Sociais: {Cores.RESET}").strip(),
        "redes_apoio": obter_lista("Redes de Apoio")
    }

    # Formatação para o PDF
    issp_formatado = [
        f"<b>Origem Social:</b> {issp['origem_social']}",
        "<b>Trajetória Educacional:</b>",
        *[f"- {item}" for item in issp['trajetoria_educacional']],
        "<b>Experiências Profissionais:</b>",
        *[f"- {item}" for item in issp['experiencias_profissionais']],
        "<b>Participação Social:</b>",
        *[f"- {item}" for item in issp['participacao_social']],
        "<b>Habilidades Sociais:</b>",
        *[f"- {item}" for item in issp['habilidades_sociais']],
        "<b>Conquistas:</b>",
        *[f"- {item}" for item in issp['conquistas']],
        f"<b>Objetivos Sociais:</b> {issp['objetivos_sociais']}",
        "<b>Redes de Apoio:</b>",
        *[f"- {item}" for item in issp['redes_apoio']]
    ]

    return issp_formatado

def escolher_formato_foto():
    while True:
        formato = input(f"{Cores.AZUL}Escolha o formato da foto (quadrada/redonda) [quadrada]: {Cores.RESET}").strip().lower()
        if formato == '':
            return 'quadrada'
        if formato in ('quadrada', 'redonda'):
            return formato
        print(f"{Cores.VERMELHO}Opção inválida. Digite 'quadrada' ou 'redonda'{Cores.RESET}")

def obter_cursos():
    print(f"\n{Cores.AZUL}CURSOS E QUALIFICAÇÕES{Cores.RESET}")
    print(f"{Cores.AMARELO}(digite 'fim' para terminar){Cores.RESET}")
    cursos = []
    while True:
        curso = input(f"{Cores.VERDE}• Curso/Qualificação (ex: 'Curso de Excel Avançado - Instituição X - 2023'): {Cores.RESET}").strip()
        if curso.lower() == 'fim':
            break
        if curso:
            cursos.append(curso)
    return cursos

def escolher_tamanho_foto():
    opcoes = {
        "1": ("3x4", (90, 110)),
        "2": ("Pequeno", (80, 80)),
        "3": ("Médio", (130, 130)),
        "4": ("Grande", (180, 180)),
    }
    print(f"{Cores.AZUL}Escolha o tamanho da foto:{Cores.RESET}")
    for k, (nome, _) in opcoes.items():
        print(f"{Cores.VERDE}{k}. {nome}{Cores.RESET}")
    while True:
        escolha = input(f"{Cores.AZUL}Tamanho (1-4) [3]: {Cores.RESET}").strip()
        if escolha == '':
            escolha = '3'
        if escolha in opcoes:
            return opcoes[escolha]
        print(f"{Cores.VERMELHO}Opção inválida. Tente novamente.{Cores.RESET}")

def escolher_tamanho_nome():
    while True:
        try:
            tamanho = int(input(f"{Cores.AZUL}Digite o tamanho do nome (18-30) [23]: {Cores.RESET}").strip() or "23")
            if 18 <= tamanho <= 30:
                return tamanho
            print(f"{Cores.VERMELHO}Valor deve estar entre 18 e 30{Cores.RESET}")
        except ValueError:
            print(f"{Cores.VERMELHO}Digite um número válido{Cores.RESET}")

def redimensionar_imagem(caminho_original, largura_max, altura_max):
    try:
        img = PILImage.open(caminho_original)
        img.thumbnail((largura_max, altura_max), PILImage.LANCZOS)
        caminho_temp = os.path.join(pasta_curriculos, "foto_redimensionada_temp.png")
        img.save(caminho_temp)
        return caminho_temp
    except Exception as e:
        print(f"{Cores.VERMELHO}Erro ao redimensionar imagem: {e}{Cores.RESET}")
        return caminho_original

def criar_foto_redonda(caminho_foto, tamanho):
    try:
        img = PILImage.open(caminho_foto).convert("RGBA")
        img = img.resize(tamanho, PILImage.LANCZOS)

        mask = PILImage.new('L', tamanho, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + tamanho, fill=255)

        img.putalpha(mask)

        temp_path = os.path.join(pasta_curriculos, "foto_redonda_temp.png")
        img.save(temp_path)
        return temp_path
    except Exception as e:
        print(f"{Cores.VERMELHO}Erro ao processar foto: {e}{Cores.RESET}")
        return caminho_foto

def limpar_arquivos_temp():
    caminho_temp = os.path.join(pasta_curriculos, "foto_redimensionada_temp.png")
    if os.path.exists(caminho_temp):
        try:
            os.remove(caminho_temp)
        except:
            pass
    caminho_temp = os.path.join(pasta_curriculos, "foto_redonda_temp.png")
    if os.path.exists(caminho_temp):
        try:
            os.remove(caminho_temp)
        except:
            pass
    caminho_temp = os.path.join(pasta_curriculos, "watermark_temp.png")
    if os.path.exists(caminho_temp):
        try:
            os.remove(caminho_temp)
        except:
            pass

def obter_marca_dagua():
    print(f"\n{Cores.AZUL}Opções de Marca d'Água:{Cores.RESET}")
    print(f"{Cores.VERDE}1. Texto{Cores.RESET}")
    print(f"{Cores.VERDE}2. Imagem{Cores.RESET}")
    print(f"{Cores.VERDE}3. Nenhuma{Cores.RESET}")

    while True:
        opcao = input(f"{Cores.AZUL}Escolha o tipo de marca d'água (1-3) [3]: {Cores.RESET}").strip()
        if not opcao:
            opcao = '3'
        if opcao in ('1', '2', '3'):
            break
        print(f"{Cores.VERMELHO}Opção inválida! Tente novamente.{Cores.RESET}")

    if opcao == '3':
        return None

    # Pedir transparência
    while True:
        try:
            opacidade = float(input(f"{Cores.VERDE}Digite a transparência (0.1 a 0.5) [0.2]: {Cores.RESET}").strip() or "0.2")
            if 0.1 <= opacidade <= 0.5:
                break
            print(f"{Cores.VERMELHO}Valor deve estar entre 0.1 e 0.5{Cores.RESET}")
        except ValueError:
            print(f"{Cores.VERMELHO}Digite um número válido{Cores.RESET}")

    if opcao == '1':
        texto = input(f"{Cores.VERDE}Digite o texto para marca d'água: {Cores.RESET}").strip()
        if not texto:
            return None

        # Pedir tamanho do texto
        while True:
            try:
                tamanho = int(input(f"{Cores.VERDE}Digite o tamanho do texto (40-100) [60]: {Cores.RESET}").strip() or "60")
                if 40 <= tamanho <= 100:
                    break
                print(f"{Cores.VERMELHO}Valor deve estar entre 40 e 100{Cores.RESET}")
            except ValueError:
                print(f"{Cores.VERMELHO}Digite um número válido{Cores.RESET}")

        return {
            'tipo': 'texto',
            'conteudo': texto,
            'opacidade': opacidade,
            'tamanho': tamanho
        }
    else:
        while True:
            caminho = input(f"{Cores.AMARELO}Digite o caminho completo da imagem para marca d'água: {Cores.RESET}").strip()
            if caminho and os.path.isfile(caminho) and caminho.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Pedir tamanho da imagem
                while True:
                    try:
                        tamanho = int(input(f"{Cores.VERDE}Digite o tamanho da imagem (200-500 pixels) [300]: {Cores.RESET}").strip() or "300")
                        if 200 <= tamanho <= 500:
                            break
                        print(f"{Cores.VERMELHO}Valor deve estar entre 200 e 500{Cores.RESET}")
                    except ValueError:
                        print(f"{Cores.VERMELHO}Digite um número válido{Cores.RESET}")

                return {
                    'tipo': 'imagem',
                    'conteudo': caminho,
                    'opacidade': opacidade,
                    'tamanho': tamanho
                }
            print(f"{Cores.VERMELHO}Arquivo não encontrado ou formato inválido. Tente novamente.{Cores.RESET}")

def gerar_curriculo_wolf_padrao1(dados, arquivo_saida, cor_primaria_hex="#000000", cor_secundaria_hex="#444444", foto_formato="quadrada", foto_tamanho=(80,100), tamanho_nome=23):
    # Adicionar marca d'água se existir
    marca_dagua = dados.get("marca_dagua")

    # Criar documento
    doc = SimpleDocTemplate(
        arquivo_saida,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()
    story = []

    # Definir cores
    cor_primaria = colors.HexColor(cor_primaria_hex)
    cor_secundaria = colors.HexColor(cor_secundaria_hex)

    # Nome centralizado e foto à direita
    nome_style = ParagraphStyle(
        name="Nome",
        fontName="Helvetica-Bold",
        fontSize=tamanho_nome,
        alignment=1,  # Centralizado
        spaceAfter=8,
        textColor=cor_primaria
    )
    nome_para = Paragraph(dados["nome"], nome_style)

    # Processar foto
    foto_path = None
    if dados.get("foto") and os.path.exists(dados["foto"]):
        largura_foto, altura_foto = foto_tamanho
        foto_path = redimensionar_imagem(dados["foto"], largura_foto, altura_foto)
        if foto_formato == "redonda":
            foto_path = criar_foto_redonda(foto_path, (largura_foto, altura_foto))
        img = Image(foto_path, width=largura_foto, height=altura_foto)
    else:
        img = Spacer(foto_tamanho[0], foto_tamanho[1])

    # Linha com nome e foto
    table = Table(
        [[nome_para, img]],
        colWidths=[360, 100],
        rowHeights=[100]
    )
    table.setStyle(TableStyle([
        ('VALIGN', (0,0), (0,0), 'MIDDLE'),
        ('VALIGN', (1,0), (1,0), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))

    # Estilos para os dados
    dados_style = ParagraphStyle(
        name="Dados",
        fontName="Helvetica",
        fontSize=10,
        alignment=0,
        spaceAfter=2,
        leading=12,
        textColor=cor_secundaria
    )
    rotulo_style = ParagraphStyle(
        name="Rotulo",
        fontName="Helvetica-Bold",
        fontSize=10,
        alignment=0,
        spaceAfter=2,
        leading=12,
        textColor=cor_primaria
    )

    # Dados pessoais (endereço, estado civil, idade, nascimento)
    for rotulo, valor in [
        ("Endereço:", dados['endereco']),
        ("Estado Civil:", dados['estado_civil']),
        ("Idade:", f"{dados['idade']} anos"),
        ("Nascido em:", dados['nascimento']),
    ]:
        linha = Table([
            [Paragraph(f"<b>{rotulo}</b>", rotulo_style), Paragraph(valor, dados_style)]
        ], colWidths=[80, 380])
        linha.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(linha)

    story.append(Spacer(1, 4))

    # Telefones com ícone WhatsApp
    for tel in filter(None, dados["telefones"]):
        try:
            icone_path = os.path.join(pasta_icones, "whatsapp.png") if tel.get("whatsapp") else os.path.join(pasta_icones, "phone.png")
            if os.path.exists(icone_path):
                icone = Image(icone_path, width=10, height=10)
            else:
                icone = Paragraph("[WhatsApp] " if tel.get("whatsapp") else "[Tel] ", dados_style)
        except:
            icone = Paragraph("[WhatsApp] " if tel.get("whatsapp") else "[Tel] ", dados_style)

        linha_tel = Table([[icone, Paragraph(tel['numero'], dados_style)]], colWidths=[12, 380])
        linha_tel.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        linha = Table([
            [Paragraph("<b>Telefone:</b>", rotulo_style), linha_tel]
        ], colWidths=[80, 380])
        linha.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(linha)

    # Email com ícone Gmail
    try:
        icone_path = os.path.join(pasta_icones, "gmail.png")
        if os.path.exists(icone_path):
            icone = Image(icone_path, width=10, height=10)
        else:
            icone = Paragraph("[Email] ", dados_style)
    except:
        icone = Paragraph("[Email] ", dados_style)

    linha_email_icone = Table([[icone, Paragraph(dados['email'], dados_style)]], colWidths=[12, 380])
    linha_email_icone.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    linha_email = Table([
        [Paragraph("<b>E-mail:</b>", rotulo_style), linha_email_icone]
    ], colWidths=[80, 380])
    linha_email.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(linha_email)

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=cor_primaria))
    story.append(Spacer(1, 6))

    # Seções
    def secao(titulo, conteudo):
        titulo_style = ParagraphStyle(
            name="TituloSecao",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=cor_primaria,
            spaceAfter=2,
            spaceBefore=8,
            alignment=0
        )
        conteudo_style = ParagraphStyle(
            name="ConteudoSecao",
            fontName="Helvetica",
            fontSize=10,
            textColor=cor_secundaria,
            spaceAfter=4,
            leading=12
        )

        story.append(Paragraph(f"- <b>{titulo}</b>", titulo_style))
        story.append(Spacer(1, 2))
        if isinstance(conteudo, list):
            for item in conteudo:
                story.append(Paragraph(f"• {item}", conteudo_style))
        else:
            story.append(Paragraph(conteudo, conteudo_style))
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1, color=cor_primaria))
        story.append(Spacer(1, 6))

    secao("OBJETIVO", dados.get("objetivo", ""))

    if dados.get("resumo_profissional"):
        secao("RESUMO PROFISSIONAL", dados["resumo_profissional"])

    if dados.get("issp"):
        secao("INFORMAÇÕES SOCIAIS E SOCIOPROFISSIONAIS", dados["issp"])

    if dados.get("formacao"):
        secao("FORMAÇÃO ACADÊMICA", dados["formacao"])

    if dados.get("experiencia"):
        secao("EXPERIÊNCIA PROFISSIONAL", dados["experiencia"])

    if dados.get("habilidades"):
        secao("HABILIDADES", dados["habilidades"])
       
    if dados.get("cursos"):
        secao("CURSOS E QUALIFICAÇÕES", dados["cursos"])  

    # Adicionar marca d'água (apenas uma vez no centro)
    if marca_dagua:
        if marca_dagua['tipo'] == 'texto':
            def add_watermark(canvas, doc):
                canvas.saveState()
                canvas.setFont('Helvetica-Bold', marca_dagua['tamanho'])
                canvas.setFillColor(colors.grey, alpha=marca_dagua['opacidade'])

                # Calcular posição central
                text = marca_dagua['conteudo']
                text_width = canvas.stringWidth(text, 'Helvetica-Bold', marca_dagua['tamanho'])
                x_center = (A4[0] - text_width) / 2
                y_center = A4[1] / 2

                # Desenhar apenas uma marca d'água no centro
                canvas.drawString(x_center, y_center, text)
                canvas.restoreState()

            doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)

        elif marca_dagua['tipo'] == 'imagem':
            def add_image_watermark(canvas, doc):
                try:
                    canvas.saveState()
                    img = PILImage.open(marca_dagua['conteudo'])
                    width, height = img.size
                    aspect = width / float(height)
                    new_width = marca_dagua['tamanho']
                    new_height = int(new_width / aspect)

                    # Centralizar a imagem na página
                    x = (A4[0] - new_width) / 2
                    y = (A4[1] - new_height) / 2

                    # Criar imagem com transparência
                    img_with_alpha = PILImage.new('RGBA', img.size)
                    img_with_alpha.paste(img, (0, 0))
                    alpha = img_with_alpha.split()[3]
                    alpha = alpha.point(lambda p: p * marca_dagua['opacidade'] * 255)
                    img_with_alpha.putalpha(alpha)

                    # Salvar temporariamente
                    temp_path = os.path.join(pasta_curriculos, "watermark_temp.png")
                    img_with_alpha.save(temp_path)

                    # Desenhar apenas uma marca d'água no centro
                    canvas.drawImage(temp_path, x, y, width=new_width, height=new_height, mask='auto')
                    canvas.restoreState()

                    # Remover arquivo temporário
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except Exception as e:
                    print(f"{Cores.VERMELHO}Erro ao processar marca d'água: {e}{Cores.RESET}")

            doc.build(story, onFirstPage=add_image_watermark, onLaterPages=add_image_watermark)
    else:
        doc.build(story)

    # Remove arquivos temporários
    limpar_arquivos_temp()
    return True

def carregar_templates():
    return {
        "1": {
            "nome": "Moderno",
            "descricao": "Foto grande centralizada no topo, nome centralizado, seções limpas",
            "config": {
                "foto_posicao": "centro",
                "cor_primaria": "#3498db",
                "cor_secundaria": "#2980b9",
            }
        },
        "2": {
            "nome": "Premium",
            "descricao": "Foto grande centralizada no topo, nome centralizado, seções elegantes",
            "config": {
                "foto_posicao": "centro",
                "cor_primaria": "#e74c3c",
                "cor_secundaria": "#c0392b",
            }
        },
        "3": {
            "nome": "Criativo",
            "descricao": "Foto grande centralizada, nome centralizado, cores vivas",
            "config": {
                "foto_posicao": "centro",
                "cor_primaria": "#27ae60",
                "cor_secundaria": "#16a085",
            }
        },
        "4": {
            "nome": "Currículo Plus",
            "descricao": "Foto pequena no topo direito, nome centralizado, formatação clássica",
            "config": {
                "foto_posicao": "topo_direito_plus",
                "cor_primaria": "#000000",
                "cor_secundaria": "#444444",
            }
        },
        "5": {
            "nome": "Wolf Premium",
            "descricao": "Layout profissional com sidebar esquerda para dados pessoais",
            "config": {
                "foto_posicao": "sidebar",
                "cor_primaria": "#2c3e50",
                "cor_secundaria": "#7f8c8d",
            }
        },
        "6": {
            "nome": "Wolf+",
            "descricao": "Layout moderno com foto à direita do nome, seções destacadas",
            "config": {
                "foto_posicao": "topo_direito_wolfplus",
                "cor_primaria": "#2c3e50",
                "cor_secundaria": "#7f8c8d",
            }
        },
        "7": {
            "nome": "Wolf Futury",
            "descricao": "Design futurista com layout inovador e elementos modernos",
            "config": {
                "foto_posicao": "topo_direito_futury",
                "cor_primaria": "#9b59b6",
                "cor_secundaria": "#8e44ad",
            }
        },
        "8": {
            "nome": "wolf-padrão",
            "descricao": "Nome centralizado, dados pessoais à esquerda e foto à direita, seções com títulos e linhas",
            "config": {
                "foto_posicao": "direita",
                "cor_primaria": "#000000",
                "cor_secundaria": "#444444",
            }
        },
        "9": {
            "nome": "wolf-padrão1",
            "descricao": "Nome centralizado, dados pessoais à esquerda, foto à direita, estilo clássico Wolf",
            "config": {
                "foto_posicao": "direita",
                "cor_primaria": "#000000",
                "cor_secundaria": "#444444",
            },
            "func_gerar_pdf": gerar_curriculo_wolf_padrao1
        }
    }

def pedir_telefones():
    tel1 = pedir_input(f"{Cores.VERDE}Telefone principal: {Cores.RESET}", validar=validar_telefone)
    whatsapp1 = input(f"{Cores.AZUL}Este telefone tem WhatsApp? (s/n): {Cores.RESET}").strip().lower() == 's'
    tel2 = pedir_input(f"{Cores.VERDE}Telefone secundário (opcional): {Cores.RESET}", obrigatorio=False, validar=validar_telefone)
    whatsapp2 = False
    if tel2:
        whatsapp2 = input(f"{Cores.AZUL}Este telefone tem WhatsApp? (s/n): {Cores.RESET}").strip().lower() == 's'
    return [
        {"numero": tel1, "whatsapp": whatsapp1},
        {"numero": tel2, "whatsapp": whatsapp2} if tel2 else None
    ]

def salvar_dados_json(dados):
    caminho_json = dados["caminho_arquivo"].replace(".pdf", ".json")
    try:
        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"{Cores.VERMELHO}Erro ao salvar dados: {e}{Cores.RESET}")
        return False

def carregar_dados_json(caminho_json):
    try:
        with open(caminho_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"{Cores.VERMELHO}Erro ao carregar dados: {e}{Cores.RESET}")
        return None

def editar_layout():
    mostrar_banner()
    print(f"{Cores.AZUL}Digite o caminho do arquivo JSON do currículo para editar:{Cores.RESET}")
    caminho_json = input().strip()
    if not os.path.isfile(caminho_json):
        print(f"{Cores.VERMELHO}Arquivo não encontrado.{Cores.RESET}")
        input(f"{Cores.AZUL}Pressione Enter para continuar...{Cores.RESET}")
        return

    dados = carregar_dados_json(caminho_json)
    if not dados:
        input(f"{Cores.AZUL}Pressione Enter para continuar...{Cores.RESET}")
        return

    templates = carregar_templates()
    print(f"\n{Cores.CIANO}Escolha o modelo de currículo:{Cores.RESET}")
    for key, value in templates.items():
        print(f"{Cores.VERDE}{key} - {value['nome']}: {Cores.AZUL}{value['descricao']}{Cores.RESET}")

    template_escolhido = pedir_input(
        f"\n{Cores.VERDE}Modelo desejado (1-{len(templates)}): {Cores.RESET}",
        validar=lambda x: x in templates.keys()
    )
    template = templates[template_escolhido]

    cor_primaria = pedir_cor(f"{Cores.AZUL}Digite a cor principal do currículo{Cores.RESET}", template["config"]["cor_primaria"])
    cor_secundaria = pedir_cor(f"{Cores.AZUL}Digite a cor secundária do currículo{Cores.RESET}", template["config"]["cor_secundaria"])
    template["config"]["cor_primaria"] = cor_primaria
    template["config"]["cor_secundaria"] = cor_secundaria

    # Adicionar opção para escolher tamanho do nome
    print(f"\n{Cores.AZUL}Deseja alterar o tamanho do nome? (s/n) [n]: {Cores.RESET}")
    if input().strip().lower() == 's':
        dados["tamanho_nome"] = escolher_tamanho_nome()

    if "foto" in dados and dados["foto"]:
        print(f"\n{Cores.AZUL}Opções de foto:{Cores.RESET}")
        dados["foto_formato"] = escolher_formato_foto()
        dados["foto_tamanho_nome"], dados["foto_tamanho_dimensoes"] = escolher_tamanho_foto()

    print(f"\n{Cores.AZUL}Deseja alterar a marca d'água atual? (s/n) [n]: {Cores.RESET}")
    if input().strip().lower() == 's':
        dados["marca_dagua"] = obter_marca_dagua()

    nome_personalizado = input(f"{Cores.AZUL}Digite o nome para salvar o currículo (deixe em branco para usar o nome padrão): {Cores.RESET}").strip()
    if nome_personalizado:
        nome_arquivo = re.sub(r'[^\w]', '_', nome_personalizado) + ".pdf"
    else:
        nome_arquivo = os.path.basename(dados["caminho_arquivo"])
    dados["caminho_arquivo"] = os.path.join(os.path.dirname(dados["caminho_arquivo"]), nome_arquivo)

    if "func_gerar_pdf" in template:
        sucesso = template["func_gerar_pdf"](
            dados,
            dados["caminho_arquivo"],
            cor_primaria_hex=template["config"]["cor_primaria"],
            cor_secundaria_hex=template["config"]["cor_secundaria"],
            foto_formato=dados.get("foto_formato", "quadrada"),
            foto_tamanho=dados.get("foto_tamanho_dimensoes", (110, 110)),
            tamanho_nome=dados.get("tamanho_nome", 23)
        )
    else:
        sucesso = gerar_curriculo_wolf_padrao1(
            dados,
            dados["caminho_arquivo"],
            cor_primaria_hex=template["config"]["cor_primaria"],
            cor_secundaria_hex=template["config"]["cor_secundaria"],
            foto_formato=dados.get("foto_formato", "quadrada"),
            foto_tamanho=dados.get("foto_tamanho_dimensoes", (110, 110)),
            tamanho_nome=dados.get("tamanho_nome", 23)
        )

    if sucesso:
        salvar_dados_json(dados)
        print(f"\n{Cores.VERDE}Currículo editado gerado com sucesso em:{Cores.RESET}")
        print(f"{Cores.AZUL}{dados['caminho_arquivo']}{Cores.RESET}")
    else:
        print(f"\n{Cores.VERMELHO}Erro ao gerar PDF editado.{Cores.RESET}")
    input(f"{Cores.AZUL}Pressione Enter para continuar...{Cores.RESET}")

def criar_curriculo():
    mostrar_banner()
    dados = {
        "nome": pedir_input(f"{Cores.VERDE}Nome completo: {Cores.RESET}", obrigatorio=True),
        "endereco": pedir_input(f"{Cores.VERDE}Endereço (Rua, Nº, Bairro, Cidade, Estado): {Cores.RESET}", obrigatorio=True),
        "estado_civil": pedir_input(f"{Cores.VERDE}Estado civil: {Cores.RESET}", obrigatorio=True),
        "idade": pedir_input(f"{Cores.VERDE}Idade: {Cores.RESET}", validar=lambda x: x.isdigit()),
        "nascimento": pedir_input(f"{Cores.VERDE}Data de nascimento (DD/MM/AAAA): {Cores.RESET}", validar=validar_data),
        "telefones": pedir_telefones(),
        "email": pedir_input(f"{Cores.VERDE}E-mail: {Cores.RESET}", validar=validar_email),
        "objetivo": pedir_input(f"\n{Cores.AZUL}Objetivo profissional: {Cores.RESET}", obrigatorio=True),
        "cursos": obter_cursos(),
 "formacao": obter_lista("Formação acadêmica"),
        "experiencia": obter_lista("Experiência profissional (Empresa e cargo)"),
        "habilidades": obter_lista("Habilidades"),
        "foto": obter_foto(),
        "tamanho_nome": 23  # Valor padrão
    }

    # Adiciona ISSP se o usuário quiser
    if input(f"{Cores.AZUL}Deseja adicionar Informações Sociais e Socioprofissionais (ISSP)? (s/n): {Cores.RESET}").strip().lower() == 's':
        dados["issp"] = obter_issp_completo()

    # Adicionar marca d'água
    dados["marca_dagua"] = obter_marca_dagua()

    if dados["foto"]:
        dados["foto_formato"] = escolher_formato_foto()
        dados["foto_tamanho_nome"], dados["foto_tamanho_dimensoes"] = escolher_tamanho_foto()

    # Perguntar se deseja alterar o tamanho do nome
    print(f"\n{Cores.AZUL}Deseja definir um tamanho personalizado para o nome? (s/n) [n]: {Cores.RESET}")
    if input().strip().lower() == 's':
        dados["tamanho_nome"] = escolher_tamanho_nome()

    templates = carregar_templates()
    print(f"\n{Cores.CIANO}Escolha o modelo de currículo:{Cores.RESET}")
    for key, value in templates.items():
        print(f"{Cores.VERDE}{key} - {value['nome']}: {Cores.AZUL}{value['descricao']}{Cores.RESET}")

    template_escolhido = pedir_input(
        f"\n{Cores.VERDE}Modelo desejado (1-{len(templates)}): {Cores.RESET}",
        validar=lambda x: x in templates.keys()
    )
    template = templates[template_escolhido]

    cor_primaria = pedir_cor(f"{Cores.AZUL}Digite a cor principal do currículo{Cores.RESET}", template["config"]["cor_primaria"])
    cor_secundaria = pedir_cor(f"{Cores.AZUL}Digite a cor secundária do currículo{Cores.RESET}", template["config"]["cor_secundaria"])
    template["config"]["cor_primaria"] = cor_primaria
    template["config"]["cor_secundaria"] = cor_secundaria

    nome_personalizado = input(f"{Cores.AZUL}Digite o nome para salvar o currículo (deixe em branco para usar o nome padrão): {Cores.RESET}").strip()
    if nome_personalizado:
        nome_arquivo = re.sub(r'[^\w]', '_', nome_personalizado) + ".pdf"
    else:
        nome_arquivo = re.sub(r'[^\w]', '_', dados["nome"]) + "_Curriculo.pdf"
    dados["caminho_arquivo"] = os.path.join(pasta_curriculos, nome_arquivo)

    if "func_gerar_pdf" in template:
        sucesso = template["func_gerar_pdf"](
            dados,
            dados["caminho_arquivo"],
            cor_primaria_hex=template["config"]["cor_primaria"],
            cor_secundaria_hex=template["config"]["cor_secundaria"],
            foto_formato=dados.get("foto_formato", "quadrada"),
            foto_tamanho=dados.get("foto_tamanho_dimensoes", (110, 110)),
            tamanho_nome=dados.get("tamanho_nome", 23)
        )
    else:
        sucesso = gerar_curriculo_wolf_padrao1(
            dados,
            dados["caminho_arquivo"],
            cor_primaria_hex=template["config"]["cor_primaria"],
            cor_secundaria_hex=template["config"]["cor_secundaria"],
            foto_formato=dados.get("foto_formato", "quadrada"),
            foto_tamanho=dados.get("foto_tamanho_dimensoes", (110, 110)),
            tamanho_nome=dados.get("tamanho_nome", 23)
        )

    if sucesso:
        salvar_dados_json(dados)
        print(f"\n{Cores.VERDE}Currículo gerado com sucesso em:{Cores.RESET}")
        print(f"{Cores.AZUL}{dados['caminho_arquivo']}{Cores.RESET}")
        try:
            if os.name == 'nt':
                os.startfile(dados["caminho_arquivo"])
            elif sys.platform == 'darwin':
                os.system(f'open "{dados["caminho_arquivo"]}"')
            else:
                os.system(f'xdg-open "{dados["caminho_arquivo"]}"')
        except:
            pass
    else:
        print(f"\n{Cores.VERMELHO}Não foi possível gerar o currículo.{Cores.RESET}")

    input(f"\n{Cores.AZUL}Pressione Enter para continuar...{Cores.RESET}")

def mostrar_sobre():
    mostrar_banner()
    print(f"{Cores.AZUL}Wolf Currículos - Criador Profissional de Currículos{Cores.RESET}")
    print(f"{Cores.VERDE}Versão 2.0{Cores.RESET}")
    print(f"{Cores.CIANO}Desenvolvido para facilitar a criação de currículos modernos e profissionais{Cores.RESET}")
    print(f"\n{Cores.MAGENTA}Recursos:{Cores.RESET}")
    print(f"{Cores.VERDE}• Modelos de currículo personalizáveis{Cores.RESET}")
    print(f"{Cores.VERDE}• Interface amigável{Cores.RESET}")
    print(f"{Cores.VERDE}• Validação de dados automática{Cores.RESET}")
    print(f"{Cores.VERDE}• Suporte para adicionar foto{Cores.RESET}")
    print(f"{Cores.VERDE}• Geração de PDF profissional{Cores.RESET}")
    print(f"{Cores.VERDE}• Opções de formato e tamanho para fotos{Cores.RESET}")
    print(f"{Cores.VERDE}• Edição de currículos existentes{Cores.RESET}")
    print(f"{Cores.VERDE}• Seção ISSP completa para currículos sociais{Cores.RESET}")
    print(f"{Cores.VERDE}• Marca d'água personalizável (texto ou imagem){Cores.RESET}")
    print(f"{Cores.VERDE}• Controle do tamanho do nome no currículo{Cores.RESET}")
    input(f"\n{Cores.AZUL}Pressione Enter para voltar...{Cores.RESET}")

def abrir_pasta_curriculos():
    try:
        if os.name == 'nt':
            os.startfile(pasta_curriculos)
        elif sys.platform == 'darwin':
            os.system(f'open "{pasta_curriculos}"')
        else:
            os.system(f'xdg-open "{pasta_curriculos}"')
    except Exception as e:
        print(f"{Cores.VERMELHO}Erro ao abrir a pasta: {e}{Cores.RESET}")
        input(f"{Cores.AZUL}Pressione Enter para continuar...{Cores.RESET}")

def menu_principal():
    while True:
        mostrar_banner()
        print(f"{Cores.AMARELO}MENU PRINCIPAL{Cores.RESET}")
        print(f"{Cores.VERDE}1. Criar novo currículo{Cores.RESET}")
        print(f"{Cores.VERDE}2. Abrir pasta de currículos{Cores.RESET}")
        print(f"{Cores.VERDE}3. Sobre{Cores.RESET}")
        print(f"{Cores.VERDE}4. Editar layout de currículo existente{Cores.RESET}")
        print(f"{Cores.VERDE}5. Sair{Cores.RESET}")

        opcao = input(f"\n{Cores.AZUL}Escolha uma opção (1-5): {Cores.RESET}").strip()

        if opcao == "1":
            criar_curriculo()
        elif opcao == "2":
            abrir_pasta_curriculos()
        elif opcao == "3":
            mostrar_sobre()
        elif opcao == "4":
            editar_layout()
        elif opcao == "5":
            print(f"\n{Cores.AZUL}Obrigado por usar o Wolf Currículos!{Cores.RESET}")
            break
        else:
            print(f"\n{Cores.VERMELHO}Opção inválida! Tente novamente.{Cores.RESET}")
            input(f"{Cores.AZUL}Pressione Enter para continuar...{Cores.RESET}")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n{Cores.VERMELHO}Programa interrompido pelo usuário.{Cores.RESET}")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}Ocorreu um erro inesperado: {e}{Cores.RESET}")
