from pathlib import Path

def gerar_laudo_markdown(informacoes: dict, caminho_arquivo_saida: Path, caminho_template: Path):
    """
    Gera um laudo em Markdown a partir de um template e um dicionário de informações.

    Args:
        informacoes (dict): Dicionário com os dados para preencher o laudo.
        caminho_arquivo_saida (Path): O caminho completo onde o laudo final será salvo.
        caminho_template (Path): O caminho para o arquivo de modelo .md.
    """
    try:
        # Lê o conteúdo do template
        template_content = caminho_template.read_text(encoding='utf-8')

        # Itera sobre as informações e substitui os placeholders no texto
        laudo_content = template_content
        for chave, valor in informacoes.items():
            placeholder = f"{{{{{chave}}}}}"
            valor_a_inserir = valor if valor is not None else ""
            laudo_content = laudo_content.replace(placeholder, valor_a_inserir)

        # Salva o novo arquivo de laudo no caminho especificado
        caminho_arquivo_saida.write_text(laudo_content, encoding='utf-8')
        
        return caminho_arquivo_saida

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de template não encontrado em {caminho_template}")
    except Exception as e:
        raise Exception(f"Erro ao gerar o laudo em Markdown: {e}")
