
## Funcionalidades

- Cadastrar, listar e remover produtos
- Repor estoque
- Realizar vendas com cálculo de total e troco
- Gerar relatório com faturamento, ticket médio e produtos com estoque baixo
- Salvar os dados automaticamente no arquivo `dados.json`

## Como usar

Ao iniciar, o menu principal aparece:

```
1 - Cadastrar produto
2 - Listar produtos
3 - Repor estoque
4 - Remover produto
5 - Realizar venda
6 - Relatório
0 - Sair
```

Digite o número da opção desejada e siga as instruções na tela.

**Exemplo de venda:**
1. Escolha a opção `5`.
2. Informe o código do produto e a quantidade.
3. Repita para outros produtos ou digite `0` para finalizar.
4. Informe o valor recebido e o sistema mostra o troco.

## Estrutura dos dados

- **Produto:** código, nome, preço e estoque
- **Venda:** lista de itens vendidos e total

Os dados ficam guardados em `dados.json`, criado automaticamente na primeira vez que algo é salvo.

## Tecnologias

- Python 3
- Módulos `json` e `os` (já vêm com o Python)