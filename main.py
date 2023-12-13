import tkinter as tk
from tkinter import messagebox, simpledialog 
from datetime import datetime
import sqlite3
import pickle

class ProdutoManager:
    def __init__(self):
        self.arquivo_produtos = 'dados_produtos.pkl'
        self.produtos = self.carregar_produtos()

    def adicionar_produto(self, produto):
        self.produtos.append(produto)
        self.salvar_produtos()

    def obter_produtos(self):
        return self.produtos

    def salvar_produtos(self):
        with open(self.arquivo_produtos, 'wb') as file:
            pickle.dump(self.produtos, file)

    def carregar_produtos(self):
        try:
            with open(self.arquivo_produtos, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

class ClienteManager:
    def __init__(self):
        self.conn = sqlite3.connect('dados_loja.db')
        self.cursor = self.conn.cursor()
        self.criar_tabela_clientes()

    def criar_tabela_clientes(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                endereco TEXT,
                telefone TEXT,
                email TEXT,
                tamanho TEXT,
                preferencias TEXT,
                historico TEXT
            )
        ''')
        self.conn.commit()

    def adicionar_cliente(self, cliente):
        self.cursor.execute('''
            INSERT INTO clientes (nome, endereco, telefone, email, tamanho, preferencias, historico)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cliente['nome'], cliente['endereco'], cliente['telefone'], cliente['email'], cliente['tamanho'], cliente['preferencias'], cliente['historico']))
        self.conn.commit()

    def obter_clientes(self):
        self.cursor.execute('SELECT * FROM clientes')
        return self.cursor.fetchall()

    def fechar_conexao(self):
        self.conn.close()

class Cliente:
    def __init__(self, nome, endereco, telefone, email, tamanho, preferencias, historico):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.tamanho = tamanho
        self.preferencias = preferencias
        self.historico = historico

class Produto:
    def __init__(self, nome, tamanho, cor, quantidade, fornecedor, preco_compra, preco_venda):
        self.nome = nome
        self.tamanho = tamanho
        self.cor = cor
        self.quantidade = quantidade
        self.fornecedor = fornecedor
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda

class Venda:
    def __init__(self, cliente, produtos, quantidade, data, total, metodo_pagamento):
        self.cliente = cliente
        self.produtos = produtos
        self.quantidade = quantidade
        self.data = data
        self.total = total
        self.metodo_pagamento = metodo_pagamento


class LojaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intimale Lingerie")
        self.cliente_manager = ClienteManager()
        self.produto_manager = ProdutoManager()
        
        self.carregar_dados()

        self.lista_clientes = []
        self.lista_produtos = []
        self.lista_vendas = []

        # Lista de clientes e produtos
        self.lst_clientes = tk.Listbox(self.root, width=50, height=10)
        self.lst_clientes.pack(pady=10)

        self.lst_produtos = tk.Listbox(self.root, width=50, height=10)
        self.lst_produtos.pack(pady=10)

        # Lista de vendas
        self.lst_vendas = tk.Listbox(self.root, width=50, height=10)
        self.lst_vendas.pack(pady=10)

        # Botões para manipulação de clientes
        self.btn_adicionar_cliente = tk.Button(self.root, text="Adicionar Cliente", command=self.adicionar_cliente)
        self.btn_adicionar_cliente.pack(side=tk.LEFT, padx=5)
        self.btn_editar_cliente = tk.Button(self.root, text="Editar Cliente", command=self.editar_cliente)
        self.btn_editar_cliente.pack(side=tk.LEFT, padx=5)
        self.btn_excluir_cliente = tk.Button(self.root, text="Excluir Cliente", command=self.excluir_cliente)
        self.btn_excluir_cliente.pack(side=tk.LEFT, padx=5)
        self.btn_ver_detalhes_cliente = tk.Button(self.root, text="Ver Detalhes", command=self.ver_detalhes_cliente)
        self.btn_ver_detalhes_cliente.pack(side=tk.LEFT, padx=5)

        # Botões para manipulação de Produtos
        self.btn_adicionar_produto = tk.Button(self.root, text="Adicionar Produto", command=self.adicionar_produto)
        self.btn_adicionar_produto.pack(side=tk.LEFT, padx=5)
        self.btn_editar_produto = tk.Button(self.root, text="Editar Produto", command=self.editar_produto)
        self.btn_editar_produto.pack(side=tk.LEFT, padx=5)
        self.btn_excluir_produto = tk.Button(self.root, text="Excluir Produto", command=self.excluir_produto)
        self.btn_excluir_produto.pack(side=tk.LEFT, padx=5)

        # Botão para realizar venda
        self.btn_realizar_venda = tk.Button(self.root, text="Realizar Venda", command=self.realizar_venda)
        self.btn_realizar_venda.pack(side=tk.LEFT, padx=5)

    def carregar_dados(self):
        # Carregar clientes
        clientes = self.cliente_manager.obter_clientes()
        for cliente in clientes:
            self.lst_clientes.insert(tk.END, cliente[1])  # Assume que o nome do cliente está na segunda coluna (índice 1)

        # Carregar produtos
        produtos = self.produto_manager.obter_produtos()
        for produto in produtos:
            self.lst_produtos.insert(tk.END, produto['nome'])

    def adicionar_cliente(self):
    # Adicione a lógica para adicionar um cliente aqui
        nome = simpledialog.askstring("Adicionar Cliente", "Digite o nome do cliente:")    
        if nome:
            endereco = simpledialog.askstring("Adicionar Cliente", "Digite o endereço:")
            telefone = simpledialog.askstring("Adicionar Cliente", "Digite o número de telefone:")
            email = simpledialog.askstring("Adicionar Cliente", "Digite o e-mail:")
            tamanho = simpledialog.askstring("Adicionar Cliente", "Digite o tamanho de lingerie:")
            preferencias = simpledialog.askstring("Adicionar Cliente", "Digite as preferências de lingerie:")
            historico = simpledialog.askstring("Adicionar Cliente", "Digite o histórico de compras:")

            novo_cliente = Cliente(nome, endereco, telefone, email, tamanho, preferencias, historico)
            self.lista_clientes.append(novo_cliente)
            self.lst_clientes.insert(tk.END, novo_cliente.nome)
            self.cliente_manager.adicionar_cliente(novo_cliente)
            # Adicione o novo cliente à lista de clientes ou outra estrutura de dados que você esteja usando


    def editar_cliente(self):
        # Adicione a lógica para editar um cliente aqui
        selecionado = self.lst_clientes.curselection()
        if selecionado:
            indice = selecionado[0]
            cliente_selecionado = self.lista_clientes[indice]
            novo_nome = simpledialog.askstring("Editar Cliente", f"Novo nome para {nome_anterior}:")

            if novo_nome:
                # Atualize o cliente na lista ou outra estrutura de dados
                cliente_selecionado.nome = novo_nome
                self.lst_clientes.delete(indice)
                self.lst_clientes.insert(indice, novo_nome)

    def excluir_cliente(self):
        # Adicione a lógica para excluir um cliente aqui
        selecionado = self.lst_clientes.curselection()
        if selecionado:
            indice = selecionado[0]
            cliente_selecionado = self.lista_clientes[indice]
            confirmacao = messagebox.askyesno("Excluir Cliente", f"Tem certeza que deseja excluir {nome_cliente}?")

            if confirmacao:
                # Remova o cliente da lista ou outra estrutura de dados
                self.lista_clientes.pop(indice)
                self.lst_clientes.delete(indice)

    def ver_detalhes_cliente(self):
        selecionado = self.lst_clientes.curselection()
        if selecionado:
            indice = selecionado[0]
            nome_cliente = self.lst_clientes.get(indice)

            # Recupera os detalhes do cliente (substitua esta lógica pela sua estrutura de dados)
            cliente_selecionado = self.obter_cliente_por_nome(nome_cliente)

            # Exibe uma janela pop-up com os detalhes do cliente
            detalhes_janela = tk.Toplevel(self.root)
            detalhes_janela.title(f"Detalhes do Cliente: {cliente_selecionado.nome}")

            # Crie e exiba rótulos com os detalhes do cliente
            tk.Label(detalhes_janela, text=f"Nome: {cliente_selecionado.nome}").pack()
            tk.Label(detalhes_janela, text=f"Endereço: {cliente_selecionado.endereco}").pack()
            tk.Label(detalhes_janela, text=f"Telefone: {cliente_selecionado.telefone}").pack()
            tk.Label(detalhes_janela, text=f"E-mail: {cliente_selecionado.email}").pack()
            tk.Label(detalhes_janela, text=f"Tamanho de Lingerie: {cliente_selecionado.tamanho}").pack()
            tk.Label(detalhes_janela, text=f"Preferências de Lingerie: {cliente_selecionado.preferencias}").pack()
            tk.Label(detalhes_janela, text=f"Histórico de Compras: {cliente_selecionado.historico}").pack()

    def obter_cliente_por_nome(self, nome_cliente):
    # Substitua esta lógica pela forma como você está armazenando e recuperando os clientes
    # por exemplo, se você estiver usando uma lista de objetos Cliente, você pode fazer:
        return next((cliente for cliente in self.lista_clientes if cliente.nome == nome_cliente), None)

    def adicionar_produto(self):
        # Adicione a lógica para adicionar um produto aqui
        nome = simpledialog.askstring("Adicionar Produto", "Digite o nome do produto:")

        if nome:
            tamanho = simpledialog.askstring("Adicionar Produto", "Digite o tamanho do produto:")
            cor = simpledialog.askstring("Adicionar Produto", "Digite a cor do produto:")
            quantidade = simpledialog.askinteger("Adicionar Produto", "Digite a quantidade em estoque:")
            fornecedor = simpledialog.askstring("Adicionar Produto", "Digite o fornecedor do produto:")
            preco_compra = simpledialog.askfloat("Adicionar Produto", "Digite o preço de compra:")
            preco_venda = simpledialog.askfloat("Adicionar Produto", "Digite o preço de venda:")

            novo_produto = Produto(nome, tamanho, cor, quantidade, fornecedor, preco_compra, preco_venda)
            self.lista_produtos.append(novo_produto)
            self.lst_produtos.insert(tk.END, novo_produto.nome)
            self.produto_manager.adicionar_produto(novo_produto)
            # Adicione o novo produto à lista de produtos ou outra estrutura de dados que você esteja usando

    def editar_produto(self):
        # Adicione a lógica para editar um produto aqui
        selecionado = self.lst_produtos.curselection()
        if selecionado:
            indice = selecionado[0]
            produto_selecionado = self.lista_produtos[indice]
            
            novo_nome = simpledialog.askstring("Editar Produto", f"Novo nome para {nome_anterior}:")

            if novo_nome:
                # Atualize o produto na lista ou outra estrutura de dados
                produto_selecionado.nome = novo_nome
                self.lst_produtos.delete(indice)
                self.lst_produtos.insert(indice, novo_nome)

    def excluir_produto(self):
        # Adicione a lógica para excluir um produto aqui
        selecionado = self.lst_produtos.curselection()
        if selecionado:
            indice = selecionado[0]
            produto_selecionado = self.lista_produtos[indice]
            
            confirmacao = messagebox.askyesno("Excluir Produto", f"Tem certeza que deseja excluir {nome_produto}?")

            if confirmacao:
                # Remova o produto da lista ou outra estrutura de dados
                self.lista_produtos.pop(indice)
                self.lst_produtos.delete(indice)

    def realizar_venda(self):
        # Adicione a lógica para realizar uma venda aqui
        selecionado_cliente = self.lst_clientes.curselection()
        selecionados_produtos = self.lst_produtos.curselection()

        if selecionado_cliente and selecionados_produtos:
            cliente_selecionado = self.lst_clientes.get(selecionado_cliente[0])
            produtos_vendidos = [self.lst_produtos.get(i) for i in selecionados_produtos]
            quantidade_vendida = simpledialog.askinteger("Realizar Venda", "Digite a quantidade vendida:")

            if quantidade_vendida:
                # Calcula o total da venda
                total_venda = self.calcular_total_venda(produtos_vendidos, quantidade_vendida)

                # Pede o método de pagamento
                metodo_pagamento = simpledialog.askstring("Realizar Venda", "Digite o método de pagamento:")

                # Atualiza o estoque dos produtos
                for produto in produtos_vendidos:
                    self.atualizar_estoque_produto(produto, quantidade_vendida)

                # Cria uma nova venda e a adiciona à lista de vendas ou outra estrutura de dados
                nova_venda = Venda(cliente_selecionado, produtos_vendidos, quantidade_vendida, datetime.now(), total_venda, metodo_pagamento)
                self.lista_vendas.append(nova_venda)
                self.lst_vendas.insert(tk.END, f"{nova_venda.cliente} comprou {quantidade_vendida} unidades de {', '.join(nova_venda.produtos)}")
        else:
            messagebox.showwarning("Realizar Venda", "Selecione um cliente e pelo menos um produto para realizar a venda.")

    def calcular_total_venda(self, produtos, quantidade):
        total = 0
        for produto_nome in produtos:
            produto = self.obter_produto_por_nome(produto_nome)
            if produto:
                total += produto.preco_venda * quantidade
        return total

    def atualizar_estoque_produto(self, nome_produto, quantidade_vendida):
        produto = self.obter_produto_por_nome(nome_produto)
        if produto:
            produto.quantidade -= quantidade_vendida

    def obter_produto_por_nome(self, nome_produto):
        for produto in self.lista_produtos:
            if produto.nome == nome_produto:
                return produto
        return None

    def fechar_janela(self):
        # Fechar gerenciadores de dados
        self.cliente_manager.fechar_conexao()

if __name__ == "__main__":
    root = tk.Tk()
    app = LojaApp(root)
    root.mainloop()
