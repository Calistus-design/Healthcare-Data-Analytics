-- Monthly Revenue Trend
SELECT 
    TO_CHAR(DATE_TRUNC('month', v.visit_date), 'YYYY-MM') AS revenue_month,
    COUNT(v.visit_id) as total_visits,
    SUM(po.total_cost) as total_revenue
FROM visits v
JOIN pharmacy_orders po ON v.visit_id = po.visit_id
GROUP BY 1
ORDER BY 1;