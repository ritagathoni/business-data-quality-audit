import unittest
from src.audit import audit,sql_audit
class AuditTests(unittest.TestCase):
 def test_duplicates(self):self.assertTrue(any(x['type']=='duplicate_invoice_id' for x in audit([{'invoice_id':'A'},{'invoice_id':'A'}])))
 def test_pii(self):self.assertTrue(any(x['type']=='potential_email_pii' for x in audit([{'invoice_id':'A','notes':'test@example.com'}])))
 def test_sql(self):self.assertEqual(sql_audit([{'invoice_id':'X'},{'invoice_id':'X'}])[0]['count'],2)
if __name__=='__main__':unittest.main()
