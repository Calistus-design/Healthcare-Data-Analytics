-- Top 5 Diseases by Visits and Revenue
SELECT 
    v.diagnosis,
    COUNT(v.visit_id) as patient_count,
    SUM(po.total_cost) as revenue_generated
FROM visits v
LEFT JOIN pharmacy_orders po ON v.visit_id = po.visit_id
GROUP BY v.diagnosis
ORDER BY patient_count DESC
LIMIT 5;
