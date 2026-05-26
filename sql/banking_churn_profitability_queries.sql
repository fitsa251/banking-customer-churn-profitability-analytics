-- Banking Customer Churn & Profitability Analytics
-- SQL Analysis Queries
-- Purpose: Analyze customer churn, profitability, balances, product usage,
-- digital engagement, support activity, and retention opportunities.

-- Expected table:
-- banking_churn_profitability_data


-- 1. Preview customer banking data
SELECT *
FROM banking_churn_profitability_data
LIMIT 20;


-- 2. Executive KPI summary
SELECT
    COUNT(*) AS total_customers,
    ROUND(SUM(total_balance), 2) AS total_customer_balance,
    ROUND(AVG(total_balance), 2) AS average_customer_balance,
    ROUND(SUM(monthly_revenue), 2) AS total_monthly_revenue,
    ROUND(SUM(monthly_profit), 2) AS total_monthly_profit,
    ROUND(AVG(product_count), 2) AS average_products_per_customer,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct,
    SUM(CASE WHEN churn_risk_band = 'High Risk' THEN 1 ELSE 0 END) AS high_churn_risk_customers
FROM banking_churn_profitability_data;


-- 3. Customer segment profitability
SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(total_balance), 2) AS total_balance,
    ROUND(AVG(total_balance), 2) AS avg_balance,
    ROUND(SUM(monthly_revenue), 2) AS total_monthly_revenue,
    ROUND(SUM(monthly_profit), 2) AS total_monthly_profit,
    ROUND(AVG(monthly_profit), 2) AS avg_monthly_profit,
    ROUND(AVG(product_count), 2) AS avg_product_count,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY customer_segment
ORDER BY total_monthly_profit DESC;


-- 4. Churn risk band summary
SELECT
    churn_risk_band,
    COUNT(*) AS customers,
    ROUND(AVG(total_balance), 2) AS avg_balance,
    ROUND(AVG(monthly_profit), 2) AS avg_monthly_profit,
    ROUND(AVG(product_count), 2) AS avg_product_count,
    ROUND(AVG(support_calls_90d), 2) AS avg_support_calls_90d,
    ROUND(AVG(digital_logins_90d), 2) AS avg_digital_logins_90d,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY churn_risk_band
ORDER BY churn_rate_pct DESC;


-- 5. Product count and churn relationship
SELECT
    product_count,
    COUNT(*) AS customers,
    ROUND(AVG(total_balance), 2) AS avg_balance,
    ROUND(AVG(monthly_profit), 2) AS avg_monthly_profit,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY product_count
ORDER BY product_count;


-- 6. Digital engagement and churn
SELECT
    CASE
        WHEN digital_logins_90d <= 5 THEN 'Very Low'
        WHEN digital_logins_90d <= 15 THEN 'Low'
        WHEN digital_logins_90d <= 30 THEN 'Medium'
        ELSE 'High'
    END AS digital_engagement_band,
    COUNT(*) AS customers,
    ROUND(AVG(monthly_profit), 2) AS avg_monthly_profit,
    ROUND(AVG(product_count), 2) AS avg_product_count,
    ROUND(AVG(support_calls_90d), 2) AS avg_support_calls_90d,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY
    CASE
        WHEN digital_logins_90d <= 5 THEN 'Very Low'
        WHEN digital_logins_90d <= 15 THEN 'Low'
        WHEN digital_logins_90d <= 30 THEN 'Medium'
        ELSE 'High'
    END
ORDER BY churn_rate_pct DESC;


-- 7. Support calls and churn
SELECT
    CASE
        WHEN support_calls_90d = 0 THEN '0 Calls'
        WHEN support_calls_90d BETWEEN 1 AND 2 THEN '1-2 Calls'
        WHEN support_calls_90d BETWEEN 3 AND 5 THEN '3-5 Calls'
        ELSE '6+ Calls'
    END AS support_call_band,
    COUNT(*) AS customers,
    ROUND(AVG(monthly_profit), 2) AS avg_monthly_profit,
    ROUND(AVG(product_count), 2) AS avg_product_count,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY
    CASE
        WHEN support_calls_90d = 0 THEN '0 Calls'
        WHEN support_calls_90d BETWEEN 1 AND 2 THEN '1-2 Calls'
        WHEN support_calls_90d BETWEEN 3 AND 5 THEN '3-5 Calls'
        ELSE '6+ Calls'
    END
ORDER BY churn_rate_pct DESC;


-- 8. Income band profitability and churn
SELECT
    income_band,
    COUNT(*) AS customers,
    ROUND(SUM(total_balance), 2) AS total_balance,
    ROUND(SUM(monthly_revenue), 2) AS total_monthly_revenue,
    ROUND(SUM(monthly_profit), 2) AS total_monthly_profit,
    ROUND(AVG(product_count), 2) AS avg_product_count,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY income_band
ORDER BY total_monthly_profit DESC;


-- 9. Tenure band churn summary
SELECT
    tenure_band,
    COUNT(*) AS customers,
    ROUND(AVG(total_balance), 2) AS avg_balance,
    ROUND(AVG(product_count), 2) AS avg_product_count,
    ROUND(AVG(monthly_profit), 2) AS avg_monthly_profit,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY tenure_band
ORDER BY churn_rate_pct DESC;


