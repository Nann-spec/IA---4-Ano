import tkinter as tk

# Criar janela principal
janela = tk.Tk()
janela.title("Minha Primeira Janela")
janela.geometry("400x300")  # Largura x Altura

# Adicionar um texto (label)
label = tk.Label(janela, text="Olá, Mundo!")
label.pack(pady=20)


# Botão Simples
def clicar():
    label.config(text="Você clicou no botão!")


botao = tk.Button(janela, text="Clique aqui", command=clicar)
botao.pack()

janela.mainloop()
