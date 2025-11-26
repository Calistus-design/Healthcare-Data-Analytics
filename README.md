# **Hospital Operations & Patient Flow Analytics**

![Dashboard Screenshot]([ SCREENSHOT IMAGE PATH HERE])

## **Summary**
In the absence of public datasets that accurately reflect the operational complexity of Kenyan healthcare facilities (linking Supply Chain, Billing, and Clinical Diagnosis), I engineered a **Full-Stack Hospital Analytics System**.

This project simulates a high-volume Nairobi hospital (65,000+ visits, 15,000 patients) to analyze:
1.  **Revenue Cycle Management:** Tracking trends across Cash vs. Insurance (NHIF, Jubilee, etc.).
2.  **Clinical-Supply Chain correlation:** Mapping ICD-10 diagnoses to pharmaceutical consumption.
3.  **Inventory Velocity:** Identifying high-value vs. high-volume assets.

---

## **Tools used**
*   **Data Engineering:** Python (Pandas, Faker, NumPy)
*   **Database:** PostgreSQL (Relational DB, Star Schema)
*   **Analysis:** SQL (Joins, Window Functions, Aggregations)
*   **Visualization:** Power BI (DAX Measures, Interactive Slicers)
*   **Context:** Kenyan Healthcare System (NHIF, KEMSA Drug List, Nairobi Wards)

---

## **The Architecture** 

### Phase 1: Data Simulation (Python)
 I wrote a Python script (`generate_data.py`) to simulate an ERP environment.
*   **Clinical Logic:** Implemented a logic engine that maps diseases to drugs (e.g., *Malaria Diagnosis* $\to$ *Triggers AL Prescription*).
*   **Seasonality:** Programmed date randomization to simulate traffic fluctuations over 3 years (2022-2024).
*   **Demographics:** Modeled patient distribution across 15 specific Nairobi wards (e.g., Westlands vs. Kibra) to analyze payer behavior.

### Phase 2: Data Warehousing (PostgreSQL)
Designed a **Star Schema** to ensure data integrity and query performance.
*   **Fact Table:** `pharmacy_orders`, `visits`
*   **Dimension Tables:** `patients`, `inventory`
*   *Skill Highlight:* Used SQL to perform data integrity checks before loading into BI tools.

### Phase 3: Business Intelligence (Power BI)
Built an executive dashboard focused on **Volume, Value, and Velocity**.
*   **DAX Measures:** Calculated `Total Revenue`, `Total Visits`, and `Avg Revenue Per Visit`.
*   **Interactivity:** Added Slicers for **Insurance Provider** to allow deep-dives into payer performance (e.g., comparing NHIF vs. Cash revenue).

---

## **Key Business Insights**

**1. The "Volume vs. Value" Disconnect**
*   **Insight:** While Antibiotics (like *Amoxicillin*) account for the highest volume of prescription units, Respiratory devices (*Salbutamol Inhalers*) drive the highest revenue per unit.
*   **Recommendation:** Inventory prioritization should focus on stock reliability for high-margin respiratory products to prevent revenue loss during seasonal spikes.

**2. Seasonal Revenue Trends**
*   **Insight:** Revenue remains relatively stable with distinct seasonal dips and spikes, correlating with the prevalence of *Upper Respiratory Infections* and *Malaria* cases during rainy seasons.

**3. Payer Demographics**
*   **Insight:** Significant variance in "Average Revenue Per Visit" between Cash payers and Private Insurance holders, influencing pricing strategies for outpatient services.

---

## **SQL Queries**

**1. Monthly Revenue Growth (Trend Analysis)**
```sql
SELECT 
    TO_CHAR(DATE_TRUNC('month', v.visit_date), 'YYYY-MM') AS revenue_month,
    COUNT(v.visit_id) as total_visits,
    SUM(po.total_cost) as total_revenue
FROM visits v
JOIN pharmacy_orders po ON v.visit_id = po.visit_id
GROUP BY 1
ORDER BY 1;
```
**2. Top 5 Diseases by Patient Visits and Revenue**
```sql 
SELECT 
    v.diagnosis,
    COUNT(v.visit_id) as patient_count,
    SUM(po.total_cost) as revenue_generated
FROM visits v
LEFT JOIN pharmacy_orders po ON v.visit_id = po.visit_id
GROUP BY v.diagnosis
ORDER BY patient_count DESC
LIMIT 5;
```

**3. Identifying High-Value Drugs moving fast**
``` sql
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
```

## **Repository Structure**

- **generate_data.py:** The Python simulation script.

- **sql queries/:** The SQL scripts used for data validation and insight generation.

- **raw_sources/:** The master data files (ICD-10 codes, KEMSA drug prices, Locations).


## **Author**
- **Calistus Mwonga**
- Data Analyst | Data Scientist
- [Portfolio Link] 