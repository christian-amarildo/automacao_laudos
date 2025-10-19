import sys
import os
import subprocess

def is_gemini_installed():
    """Verifica se o comando 'gemini' está no PATH do sistema (para Windows)."""
    try:
        subprocess.run(['where', 'gemini'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    if len(sys.argv) < 2:
        print("Erro: Caminho da pasta do caso não fornecido.")
        return

    caminho_caso = sys.argv[1]
    if not os.path.isdir(caminho_caso):
        print(f"Erro: Diretório não encontrado: {caminho_caso}")
        return

    cd_command = f'cd /d "{caminho_caso}"'

    if is_gemini_installed():
        final_command = f'start cmd.exe /K "{cd_command} && echo Gemini CLI pronto para uso na pasta do caso. && gemini"'
    else:
        final_command = (
            f'start cmd.exe /K "{cd_command} && ' 
            f'echo. && ' 
            f'echo ----------------------------------------------------------------- && ' 
            f'echo ERRO: O comando \'gemini\' nao foi encontrado em seu sistema. && ' 
            f'echo. && ' 
            f'echo Para usa-lo, o Gemini CLI precisa estar instalado e && ' 
            f'echo configurado corretamente em seu ambiente (PATH). && ' 
            f'echo. && ' 
            f'echo Encontre as instrucoes de instalacao no repositorio oficial: && ' 
            f'echo https://github.com/google-gemini/gemini-cli && ' 
            f'echo ----------------------------------------------------------------- && ' 
            f'echo."'
        )

    try:
        print(f"Iniciando terminal na pasta: {caminho_caso}")
        subprocess.Popen(final_command, shell=True)
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao tentar abrir o terminal: {e}")

if __name__ == "__main__":
    main()
