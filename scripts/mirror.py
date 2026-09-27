"""Create a local mirror of the published invitation and its dependencies."""
import concurrent.futures
import hashlib
import html
import json
import pathlib
import re
import subprocess
import urllib.parse
from event_tiles import patch_html, patch_module
from invitation_edits import personalize, add_styles

ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
SOURCE = 'https://splendid-embeds-956985.framer.app/bride/mehendireception'
URLS = re.compile(r'https://(?:framerusercontent\.com|fonts\.gstatic\.com)/[^\s\"\'`<>\\)]+')
MODULES = re.compile(r'''["'`](\.?\.?/[^"'`]+\.mjs(?:\?[^"'`]*)?)["'`]''')
mapping = {}
contents = {}

def local_path(url):
    p = urllib.parse.urlsplit(url)
    name = pathlib.PurePosixPath(p.path).name
    return '/assets/' + hashlib.sha256(url.encode()).hexdigest()[:12] + '-' + name

def fetch(url):
    target = PUBLIC / mapping[url].lstrip('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['curl', '-f', '-sS', '-L', '--retry', '2', '--max-time', '90', url, '-o', str(target)], check=True)
    if target.suffix in ('.mjs', '.css', '.js'):
        return url, target.read_text()
    return url, None

page = (ROOT / 'scripts' / 'source.html').read_text()
pending = {html.unescape(u) for u in URLS.findall(page)}
while pending:
    for url in pending:
        mapping[url] = local_path(url)
    print(f'Downloading {len(pending)} assets ({len(mapping)} total)', flush=True)
    found = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        for url, source in pool.map(fetch, sorted(pending)):
            if source is not None:
                contents[url] = source
                found.update(html.unescape(u) for u in URLS.findall(source) if re.search(r'\.(?:mjs|js|css|png|jpg|jpeg|webp|svg|woff2?|mp3)(?:\?|$)', u))
                found.update(urllib.parse.urljoin(url, u) for u in MODULES.findall(source))
    pending = found - mapping.keys()

def rewrite(source):
    source = personalize(source)
    source = patch_module(source)
    source = source.replace('autoPlay:H,onLoadedMetadata:U', 'autoPlay:!1,onLoadedMetadata:U')
    # Responsive copies must not play simultaneously or leave hidden audio running.
    source = source.replace(
        'le=()=>{ae&&I.current.play().catch(e=>{})},de=()=>{var e,t;I.current.pause(),',
        'le=()=>{ae&&I.current.parentElement?.getClientRects().length&&(ce(),I.current.play().catch(e=>{}))},de=()=>{var e,t;ce(),'
    )
    source = source.replace('FarazGotHisTasha', 'ArmanGotHisZernab')
    def rename(match):
        name = {'mantasha': 'Zernab', 'faraz': 'Arman'}[match.group().lower()]
        return name.upper() if match.group().isupper() else name.lower() if match.group().islower() else name
    source = re.sub('mantasha|faraz', rename, source, flags=re.I)
    for url in sorted(mapping, key=len, reverse=True):
        source = source.replace(url, mapping[url]).replace(html.escape(url, quote=False), mapping[url])
    return source

for url, source in contents.items():
    source = MODULES.sub(lambda m: m.group(0).replace(m.group(1), mapping.get(urllib.parse.urljoin(url, m.group(1)), m.group(1))), source)
    (PUBLIC / mapping[url].lstrip('/')).write_text(rewrite(source))

# Analytics and editor tools are unnecessary in the local copy.
page = re.sub(r'<script\b[^>]*src="https://events\.framer\.com/[^>]*></script>', '', page)
page = re.sub(r'<script>try\{if\(localStorage\.get\("__framer_force_showing_editorbar_since"\).*?</script>', '', page, flags=re.S)
page = re.sub(r'<link\b[^>]*rel="canonical"[^>]*>', '', page)
(PUBLIC / 'index.html').write_text(add_styles(patch_html(rewrite(page))))
(ROOT / 'asset-manifest.json').write_text(json.dumps({'source': SOURCE, 'assets': mapping}, indent=2))
print(f'Finished: {len(mapping)} local assets', flush=True)
