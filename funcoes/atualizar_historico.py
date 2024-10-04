# from docx import Document

# def atualizar_historico(caminho_modelo, caminho_saida, informacoes):
#     # Abrir o documento modelo
#     doc = Document(caminho_modelo)

#     # Modificar partes específicas do documento
#     for par in doc.paragraphs:
#         par.text = par.text.replace("REQUISTAO_NUMERO", informacoes['requisicao'])
#         par.text = par.text.replace("DATA_REQUISICAO", informacoes['data'])
#         par.text = par.text.replace("INQUERITO_NUMERO", informacoes['inquerito'])
#         par.text = par.text.replace("AUTORIDADE", informacoes['autoridade'])
#         par.text = par.text.replace("LACRE_NUMERO", informacoes['lacre'])
#         par.text = par.text.replace("SACO_NUMERO", informacoes['saco'])
#         par.text = par.text.replace("ILUSTRACAO_1_2", informacoes['ilustracoes_1_2'])
#         par.text = par.text.replace("ILUSTRACAO_3", informacoes['ilustracao_3'])
#         par.text = par.text.replace("ILUSTRACAO_7", informacoes['ilustracao_7'])

#     # Salvar o documento modificado
#     doc.save(caminho_saida)

# # Exemplo de uso
# informacoes = {
#     "requisicao": "00001-2024-111744-2",
#     "data": "27/08/2024",
#     "inquerito": "00615/2023.100032-2",
#     "autoridade": "TOBIAS FERREIRA RODRIGUES",
#     "lacre": "Y220061313",
#     "saco": "A220001192",
#     "ilustracoes_1_2": "ver Ilustração 01 e 02",
#     "ilustracao_3": "ver Ilustração 03",
#     "ilustracao_7": "Ilustração 07"
# }

# atualizar_historico('modelo_laudo.docx', 'laudos/laudo_pericial.docx', informacoes)
