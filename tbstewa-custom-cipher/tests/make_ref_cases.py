"""Generate reference (key, message, init, ciphertext, S-box) cases from the author's crypt.py.
Usage: python3 -I make_ref_cases.py ref_cases.json  ; then: node test_lab_engine.js ../report.html ref_cases.json"""
import json, sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, '..', 'crypt-test', 'crypt.py')).read().split('# --- Test & Verification ---')[0]
ns = {}; exec(src, ns)          # author's functions, reviewed earlier; test block excluded
cases = []
keys = ['erxxdmjfirc6mk5dfrf86jsi', 'SuperSecretPassphrase', '', 'a', 'é ü 日本 🐝', 'x'*200, 'correct horse battery staple', 'k3y!@#$%^&*()']
msgs = ['test text', 'According to all known laws of aviation, there is no way a bee should be able to fly.', '~ !"#$%&\'()*+,-./0123456789:;<=>?@AZ[\\]^_`az{|}', ' ', 'Hello, World!']
for ki, key in enumerate(keys):
    fwd, inv = ns['generate_sbox'](key)
    for mi, msg in enumerate(msgs):
        init = [45, 0, 94, 21, 7][(ki + mi) % 5]
        enc = ns['encrypt'](msg, key, init)
        assert ns['decrypt'](enc, key, init) == msg
        cases.append({'key': key, 'msg': msg, 'init': init, 'enc': enc, 'forward': fwd})
json.dump(cases, open(sys.argv[1], 'w'))
print(len(cases), 'cases; sample key self-test:', ns['encrypt']('test text', 'erxxdmjfirc6mk5dfrf86jsi', 45))
