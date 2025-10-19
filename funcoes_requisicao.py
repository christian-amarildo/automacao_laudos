import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
import re  # Biblioteca para trabalhar com expressões regulares, usada para buscar padrões de texto
from docling.document_converter import DocumentConverter, FormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractCliOcrOptions
from docling.datamodel.base_models import InputFormat
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
import configparser # Importa a biblioteca para ler arquivos de configuração

# Função responsável por realizar o OCR em uma imagem e transcrever seu conteúdo para texto
def transcrever_imagem(caminho_imagem):
    # Lê o arquivo de configuração para obter o caminho do Tesseract
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    tesseract_path = config.get('Paths', 'tesseract_cmd_path')

    # 1. Create pipeline options
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    ocr_options = TesseractCliOcrOptions()
    if tesseract_path:
        ocr_options.tesseract_cmd = tesseract_path
    ocr_options.force_full_page_ocr = True
    pipeline_options.ocr_options = ocr_options


    # 2. Create a FormatOption
    format_option = FormatOption(
        pipeline_cls=StandardPdfPipeline,
        backend=DoclingParseV4DocumentBackend,
        pipeline_options=pipeline_options,
    )

    # 3. Create DocumentConverter with custom format_options
    converter = DocumentConverter(
        format_options={
            InputFormat.IMAGE: format_option
        }
    )

    # 4. Convert the document
    result = converter.convert(caminho_imagem)
    doc = result.document
    
    # Export the parsed document to text
    texto = doc.export_to_text()

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
        print("--- Texto Transcrito ---")
        print(texto_transcrito)
        print("------------------------")

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
