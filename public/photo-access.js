(() => {
  const message = 'Hello! Could you please give me access to Zernab & Arman’s event photos?';
  const href = 'https://wa.me/919151155786?text=' + encodeURIComponent(message);
  function mount() {
    document.querySelectorAll('.event-photo-link').forEach(album => {
      const parent = album.parentElement;
      if (!parent || parent.querySelector('.photo-access-link')) return;
      const link = document.createElement('a');
      link.className = 'photo-access-link';
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
