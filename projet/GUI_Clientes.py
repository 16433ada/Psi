##########################Instruções#######################################
"""
Ler o csv do moodle
o csv está dividido por 'Nome Empresa;Morada;Localidade;Região'
"""
from tkinter import *
from Biblio_posicao import centrar
from login import *

class UserWindow():
    def __init__(self):
        self.usr=Toplevel()
        self.usr.title("User")

class AdminWindow():
    def __init__(self):
        self.adm=Toplevel()
        self.adm.title("Admin")
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

        self.login = Button(f1, text="Login", bg="white", width="10", font=("", 15), command=lambda: logar(self, self.user, self.passw,UserWindow,AdminWindow))
        self.login.grid(row=6, column=0, sticky="w", padx=100)

        self.jan.mainloop()


if __name__=="__main__":
    GUI()
    UserWindow()
    AdminWindow

'''with open("empresa.csv","r",encoding="utf-8") as fp:
    fp.read().split("\n")
    for _ in fp:'''