-- 10. State-level customer profitability
SELECT
    state,
    COUNT(*) AS customers,
    ROUND(SUM(total_balance), 2) AS total_balance,
    ROUND(SUM(monthly_revenue), 2) AS total_monthly_revenue,
    ROUND(SUM(monthly_profit), 2) AS total_monthly_profit,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY state
ORDER BY total_monthly_profit DESC;


-- 11. High-value at-risk customer retention list
SELECT
    customer_id,
    state,
    customer_segment,
    income_band,
    credit_score_band,
    tenure_band,
    total_balance,
    product_count,
    monthly_revenue,
    monthly_profit,
    support_calls_90d,
    digital_logins_90d,
    churn_probability,
    churn_risk_band
FROM banking_churn_profitability_data
WHERE
    churn_risk_band = 'High Risk'
    AND (
        monthly_profit > (
            SELECT AVG(monthly_profit)
            FROM banking_churn_profitability_data
        )
        OR total_balance > (
            SELECT AVG(total_balance)
            FROM banking_churn_profitability_data
        )
    )
ORDER BY monthly_profit DESC, total_balance DESC
LIMIT 50;


-- 12. Low-product customers with higher churn risk
SELECT
    customer_id,
    state,
    customer_segment,
    income_band,
    tenure_band,
    total_balance,
    product_count,
    monthly_profit,
    churn_probability,
    churn_risk_band,
    churned
FROM banking_churn_profitability_data
WHERE product_count <= 2
ORDER BY churn_probability DESC, monthly_profit DESC
LIMIT 50;


-- 13. Profitable customers with low product depth
SELECT
    customer_id,
    state,
    customer_segment,
    income_band,
    total_balance,
    product_count,
    monthly_revenue,
    monthly_profit,
    churn_probability,
    churn_risk_band
FROM banking_churn_profitability_data
WHERE
    monthly_profit > (
        SELECT AVG(monthly_profit)
        FROM banking_churn_profitability_data
    )
    AND product_count <= 3
ORDER BY monthly_profit DESC
LIMIT 50;


-- 14. Negative-profit customers
SELECT
    customer_id,
    state,
    customer_segment,
    income_band,
    total_balance,
    product_count,
    monthly_revenue,
    servicing_cost,
    monthly_profit,
    support_calls_90d,
    churn_probability,
    churn_risk_band
FROM banking_churn_profitability_data
WHERE monthly_profit < 0
ORDER BY monthly_profit ASC
LIMIT 50;


-- 15. Product ownership summary
SELECT
    SUM(has_credit_card) AS customers_with_credit_card,
    SUM(has_personal_loan) AS customers_with_personal_loan,
    SUM(has_mortgage) AS customers_with_mortgage,
    SUM(has_investment_account) AS customers_with_investment_account,
    SUM(has_business_account) AS customers_with_business_account
FROM banking_churn_profitability_data;


-- 16. Product ownership by customer segment
SELECT
    customer_segment,
    COUNT(*) AS customers,
    SUM(has_credit_card) AS customers_with_credit_card,
    SUM(has_personal_loan) AS customers_with_personal_loan,
    SUM(has_mortgage) AS customers_with_mortgage,
    SUM(has_investment_account) AS customers_with_investment_account,
    SUM(has_business_account) AS customers_with_business_account
FROM banking_churn_profitability_data
GROUP BY customer_segment
ORDER BY customers DESC;


-- 17. Credit score band profitability and churn
SELECT
    credit_score_band,
    COUNT(*) AS customers,
    ROUND(AVG(total_balance), 2) AS avg_balance,
    ROUND(AVG(monthly_profit), 2) AS avg_monthly_profit,
    ROUND(AVG(product_count), 2) AS avg_product_count,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY credit_score_band
ORDER BY churn_rate_pct DESC;


-- 18. Customers for cross-sell opportunity
SELECT
    customer_id,
    state,
    customer_segment,
    income_band,
    credit_score_band,
    total_balance,
    product_count,
    has_credit_card,
    has_personal_loan,
    has_mortgage,
    has_investment_account,
    monthly_profit,
    churn_probability,
    churn_risk_band
FROM banking_churn_profitability_data
WHERE
    churn_risk_band IN ('Low Risk', 'Medium Risk')
    AND product_count BETWEEN 2 AND 4
    AND total_balance > (
        SELECT AVG(total_balance)
        FROM banking_churn_profitability_data
    )
ORDER BY total_balance DESC, monthly_profit DESC
LIMIT 50;


-- 19. Retention priority summary by segment and risk band
SELECT
    customer_segment,
    churn_risk_band,
    COUNT(*) AS customers,
    ROUND(SUM(total_balance), 2) AS total_balance,
    ROUND(SUM(monthly_profit), 2) AS total_monthly_profit,
    ROUND(AVG(product_count), 2) AS avg_product_count,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY customer_segment, churn_risk_band
ORDER BY customer_segment, churn_rate_pct DESC;


-- 20. Overall business summary by segment
SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(total_balance), 2) AS total_balance,
    ROUND(SUM(monthly_revenue), 2) AS total_monthly_revenue,
    ROUND(SUM(monthly_profit), 2) AS total_monthly_profit,
    ROUND(AVG(product_count), 2) AS avg_product_count,
    SUM(CASE WHEN churn_risk_band = 'High Risk' THEN 1 ELSE 0 END) AS high_risk_customers,
    ROUND(AVG(churned) * 100, 2) AS churn_rate_pct
FROM banking_churn_profitability_data
GROUP BY customer_segment
ORDER BY total_monthly_profit DESC;