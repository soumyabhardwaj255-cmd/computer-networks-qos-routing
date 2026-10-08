"""Validate documents and assemble a clean final submission without changing results."""
import ast
import csv
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'submission'/'project'
ZIP = ROOT/'FINAL_Computer_Networks_Project.zip'
TOP = ['README.md','requirements.txt','config.json','run.py','prepare.py','verify_outputs.py',
       'final_audit.py','package_project.py','FINAL_CHECKLIST.md']
FOLDERS = ['src','results','figures','tests','docs','packet_tracer','audit']


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_files():
    files=[ROOT/name for name in TOP]
    for folder in FOLDERS:
        files += [p for p in (ROOT/folder).rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.zip'}]
    return sorted(files)


def main():
    expected=json.loads((ROOT/'audit/preserved_files_before.json').read_text())
    assert all(digest(ROOT/name)==value for name,value in expected.items()), 'Protected originals changed'
    audit=json.loads((ROOT/'audit/audit.json').read_text())
    assert audit['status']=='PASS' and audit['trial_rows']==540
    assert all(r['status']=='BYTE_IDENTICAL' for r in audit['reproduced_files'])
    needed=['REPORT.md','VIVA.md','ASSESSMENT6.md','ABSTRACT.md','RESULTS_SUMMARY.md','LITERATURE.md','CONFIGURATION.md']
    assert all((ROOT/'docs'/n).is_file() for n in needed)
    report=(ROOT/'docs/REPORT.md').read_text(encoding='utf-8')
    summary=(ROOT/'docs/RESULTS_SUMMARY.md').read_text(encoding='utf-8')
    for section in ['Abstract','Introduction','Problem statement','Objectives','Existing work','Gap identified',
                    'Network model','Proposed methodology','Baseline algorithm','QoS cost formulation',
                    'Proposed algorithm','Pseudocode','Flowchart','Experimental setup','Metrics and statistics',
                    'Results','Discussion and trade-offs','Limitations','Conclusion','Future scope','References']:
        assert re.search(r'^#{2,3} '+re.escape(section),report,re.M), section
    with (ROOT/'results/summary.csv').open(newline='') as f:
        for row in csv.DictReader(f):
            metrics=['delay_ms','loss_pct','throughput_mbps','pdr_pct','hops','qos_cost','static_cost']
            line='| '+row['condition']+' | '+row['algorithm']+' | '+' | '.join(f'{float(row[m]):.4f}' for m in metrics)+' |'
            assert line in report and line in summary, 'Report/summary table mismatch'
    with (ROOT/'results/congestion_sweep.csv').open(newline='') as f:
        for row in csv.DictReader(f):
            line='| '+row['utilization']+' | '+row['algorithm']+' | '+' | '.join(f'{float(row[m]):.4f}' for m in metrics[:-1])+' |'
            assert line in summary, 'Sweep table mismatch'
    files=source_files()
    for p in files:
        assert not p.is_symlink(), f'Unexpected symlink: {p}'
        if p.suffix=='.py':
            ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
        if p.suffix=='.md':
            body=p.read_text(encoding='utf-8-sig')
            for target in re.findall(r'\]\(([^)]+)\)',body):
                if '://' in target or target.startswith('#'):
                    continue
                path=target.split('#',1)[0].strip('<>')
                assert (p.parent/path).exists(), f'Broken local link in {p}: {target}'
    review={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS',
            'checks':['Protected originals unchanged','Required report sections and documents present',
                      'Summary/sweep tables agree with saved CSV at displayed precision',
                      'Local Markdown links resolve','All included Python parses',
                      'Clean allowlist excludes virtual environments, caches, old archives and Git metadata'],
            'manual':['Packet Tracer execution, genuine .pkt, genuine screenshots']}
    (ROOT/'audit/package_validation.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
    files=source_files()
    intended={p.relative_to(ROOT) for p in files}|{Path('MANIFEST_SHA256.json')}
    if STAGE.exists():
        extra=[p for p in STAGE.rglob('*') if p.is_file() and p.relative_to(STAGE) not in intended]
        if extra:
            raise RuntimeError('Unexpected files in staging; inspect before rebuilding: '+str(extra))
    STAGE.mkdir(parents=True,exist_ok=True)
    for p in files:
        destination=STAGE/p.relative_to(ROOT)
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,destination)
    manifest={p.relative_to(ROOT).as_posix():digest(p) for p in files}
    (STAGE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(STAGE.rglob('*')):
            if p.is_file(): archive.write(p,Path('project')/p.relative_to(STAGE))
    with zipfile.ZipFile(ZIP) as archive:
        assert archive.testzip() is None
        for name, value in manifest.items():
            assert hashlib.sha256(archive.read('project/'+name)).hexdigest()==value
        assert len(archive.namelist())==len(manifest)+1
    print(f'PASS: {len(manifest)} files plus SHA-256 manifest, archive integrity and contents verified.')
    print('Folder: '+str(STAGE))
    print('Archive: '+str(ZIP))
    print('Only Packet Tracer construction/verification, native .pkt and real screenshots remain manual.')


if __name__=='__main__':
    main()
