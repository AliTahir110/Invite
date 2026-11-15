(() => {
  const message = 'Hello! Could you please give me access to Zernab & Arman’s event photos?';
  const href = 'https://wa.me/919151155786?text=' + encodeURIComponent(message);
  function mount() {
    document.querySelectorAll('.event-photo-link').forEach(album => {
      const parent = album.parentElement;
      if (!parent || parent.querySelector('.photo-access-link')) return;
      const link = document.createElement('a');
      link.className = 'photo-access-link';
      // Keep the link styled even when a browser reuses an older stylesheet.
      Object.assign(link.style, {
        display: 'block', width: 'fit-content', maxWidth: '100%',
        margin: '14px auto 0', padding: '6px 0',
        fontSize: '14px', lineHeight: '1.5', textAlign: 'center',
        fontFamily: 'inherit', textUnderlineOffset: '3px'
      });
      link.style.setProperty('color', '#555a25', 'important');
      link.style.setProperty('text-decoration', 'underline', 'important');
      link.href = href;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = 'Need access? Message us on WhatsApp';
      link.addEventListener('click', () => window.invitationMusic?.stop());
      album.insertAdjacentElement('afterend', link);
    });
  }
  new MutationObserver(mount).observe(document.body, {childList: true, subtree: true});
  mount();
})();
