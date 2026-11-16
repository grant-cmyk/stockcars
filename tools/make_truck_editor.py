"""Build docs/tools/truck_editor.html: the 24 x 24 truck pixel editor, loaded with tools/truck_art.txt
(one shared BODY and each weapon drawn over it). Publish the result as a Claude artifact for Grant."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); DOCS = os.path.join(HERE, '..', 'docs', 'tools')
t = open(os.path.join(HERE, 'truck_art.txt')).read()
art = {m.group(1): m.group(2).split() for m in re.finditer(r'== (\w+) ==\n((?:[Xo.]+\n)+)', t)}
assert 'BODY' in art and all(len(r) == 24 for g in art.values() for r in g)
page = open(os.path.join(DOCS, 'truck_editor.template.html')).read().replace('__ART__', json.dumps(art, separators=(',', ':')))
open(os.path.join(DOCS, 'truck_editor.html'), 'w').write(page); print('ok', list(art))
