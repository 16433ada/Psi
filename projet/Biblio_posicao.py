def centrar(jan, largjan, altjan):

    largura_ecra = jan.winfo_screenwidth()
    altura_ecra = jan.winfo_screenheight()

    pos_x = (largura_ecra // 2) - (largjan // 2)
    pos_y = (altura_ecra // 2) - (altjan // 2)

    jan.geometry(f"{largjan}x{altjan}+{pos_x}+{pos_y}")
