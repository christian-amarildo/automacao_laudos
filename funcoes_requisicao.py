import re  # Biblioteca para trabalhar com expressões regulares, usada para buscar padrões de texto
import pytesseract  # Interface Python para Tesseract, que permite realizar OCR (Reconhecimento Óptico de Caracteres)
from PIL import Image  # Biblioteca PIL (Pillow) usada para abrir e manipular imagens
import configparser # Importa a biblioteca para ler arquivos de configuração

# Função responsável por realizar o OCR em uma imagem e transcrever seu conteúdo para texto
def transcrever_imagem(caminho_imagem):
    # Lê o arquivo de configuração para obter o caminho do Tesseract
    config = configparser.ConfigParser()
    # Usar o encoding='utf-8' para evitar problemas com caracteres especiais no .ini
    config.read('config.ini', encoding='utf-8')
    
    # Define o caminho do executável do Tesseract a partir do config.ini
    # Isso evita a necessidade de ter o Tesseract no PATH do sistema
    try:
        tesseract_path = config.get('Paths', 'tesseract_cmd_path')
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            raise ValueError("O caminho para o Tesseract não pode ser vazio em config.ini.")
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
        # Lança um erro mais claro se a configuração não for encontrada ou for inválida
        raise FileNotFoundError(f"Erro ao ler 'tesseract_cmd_path' do 'config.ini': {e}. Verifique se o arquivo existe e se a configuração está correta.")

    # Abre a imagem a partir do caminho especificado
    image = Image.open(caminho_imagem)

    # Usa o pytesseract para realizar OCR na imagem e retornar o texto extraído
    texto = pytesseract.image_to_string(image)

    # Retorna o texto que foi extraído da imagem
    return texto

# Função responsável por processar o texto extraído e identificar as informações específicas da requisição
def processar_texto(texto):
    # Lê as expressões regulares do arquivo de configuração
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    # Verifica se a seção de padrões de regex existe
    if not config.has_section('RegexPatterns'):
        raise ValueError("A seção [RegexPatterns] não foi encontrada no arquivo config.ini")

    patterns = config['RegexPatterns']
    info = {}

    # Itera sobre cada item na seção de padrões e busca no texto
    for key, pattern in patterns.items():
        # O re.search vai procurar pelo padrão em qualquer parte do texto
        # re.IGNORECASE torna a busca não sensível a maiúsculas/minúsculas
        match = re.search(pattern, texto, re.IGNORECASE)
        
        # Se um padrão for encontrado (match), o grupo de captura 1 é extraído.
        # O grupo de captura (definido por parênteses na regex) pega apenas o valor desejado.
        if match:
            # .strip() remove espaços em branco do início e do fim do valor encontrado
            info[key] = match.group(1).strip()
        else:
            # Se nada for encontrado, um valor padrão "Não encontrado" é atribuído
            info[key] = "Não encontrado"

    return info

# Função para salvar a transcrição em um arquivo de texto
def salvar_transcricao(texto, caminho_saida):
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(texto)  # Escreve o texto transcrito no arquivo

# Bloco principal de execução, onde o código será executado quando o script for rodado
if __name__ == "__main__":
    # Definindo o caminho da imagem que contém a requisição, para ser processada
    caminho_imagem = r'.\BOP 000000000.000000-0 Celular crimes contra\Figura 00 - Requisição.jpg'
    
    # Definindo o caminho do arquivo de saída para a transcrição
    caminho_saida_transcricao = r'.\BOP 000000000.000000-0 Celular crimes contra\transcrição da requisição2.txt'
    
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
