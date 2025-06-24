
-- Total de pedidos por estado
SELECT c.customer_state, COUNT(o.order_id) AS total_pedidos
FROM olist_orders_dataset o
JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY total_pedidos DESC;

-- Receita total por tipo de pagamento
SELECT payment_type, SUM(payment_value) AS receita_total
FROM olist_order_payments_dataset
GROUP BY payment_type
ORDER BY receita_total DESC;

-- Tempo médio de entrega
SELECT AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)) AS tempo_medio_entrega
FROM olist_orders_dataset o
WHERE o.order_delivered_customer_date IS NOT NULL;
