-- Identifying High-Value Drugs moving fast
SELECT 
    i.drug_name,
    i.category,
    i.unit_price,
    COUNT(po.order_id) as times_sold,
    SUM(po.total_cost) as total_sales_value
FROM inventory i
JOIN pharmacy_orders po ON i.drug_id = po.drug_id
GROUP BY 1, 2, 3
ORDER BY total_sales_value DESC
LIMIT 10;