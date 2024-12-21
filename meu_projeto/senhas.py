import random
import string
import json
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext


class GeradorSenhas:
    def __init__(self, comprimento=8, incluir_maiusculas=True, incluir_numeros=True, incluir_simbolos=True):
        self._comprimento = comprimento
        self._incluir_maiusculas = incluir_maiusculas
        self._incluir_numeros = incluir_numeros
        self._incluir_simbolos = incluir_simbolos
        self._caracteres = string.ascii_lowercase

    def _configurar_caracteres(self):
        self._caracteres = string.ascii_lowercase
        if self._incluir_maiusculas:
            self._caracteres += string.ascii_uppercase
        if self._incluir_numeros:
            self._caracteres += string.digits
        if self._incluir_simbolos:
            self._caracteres += string.punctuation

    def gerar_senha(self):
        self._configurar_caracteres()
        return ''.join(random.choice(self._caracteres) for _ in range(self._comprimento))



class BancoDeDados:
    def __init__(self, arquivo="senhas.json"):
        self._arquivo = arquivo
        if not os.path.exists(self._arquivo):
            with open(self._arquivo, 'w') as f:
                json.dump([], f)

    def salvar_conta(self, app, usuario, senha):
        with open(self._arquivo, 'r') as f:
            dados = json.load(f)

        dados.append({"Aplicativo": app, "Usuário": usuario, "Senha": senha})

        with open(self._arquivo, 'w') as f:
            json.dump(dados, f, indent=4)

    def carregar_contas(self):
        with open(self._arquivo, 'r') as f:
            return json.load(f)



class InterfaceApp:
    def __init__(self, titulo="Aplicativo", tamanho="400x400"):
        self._janela = tk.Tk()
        self._janela.title(titulo)
        self._janela.geometry(tamanho)
        self._janela.resizable(False, False)

    def executar(self):
        self._janela.mainloop()



class JanelaGeradorSenhas(InterfaceApp):
    def __init__(self):
        super().__init__(titulo="Gerador de Senhas", tamanho="450x550")
        self._banco = BancoDeDados()

        tk.Label(self._janela, text="Gerador de Senhas", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self._janela, text="Nome do Aplicativo/Serviço:").pack()
        self._entry_aplicativo = tk.Entry(self._janela, width=30)
        self._entry_aplicativo.pack(pady=5)

        tk.Label(self._janela, text="Nome de Usuário:").pack()
        self._entry_usuario = tk.Entry(self._janela, width=30)
        self._entry_usuario.pack(pady=5)

        tk.Label(self._janela, text="Comprimento da senha:").pack()
        self._entry_comprimento = tk.Entry(self._janela, width=5, justify="center")
        self._entry_comprimento.insert(0, "8")
        self._entry_comprimento.pack(pady=5)

        self._var_maiusculas = tk.BooleanVar(value=True)
        self._var_numeros = tk.BooleanVar(value=True)
        self._var_simbolos = tk.BooleanVar(value=True)

        tk.Checkbutton(self._janela, text="Incluir letras maiúsculas", variable=self._var_maiusculas).pack(anchor="w", padx=50)
        tk.Checkbutton(self._janela, text="Incluir números", variable=self._var_numeros).pack(anchor="w", padx=50)
        tk.Checkbutton(self._janela, text="Incluir símbolos", variable=self._var_simbolos).pack(anchor="w", padx=50)

        tk.Button(self._janela, text="Gerar Senha", command=self._gerar_senha, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

        self._label_resultado = tk.Label(self._janela, text="", font=("Arial", 12), fg="blue")
        self._label_resultado.pack(pady=5)

        tk.Button(self._janela, text="Mostrar Contas Armazenadas", command=self._mostrar_contas, bg="blue", fg="white").pack(pady=5)
        self._texto_contas = scrolledtext.ScrolledText(self._janela, width=50, height=10, wrap="word")
        self._texto_contas.pack(pady=10)

        tk.Label(self._janela, text="Desenvolvido por Arthur Gomes", font=("Arial", 8), fg="gray").pack(side="bottom", pady=5)

    def _gerar_senha(self):
        app = self._entry_aplicativo.get().strip()
        usuario = self._entry_usuario.get().strip()
        try:
            comprimento = int(self._entry_comprimento.get())
        except ValueError:
            messagebox.showerror("Erro", "Comprimento deve ser um número!")
            return

        if not app or not usuario:
            messagebox.showerror("Erro", "Preencha o nome do aplicativo e do usuário!")
            return

        gerador = GeradorSenhas(
            comprimento=comprimento,
            incluir_maiusculas=self._var_maiusculas.get(),
            incluir_numeros=self._var_numeros.get(),
            incluir_simbolos=self._var_simbolos.get()
        )
        senha = gerador.gerar_senha()
        self._banco.salvar_conta(app, usuario, senha)

        self._label_resultado.config(text=f"Aplicativo: {app}\nUsuário: {usuario}\nSenha: {senha}", fg="blue")
        messagebox.showinfo("Sucesso", "Senha salva com sucesso!")

    def _mostrar_contas(self):
        contas = self._banco.carregar_contas()
        self._texto_contas.delete("1.0", tk.END)
        if not contas:
            self._texto_contas.insert(tk.END, "Nenhuma conta armazenada ainda.")
        else:
            for conta in contas:
                self._texto_contas.insert(tk.END, f"Aplicativo: {conta['Aplicativo']}\nUsuário: {conta['Usuário']}\nSenha: {conta['Senha']}\n\n")


if __name__ == "__main__":
    app = JanelaGeradorSenhas()
    app.executar()





