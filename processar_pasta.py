import os
from docling.document_converter import DocumentConverter, FormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractCliOcrOptions
from docling.datamodel.base_models import InputFormat
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
import configparser

def processar_pasta(caminho_pasta, caminho_arquivo_saida=None):
    """
    Processa todos os arquivos em uma pasta de forma recursiva, extraindo o texto de cada um.

    Args:
        caminho_pasta (str): O caminho para a pasta a ser processada.
        caminho_arquivo_saida (str, optional): O caminho do arquivo para salvar o texto combinado. 
                                              Se None, o texto é retornado em vez de salvo.

    Returns:
        str or None: O texto combinado de todos os arquivos se caminho_arquivo_saida for None, 
                     caso contrário, None.
    """
    texto_combinado = ""
    
    # Configura o docling para usar OCR
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    tesseract_path = config.get('Paths', 'tesseract_cmd_path')

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    ocr_options = TesseractCliOcrOptions()
    if tesseract_path:
        ocr_options.tesseract_cmd = tesseract_path
    ocr_options.force_full_page_ocr = True
    pipeline_options.ocr_options = ocr_options

    format_option = FormatOption(
        pipeline_cls=StandardPdfPipeline,
        backend=DoclingParseV4DocumentBackend,
        pipeline_options=pipeline_options,
    )

    # We need to create a dictionary of format options for all possible input formats
    # that we want to handle. For simplicity, we will use the same options for all.
    # A better approach would be to have different options for different file types.
    format_options = {
        InputFormat.IMAGE: format_option,
        InputFormat.PDF: format_option,
        InputFormat.DOCX: format_option,
        # Add other formats as needed
    }

    converter = DocumentConverter(format_options=format_options)

    for root, _, files in os.walk(caminho_pasta):
        for file in files:
            caminho_arquivo = os.path.join(root, file)
            try:
                print(f"Processando arquivo: {caminho_arquivo}")
                result = converter.convert(caminho_arquivo)
                doc = result.document
                texto_combinado += f"--- Conteúdo de {caminho_arquivo} ---\n"
                texto_combinado += doc.export_to_text()
                texto_combinado += "\n\n"
            except Exception as e:
                print(f"Erro ao processar o arquivo {caminho_arquivo}: {e}")
    
    if caminho_arquivo_saida:
        with open(caminho_arquivo_saida, "w", encoding="utf-8") as f:
            f.write(texto_combinado)
        print(f"\nProcessamento da pasta concluído. O resultado foi salvo em '{caminho_arquivo_saida}'")
        return None
    else:
        return texto_combinado

if __name__ == '__main__':
    # Exemplo de uso:
    # Substitua pelo caminho da pasta que você deseja processar
    pasta_exemplo = r'.\\BOP 000000000.000000-0 Celular crimes contra'
    arquivo_saida_exemplo = os.path.join(pasta_exemplo, "resultado_completo.txt")
    
    # Processa a pasta e salva o resultado diretamente no arquivo de saída
    processar_pasta(pasta_exemplo, arquivo_saida_exemplo)
