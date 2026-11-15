(() => {
  function mount() {
    document.querySelectorAll('.framer-stokf1-container').forEach(host => {
      const parent = host.parentElement;
      if (!parent || parent.querySelector('.guest-rsvp')) return;
      const form = document.createElement('form');
      form.className = 'guest-rsvp';
      form.innerHTML = `<label>Your name<input name="guestName" autocomplete="name" placeholder="Enter your full name" maxlength="120" required></label><button type="submit"><svg aria-hidden="true" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M20.5 11.5a8.5 8.5 0 0 1-12.7 7.4L3 20l1.2-4.5a8.5 8.5 0 1 1 16.3-4Z"/><path d="M8 7c0 4 3 7 7 8l2-2-3-2-1 1-2-2 1-1-2-3Z"/></svg>Send your reply</button><p>WhatsApp will open with your reply ready.<br>Tap Send in WhatsApp to share it with us.</p>`;
      form.addEventListener('submit', event => {
        event.preventDefault();
        const input = form.elements.guestName;
        const name = input.value.trim();
        if (!name) { input.value = ''; input.reportValidity(); return; }
        window.invitationMusic?.stop();
        const message = `Hello! This is ${name}. Thank you for inviting me to Zernab & Arman's wedding celebrations. I would like to RSVP.`;
        window.open('https://wa.me/919151155786?text=' + encodeURIComponent(message), '_blank', 'noopener,noreferrer');
      });
      host.insertAdjacentElement('afterend', form);
    });
  }
  new MutationObserver(mount).observe(document.body, {childList:true, subtree:true});
  mount();
})();
