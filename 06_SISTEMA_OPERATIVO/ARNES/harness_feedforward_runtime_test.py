#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
root = Path(__file__).resolve().parents[2]
payload = root / 'harness-feedforward.json'
consumer = root / '06_SISTEMA_OPERATIVO/ARNES/harness_feedforward_runtime.py'
context = root / '06_SISTEMA_OPERATIVO/ARNES/harness-runtime-context.json'
subprocess.run([sys.executable, str(consumer)], cwd=root, check=True)
p = json.loads(payload.read_text(encoding='utf-8'))
c = json.loads(context.read_text(encoding='utf-8'))
assert c['guide_id'] == p['guide_id']
assert c['feedforward_sha256'] == p['sha256']
assert c['guide_content'] == p['guide_content']
assert c['preparation_status'] == 'CONSUMED_FOR_RUNTIME_CONTEXT'
assert c['execution'] == 'NOT_EXECUTED_BY_CONSUMER'
assert c['authority'] == 'NOT_GRANTED'
print('FEEDFORWARD_RUNTIME_CONSUMED')
