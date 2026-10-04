(() => {
  if (window.invitationMusic) return;
  const audio = new Audio('/assets/966a906a68fe-wIT09MUVvJeniSMnCEPNcvavO4.mp3');
  audio.loop = true;
  audio.volume = 0.7;
  audio.preload = 'auto';
  audio.autoplay = true;
  let wanted = true;
  let suspended = document.hidden;
  let generation = 0;
  let pending = null;
  const playIcon = '<path d="M4 2 L14 8 L4 14 Z" fill="#333"/>';
  const pauseIcon = '<path d="M3 2h4v12H3zM10 2h4v12h-4z" fill="#333"/>';
  function update() {
    document.querySelectorAll('.framer-audio-icon').forEach(icon => {
      const playing = !audio.paused;
      const label = playing ? 'Pause music' : 'Play music';
      if (icon.getAttribute('aria-label') !== label) {
        icon.setAttribute('aria-label', label);
        icon.innerHTML = playing ? pauseIcon : playIcon;
        icon.setAttribute('role', 'button');
        icon.setAttribute('tabindex', '0');
      }
    });
  }
  function stop() {
    suspended = true;
    generation++;
    audio.pause();
    document.querySelectorAll('audio.framer-audio').forEach(other => other.pause());
    update();
  }
  async function start() {
    if (!wanted || suspended || document.hidden || pending || !audio.paused) return;
    const ticket = generation;
    pending = audio.play();
    try {
      await pending;
      if (ticket !== generation || suspended || document.hidden || !wanted) audio.pause();
    } catch (_) { /* Browser autoplay policy may require a gesture. */ }
    finally { pending = null; update(); }
  }
  function resume() {
    if (document.hidden) return;
    suspended = false;
    start();
  }
  function toggle(event) {
    event.preventDefault();
    event.stopImmediatePropagation();
    wanted = audio.paused;
    if (wanted) resume(); else stop();
  }
  window.invitationMusic = { stop };
  const unlock = event => {
    if (event.target.closest?.('.framer-bt19rz-container, a[href], .framer-stokf1-container')) return;
    start();
  };
  document.addEventListener('pointerdown', unlock, { capture: true, passive: true });
  document.addEventListener('touchend', unlock, { capture: true, passive: true });
  document.addEventListener('click', event => {
    if (event.target.closest?.('.framer-bt19rz-container')) return toggle(event);
    const link = event.target.closest?.('a[href]');
    const whatsapp = event.target.closest?.('.framer-stokf1-container');
    if (whatsapp || (link && new URL(link.href, location.href).origin !== location.origin)) {
      stop();
      return;
    }
    start();
  }, true);
  document.addEventListener('keydown', event => {
    if (['Enter', ' '].includes(event.key) && event.target.closest?.('.framer-bt19rz-container')) toggle(event);
    else unlock(event);
  }, true);
  document.addEventListener('visibilitychange', () => document.hidden ? stop() : resume());
  document.addEventListener('freeze', stop);
  window.addEventListener('blur', stop);
  window.addEventListener('pagehide', stop);
  window.addEventListener('beforeunload', stop);
  window.addEventListener('focus', resume);
  window.addEventListener('pageshow', resume);
  audio.addEventListener('play', () => {
    if (suspended || document.hidden || !wanted) audio.pause();
    update();
  });
  audio.addEventListener('pause', update);
  audio.addEventListener('canplay', start);
  window.addEventListener('load', start);
  new MutationObserver(update).observe(document.body, { childList: true, subtree: true });
  update();
  start();
})();
