-- SQLite syntax; response rate excludes missing/unknown timely-response values.
SELECT substr(received,1,7) AS month, COUNT(*) AS complaints,
 SUM(timely='Yes') AS timely_yes, SUM(timely IN ('Yes','No')) AS known_timely,
 100.0*SUM(timely='Yes')/NULLIF(SUM(timely IN ('Yes','No')),0) AS timely_response_pct
FROM complaints GROUP BY month ORDER BY month;

SELECT issue, COUNT(*) AS complaints,
 100.0*COUNT(*)/(SELECT COUNT(*) FROM complaints) AS complaint_share_pct,
 100.0*SUM(timely='Yes')/NULLIF(SUM(timely IN ('Yes','No')),0) AS timely_response_pct
FROM complaints GROUP BY issue ORDER BY complaints DESC;

WITH monthly AS (
 SELECT substr(received,1,7) AS month,COUNT(*) AS n FROM complaints GROUP BY month
)
SELECT month,n,LAG(n) OVER(ORDER BY month) AS previous_n,
 100.0*(n-LAG(n) OVER(ORDER BY month))/NULLIF(LAG(n) OVER(ORDER BY month),0) AS mom_pct
FROM monthly ORDER BY month;

SELECT response,COUNT(*) AS complaints FROM complaints GROUP BY response ORDER BY complaints DESC;
