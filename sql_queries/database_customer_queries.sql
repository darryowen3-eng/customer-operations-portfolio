SELECT
	customer_id,
	region,
	total_spent,
	DENSE_RANK() OVER(
	PARTITION BY region ORDER BY total_spent DESC
	) AS regional_spent_rank
FROM customers
WHERE total_spent > 0
LIMIT 10;



SELECT 
	escalation_reason,
	COUNT(customer_id) AS total_complaints,
	ROUND(AVG(customer_rating), 2) AS avg_rating_impact,
	ROUND(SUM(total_spent), 2) AS revenue_risk
FROM customers
WHERE has_escalation = 'True'
AND escalation_reason != 'Unknown'
AND customer_rating != 'Unknown'
GROUP BY escalation_reason ORDER BY revenue_risk DESC;



SELECT
	customer_id,
	region,
	total_spent,
	CASE
		WHEN total_spent >= 15000 THEN 'VIP tier'
		WHEN total_spent >= 10000 THEN 'Gold tier'
		ELSE 'Standard tier'
	END AS customer_value_segment
FROM customers
WHERE signup_date != '2026-01-01'
ORDER BY total_spent DESC LIMIT 10;