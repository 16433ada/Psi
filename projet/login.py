from tkinter.messagebox import *
def logar(self,user,passw,UserWindow,AdminWindow):
    user = self.user.get().strip()
    passw = self.passw.get().strip()

    if not user or not passw:
        showerror("Erro", "Por favor, preencha todos os campos!")
        return

    # /media/teixeira/Teixeira/Escola/PSI/11º/Casa/login-casa/
    with open("clientes.csv",
              "r", encoding="utf-8-sig") as fp:

        login_sucesso = False
        dados = fp.read().split("\n")
        for linha in dados:
            info = linha.split(";")
            if info[1] == user and info[1] == passw :
                login_sucesso = True
                showinfo("Login Efetuado", f"Bem-vindo {user}!")
                self.jan.withdraw()

                if user=="admin" and passw=="admin":
                    AdminWindow(self.jan, user, passw)
                else:
                    UserWindow(self.jan, user, passw)

        if not login_sucesso:
            showerror("Erro", "User ou passe incorretos.")

