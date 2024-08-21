from flask import Blueprint, render_template, request
import google.generativeai as genai
from app.senha import GEMINI_API_KEY
from bs4 import BeautifulSoup
import requests

main_controller = Blueprint('main_controller', __name__)

# Configure a chave da API do Gemini
genai.configure(api_key=GEMINI_API_KEY)

@main_controller.route('/')
def index():
    return render_template('index.html')

@main_controller.route('/', methods=['POST'])
def scrape():
    url = request.form['url']
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta um erro para códigos de status 4xx ou 5xx
        
        # Usar BeautifulSoup para analisar o conteúdo HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extrair texto de todas as tags <p>
        paragraphs = soup.find_all('p')
        page_content = '\n'.join([p.get_text() for p in paragraphs])  # Juntar todos os textos em uma única string
        
        # Use a API do Gemini para gerar uma resposta
        model = genai.GenerativeModel('gemini-1.5-flash')
        result = model.generate_content(f"Resuma o texto em no máx 100 palavras, não passe disso:\n\n{page_content}")
        
        summary = result.text.strip()
        
    except requests.exceptions.RequestException as e:
        page_content = f"Erro ao acessar a URL: {str(e)}"
        summary = ""
    except Exception as e:
        page_content = "Ocorreu um erro interno no servidor."
        summary = f"Erro interno no servidor: {str(e)}"
    
    return render_template('index.html', page_content=page_content, summary=summary)
