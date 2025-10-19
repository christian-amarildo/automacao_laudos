from docling.document_converter import DocumentConverter
import os

# Define o caminho para o documento
file_path = "Laudo prot - Celular extração e análise.docx"

# Verifica se o arquivo existe
if not os.path.exists(file_path):
    print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    print(f"Verifique se o arquivo está no diretório: {os.getcwd()}")
else:
    try:
        print(f"Carregando o documento: {file_path}")
        
        # Usa o Docling para converter o documento
        converter = DocumentConverter()
        result = converter.convert(file_path)
        doc = result.document
        
        # Imprime algumas informações básicas sobre o documento
        print("\n--- Análise do Documento com Docling ---")
        
        # Export the parsed document to Markdown format
        markdown_output = doc.export_to_markdown()
        print(markdown_output)
        
        print("\nDocling carregou o documento com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao usar o Docling para processar o arquivo: {e}")