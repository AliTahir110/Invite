(() => {
  function mount() {
    document.querySelectorAll('.event-photo-link').forEach(album => {
      const parent = album.parentElement;
      if (!parent || parent.querySelector('.photo-access-form')) return;
      parent.querySelector('.photo-access-link')?.remove();
      // Use a sibling of the paragraph: a form cannot be nested inside a <p>.
      const form = document.createElement('form');
      form.className = 'photo-access-form';
      form.innerHTML = '<label>Need photo access?<input type="email" name="email" autocomplete="email" inputmode="email" placeholder="Your email address" aria-label="Email address for photo access" maxlength="254" required></label><button type="submit">Request access on WhatsApp</button>';
      form.addEventListener('submit', event => {
        event.preventDefault();
        const input = form.elements.email;
        input.value = input.value.trim();
        if (!form.reportValidity()) return;
        const message = 'Hello! Please give me access to Zernab & Arman’s event photos. My email address is ' + input.value + '.';
        window.invitationMusic?.stop();
        window.open('https://wa.me/919151155786?text=' + encodeURIComponent(message), '_blank', 'noopener,noreferrer');
      });
      // Framer can render responsive duplicates; keep one form per text block.
      if (parent.nextElementSibling?.classList.contains('photo-access-form')) return;
      parent.insertAdjacentElement('afterend', form);
    });
  }
  new MutationObserver(mount).observe(document.body, {childList: true, subtree: true});
  mount();
})();
