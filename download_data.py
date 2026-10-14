"""Download public CFPB checking/savings complaints for the 2025 cohort."""
from pathlib import Path
from urllib.request import urlopen
import shutil
URL='https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?format=csv&date_received_min=2025-01-01&date_received_max=2026-01-01&product=Checking%20or%20savings%20account'
root=Path(__file__).resolve().parent
(root/'data').mkdir(exist_ok=True)
with urlopen(URL,timeout=120) as response, (root/'data/complaints.csv').open('wb') as output:
 shutil.copyfileobj(response,output)
print('Saved data/complaints.csv. Run python3 analyze.py next. Source changes may alter counts.')
