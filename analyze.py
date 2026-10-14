import csv,json,sqlite3,collections,pathlib,hashlib,datetime
root=pathlib.Path(__file__).resolve().parent
source=root/'data/complaints.csv'
rows=list(csv.DictReader(source.open(encoding='utf-8-sig')))
print('Raw rows:',len(rows));print('Fields:',list(rows[0]))
seen=set(); clean=[]; duplicates=0; rejected=0
for r in rows:
 ident=r['Complaint ID'];date=r['Date received'][:10]
 try: date=datetime.datetime.strptime(date,'%m/%d/%Y').date().isoformat()
 except ValueError:
  try: datetime.date.fromisoformat(date)
  except ValueError: rejected+=1;continue
 if r['Product']!='Checking or savings account' or not '2025-01-01'<=date<'2026-01-01':rejected+=1;continue
 if ident in seen:duplicates+=1;continue
 seen.add(ident)
 clean.append((ident,date,r['Sub-product'] or 'Unknown',r['Issue'] or 'Unknown',r['Company response to consumer'] or 'Unknown',r['Timely response?'] or 'Unknown',r['Company'],bool(r.get('Consumer complaint narrative','').strip())))
con=sqlite3.connect(root/'data/analytics.sqlite')
con.execute('DROP TABLE IF EXISTS complaints');con.execute('CREATE TABLE complaints(id TEXT PRIMARY KEY,received TEXT,subproduct TEXT,issue TEXT,response TEXT,timely TEXT,company TEXT,has_narrative INTEGER)')
con.executemany('INSERT INTO complaints VALUES(?,?,?,?,?,?,?,?)',clean);con.commit()
cube=con.execute('SELECT substr(received,1,7),subproduct,issue,response,timely,COUNT(*) FROM complaints GROUP BY 1,2,3,4,5').fetchall()
issues=con.execute('SELECT issue,COUNT(*) FROM complaints GROUP BY 1 ORDER BY 2 DESC').fetchall()
months=con.execute('SELECT substr(received,1,7),COUNT(*) FROM complaints GROUP BY 1 ORDER BY 1').fetchall()
known=sum(r[5] in ('Yes','No') for r in clean);yes=sum(r[5]=='Yes' for r in clean)
meta={'n':len(clean),'raw':len(rows),'duplicates':duplicates,'rejected':rejected,'knownTimely':known,'timelyYes':yes,'narrativeCount':sum(r[7] for r in clean),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'retrieved':'2026-10-14','period':'2025-01-01 to 2025-12-31','source':'https://www.consumerfinance.gov/data-research/consumer-complaints/','cube':cube}
(root/'dist/data.js').write_text('window.ANALYTICS='+json.dumps(meta)+';',encoding='utf-8')
(root/'data/summary.json').write_text(json.dumps({**meta,'cube':None,'issues':issues,'months':months},indent=2))
# Validate aggregates independently against cleaned rows.
assert sum(x[5] for x in cube)==len(clean)==con.execute('SELECT COUNT(*) FROM complaints').fetchone()[0]
assert len(seen)==len(clean)
assert sum(n for _,n in months)==len(clean)
assert sum(n for _,n in issues)==len(clean)
assert yes<=known<=len(clean)
for m,n in months:assert n==sum(r[1].startswith(m) for r in clean)
print(json.dumps({'n':len(clean),'duplicates':duplicates,'rejected':rejected,'timelyPct':100*yes/known,'issues':issues[:3],'months':months},indent=2))
print('Validation passed: IDs, date/product scope, monthly totals, issue totals, cube totals, response denominator.')
