# import pytesseract
# from PIL import Image

# def transcrever_imagem(caminho_imagem, caminho_texto):
#     # Configurar o caminho do Tesseract no Windows
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#     # Abrir a imagem
#     image = Image.open(caminho_imagem)

#     # Realizar OCR (extração de texto)
#     texto = pytesseract.image_to_string(image)

#     # Salvar o texto extraído em um arquivo .txt
#     with open(caminho_texto, 'w', encoding='utf-8') as arquivo:
#         arquivo.write(texto)

#     return texto
