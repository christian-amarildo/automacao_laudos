import re  # Biblioteca para trabalhar com expressões regulares, usada para buscar padrões de texto
import pytesseract  # Interface Python para Tesseract, que permite realizar OCR (Reconhecimento Óptico de Caracteres)
from PIL import Image  # Biblioteca PIL (Pillow) usada para abrir e manipular imagens

# Função responsável por realizar o OCR em uma imagem e transcrever seu conteúdo para texto
def transcrever_imagem(caminho_imagem):
    # Configura o caminho do Tesseract no Windows, necessário para usar o Tesseract em um ambiente Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Abre a imagem a partir do caminho especificado
    image = Image.open(caminho_imagem)

    # Usa o pytesseract para realizar OCR na imagem e retornar o texto extraído
    texto = pytesseract.image_to_string(image)

    # Retorna o texto que foi extraído da imagem
    return texto

# Função responsável por processar o texto extraído e identificar as informações específicas da requisição
def processar_texto(texto):
    # Definindo padrões com expressões regulares para capturar informações específicas no texto extraído
    requisicao_pattern = r"REQUIZAO DE PERÍCIA Nº\s*(\d{5}-\d{4}-\d{6})"
    inquerito_pattern = r"INQUÉRITO POR PORTARIA Nº\s*(\d{5}/\d{4}\.\d{6}-\d{1})"
    data_pattern = r"datada de\s*(\d{2}/\d{2}/\d{4})"
    autoridade_pattern = r"assinado pela autoridade\s*([A-Z\s]+),"
    lacre_pattern = r"Lacre nº\s*([Y\d]+)"

    # Usando expressões regulares para buscar as informações no texto
    requisicao = re.search(requisicao_pattern, texto, re.IGNORECASE)
    inquerito = re.search(inquerito_pattern, texto, re.IGNORECASE)
    data = re.search(data_pattern, texto, re.IGNORECASE)
    autoridade = re.search(autoridade_pattern, texto, re.IGNORECASE)
    lacre = re.search(lacre_pattern, texto, re.IGNORECASE)

    # Armazenando as informações encontradas em variáveis
    requisicao_numero = requisicao.group(1) if requisicao else "Não encontrado"
    inquerito_numero = inquerito.group(1) if inquerito else "Não encontrado"
    data_requisicao = data.group(1) if data else "Não encontrado"
    autoridade_nome = autoridade.group(1).strip() if autoridade else "Não encontrado"
    lacre_numero = lacre.group(1) if lacre else "Não encontrado"

    # Retorna as informações extraídas em um dicionário
    return {
        "requisicao": requisicao_numero,
        "inquerito": inquerito_numero,
        "data": data_requisicao,
        "autoridade": autoridade_nome,
        "lacre": lacre_numero
    }

# Função para salvar a transcrição em um arquivo de texto
def salvar_transcricao(texto, caminho_saida):
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(texto)  # Escreve o texto transcrito no arquivo

# Bloco principal de execução, onde o código será executado quando o script for rodado
if __name__ == "__main__":
    # Definindo o caminho da imagem que contém a requisição, para ser processada
    caminho_imagem = r'"C:\Users\Harpia\Documents\vscode\projetos\automacao laudos\BOP 000000000.000000-0 Celular crimes contra\Figura 00 - Requisição.jpg"'
    
    # Definindo o caminho do arquivo de saída para a transcrição
    caminho_saida_transcricao = r'C:\Users\Harpia\Documents\vscode\projetos\automacao laudos\BOP 000000000.000000-0 Celular crimes contra\Figura 00 - Requisição2.txt'
    
    try:
        # Chama a função para transcrever o texto a partir da imagem da requisição
        texto_transcrito = transcrever_imagem(caminho_imagem)

        # Salva a transcrição em um arquivo .txt, sobrescrevendo se já existir
        salvar_transcricao(texto_transcrito, caminho_saida_transcricao)

        # Chama a função para processar o texto e extrair as informações da requisição
        informacoes_requisicao = processar_texto(texto_transcrito)

        # Exibir as informações extraídas da requisição
        print("Informações extraídas da requisição:")
        for chave, valor in informacoes_requisicao.items():
            print(f"{chave}: {valor}")

    except FileNotFoundError as e:
        print(f"Erro: O arquivo de imagem não foi encontrado. Verifique o caminho especificado: {e}")

    except Exception as e:
        print(f"Ocorreu um erro ao processar a imagem ou o texto: {e}")
