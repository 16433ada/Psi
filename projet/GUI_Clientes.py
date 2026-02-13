##########################Instruções#######################################
"""
Ler o csv do moodle
o csv está dividido por 'Nome Empresa;Morada;Localidade;Região'
"""
from tkinter import *
from tkinter import simpledialog
from biblio import *
from tkinter import ttk

class UserWindow():
    def __init__(self, empresa_logada):
        self.empresa = empresa_logada
        self.usr = Toplevel()
        self.usr.title(f"User - {self.empresa}")
        centrar(self.usr, 600, 600)

        self.dados_empresa = ler_csv(filtro_empresa=self.empresa)

        # MENUBAR
        self.menubar = Menu(self.usr)
        self.usr.config(menu=self.menubar)

        # MENU FICHEIRO
        self.ficheiro = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ficheiro", menu=self.ficheiro)
        self.ficheiro.add_command(label="Exportar CSV",
                                  command=lambda: export_empresa(self.dados_empresa, self.empresa))
        self.ficheiro.add_separator()
        self.ficheiro.add_command(label="Sair", command=self.usr.destroy)

        # MENU EMPRESA
        self.empresa_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Empresa", menu=self.empresa_menu)
        self.empresa_menu.add_command(label="Alterar Informações", command=self.altera_empresa)

        # MENU SOBRE
        self.sobre = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Sobre", menu=self.sobre)
        self.sobre.add_command(label="Ajuda", command=self.ajuda)

        # FRAME PRINCIPAL

        self.usr.grid_rowconfigure(0, weight=1)
        self.usr.grid_columnconfigure(0, weight=1)

        self.f1 = Frame(self.usr, bg="white", padx=125, pady=125)
        self.f1.grid(row=0, column=0)

        self.f1.grid_columnconfigure(0, weight=1)

        self.f1.grid_columnconfigure(0, weight=1)
        self.f1.grid_rowconfigure(0, weight=1)

        Label(self.f1, text="INFOS", bg="white", font=("Arial", 25)).grid(row=0, column=0, columnspan=2,
                                                                               sticky="EW", pady=(0,20))

        self.labels = {}
        dados = list(self.dados_empresa.values())[0]

        self.labels["nome"] = Label(self.f1, text=f"Nome: {dados['nome']}", bg="white", font=("Arial",13))
        self.labels["nome"].grid(row=1, column=0, sticky="W", pady=2)

        self.labels["morada"] = Label(self.f1, text=f"Morada: {dados['morada']}", bg="white", font=("Arial",13))
        self.labels["morada"].grid(row=2, column=0, sticky="W", pady=2)

        self.labels["localidade"] = Label(self.f1, text=f"Localidade: {dados['localidade']}", bg="white", font=("Arial",13))
        self.labels["localidade"].grid(row=3, column=0, sticky="W", pady=2)

        self.labels["regiao"] = Label(self.f1, text=f"Região: {dados['regiao']}", bg="white", font=("Arial",13))
        self.labels["regiao"].grid(row=4, column=0, sticky="W", pady=2)

    def altera_empresa(self):
        resposta = messagebox.askyesno(
            "Alterar Informações",
            "Deseja alterar alguma informação da empresa?",
            parent=self.usr
        )

        if not resposta:
            return

        dados = list(self.dados_empresa.values())[0]
        id_emp = list(self.dados_empresa.keys())[0]

        nome_original = dados["nome"]

        valores = (
            f"Valores atuais:\n\n"
            f"Nome: {dados['nome']}\n"
            f"Morada: {dados['morada']}\n"
            f"Localidade: {dados['localidade']}\n"
            f"Região: {dados['regiao']}\n\n"
            f"O que deseja alterar?\n"
            f"Opções: nome, morada, localidade, regiao"
        )

        campo = simpledialog.askstring(
            "Alterar Informação",
            valores,
            parent=self.usr
        )

        if campo is None:
            return

        campo = campo.lower().strip()
        if campo not in ["nome", "morada", "localidade", "regiao"]:
            messagebox.showerror(
                "Erro",
                "Campo inválido! Escolha: nome, morada, localidade ou regiao",
                parent=self.usr
            )
            return

        valor_atual = dados[campo]
        novo_valor = simpledialog.askstring(
            "Alterar Informação",
            f"Valor atual: {valor_atual}\n\nNovo valor para {campo}:",
            parent=self.usr
        )

        if not novo_valor:
            messagebox.showinfo(
                "Info",
                "Operação cancelada ou valor vazio.",
                parent=self.usr
            )
            return

        self.dados_empresa[id_emp][campo] = novo_valor

        # Atualiza o CSV
        linhas = []
        with open("clientes.csv", "r", encoding="utf-8-sig") as fp:
            for linha in fp:
                linha = linha.strip()
                if not linha:
                    continue

                partes = [p.strip() for p in linha.split(";")]

                if partes[1] == nome_original:
                    if campo == "nome":
                        partes[1] = novo_valor
                    elif campo == "morada":
                        partes[2] = novo_valor
                    elif campo == "localidade":
                        partes[3] = novo_valor
                    elif campo == "regiao":
                        partes[4] = novo_valor

                linhas.append(";".join(partes))

        with open("clientes.csv", "w", encoding="utf-8-sig") as fp:
            fp.write("\n".join(linhas) + "\n")

        self.atualizar_labels()

        messagebox.showinfo(
            "Sucesso",
            f"{campo.capitalize()} atualizado para:\n{novo_valor}",
            parent=self.usr
        )

    def atualizar_labels(self):
        id_emp = list(self.dados_empresa.keys())[0]
        dados = self.dados_empresa[id_emp]

        self.labels["nome"].config(text=f"Nome: {dados['nome']}")
        self.labels["morada"].config(text=f"Morada: {dados['morada']}")
        self.labels["localidade"].config(text=f"Localidade: {dados['localidade']}")
        self.labels["regiao"].config(text=f"Região: {dados['regiao']}")

    def ajuda(self):
        messagebox.showinfo(
            "Sobre",
            "Gestão de Clientes v.20/20\n"
            "© 2026 - Teixeira & Edgar\n"
            "Aplicação para gestão de empresas e clientes."
        )
