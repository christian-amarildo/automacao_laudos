# import re

# def processar_texto(texto):
#     # Definindo padrões para extração de informações
#     requisicao_pattern = r"REQUIZAO DE PERÍCIA Nº\s*(\d{5}-\d{4}-\d{6})"  
#     inquerito_pattern = r"INQUÉRITO POR PORTARIA Nº\s*(\d{5}/\d{4}\.\d{6}-\d{1})"  
#     data_pattern = r"datada de\s*(\d{2}/\d{2}/\d{4})"  
#     autoridade_pattern = r"assinado pela autoridade\s*([A-Z\s]+),"  
#     lacre_pattern = r"Lacre nº\s*([Y\d]+)"  

#     # Extraindo informações usando regex
#     requisicao = re.search(requisicao_pattern, texto, re.IGNORECASE)
#     inquerito = re.search(inquerito_pattern, texto, re.IGNORECASE)
#     data = re.search(data_pattern, texto, re.IGNORECASE)
#     autoridade = re.search(autoridade_pattern, texto, re.IGNORECASE)
#     lacre = re.search(lacre_pattern, texto, re.IGNORECASE)

#     return {
#         "requisicao": requisicao.group(1) if requisicao else "Não encontrado",
#         "inquerito": inquerito.group(1) if inquerito else "Não encontrado",
#         "data": data.group(1) if data else "Não encontrado",
#         "autoridade": autoridade.group(1).strip() if autoridade else "Não encontrado",
#         "lacre": lacre.group(1) if lacre else "Não encontrado"
#     }
