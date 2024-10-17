import tkinter as tk
from tkinter import filedialog, messagebox
from funcoes_requisicao import transcrever_imagem, processar_texto
from clonar_pasta_modelo import clonar_e_renomear_pasta, renomear_imagens

def abrir_imagem():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagem", "*.jpg;*.jpeg;*.png")])
    if caminho_imagem:
        caminho_imagem_label.config(text=caminho_imagem)
    return caminho_imagem

def processar_arquivo():
    try:
        caminho_imagem = abrir_imagem()
        texto_transcrito = transcrever_imagem(caminho_imagem)
        informacoes_requisicao = processar_texto(texto_transcrito)

        # Atualiza os campos da interface com as informações extraídas
        for chave, valor in informacoes_requisicao.items():
            output_text.insert(tk.END, f"{chave}: {valor}\n")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar a imagem: {e}")

def clonar_pasta():
    caminho_pasta_original = filedialog.askdirectory()
    inquerito = informacoes_requisicao.get('inquerito')
    try:
        if inquerito:
            novo_caminho = clonar_e_renomear_pasta(caminho_pasta_original, inquerito)
            messagebox.showinfo("Sucesso", f"Pasta clonada em {novo_caminho}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao clonar pasta: {e}")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Automação de Laudos")
root.geometry("600x400")

# Botão para abrir imagem
btn_abrir_imagem = tk.Button(root, text="Abrir Imagem", command=processar_arquivo)
btn_abrir_imagem.pack(pady=10)

# Label para mostrar caminho da imagem
caminho_imagem_label = tk.Label(root, text="Nenhuma imagem selecionada")
caminho_imagem_label.pack()

# Texto de saída para informações extraídas
output_text = tk.Text(root, height=10)
output_text.pack(pady=10)

# Botão para clonar pasta
btn_clonar_pasta = tk.Button(root, text="Clonar Pasta", command=clonar_pasta)
btn_clonar_pasta.pack(pady=10)

root.mainloop()
