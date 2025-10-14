import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from funcoes_requisicao import transcrever_imagem, processar_texto
from clonar_pasta_modelo import clonar_e_renomear_pasta, renomear_imagens
import os
import re
import shutil

class AutomacaoLaudosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação de Laudos v3")
        self.root.geometry("700x600")

        # Variáveis para armazenar os caminhos e informações
        self.caminho_imagem = ".\\BOP 000000000.000000-0 Celular crimes contra\\Figura 00 - Requisição.jpg"
        self.caminho_pasta = ""
        self.caminho_pasta_destino = ""  # Variável para armazenar o caminho da pasta de destino
        self.informacoes_requisicao = {}
        self.marca_celular = ""
        
        # --- Novos widgets para campos editáveis ---
        self.info_frame = None
        self.info_entries = {}
        # -----------------------------------------

        # Carregar última pasta utilizada (se existir)
        self.carregar_ultima_pasta()

        # Frame principal para botões
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        # Botão para mudar imagem
        self.btn_mudar_imagem = tk.Button(top_frame, text="Mudar Imagem da Requisição", command=self.mudar_imagem)
        self.btn_mudar_imagem.pack(side=tk.LEFT, padx=5)

        # Botão para processar imagem
        self.btn_processar_imagem = tk.Button(top_frame, text="Processar Imagem", command=self.processar_arquivo)
        self.btn_processar_imagem.pack(side=tk.LEFT, padx=5)

        # Label para mostrar caminho da imagem
        self.caminho_imagem_label = tk.Label(root, text=self.caminho_imagem, wraplength=680)
        self.caminho_imagem_label.pack()

        # --- O antigo output_text foi removido ---

        # Frame inferior para os botões de ação
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(pady=20, side=tk.BOTTOM)

        # Botão para pedir a marca do celular
        self.btn_pedir_marca = tk.Button(bottom_frame, text="Insira a Marca do Celular", command=self.pedir_marca_celular)
        self.btn_pedir_marca.pack(side=tk.LEFT, padx=5)

        # Botão para selecionar a pasta de origem
        self.btn_selecionar_pasta = tk.Button(bottom_frame, text="Selecionar Pasta de Origem", command=self.selecionar_pasta)
        self.btn_selecionar_pasta.pack(side=tk.LEFT, padx=5)

        # Botão para clonar pasta
        self.btn_clonar_pasta = tk.Button(bottom_frame, text="Clonar Pasta", command=self.clonar_pasta)
        self.btn_clonar_pasta.pack(side=tk.LEFT, padx=5)

    def mudar_imagem(self):
        try:
            novo_caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagem", "*.jpg;*.jpeg;*.png")])
            if novo_caminho_imagem:
                self.caminho_imagem = novo_caminho_imagem
                self.caminho_imagem_label.config(text=self.caminho_imagem)
                messagebox.showinfo("Imagem Atualizada", "A imagem foi atualizada com sucesso.")
            else:
                messagebox.showwarning("Aviso", "Nenhuma imagem foi selecionada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mudar a imagem: {e}")

    def processar_arquivo(self):
        if not self.caminho_imagem:
            messagebox.showerror("Erro", "Nenhuma imagem foi selecionada.")
            return
        
        try:
            # Transcrever o texto da imagem
            texto_transcrito = transcrever_imagem(self.caminho_imagem)

            # Processar o texto e extrair as informações da requisição
            self.informacoes_requisicao = processar_texto(texto_transcrito)

            # Exibir as informações em campos editáveis
            self.display_editable_info()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar a imagem: {e}")

    def display_editable_info(self):
        # Destruir o frame antigo se ele existir
        if self.info_frame:
            self.info_frame.destroy()

        self.info_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.info_frame.pack(pady=10, padx=10, fill=tk.X)

        self.info_entries = {}
        
        # Adiciona um título
        title_label = tk.Label(self.info_frame, text="Informações Extraídas (edite se necessário)", font=("Helvetica", 10, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=5)

        # Cria um label e um entry para cada item
        row_num = 1
        for chave, valor in self.informacoes_requisicao.items():
            label = tk.Label(self.info_frame, text=f"{chave}:", anchor="w")
            label.grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
            
            entry = tk.Entry(self.info_frame, width=60)
            entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
            entry.insert(0, valor if valor else "")
            
            self.info_entries[chave] = entry
            row_num += 1
        
        # Botão para salvar as correções
        save_button = tk.Button(self.info_frame, text="Salvar Correções", command=self.save_corrections)
        save_button.grid(row=row_num, column=0, columnspan=2, pady=10)

    def save_corrections(self):
        if not self.info_entries:
            messagebox.showwarning("Aviso", "Nenhuma informação para salvar. Processe uma imagem primeiro.")
            return

        try:
            # Atualiza o dicionário com os valores dos campos de entrada
            for chave, entry_widget in self.info_entries.items():
                self.informacoes_requisicao[chave] = entry_widget.get()
            
            messagebox.showinfo("Sucesso", "Informações corrigidas foram salvas com sucesso!\nAgora você pode prosseguir para clonar a pasta.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar as informações: {e}")

    def selecionar_pasta(self):
        try:
            # Permitir ao usuário selecionar uma nova pasta de origem
            self.caminho_pasta = filedialog.askdirectory(initialdir=self.caminho_pasta_destino or os.getcwd())
            if self.caminho_pasta:
                self.salvar_ultima_pasta(self.caminho_pasta)
                messagebox.showinfo("Pasta Selecionada", f"Pasta de origem selecionada: {self.caminho_pasta}")
            else:
                messagebox.showwarning("Aviso", "Nenhuma pasta foi selecionada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar a pasta: {e}")

    def clonar_pasta(self):
        if not self.caminho_pasta:
            messagebox.showerror("Erro", "Nenhuma pasta foi selecionada.")
            return

        # Verifica se as informações da requisição foram processadas
        if not self.informacoes_requisicao or 'inquerito' not in self.informacoes_requisicao:
            messagebox.showerror("Erro", "Informações do inquérito não encontradas. Verifique a legibilidade da imagem.")
            return

        # Solicitar ao usuário o caminho de destino para a pasta clonada
        caminho_pasta_destino = filedialog.askdirectory(title="Selecione o diretório de destino para a pasta clonada")
        if not caminho_pasta_destino:
            messagebox.showerror("Erro", "Nenhum diretório de destino foi selecionado.")
            return

        try:
            inquerito = self.informacoes_requisicao['inquerito']
            tipo_crime = self.informacoes_requisicao.get('tipo_crime', '').strip()
            
            # Ajuste o nome do inquérito para evitar caracteres inválidos
            inquerito_numero = re.sub(r'[<>:"/\\|?*]', '.', inquerito)

            # Formatar o novo nome da pasta
            novo_nome = f"BOP {inquerito_numero} Celular {self.marca_celular} crimes contra {tipo_crime}"
            novo_caminho = os.path.join(caminho_pasta_destino, novo_nome)

            # Verificar se a pasta original existe
            if not os.path.exists(self.caminho_pasta):
                raise FileNotFoundError(f"Pasta original não encontrada: {self.caminho_pasta}")

            # Verificar se a nova pasta já existe para evitar sobrescrita
            if os.path.exists(novo_caminho):
                raise FileExistsError(f"A pasta já existe: {novo_caminho}")

            # Clonar a pasta original para a nova pasta
            shutil.copytree(self.caminho_pasta, novo_caminho)

            # Renomear as imagens na nova pasta clonada
            renomear_imagens(self.marca_celular, novo_caminho)

            messagebox.showinfo("Sucesso", f"Pasta clonada e imagens renomeadas em: {novo_caminho}")
        except FileNotFoundError as e:
            messagebox.showerror("Erro", f"Pasta original não encontrada: {e}")
        except FileExistsError as e:
            messagebox.showerror("Erro", f"A pasta já existe: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao clonar e renomear a pasta: {e}")

    def pedir_marca_celular(self):
        try:
            self.marca_celular = simpledialog.askstring("Marca do Celular", "Insira a marca do celular:")
            if not self.marca_celular:
                messagebox.showwarning("Aviso", "Marca do celular não foi fornecida. Você poderá inserir novamente ao clonar a pasta.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao solicitar a marca do celular: {e}")

    def salvar_ultima_pasta(self, caminho):
        try:
            with open("ultima_pasta.txt", "w") as file:
                file.write(caminho)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar a última pasta: {e}")

    def carregar_ultima_pasta(self):
        try:
            if os.path.exists("ultima_pasta.txt"):
                with open("ultima_pasta.txt", "r") as file:
                    self.caminho_pasta_destino = file.read()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar a última pasta: {e}")

