import os
import shutil
import re
import json

def _renomear_imagens(modelo_dispositivo, novo_caminho):
    """Função interna para renomear imagens na pasta de destino."""
    if not modelo_dispositivo:
        print("Aviso: Modelo do dispositivo não fornecido, pulando renomeação de imagens.")
        return

    for file_name in os.listdir(novo_caminho):
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            old_path = os.path.join(novo_caminho, file_name)
            # A lógica agora substitui 'dispositivoo' (case-insensitive)
            if 'dispositivoo' in file_name.lower():
                new_file_name = re.sub('dispositivoo', modelo_dispositivo, file_name, flags=re.IGNORECASE)
                new_path = os.path.join(novo_caminho, new_file_name)
                os.rename(old_path, new_path)
                print(f"Imagem renomeada: {file_name} -> {new_file_name}")


def executar_clonagem_completa(caminho_origem, caminho_destino_base, info_requisicao, modelo_dispositivo):
    """
    Executa o processo completo de clonagem, incluindo nomeação, cópia e renomeação de imagens.
    """
    # 1. Validar entradas
    if not caminho_origem or not os.path.exists(caminho_origem):
        raise FileNotFoundError(f"A pasta de origem selecionada não existe: {caminho_origem}")
    if not caminho_destino_base:
        raise ValueError("Nenhum diretório de destino foi selecionado.")

    # 2. Montar o nome da nova pasta
    inquerito = info_requisicao.get('inquerito', 'N_A')
    tipo_crime = info_requisicao.get('tipo_crime', '').strip()
    inquerito_numero = re.sub(r'[<>:"/\\|?*]', '.', inquerito)
    
    novo_nome_pasta = f"BOP {inquerito_numero} Dispositivo {modelo_dispositivo} crimes contra {tipo_crime}"
    caminho_final_pasta = os.path.join(caminho_destino_base, novo_nome_pasta)

    if os.path.exists(caminho_final_pasta):
        raise FileExistsError(f"A pasta de destino já existe: {caminho_final_pasta}")

    # 3. Copiar a árvore de diretórios
    shutil.copytree(caminho_origem, caminho_final_pasta)
    print(f"Pasta clonada para: {caminho_final_pasta}")

    # 4. Renomear as imagens na nova pasta
    _renomear_imagens(modelo_dispositivo, caminho_final_pasta)

    return caminho_final_pasta
