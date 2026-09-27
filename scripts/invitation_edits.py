"""Personalized family text, shared by the snapshot and runtime bundles."""
import re

def personalize(source):
    # Nikah countdown: 11 January 2027, 3:00 pm India Standard Time.
    source = source.replace('2026-03-21T00:00:00.000Z', '2027-01-11T15:00:00+05:30')
    source = source.replace('2026-05-21T00:00:00.000Z', '2027-01-11T15:00:00+05:30')
    # The mirrored countdown originally overwrote the supplied timestamp with a
    # whole UTC hour. Use the complete ISO timestamp so 3:00 pm IST is exact.
    source = source.replace(
        'D=new Date(t).setUTCHours(r)-+new Date',
        'D=+new Date(t)-+new Date'
    )
    # Invitation copy and family details.
    source = source.replace(
        'Lt. Mr. Tahir Hussain & Lt. Mrs. Hamida Bano',
        'Lt. Mr. Tahir Hussain & Lt. Mrs. Hamida Bano\\nLt. Mr. Mohsin Rizvi & Lt. Gunguna Rizvi'
    ).replace(
        'Lt. Mr. Tahir Hussain &amp; Lt. Mrs. Hamida Bano',
        'Lt. Mr. Tahir Hussain &amp; Lt. Mrs. Hamida Bano\nLt. Mr. Mohsin Rizvi &amp; Lt. Gunguna Rizvi'
    )
    # Keep this idempotent when the personalization script is rerun.
    source = source.replace(
        'Lt. Mr. Tahir Hussain & Lt. Mrs. Hamida Bano\\nLt. Mr. Mohsin Rizvi & Lt. Gunguna Rizvi\\nLt. Mr. Mohsin Rizvi & Lt. Gunguna Rizvi',
        'Lt. Mr. Tahir Hussain & Lt. Mrs. Hamida Bano\\nLt. Mr. Mohsin Rizvi & Lt. Gunguna Rizvi'
    ).replace(
        'Lt. Mr. Tahir Hussain &amp; Lt. Mrs. Hamida Bano\nLt. Mr. Mohsin Rizvi &amp; Lt. Gunguna Rizvi\nLt. Mr. Mohsin Rizvi &amp; Lt. Gunguna Rizvi',
        'Lt. Mr. Tahir Hussain &amp; Lt. Mrs. Hamida Bano\nLt. Mr. Mohsin Rizvi &amp; Lt. Gunguna Rizvi'
    )
    source = source.replace('Capt. Javed Patel & Mrs. Rubina Patel', '').replace('Capt. Javed Patel &amp; Mrs. Rubina Patel', '')
    source = source.replace('sKFuJb5xa:`Son of`', 'sKFuJb5xa:``')
    source = source.replace('>Son of<', '><')

    # RSVP contact and custom footer credit.
    source = source.replace('+44 7732795991', '+91 9454268942')
    source = source.replace('https://wa.me/91XXXXXXXXXX', 'https://wa.me/919454268942')
    source = source.replace('tel:+919454268942', 'https://wa.me/919454268942')
    source = source.replace('© Missing Piece 2026 ', 'Made by')
    source = source.replace('© Missing Piece 2026', 'Made by')
    source = source.replace('Get your wedding invite from', '')
    source = source.replace('https://www.missingpieceinvites.com', 'https://portfolio-website-h1jg.onrender.com')
    source = source.replace('missingpieceinvites.com', 'View portfolio')
    source = re.sub(
        r'(?:https://framerusercontent\.com/images/|/assets/[a-f0-9]+-)22xXcSSm9sQYXLb74vUWOaNwXY\.png(?:\?[^\s\"\x27`<>]*)?',
        '/assets/bridal-blessing.jpg', source)
    source = re.sub(
        r'(?:https://framerusercontent\.com/images/|/assets/[a-f0-9]+-)O07fRruEj5em3moPWz2blxIGqRI\.png(?:\?[^\s\"\x27`<>]*)?',
        '/assets/wedding-blessing.jpg', source)
    source = re.sub(
        r'(?:https://framerusercontent\.com/images/|/assets/[a-f0-9]+-)T1dORVl8kMLXNd7ShMJWzCpoHtM\.png(?:\?[^\s\"\x27`<>]*)?',
        '/assets/zernab-arman-nikkah.jpg', source)
    source = source.replace('Vintage car', 'Nikkah portrait')
    source = re.sub(
        r'(?:https://framerusercontent\.com/images/|/assets/[a-f0-9]+-)KLX9NKaAZPU198E9L0pwLoWDxeE\.jpg(?:\?[^\s\"\x27`<>]*)?',
        '/assets/zernab-arman.jpg', source)
    for ampersand in ('&amp;', '&'):
        removed = 'Lt. Syed Anwar Abbas Zaidi ' + ampersand + ' Mrs. Fakhrun Nisa'
        source = source.replace('\\n' + removed, '').replace('\n' + removed, '').replace(removed, '')
        source = source.replace('Dr. Tanveer Tahir ' + ampersand + ' Mrs. Zeba Tahir',
                                'Naved Tahir ' + ampersand + ' Uroos Rizvi')
    return source

def add_styles(source):
    if 'href="/invitation.css"' not in source:
        source = source.replace('</head>', '<link rel="stylesheet" href="/invitation.css"></head>')
    return source

if __name__ == '__main__':
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    for path in [root / 'scripts/source.html', *(root / 'public').rglob('*')]:
        if path.is_file() and path.suffix in ('.html', '.mjs', '.json'):
            source = path.read_text()
            updated = personalize(source)
            if path.suffix == '.html':
                updated = add_styles(updated)
            if updated != source:
                path.write_text(updated)
