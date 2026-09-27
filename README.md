# Zernab & Arman Wedding Invitation

A responsive wedding invitation for Zernab and Arman, with event details, map links, RSVP information, music controls, and a live countdown to 11 January 2027.

## Run

With Node.js installed:

```sh
npm run dev
```

Open http://localhost:3000/bride/mehendireception (the root URL works too).
No npm dependencies or installation step are required. Set `PORT` to use another port.

## Files

- `public/index.html`: original published markup and responsive styles.
- `public/assets/`: 134 local images, fonts, audio files, and JavaScript modules.
- `asset-manifest.json`: original asset URLs mapped to local files.
- `server.js`: dependency-free local web server.
- `scripts/source.html`: source snapshot used to create the mirror.
- `scripts/mirror.py`: asset download and URL rewriting utility.
- `scripts/event_tiles.py`: event-tile editing utility.

The original Framer runtime is retained to preserve animations, slideshow, music controls, and countdown. The page's analytics script and editor loader were removed.

To host the site, serve `public/` as static files and map `/bride/mehendireception` to `index.html`.

For Render, create a **Static Site**, leave the build command empty, and set the publish directory to `public`.

Music playback may require clicking the play control due to browser autoplay rules.

## Verification

The local invitation route returns HTTP 200. All manifest assets and referenced local asset paths are included in the repository.
