from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
m=json.loads((p/'manifest.json').read_text())
for rel,expected in m.items():
 actual=hashlib.sha256((p/rel).read_bytes()).hexdigest()
 assert actual==expected,rel
print('Manifest verified:',len(m),'files')
