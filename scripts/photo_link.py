"""Replace guest-information introduction with the event photo album link."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OLD = 'To help you feel at ease and enjoy every moment of the celebrations, we’ve gathered a few thoughtful details we’d love for you to know before the big day.'
MESSAGE = 'Relive the joy of our celebrations. Photos from all our events will be uploaded here for you to enjoy.'
URL = 'https://drive.google.com/drive/folders/1OLiaYEzrdKpJLnoMVpSpJ5Bt3Y-sFna9?usp=sharing'
for path in [ROOT / 'scripts/source.html', *(ROOT / 'public').rglob('*')]:
    if not path.is_file() or path.suffix not in ('.html', '.mjs', '.json'):
        continue
    source = path.read_text()
    if path.suffix == '.html':
        updated = source.replace('>' + OLD + '</p>', '>' + MESSAGE + '<br><a class="event-photo-link" href="' + URL + '" target="_blank" rel="noopener noreferrer">View event photos</a></p>')
    elif path.suffix == '.mjs':
        # The generated page uses o() as its JSX factory in the active route.
        # Infer each paragraph's factory to preserve other mirrored routes too.
        pattern = r'([a-zA-Z_$][\w$]*)\(`p`,\{[^{}]*(?:style:\{[^{}]*\},)?children:`' + re.escape(OLD) + r'`'
        def replace(match):
            factory = match[1]
            children = '[`' + MESSAGE + '`, ' + factory + '(`br`,{}), ' + factory + '(`a`,{className:`event-photo-link`,href:`' + URL + '`,target:`_blank`,rel:`noopener noreferrer`,children:`View event photos`})]'
            return match[0].replace('children:`' + OLD + '`', 'children:' + children)
        updated = re.sub(pattern, replace, source)
    else:
        updated = source.replace(OLD, MESSAGE)
    if updated != source:
        path.write_text(updated)
        print(path.relative_to(ROOT))
