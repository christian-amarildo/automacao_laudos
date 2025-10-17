import os
import shutil
import re

def _sanitizar_nome(nome):
    """Remove caracteres inválidos para nomes de arquivo/pasta."""
    return re.sub(r'[<>:"/\\|?*]', '-', nome)

def _renomear_arquivos_e_pastas(caminho_raiz, modelo_dispositivo):
    """Renomeia recursivamente arquivos e pastas que contêm 'dispositivoo'."""
    if not modelo_dispositivo:
        print("Aviso: Modelo do dispositivo não fornecido, pulando renomeação.")
        return

    # Renomeia de baixo para cima para evitar problemas com caminhos que mudam
    for raiz, dirs, files in os.walk(caminho_raiz, topdown=False):
        # Renomeia arquivos
        for nome_arquivo in files:
            if 'dispositivoo' in nome_arquivo.lower():
                novo_nome_arquivo = re.sub('dispositivoo', modelo_dispositivo, nome_arquivo, flags=re.IGNORECASE)
                caminho_antigo = os.path.join(raiz, nome_arquivo)
                caminho_novo = os.path.join(raiz, novo_nome_arquivo)
                os.rename(caminho_antigo, caminho_novo)
                print(f"Arquivo renomeado: {nome_arquivo} -> {novo_nome_arquivo}")

        # Renomeia diretórios
        for nome_dir in dirs:
            if 'dispositivoo' in nome_dir.lower():
                novo_nome_dir = re.sub('dispositivoo', modelo_dispositivo, nome_dir, flags=re.IGNORECASE)
                caminho_antigo = os.path.join(raiz, nome_dir)
                caminho_novo = os.path.join(raiz, novo_nome_dir)
                os.rename(caminho_antigo, caminho_novo)
                print(f"Diretório renomeado: {nome_dir} -> {novo_nome_dir}")


def executar_clonagem_completa(caminho_origem, caminho_destino_base, info_requisicao, modelo_dispositivo):
    """
    Executa o processo completo de clonagem, incluindo nomeação, cópia e renomeação.
    """
    # 1. Validar entradas
    if not caminho_origem or not os.path.exists(caminho_origem):
        raise FileNotFoundError(f"A pasta de origem selecionada não existe: {caminho_origem}")
    if not caminho_destino_base:
        raise ValueError("Nenhum diretório de destino foi selecionado.")

    # 2. Montar o nome da nova pasta usando os campos solicitados e sanitizando-os
    bop = info_requisicao.get('inquerito', 'BOP_NA') # Usando 'inquerito' como BOP, conforme extração
    protocolo = info_requisicao.get('protocolo', 'Protocolo_NA')
    tipo_crime = info_requisicao.get('tipo_crime', 'N_A')
    
    # Sanitiza cada parte do nome para remover caracteres inválidos
    bop_sanitizado = _sanitizar_nome(bop)
    protocolo_sanitizado = _sanitizar_nome(protocolo)
    modelo_dispositivo_sanitizado = _sanitizar_nome(modelo_dispositivo)
    tipo_crime_sanitizado = _sanitizar_nome(tipo_crime)

    novo_nome_pasta = f"BOP {bop_sanitizado} - {protocolo_sanitizado} - {modelo_dispositivo_sanitizado} crimes contra {tipo_crime_sanitizado}"
    caminho_final_pasta = os.path.join(caminho_destino_base, novo_nome_pasta)

    if os.path.exists(caminho_final_pasta):
        raise FileExistsError(f"A pasta de destino já existe: {caminho_final_pasta}")

    # 3. Copiar a árvore de diretórios
    shutil.copytree(caminho_origem, caminho_final_pasta)
    print(f"Pasta clonada para: {caminho_final_pasta}")

    # 4. Renomear os arquivos e pastas na nova estrutura
    _renomear_arquivos_e_pastas(caminho_final_pasta, modelo_dispositivo)

    return caminho_final_pasta
