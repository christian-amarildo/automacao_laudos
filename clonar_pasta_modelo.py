import os
import shutil
from funcoes_requisicao import processar_texto  # Importa a função de processamento
from funcoes_requisicao import transcrever_imagem  # Importa a função de transcrição de imagem
import re  # Certifique-se de que a biblioteca re está importada

def clonar_e_renomear_pasta(caminho_pasta_original, caminho_pasta_destino, marca_celular, inquerito):
    # Substituir caracteres inválidos do inquérito
    inquerito_numero = re.sub(r'[<>:"/\\|?*]', '.', inquerito)

    # Formatar o novo nome da pasta
    novo_nome = f"BOP {inquerito_numero} Celular {marca_celular} crimes contra"

    # Criar o novo caminho para a pasta clonada dentro do caminho de destino
    novo_caminho = os.path.join(os.path.dirname(caminho_pasta_original), novo_nome)
    # Verificar se o caminho da pasta original existe
    if not os.path.exists(caminho_pasta_original):
        raise FileNotFoundError(f"Pasta original não encontrada: {caminho_pasta_original}")

    # Verificar se a nova pasta já existe para evitar sobrescrita
    if os.path.exists(novo_caminho):
        raise FileExistsError(f"A pasta já existe: {novo_caminho}")

    # Clonar a pasta original para a nova pasta
    try:
        shutil.copytree(caminho_pasta_original, novo_caminho)
    except Exception as e:
        raise Exception(f"Erro ao clonar a pasta: {e}")
    
    print(f"Pasta clonada e renomeada para: {novo_nome}")
    return novo_caminho


def renomear_imagens(marca_celular, novo_caminho):
    # Percorre todos os arquivos na nova pasta
    for file_name in os.listdir(novo_caminho):
        # Garante que estamos trabalhando apenas com arquivos que são imagens
        if file_name.endswith(('.jpg', '.jpeg', '.png')):  # Filtra apenas imagens
            print(f"Arquivo encontrado: {file_name}")  # Exibe o nome do arquivo encontrado
            
            # Cria o caminho completo do arquivo antigo
            old_name = os.path.join(novo_caminho, file_name)
            # Renomeia o arquivo, substituindo 'celular' pelo nome fornecido
            new_name = os.path.join(novo_caminho, file_name.replace('celularr', marca_celular))
            
            if 'celularr' in file_name:
                # Renomeia o arquivo
                os.rename(old_name, new_name)
                print(f"Imagem renomeada: {old_name} -> {new_name}")  # Mostra o renomeio
            else:
                print(f"A parte 'celularr' não encontrada em: {file_name}")