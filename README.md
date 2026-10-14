# Banking Customer Feedback Analytics

Independent portfolio case study by Wenyu (Pearl) Dai. Python + SQL (SQLite) + JavaScript/HTML/CSS. No frameworks or external chart services required.

## Business question
Which checking/savings account complaint categories should a customer-experience team investigate first?

## Reproduce
Run `python3 download_data.py` to fetch the public CSV, then `python3 analyze.py` from this directory (standard library only). It rebuilds `data/analytics.sqlite`, `data/summary.json`, and `dist/data.js`, with assertions validating counts and scope. Open `dist/index.html` directly, or serve `dist/` with `python3 -m http.server 8765`. Run `analysis.sql` against the SQLite database for monthly volume, issue share, response timeliness, month-over-month change, and response categories.

## Source and provenance
Official CFPB public Consumer Complaint Database:
https://www.consumerfinance.gov/data-research/consumer-complaints/

CSV downloaded October 14, 2026 using:
https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?format=csv&date_received_min=2025-01-01&date_received_max=2026-01-01&product=Checking%20or%20savings%20account

The downloaded snapshot includes 84,348 rows. Parsing dates and enforcing the target cohort retains 84,195 unique records and rejects 153 outside the date/product scope. Duplicate complaint IDs: 0. See summary.json for SHA-256 checksum. API output may change; the retained snapshot makes this version reproducible.

## Metrics and limitations
- Complaint count: unique IDs in the filtered cohort.
- Issue share: issue count divided by selected complaint count.
- Timely-response rate: Yes divided by Yes + No; unknown values excluded.
- MoM growth: (current month - prior month) / prior month. Not seasonally adjusted.
- Categories are consumer-reported. Public complaints are not a random customer sample.
- Counts cannot establish bank quality without customer/base or transaction denominators.
- Timely response is not successful resolution, CSAT, or NPS.
- This download does not contain complaint narratives. No NLP or sentiment model is claimed.
- No causal or statistical significance claims are made.

## Dashboard
Filters: month, account type, issue. Charts, KPI cards, response table, CSV export, reset, empty-state handling. Investigation cards are explicitly fixed to the full cohort. Hosted site includes aggregated data only; raw data and SQLite database can be regenerated locally with the downloader and analysis script.

## Evidence and next steps
See [the one-page brief](Banking_Customer_Feedback_Insights.pdf) or dist/report.html. January concentration requires further source/event review. Company concentrations are diagnostic, not rankings. Recommended actions are hypotheses to investigate; no deployed intervention or business impact is claimed.

## Honest resume description
Built an interactive dashboard analyzing 84,195 public banking complaints with Python and SQL; validated data quality and visualized monthly trends, customer pain points, and response timeliness. Produced an evidence-based CX insights brief documenting metric definitions and analytical limitations.

## Validation
Run `node verify.js` to check filter, empty-state, reset, and CSV-export behavior. Analysis assertions validate record IDs, date/product scope, and aggregation totals.

## Live demo
https://pearl-banking-feedback-analytics.social-dell-7293.chatgpt.site/

The hosted demo currently requires the owner's login. To view it without hosting access, open `dist/index.html` locally after cloning; bundled aggregate data is sufficient.