class AdminWindow():
    def __init__(self):
        self.adm = Toplevel()
        self.adm.title("Admin")
        centrar(self.adm, 700, 500)

        self.dados_empresas = ler_csv()

        # MENUBAR
        self.menubar = Menu(self.adm)
        self.adm.config(menu=self.menubar)

        # MENU FICHEIROS
        self.ficheiro = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ficheiro", menu=self.ficheiro)
        self.ficheiro.add_command(label="Exportar CSV",
                                  command=lambda: export_empresa(self.dados_empresas, self.empresas))
        self.ficheiro.add_separator()
        self.ficheiro.add_command(label="Sair", command=self.adm.destroy)

        # MENU ADMIN
        self.admin_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Admin", menu=self.admin_menu)
        self.admin_menu.add_command(label="Empresas", command=self.mostrar_empresas)
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Adicionar Empresa", command=self.adicionar_empresa)
        self.admin_menu.add_command(label="Remover Empresa", command=self.remover_empresa)
        self.admin_menu.add_command(label="Editar Empresa", command=self.editar_empresa)

        # MENU ESTATISTICAS

        self.estatisticas_menu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Estatisticas", menu=self.estatisticas_menu)
        self.estatisticas_menu.add_command(label="Resumo Geral", command=self.estatisticas_resumo)
        self.estatisticas_menu.add_command(label="Por Região", command=self.estatisticas_regiao)


        # MENU SOBRE
        self.sobre = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Sobre", menu=self.sobre)
        self.sobre.add_command(label="Ajuda", command=self.ajuda)

    def ajuda(self):
        messagebox.showinfo(
            "Sobre",
            "Gestão de Clientes v.20/20\n"
            "© 2026 - Teixeira & Edgar\n"
            "Aplicação para gestão de empresas e clientes."
        )

    def mostrar_empresas(self):

            if hasattr(self, "infos"):
                self.infos.destroy()

            self.infos = Frame(self.adm)
            self.infos.pack(fill="both", expand=True, padx=20, pady=20)

            Label(self.infos, text="Empresas:",
                  font=("Arial", 16, "bold")).pack(pady=10)

            colunas = ("Id", "Nome", "Morada", "Localidade")

            self.tree = ttk.Treeview(self.infos, columns=colunas, show="headings")

            self.tree.heading("Id", text="ID")
            self.tree.column("Id", width=80, anchor="center")

            self.tree.heading("Nome", text="Nome")
            self.tree.column("Nome", width=180, anchor="center")

            self.tree.heading("Morada", text="Morada")
            self.tree.column("Morada", width=250, anchor="center")

            self.tree.heading("Localidade", text="Localidade")
            self.tree.column("Localidade", width=150, anchor="center")

            self.tree.pack(fill="both", expand=True)

            # Atualiza dados do CSV
            self.dados_empresas = ler_csv()

            for id_empresa, dados in self.dados_empresas.items():
                self.tree.insert("", "end",
                                 values=(id_empresa,
                                         dados["nome"],
                                         dados["morada"],
                                         dados["localidade"]))

    def adicionar_empresa(self):

        janela = Toplevel(self.adm)
        janela.title("Adicionar Empresa")
        centrar(janela, 400, 400)

        frame = Frame(janela, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Nova Empresa",
              font=("Arial", 16, "bold")).pack(pady=10)

        Label(frame, text="Nome").pack(anchor="w")
        entry_nome = Entry(frame)
        entry_nome.pack(fill="x", pady=5)

        Label(frame, text="Morada").pack(anchor="w")
        entry_morada = Entry(frame)
        entry_morada.pack(fill="x", pady=5)

        Label(frame, text="Localidade").pack(anchor="w")
        entry_localidade = Entry(frame)
        entry_localidade.pack(fill="x", pady=5)

        Label(frame, text="Região").pack(anchor="w")

        entry_regiao = ttk.Combobox(frame, state="readonly")
        entry_regiao["values"] = ("Norte", "Sul", "Centro")
        entry_regiao.pack(fill="x", pady=5)
        entry_regiao.current(0)


        def guardar():
            nome = entry_nome.get().strip()
            morada = entry_morada.get().strip()
            localidade = entry_localidade.get().strip()
            regiao = entry_regiao.get().strip()

            if not nome or not morada or not localidade or not regiao:
                messagebox.showerror("Erro", "Preencha todos os campos!", parent=janela)
                return

            self.dados_empresas = ler_csv()

            if self.dados_empresas:
                novo_id = max(map(int, self.dados_empresas.keys())) + 1
            else:
                novo_id = 1

            with open("clientes.csv", "a", encoding="utf-8-sig") as f:
                f.write(f"\n{novo_id};{nome};{morada};{localidade};{regiao}")

            messagebox.showinfo("Sucesso", "Empresa adicionada com sucesso!", parent=janela)

            janela.destroy()

            if hasattr(self, "tree"):
                self.mostrar_empresas()


        Button(frame, text="Guardar", command=guardar).pack(pady=15)

    def remover_empresa(self):

        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma empresa.")
            return

        valores = self.tree.item(selecionado)["values"]
        id_empresa = str(valores[0])

        confirmar = messagebox.askyesno("Confirmar","Tem a certeza que deseja remover esta empresa?")

        linhas = []

        with open("clientes.csv", "r", encoding="utf-8-sig") as f:
            for linha in f:
                partes = linha.strip().split(";")

                if partes[0] != id_empresa:
                    linhas.append(linha.strip())

        with open("clientes.csv", "w", encoding="utf-8-sig") as f:
            for linha in linhas:
                f.write(linha + "\n")

        messagebox.showinfo("Sucesso", "Empresa removida.")

        self.mostrar_empresas()

    def editar_empresa(self):

        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma empresa.")
            return

        valores = self.tree.item(selecionado)["values"]
        id_empresa = str(valores[0])

        self.dados_empresas = ler_csv()
        dados = self.dados_empresas[id_empresa]

        janela = Toplevel(self.adm)
        janela.title(f"Empresa - {dados['nome']}")
        centrar(janela, 700, 400)

        frame_esq = Frame(janela, padx=20, pady=20)
        frame_esq.pack(side="left", fill="both", expand=True)

        Label(frame_esq, text="Informações da Empresa",
              font=("Arial", 14, "bold")).pack(pady=10)

        lbl_nome = Label(frame_esq, text=f"Nome: {dados['nome']}")
        lbl_nome.pack(anchor="w")

        lbl_morada = Label(frame_esq, text=f"Morada: {dados['morada']}")
        lbl_morada.pack(anchor="w")

        lbl_localidade = Label(frame_esq, text=f"Localidade: {dados['localidade']}")
        lbl_localidade.pack(anchor="w")

        lbl_regiao = Label(frame_esq, text=f"Região: {dados['regiao']}")
        lbl_regiao.pack(anchor="w")

        # ---------- FUNÇÕES INTERNAS ----------

        def alterar_info():

            campo = simpledialog.askstring(
                "Alterar",
                "Qual campo deseja alterar?\n(nome, morada, localidade, regiao)",
                parent=janela
            )

            if campo not in ["nome", "morada", "localidade", "regiao"]:
                return

            novo_valor = simpledialog.askstring(
                "Novo Valor",
                f"Novo valor para {campo}:",
                parent=janela
            )

            if not novo_valor:
                return

            linhas = []
            with open("clientes.csv", "r", encoding="utf-8-sig") as f:
                for linha in f:
                    partes = linha.strip().split(";")

                    if partes[0] == id_empresa:
                        if campo == "nome":
                            partes[1] = novo_valor
                        elif campo == "morada":
                            partes[2] = novo_valor
                        elif campo == "localidade":
                            partes[3] = novo_valor
                        elif campo == "regiao":
                            partes[4] = novo_valor

                    linhas.append(";".join(partes))

            with open("clientes.csv", "w", encoding="utf-8-sig") as f:
                for linha in linhas:
                    f.write(linha + "\n")

            messagebox.showinfo("Sucesso", "Informação alterada.")
            self.mostrar_empresas()


        Button(frame_esq, text="Alterar Informações",
               command=alterar_info).pack(pady=5)

        frame_dir = Frame(janela, bg="#f2f2f2", padx=20, pady=20)
        frame_dir.pack(side="right", fill="both", expand=True)

        Label(frame_dir, text="Estatísticas",
              font=("Arial", 14, "bold"), bg="#f2f2f2").pack(pady=10)

        Label(frame_dir,
              text=f"ID da Empresa: {id_empresa}",
              bg="#f2f2f2").pack(anchor="w")

        Label(frame_dir,
              text=f"Região: {dados['regiao']}",
              bg="#f2f2f2").pack(anchor="w")

    def estatisticas_resumo(self):
        self.clientes=ler_csv()
        qt = len(self.clientes)
        Label(self.adm,text=qt).pack()

    def estatisticas_regiao(self):
        self.clientes = ler_csv()

        N, S, C = 0, 0, 0

        for x in self.clientes.values():
            if x["regiao"] == "Norte":
                N += 1
            elif x["regiao"] == "Sul":
                S += 1
            elif x["regiao"] == "Centro":
                C += 1

        total = len(self.clientes)
        N = N * 100 / total
        S = S * 100 / total
        C = C * 100 / total

        Label(self.adm, text=f"Norte: {N:.2f}%").grid(row=0, column=0)
        Label(self.adm, text=f"Sul: {S:.2f}").grid(row=1, column=0)
        Label(self.adm, text=f"Centro: {C:.2f}%").grid(row=2, column=0)



