# import pytesseract
# from PIL import Image

# # Configurar o caminho do Tesseract no Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Abrir uma imagem de exemplo
# image = Image.open('exemplo.jpg')

# # Realizar OCR (extração de texto)
# texto = pytesseract.image_to_string(image)

# # Exibir o texto extraído
# print(texto)


import pytesseract
from PIL import Image

# Configurar o caminho do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Abrir uma imagem de exemplo
image = Image.open('exemplo.jpg')

# Realizar OCR (extração de texto)
texto = pytesseract.image_to_string(image)

# Exibir o texto extraído
print(texto)

# Salvar o texto extraído em um arquivo .txt
with open('transcrição da requisição.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write(texto)

print("Texto extraído salvo em 'texto_extraido.txt'")
