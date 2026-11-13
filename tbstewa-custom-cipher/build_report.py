#!/usr/bin/env python3
"""Render report.html (self-contained) from report_data.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, 'report_data.json')))
blob = json.dumps(data).replace('<', '\\u003c')
html = open(os.path.join(HERE, 'report_template.html')).read().replace('__DATA__', blob)
open(os.path.join(HERE, 'report.html'), 'w').write(html)
print('wrote report.html', len(html), 'bytes')