class GUI():
    def __init__(self):
        self.jan = Tk()
        self.jan.title("Login")
        self.jan.geometry(centrar(self.jan, 600, 600))
        self.jan.resizable(0,0)
        self.jan.configure(bg="#f2f2f2")

        self.jan.grid_rowconfigure(0, weight=1)
        self.jan.grid_columnconfigure(0, weight=1)


        f1 = Frame(self.jan, bg="white", padx=100, pady=100)
        f1.grid(row=0, column=0)

        f1.grid_columnconfigure(0, weight=1)

        self.title = Label(f1,text="Iniciar Sessão",bg="white",fg="#555",font=("Arial", 25))
        self.title.grid(row=1, column=0, pady=(0, 25))

        Label(f1, text="Nome Empresa", bg="white", anchor="w").grid(row=2, column=0, sticky="w")

        self.user = (Entry(f1))
        self.user.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        Label(f1, text="Palavra-passe", bg="white", anchor="w").grid(row=4, column=0, sticky="w")

        self.passw = Entry(f1, show="*")
        self.passw.grid(row=5, column=0, sticky="ew", pady=(0, 20))

        self.login = Button(f1, text="Login", bg="white", width="10", font=("", 15)
                            , command=lambda: logar(self, self.user.get(), self.passw.get(), UserWindow, AdminWindow))
        self.login.grid(row=6, column=0, sticky="w", padx=100)
        self.jan.mainloop()
if __name__=="__main__":
    GUI()
