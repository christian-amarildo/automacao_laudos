import os
import shutil
import re
from funcoes_requisicao import processar_texto  # Importa a função de processamento
from funcoes_requisicao import transcrever_imagem  # Importa a função de transcrição de imagem

# Função para clonar uma pasta e renomeá-la
def clonar_e_renomear_pasta(caminho_pasta_original, inquerito):
    # Substitui '/' por '.' no inquérito
    inquerito_numero = inquerito.replace('/', '.')  # Modificando o inquérito
    
    novo_nome = f"BOP {inquerito_numero} Celular crimes contra"  # Formatação do novo nome
    
    # Cria o caminho para a nova pasta
    novo_caminho = os.path.join(os.path.dirname(caminho_pasta_original), novo_nome)
    
    # Clona a pasta original para a nova pasta
    shutil.copytree(caminho_pasta_original, novo_caminho)
    
    print(f"Pasta clonada e renomeada para: {novo_nome}")

# Exemplo de uso
if __name__ == "__main__":
    # Caminho da pasta original
    caminho_pasta_original = r'C:\Users\Harpia\Documents\vscode\projetos\automacao laudos\BOP 000000000.000000-0 Celular crimes contra'

    # Caminho do arquivo de imagem que será processado
    caminho_imagem = r'C:\Users\Harpia\Documents\vscode\projetos\automacao laudos\BOP 000000000.000000-0 Celular crimes contra\Figura 00 - Requisição.jpg'
    
    try:
        # Transcreve o texto da imagem
        texto_transcrito = transcrever_imagem(caminho_imagem)  # Chama a função para transcrever o texto
        
        # Chama a função de processamento para obter o inquérito
        informacoes_requisicao = processar_texto(texto_transcrito)  # Chama a função para processar o texto

        # Obtém o inquérito do dicionário
        inquerito_numero = informacoes_requisicao['inquerito']  # Acesse o inquérito do dicionário

        # Chama a função para clonar e renomear a pasta
        clonar_e_renomear_pasta(caminho_pasta_original, inquerito_numero)  # Passa o inquérito para renomear a pasta

    except FileNotFoundError as e:
        print(f"Erro: O arquivo de imagem não foi encontrado. Verifique o caminho especificado: {e}")

    except Exception as e:
        print(f"Ocorreu um erro ao processar a imagem ou o texto: {e}")
