"""Synthetic operational-data audit with no external dependencies."""
import json,re,sqlite3
from pathlib import Path

def audit(records):
    issues=[];seen=set();totals={}
    for r in records:
        rid=r.get('invoice_id','UNKNOWN')
        if not rid:issues.append({'id':rid,'type':'missing_invoice_id'})
        if rid in seen:issues.append({'id':rid,'type':'duplicate_invoice_id'})
        seen.add(rid)
        if not isinstance(r.get('amount'),(int,float)) or isinstance(r.get('amount'),bool):
            issues.append({'id':rid,'type':'amount_not_numeric'})
        elif r['amount']<0:issues.append({'id':rid,'type':'negative_amount'})
        if r.get('currency') not in {'KES','USD'}:issues.append({'id':rid,'type':'unexpected_currency'})
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',str(r.get('date',''))):
            issues.append({'id':rid,'type':'date_format'})
        if re.search(r'\b[\w.%-]+@[\w.-]+\.[A-Za-z]{2,}\b',str(r.get('notes',''))):
            issues.append({'id':rid,'type':'potential_email_pii'})
    return issues

def sql_audit(records):
    db=sqlite3.connect(':memory:')
    db.execute('CREATE TABLE invoices (invoice_id TEXT, supplier TEXT, amount REAL)')
    db.executemany('INSERT INTO invoices VALUES (?,?,?)',[(r.get('invoice_id'),r.get('supplier'),r.get('amount') if isinstance(r.get('amount'),(int,float)) else None) for r in records])
    duplicates=db.execute('SELECT invoice_id, COUNT(*) FROM invoices GROUP BY invoice_id HAVING COUNT(*)>1').fetchall()
    db.close()
    return [{'invoice_id':i,'count':c} for i,c in duplicates]

if __name__=='__main__':
    records=json.loads(Path('data/synthetic_invoices.json').read_text())
    print(json.dumps({'records':len(records),'issues':audit(records),'duplicates_sql':sql_audit(records)},indent=2))
