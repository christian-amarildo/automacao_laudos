from docx import Document
from funcoes_requisicao import processar_texto  # Importa a função de processamento

# Caminho do documento
caminho_documento = 'C:/Users/Harpia/Documents/vscode/projetos/automacao laudos/BOP 000000000.000000-0 Celular crimes contra/Laudo prot - Celular extração e análise.docx'

# Carregar o documento existente
doc = Document(caminho_documento)

# Texto simulado extraído para o exemplo
texto_extraido = """
Atendimento a Nº 00001-2024-100059-1, datada de 02/10/2024, referente ao INQUERITO POR PORTARIA Nº 00001/2024.113864-9 
DIVISÃO DE COMBATE A CRIMES CONTRA DIREITOS INDIVIDUAIS POR MEIOS CIBERNÉTICOS, e assinado pela autoridade X.
"""

# Processar o texto para extrair as informações
informacoes = processar_texto(texto_extraido)

# Iterar sobre os parágrafos e substituir o texto no parágrafo específico
for paragraph in doc.paragraphs:
    if paragraph.text.startswith("1- HISTÓRICO:"):
        # Limpando o parágrafo existente
        paragraph.clear()

        # Criando o novo conteúdo com negrito para partes específicas
        run = paragraph.add_run("1- HISTÓRICO:\n")
        run.bold = True  # Negrito para o título

        run = paragraph.add_run(f"Em virtude ao atendimento a REQUISIÇÃO DE PERÍCIA Nº {informacoes['requisicao']}, datada de {informacoes['data']}, ")
        run = paragraph.add_run("referente ao ")
        
        # Negrito para o inquérito por portaria
        run = paragraph.add_run(f"INQUÉRITO POR PORTARIA Nº {informacoes['inquerito']}– DIVISÃO DE COMBATE A CRIMES CONTRA DIREITOS INDIVIDUAIS POR MEIOS CIBERNÉTICOS")
        run.bold = True

        run = paragraph.add_run(", e assinado pela autoridade acima mencionada, solicitando Perícia em aparelho celular a fim de extração de dados ")
        run = paragraph.add_run("(registro de chamadas, contatos, fotos, imagens, áudios, vídeos, conversas de aplicativos e de mensagens de texto) ")
        run.bold = True

        run = paragraph.add_run("e análise de conteúdo")
        run.bold = True
        
        run = paragraph.add_run(", a fim de colaborar com as investigações. O aparelho de telefonia celular foi recebido pelo perito signatário para exame pericial onde se constatou que o aparelho ")
        run = paragraph.add_run("encontrava-se lacrado ")
        run.bold = True
        
        run = paragraph.add_run(f"(Lacre nº {informacoes['lacre']}) ")
        run.bold = True
        
        run = paragraph.add_run("no saco de evidências (Saco nº A231650563) (ver Ilustração 01 e 02), em seguida foi deslacrado pelo Perito (ver Ilustração 03). Após ligar o aparelho, o Perito observou que o aparelho de telefonia celular estava em ")
        run = paragraph.add_run("modo avião")
        run.bold = True
        
        run = paragraph.add_run(", conforme “Ilustração 07”.")
        break

# Salvar o documento modificado
doc.save('C:/Users/Harpia/Documents/vscode/projetos/automacao laudos/BOP 000000000.000000-0 Celular crimes contra/novo_documento.docx')
