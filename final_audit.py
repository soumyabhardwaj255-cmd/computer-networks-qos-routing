"""Reproduce the saved default experiment in a clean temporary environment.

Never overwrites the original results, figures, configuration or simulation code.
Writes evidence to audit/. Requires Python 3.12, venv and package-index access.
"""
import ast
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'audit'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    protected = [ROOT/'config.json', ROOT/'run.py', ROOT/'prepare.py', ROOT/'requirements.txt',
                 ROOT/'docs/ABSTRACT.md']
    protected += [p for folder in ['src','tests','results','figures']
                  for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    before = {str(p.relative_to(ROOT)): digest(p) for p in protected}
    (OUT/'preserved_files_before.json').write_text(json.dumps(before,indent=2))
    evidence = {'utc':datetime.now(timezone.utc).isoformat(), 'python':sys.version,
                'checks':[], 'manual':['Packet Tracer construction, execution, .pkt and screenshots']}
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE':'1', 'MPLBACKEND':'Agg'}

    def run(args, cwd, logfile):
        print('Running: '+logfile,flush=True)
        result = subprocess.run([str(a) for a in args],cwd=cwd,env=env,
                                stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (OUT/logfile).write_text(result.stdout,encoding='utf-8')
        if result.returncode:
            print(result.stdout,flush=True)
            raise RuntimeError(f'{logfile} failed with exit code {result.returncode}')
        evidence['checks'].append({'check':logfile,'status':'PASS'})
        return result.stdout

    # TemporaryDirectory cleans up only its own newly created directory.
    with tempfile.TemporaryDirectory(prefix='cn_qos_audit_') as temp:
        temp = Path(temp)
        project = temp/'project'
        project.mkdir()
        for name in ['run.py','prepare.py','verify_outputs.py','config.json','requirements.txt']:
            shutil.copy2(ROOT/name,project/name)
        for name in ['src','tests','packet_tracer']:
            shutil.copytree(ROOT/name,project/name,ignore=shutil.ignore_patterns('__pycache__'))
        runtime = temp/'venv'
        run([sys.executable,'-m','venv',runtime],temp,'01_environment.log')
        python = runtime/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
        run([python,'-m','pip','install','-r',project/'requirements.txt'],temp,'02_install.log')
        run([python,'-m','pip','check'],project,'03_pip_check.log')
        run([python,'-m','pip','freeze'],project,'04_dependencies.log')
        for p in project.rglob('*.py'):
            ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
        evidence['checks'].append({'check':'Python syntax parsing','status':'PASS'})
        run([python,'-m','unittest','discover','-s','tests','-v'],project,'05_tests.log')
        run([python,'run.py'],project,'06_reproduction.log')
        files=['trials.csv','summary.csv','paired_differences.csv','dynamic_routes.csv','congestion_sweep.csv','FINAL_RESULTS.md']
        comparisons=[]
        for name in files:
            original, regenerated = ROOT/'results'/name,project/'results'/name
            assert original.read_bytes()==regenerated.read_bytes(), f'Reproduction mismatch: {name}'
            comparisons.append({'file':name,'sha256':digest(original),'status':'BYTE_IDENTICAL'})
        evidence['reproduced_files']=comparisons
        with (project/'results/trials.csv').open(newline='') as f:
            evidence['trial_rows']=len(list(csv.DictReader(f)))
        assert evidence['trial_rows']==540
        original_meta=json.loads((ROOT/'results/run_metadata.json').read_text())
        new_meta=json.loads((project/'results/run_metadata.json').read_text())
        assert original_meta['config']==new_meta['config']
        assert original_meta['config_sha256']==new_meta['config_sha256']
        evidence['checks'].append({'check':'Metadata configuration/hash (timestamp intentionally differs)','status':'PASS'})
        figures=sorted(p.name for p in (ROOT/'figures').glob('*.png'))
        assert len(figures)==9
        assert figures==sorted(p.name for p in (project/'figures').glob('*.png'))
        # PIL is a Matplotlib dependency, available only in the new environment.
        run([python,'-c',"from pathlib import Path; from PIL import Image; "
             "files=list(Path('figures').glob('*.png')); "
             "[(Image.open(p).verify()) for p in files]; print('All',len(files),'PNG files decode successfully.')"],
            project,'07_figures.log')
        evidence['figures']=[{'file':name,'byte_identical':digest(ROOT/'figures'/name)==digest(project/'figures'/name)} for name in figures]
        run([python,'packet_tracer/review_consistency.py'],project,'08_consistency.log')
        run([python,'verify_outputs.py'],project,'09_legacy_verifier.log')
        # Check default generator only in the disposable copy, after reproduction.
        config_hash=digest(project/'config.json')
        router_hashes={n:digest(project/'packet_tracer'/f'{n}.txt') for n in ['R1','R2','R3','R4']}
        run([python,'prepare.py'],project,'10_prepare.log')
        assert digest(project/'config.json')==config_hash
        assert all(digest(project/'packet_tracer'/f'{n}.txt')==h for n,h in router_hashes.items())
        evidence['checks'].append({'check':'prepare.py reproduces default config and router files','status':'PASS'})
    after={name:digest(ROOT/name) for name in before}
    assert before==after, 'Protected original files changed'
    evidence['checks'].append({'check':'Original source/config/tests/results/figures/abstract unchanged','status':'PASS'})
    evidence['status']='PASS'
    (OUT/'audit.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print('PASS: clean install, tests, full reproduction, consistency and preservation checks.',flush=True)


if __name__=='__main__':
    main()
