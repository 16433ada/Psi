from tkinter.messagebox import *
from tkinter import filedialog, messagebox
def centrar(jan, largjan, altjan):

    largura_ecra = jan.winfo_screenwidth()
    altura_ecra = jan.winfo_screenheight()

    pos_x = (largura_ecra // 2) - (largjan // 2)
    pos_y = (altura_ecra // 2) - (altjan // 2)

    jan.geometry(f"{largjan}x{altjan}+{pos_x}+{pos_y}")
def logar(self, user, passw, UserWindow, AdminWindow):

    user = self.user.get().strip()
    passw = self.passw.get().strip()

    if not user or not passw:
        showerror("Erro", "Por favor, preencha todos os campos!")
        return

    if user == "adm" and passw == "adm":
        showinfo("Login Efetuado", f"Bem-vindo {user}!")
        self.jan.withdraw()
        AdminWindow()
        return

    if user != passw:
        showerror("Erro", "User ou passe incorretos.")
        return

    login_sucesso = False

    with open("clientes.csv", "r", encoding="utf-8-sig") as fp:
        for linha in fp:
            info = linha.strip().split(";")
            if info[1] == user:
                login_sucesso = True
                break

    if login_sucesso:
        showinfo("Login Efetuado", f"Bem-vindo {user}!")
        self.jan.withdraw()
        UserWindow(user)
    else:
        showerror("Erro", "User ou passe incorretos.")

def ler_csv(filtro_empresa=None):
    clientes = {}

    with open("clientes.csv", "r", encoding="utf-8-sig") as fp:
        conteudo = fp.read().split("\n")

        for linha in conteudo:
            dados = linha.strip().split(";")
            if len(dados) == 5:
                # Se tiver filtro, só adiciona se for a empresa certa
                if filtro_empresa:
                    if dados[1] == filtro_empresa:
                        clientes[dados[0]] = {
                            "nome": dados[1],
                            "morada": dados[2],
                            "localidade": dados[3],
                            "regiao": dados[4]
                        }
                else:
                    clientes[dados[0]] = {
                        "nome": dados[1],
                        "morada": dados[2],
                        "localidade": dados[3],
                        "regiao": dados[4]
                    }

    return clientes


def export_empresa(dados_empresa, nome_empresa):
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile=f"{nome_empresa}.csv"
    )

    if filepath:
        with open(filepath, "w", encoding="utf-8-sig") as fp:
            for id_emp, dados in dados_empresa.items():
                linha = f"{id_emp};{dados['nome']};{dados['morada']};{dados['localidade']};{dados['regiao']}\n"
                fp.write(linha)
        messagebox.showinfo("Sucesso", f"Ficheiro exportado: {filepath}")

