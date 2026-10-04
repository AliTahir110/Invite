"""Render the four wedding events in both static HTML and the Framer runtime."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import re
import json

EVENTS = [
    ('Manjha', 'Saturday, 9th January, 2027', 'Hotel Charans Habibullah Estate, 11, Hazratganj, Lucknow', '6 pm', 'https://maps.app.goo.gl/hKYXudu8ky3fgNrx6'),
    ('Mehndi', 'Sunday, 10th January, 2027', 'Khaas Baradari, Hussariya Crossing, Gomti Nagar, Lucknow', '', 'https://maps.app.goo.gl/LhXVhTxJ7RSpEKPeA'),
    ('Nikah Ceremony', 'Monday, 11th January, 2027', 'Shah Najaf Imam Bara, Hazratganj, Lucknow', '3 pm', 'https://www.google.com/maps/place/Shah+Najaf+Imam+Bara/@26.8578032,80.9436443,17z/data=!3m1!4b1!4m6!3m5!1s0x399bfd0b25000a27:0xe9fe770ae5a2e55b!8m2!3d26.8578032!4d80.9462192!16s%2Fm%2F0wzxwgm?hl=en-IN&entry=ttu&g_ep=EgoyMDI2MDkyMy4wIKXMDSoASAFQAw%3D%3D'),
    ('Nikah Reception', 'Tuesday, 12th January, 2027', 'Balrampur Gardens, Ashok Marg, Hazratganj, Lucknow', '7:30 pm', 'https://www.google.com/maps/place/Balrampur+Garden/@26.854854,80.9475689,17z/data=!3m1!4b1!4m6!3m5!1s0x399bfd0c3ba16e03:0x3255312237e4f1cc!8m2!3d26.854854!4d80.9501438!16s%2Fg%2F1tykssny?entry=ttu&g_ep=EgoyMDI2MDkyMy4wIKXMDSoASAFQAw%3D%3D'),
]
TEMPLATES = json.loads(Path(__file__).with_name('event-templates.json').read_text())

def patch_module(source):
    marker = 's(yt,{className:`framer-1okr3uu`,"data-framer-name":`Events`,children:['
    if marker not in source:
        return source
    start = source.index(marker) + len(marker)
    end = source.index(']}),o(_', start)
    cards = []
    for index, (name, date, venue, time, url) in enumerate(EVENTS):
        tile = TEMPLATES['module'].replace('`Reception`', f'`{name}`').replace('`Card 6`', f'`{name}`')
        tile = tile.replace('hs4t8FNOD', f'weddingEvent{index}')
        tile = tile.replace('Friday, 22nd May', date).replace('Chokhi Dhani, SW11 8AW', venue).replace('5:30 pm onwards', time)
        tile = tile.replace('b0Odmcs_Z:', f'Ze39EmOzQ:`{url}`,b0Odmcs_Z:')
        cards.append(tile)
    return source[:start] + ','.join(cards) + source[end:]

class EventParser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer('\n', source))
        self.stack = []
        self.events = []

    def position(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag in ('img','br','link','meta','input','source','hr','wbr','area','base','embed','param','track','col'):
            return
        self.stack.append({'tag': tag, 'attrs': dict(attrs), 'start': self.position(), 'children': []})

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1]['tag'] != tag:
            return
        node = self.stack.pop()
        node['end'] = self.position() + len(f'</{tag}>')
        if self.stack:
            self.stack[-1]['children'].append(node)
        if node['attrs'].get('data-framer-name') == 'Events':
            self.events.append(node)

def patch_html(source):
    source = re.sub(r'<style id="additional-event-tiles">.*?</style>', '', source)
    parser = EventParser(source)
    parser.feed(source)
    assert len(parser.events) == 2
    edits = []
    for section, originals in zip(parser.events, TEMPLATES['html']):
        cards = []
        for name, date, venue, time, url in EVENTS:
            for original in originals:
                tile = original.replace('"Card 6"', f'"{name}"')
                tile = re.sub(r'(data-framer-name="Event name"[^>]*><p[^>]*>).*?(</p>)', lambda m: m[1] + name + m[2], tile, flags=re.S)
                tile = tile.replace('Friday, 22nd May', date).replace('Chokhi Dhani, SW11 8AW', venue).replace('5:30 pm onwards', time)
                tile = tile.replace('<a class="framer-text framer-styles-preset-s3v1ib"', f'<a href="{escape(url, quote=True)}" class="framer-text framer-styles-preset-s3v1ib"')
                cards.append(tile)
        start = source.index('>', section['start']) + 1
        edits.append((start, section['end'] - 6, ''.join(cards)))
    for start, end, cards in sorted(edits, reverse=True):
        source = source[:start] + cards + source[end:]
    return source

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    for page in (root / 'public/index.html', root / 'scripts/source.html'):
        page.write_text(patch_html(page.read_text()))
    for module in (root / 'public/assets').glob('*.mjs'):
        source = module.read_text()
        updated = patch_module(source)
        if updated != source:
            module.write_text(updated)
            print('Updated', module.name)
