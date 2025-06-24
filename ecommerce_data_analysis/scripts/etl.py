import pandas as pd
import os

RAW_PATH = r'C:\Projetos\ecommerce_data_analysis\data\raw'
PROCESSED_PATH = r'C:\Projetos\ecommerce_data_analysis\data\processed'

def carregar_dados():
    pedidos = pd.read_csv(os.path.join(RAW_PATH, 'orders_dataset.csv'))
    clientes = pd.read_csv(os.path.join(RAW_PATH, 'customers_dataset.csv'))
    pagamentos = pd.read_csv(os.path.join(RAW_PATH, 'order_payments_dataset.csv'))
    produtos = pd.read_csv(os.path.join(RAW_PATH, 'products_dataset.csv'))
    entregas = pd.read_csv(os.path.join(RAW_PATH, 'order_items_dataset.csv'))
    return pedidos, clientes, pagamentos, produtos, entregas

def validar_dados(pedidos, clientes, pagamentos, produtos, entregas):
    print("### Validação de Dados ###")

    # ---- Pedidos ----
    print("\nPedidos:")
    print(pedidos.isnull().sum())
    if (pedidos['order_status'].isin([
        'delivered', 'shipped', 'canceled', 'unavailable', 'processing', 'invoiced', 'created', 'approved'
    ]) == False).any():
        print("Atenção: Existem status de pedido fora dos valores esperados.")

    # ---- Clientes ----
    print("\nClientes:")
    print(clientes.isnull().sum())

    # ---- Pagamentos ----
    print("\nPagamentos:")
    print(pagamentos.isnull().sum())
    if (pagamentos['payment_type'].isin([
        'credit_card', 'boleto', 'voucher', 'debit_card', 'not_defined'
    ]) == False).any():
        print("Atenção: Existem tipos de pagamento fora dos valores esperados.")
    if (pagamentos['payment_value'] < 0).any():
        print("Atenção: Existem pagamentos com valor negativo.")

    # ---- Produtos ----
    print("\nProdutos:")
    print(produtos.isnull().sum())

    # ---- Entregas ----
    print("\nEntregas:")
    print(entregas.isnull().sum())
    if (entregas['price'] < 0).any() or (entregas['freight_value'] < 0).any():
        print("Atenção: Existem preços ou fretes com valor negativo.")

def tratar_dados(pedidos, clientes, pagamentos, produtos, entregas):
    print("### Tratamento de Dados ###")

    # Remover duplicatas
    pedidos = pedidos.drop_duplicates()
    clientes = clientes.drop_duplicates()
    pagamentos = pagamentos.drop_duplicates()
    produtos = produtos.drop_duplicates()
    entregas = entregas.drop_duplicates()

    # Conversão de datas
    pedidos['order_purchase_timestamp'] = pd.to_datetime(pedidos['order_purchase_timestamp'], errors='coerce')
    pedidos['order_delivered_customer_date'] = pd.to_datetime(pedidos['order_delivered_customer_date'], errors='coerce')

    # Preencher valores nulos críticos, se desejado
    pedidos = pedidos.dropna(subset=['order_id', 'customer_id'])
    clientes = clientes.dropna(subset=['customer_id'])
    pagamentos = pagamentos.dropna(subset=['order_id'])
    entregas = entregas.dropna(subset=['order_id', 'product_id'])

    return pedidos, clientes, pagamentos, produtos, entregas

def salvar_dados(pedidos, clientes, pagamentos, produtos, entregas):
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    pedidos.to_csv(os.path.join(PROCESSED_PATH, 'pedidos.csv'), index=False)
    clientes.to_csv(os.path.join(PROCESSED_PATH, 'clientes.csv'), index=False)
    pagamentos.to_csv(os.path.join(PROCESSED_PATH, 'pagamentos.csv'), index=False)
    produtos.to_csv(os.path.join(PROCESSED_PATH, 'produtos.csv'), index=False)
    entregas.to_csv(os.path.join(PROCESSED_PATH, 'entregas.csv'), index=False)

def main():
    pedidos, clientes, pagamentos, produtos, entregas = carregar_dados()

    validar_dados(pedidos, clientes, pagamentos, produtos, entregas)

    pedidos, clientes, pagamentos, produtos, entregas = tratar_dados(
        pedidos, clientes, pagamentos, produtos, entregas
    )

    salvar_dados(pedidos, clientes, pagamentos, produtos, entregas)
    print("Dados processados e salvos com sucesso!")

if __name__ == "__main__":
    main()
