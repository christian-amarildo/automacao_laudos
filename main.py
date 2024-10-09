import pytesseract
from PIL import Image
from funcoes import processar_texto, atualizar_historico  # Importando funções do arquivo "funções"

# Configurar o caminho do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Função principal
def main():
    # Abrir uma imagem de exemplo
    image = Image.open('imagens/requisicao.jpg')

    # Realizar OCR (extração de texto)
    texto = pytesseract.image_to_string(image)

    # Salvar o texto extraído em um arquivo .txt
    with open('textos/transcricao.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(texto)

    print("Texto extraído salvo em 'textos/transcricao.txt'")

    # Processar o texto extraído
    informacoes = processar_texto(texto)

    # Exibir as informações extraídas
    print("Informações extraídas:")
    print(informacoes)

    # Atualizar o modelo de laudo com as informações extraídas
    atualizar_historico('modelo_laudo.docx', 'laudos/laudo_pericial.docx', informacoes)
    print("Laudo atualizado e salvo em 'laudos/laudo_pericial.docx'.")

if __name__ == "__main__":
    main()
