"""Build a separate invitation with only the Nikkah Ceremony event."""
from pathlib import Path
import re
import event_tiles

root = Path(__file__).resolve().parents[1]
public = root / 'public'
source = (public / 'index.html').read_text()
bootstrap_name = re.search(r'src="/assets/([^"]+script_main[^\"]+\.mjs)"', source)[1]
bootstrap = (public / 'assets' / bootstrap_name).read_text()
module_name = re.search(r'/assets/([^`]+m5y5yj13nj[^`]+\.mjs)', bootstrap)[1]
event_tiles.EVENTS = [event for event in event_tiles.EVENTS if event[0] == 'Nikkah Ceremony']
assert len(event_tiles.EVENTS) == 1
module = event_tiles.patch_module((public / 'assets' / module_name).read_text())
(public / 'assets/nikkah-only-page.mjs').write_text(module)
bootstrap = bootstrap.replace(module_name, 'nikkah-only-page.mjs').replace('path:`/bride/mehendireception`', 'path:`/nikkah.html`')
(public / 'assets/nikkah-only-main.mjs').write_text(bootstrap)
page = event_tiles.patch_html(source).replace(module_name, 'nikkah-only-page.mjs').replace(bootstrap_name, 'nikkah-only-main.mjs')
page = page.replace('>Nikkah Ceremony</p>', '>Nikkah<br>Ceremony</p>')
(public / 'nikkah.html').write_text(page)
print('Created public/nikkah.html with one event.')
