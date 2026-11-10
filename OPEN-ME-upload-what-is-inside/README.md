# Nolan Herman, REALTOR® | Nestlewood Realty (Elite site)

A cinematic multi-page site with animated Blue Ridge mountain scenes, glass menus and cards, and lots of motion.

## Pages
Home (`index.html`), About, Buy, Sell, Listings, Areas, Hickory, Newton, Granite Falls, Contact.

## Files
- `*.html`: the pages.
- `elite.css`: design and animations.
- `elite.js`: the animated mountain scenes and all the motion. Settings at the top:
  - `HERO_VIDEO`: put a mountain/drone video in `images/` and add its name here (e.g. `"images/blue-ridge.mp4"`).
  - `FORM_ENDPOINT`: optional formspree.io link so leads go straight to your inbox.
- `images/`: logo, headshot, listing photos.
- `Hickory-Area-Home-Buyers-Guide.pdf`: the free guide.
- `_build/build.py`: all the site's text, listings, areas and links live at the top of this file.
  After editing it, run `python3 _build/build.py` to rebuild every page.

## Still placeholders
Listing prices, the Henry Smith St photo, action shots, area photos, market numbers on area pages,
and the Calendly link (paste it into `CALENDLY` in `_build/build.py`).
