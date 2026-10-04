const vm = require('node:vm');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const events = {};
let player, instances = 0, resolvePlay;
class Audio {
  constructor() { instances++; player = this; this.paused = true; this.events = {}; }
  addEventListener(name, fn) { this.events[name] = fn; }
  play() { this.paused = false; this.events.play?.(); return new Promise(r => { resolvePlay = r; }); }
  pause() { this.paused = true; this.events.pause?.(); }
}
const document = { hidden: false, body: {}, querySelectorAll: () => [], addEventListener: (n,f) => { events[n] = f; } };
const window = { addEventListener: (n,f) => { events[n] = f; } };
const context = vm.createContext({ Audio, document, window, URL, location: {origin:'https://invite.test',href:'https://invite.test'}, MutationObserver: class { observe() {} } });
const source = fs.readFileSync('public/music.js','utf8');
(async () => {
 vm.runInContext(source, context);
 vm.runInContext(source, context);
 assert.equal(instances, 1);
 events.click({target:{closest: selector => selector === 'a[href]' ? {href:'https://maps.google.com'} : null}});
 assert.equal(player.paused, true);
 document.hidden = true; events.visibilitychange();
 resolvePlay(); await new Promise(setImmediate);
 assert.equal(player.paused, true, 'pending play must not survive navigation');
 document.hidden = false; events.visibilitychange();
 resolvePlay(); await new Promise(setImmediate);
 assert.equal(player.paused, false);
 assert.equal(instances, 1);
 events.pagehide(); assert.equal(player.paused, true);
 events.pageshow(); resolvePlay(); await new Promise(setImmediate);
 events.blur(); assert.equal(player.paused, true);
 console.log('PASS: one player, external navigation, pending play cancellation, return, pagehide and blur');
})();
