""""
Funcionalidades:
  - Cadastrar, listar, repor estoque e remover produtos
  - Realizar vendas com cálculo de total e troco
  - Relatório de vendas e estoque baixo
  - Os dados são salvos no arquivo dados.json
"""
import json
import os

ARQUIVO = "dados.json"

produtos = []
vendas = []

def carregar_dados():
    """Lê os dados do arquivo JSON, se ele existir."""
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        produtos.extend(dados["produtos"])
        vendas.extend(dados["vendas"])


def salvar_dados():
    """Grava produtos e vendas no arquivo JSON."""
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump({"produtos": produtos, "vendas": vendas}, f, ensure_ascii=False, indent=2)


def ler_numero(mensagem, tipo=float):
    """Pede um número ao usuário até ele digitar um valor válido (>= 0)."""
    while True:
        try:
            valor = tipo(input(mensagem).replace(",", "."))
            if valor < 0:
                print("Digite um valor positivo.")
            else:
                return valor
        except ValueError:
            print("Valor inválido. Tente novamente.")


def buscar_produto(codigo):
    """Procura um produto pelo código. Retorna o produto ou None."""
    for p in produtos:
        if p["codigo"] == codigo:
            return p
    return None



# CADASTRO DE PRODUTOS 

def cadastrar_produto():
    nome = input("Nome do produto: ").strip()
    if nome == "":
        print("O nome não pode ser vazio.")
        return
    preco = ler_numero("Preço (R$): ")
    estoque = ler_numero("Quantidade em estoque: ", int)

    # novo código = maior código existente + 1
    codigo = max([p["codigo"] for p in produtos], default=0) + 1
    produtos.append({"codigo": codigo, "nome": nome, "preco": preco, "estoque": estoque})
    salvar_dados()
    print(f"Produto cadastrado com o código {codigo}!")


def listar_produtos():
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return
    print(f"\n{'Cód':<5}{'Nome':<25}{'Preço':>10}{'Estoque':>10}")
    print("-" * 50)
    for p in produtos:
        print(f"{p['codigo']:<5}{p['nome']:<25}{p['preco']:>10.2f}{p['estoque']:>10}")



# ESTOQUE

def repor_estoque():
    codigo = ler_numero("Código do produto: ", int)
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return
    qtd = ler_numero(f"Quantidade a adicionar em '{produto['nome']}': ", int)
    produto["estoque"] += qtd
    salvar_dados()
    print(f"Novo estoque: {produto['estoque']}")


def remover_produto():
    codigo = ler_numero("Código do produto: ", int)
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return
    produtos.remove(produto)
    salvar_dados()
    print("Produto removido.")



# VENDAS 

def realizar_venda():
    carrinho = []   # itens da venda atual
    total = 0.0

    print("\n--- NOVA VENDA --- (digite 0 para finalizar)")
    while True:
        codigo = ler_numero("Código do produto: ", int)
        if codigo == 0:
            break

        produto = buscar_produto(codigo)
        if produto is None:
            print("Produto não encontrado.")
            continue

        qtd = ler_numero(f"Quantidade de '{produto['nome']}': ", int)
        if qtd > produto["estoque"]:
            print(f"Estoque insuficiente! Disponível: {produto['estoque']}")
            continue

        # baixa no estoque e adiciona ao carrinho
        produto["estoque"] -= qtd
        subtotal = produto["preco"] * qtd
        total += subtotal
        carrinho.append({"nome": produto["nome"], "qtd": qtd, "subtotal": subtotal})
        print(f"Adicionado: {qtd}x {produto['nome']} = R$ {subtotal:.2f}")

    if len(carrinho) == 0:
        print("Venda cancelada (carrinho vazio).")
        return

    # Mostra o cupom
    print("\n====== CUPOM ======")
    for item in carrinho:
        print(f"{item['qtd']}x {item['nome']:<20} R$ {item['subtotal']:>8.2f}")
    print(f"TOTAL: R$ {total:.2f}")

    # Pagamento
    pago = ler_numero("Valor recebido (R$): ")
    while pago < total:
        print("Valor insuficiente!")
        pago = ler_numero("Valor recebido (R$): ")
    print(f"Troco: R$ {pago - total:.2f}")
    print("===================")

    vendas.append({"itens": carrinho, "total": total})
    salvar_dados()


# RELATORIO

def relatorio():
    print("\n--- RELATÓRIO ---")
    faturamento = sum(v["total"] for v in vendas)
    print(f"Total de vendas realizadas: {len(vendas)}")
    print(f"Faturamento total: R$ {faturamento:.2f}")
    if len(vendas) > 0:
        print(f"Ticket médio: R$ {faturamento / len(vendas):.2f}")

    print("\nProdutos com estoque baixo (5 ou menos):")
    achou = False
    for p in produtos:
        if p["estoque"] <= 5:
            print(f"  [{p['codigo']}] {p['nome']} - estoque: {p['estoque']}")
            achou = True
    if not achou:
        print("  Nenhum.")


# =====================================================
# PARTE 6 - MENU PRINCIPAL (Integrante 6)
# =====================================================
def menu():
    while True:
        print("\n===== SISTEMA DE MERCADO =====")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Repor estoque")
        print("4 - Remover produto")
        print("5 - Realizar venda")
        print("6 - Relatório")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            repor_estoque()
        elif opcao == "4":
            remover_produto()
        elif opcao == "5":
            realizar_venda()
        elif opcao == "6":
            relatorio()
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida!")


# Início do programa
carregar_dados()
menu()