import re

def processar_texto(texto):
    # Exemplo de como você pode definir padrões para extrair informações
    nome_pattern = r"Nome:\s*(.*)"
    data_pattern = r"Data:\s*(\d{2}/\d{2}/\d{4})"  # Exemplo para formato de data DD/MM/AAAA
    protocolo_pattern = r"Protocolo:\s*(\d+)"
    
    nome = re.search(nome_pattern, texto)
    data = re.search(data_pattern, texto)
    protocolo = re.search(protocolo_pattern, texto)
    
    return {
        "nome": nome.group(1) if nome else "Não encontrado",
        "data": data.group(1) if data else "Não encontrado",
        "protocolo": protocolo.group(1) if protocolo else "Não encontrado"
    }

# Testando a função com um texto de exemplo
texto_extraido = """Nome: João da Silva
Data: 01/01/2024
Protocolo: 123456789
Este é um laudo pericial..."""

informacoes = processar_texto(texto_extraido)
print(informacoes)
