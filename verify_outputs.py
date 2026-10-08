"""Check saved experimental accounting and create a portable submission archive."""
import csv
from pathlib import Path
import zipfile
root = Path(__file__).resolve().parent
with (root/'results/trials.csv').open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 540, 'Default configuration should produce 540 rows'
for r in rows:
    assert 0 <= int(r['delivered']) <= int(r['sent'])
    assert abs(float(r['pdr_pct'])+float(r['loss_pct'])-100) < 1e-8
    assert abs(float(r['throughput_mbps'])-.24*float(r['pdr_pct'])/100) < 1e-8
assert len(list((root/'figures').glob('*.png'))) == 9
with zipfile.ZipFile(root/'Assessment6_QoS_Routing.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.rglob('*')):
        if not p.is_file() or any(x in {'.venv','.git','__pycache__'} for x in p.relative_to(root).parts):
            continue
        if p.suffix == '.zip':
            continue
        z.write(p,Path('Assessment6_QoS_Routing')/p.relative_to(root))
print('Verified 540 trial rows, accounting identities, and 9 figures. Submission ZIP created.')
