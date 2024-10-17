import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog  # Importa o módulo correto para askstring
from funcoes_requisicao import transcrever_imagem, processar_texto
from clonar_pasta_modelo import clonar_e_renomear_pasta, renomear_imagens

class AutomacaoLaudosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação de Laudos")
        self.root.geometry("600x400")

        # Variáveis para armazenar os caminhos
        self.caminho_imagem = ""
        self.caminho_pasta = ""
        self.informacoes_requisicao = {}

        # Botão para abrir imagem
        self.btn_abrir_imagem = tk.Button(root, text="Abrir Imagem", command=self.abrir_imagem)
        self.btn_abrir_imagem.pack(pady=10)

        # Label para mostrar caminho da imagem
        self.caminho_imagem_label = tk.Label(root, text="Nenhuma imagem selecionada")
        self.caminho_imagem_label.pack()

        # Botão para processar imagem
        self.btn_processar_imagem = tk.Button(root, text="Processar Imagem", command=self.processar_arquivo)
        self.btn_processar_imagem.pack(pady=10)

        # Texto de saída para informações extraídas
        self.output_text = tk.Text(root, height=10)
        self.output_text.pack(pady=10)

        # Botão para selecionar a pasta
        self.btn_selecionar_pasta = tk.Button(root, text="Selecionar Pasta", command=self.selecionar_pasta)
        self.btn_selecionar_pasta.pack(pady=10)

        # Botão para clonar pasta
        self.btn_clonar_pasta = tk.Button(root, text="Clonar Pasta", command=self.clonar_pasta)
        self.btn_clonar_pasta.pack(pady=10)

    def abrir_imagem(self):
        self.caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagem", "*.jpg;*.jpeg;*.png")])
        if self.caminho_imagem:
            self.caminho_imagem_label.config(text=self.caminho_imagem)
        return self.caminho_imagem

    def processar_arquivo(self):
        if not self.caminho_imagem:
            messagebox.showerror("Erro", "Nenhuma imagem foi selecionada.")
            return
        
        try:
            # Transcrever o texto da imagem
            texto_transcrito = transcrever_imagem(self.caminho_imagem)

            # Processar o texto e extrair as informações da requisição
            self.informacoes_requisicao = processar_texto(texto_transcrito)

            # Exibir as informações extraídas
            self.output_text.delete(1.0, tk.END)
            for chave, valor in self.informacoes_requisicao.items():
                self.output_text.insert(tk.END, f"{chave}: {valor}\n")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar a imagem: {e}")

    def selecionar_pasta(self):
        self.caminho_pasta = filedialog.askdirectory()
        if self.caminho_pasta:
            messagebox.showinfo("Pasta Selecionada", f"Pasta selecionada: {self.caminho_pasta}")

    def clonar_pasta(self):
        if not self.caminho_pasta:
            messagebox.showerror("Erro", "Nenhuma pasta foi selecionada.")
            return
        
        if 'inquerito' not in self.informacoes_requisicao:
            messagebox.showerror("Erro", "Informações da requisição não processadas. Processar a imagem primeiro.")
            return

        try:
            inquerito = self.informacoes_requisicao['inquerito']
            novo_caminho = clonar_e_renomear_pasta(self.caminho_pasta, inquerito)

            # Perguntar ao usuário qual é a marca do celular
            marca_celular = simpledialog.askstring("Marca do Celular", "Insira a marca do celular:")  # Usar simpledialog

            # Renomear as imagens na nova pasta clonada
            if marca_celular:
                renomear_imagens(marca_celular, novo_caminho)

            messagebox.showinfo("Sucesso", f"Pasta clonada e imagens renomeadas em: {novo_caminho}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao clonar pasta: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomacaoLaudosGUI(root)
    root.mainloop()
