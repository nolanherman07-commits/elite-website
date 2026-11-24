# Builds every page of Jose Lugo's Elite site. Run: python3 _build/build.py
import os, html, json
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
E = html.escape

# ===== AGENT INFO =====
# PLACEHOLDERS: phone, email, brokerage, office address, logo and headshot still need Jose's real info.
NAME, FIRST = "Jose Lugo", "Jose"
BROKERAGE = "Brokerage name"          # PLACEHOLDER
PHONE, TEL, EMAIL = "910-555-0100", "+19105550100", "jose@example.com"  # PLACEHOLDERS
ADDRESS = "Wilmington, NC"           # PLACEHOLDER: office street address
MAP = "https://www.google.com/maps/search/?api=1&query=" + ADDRESS.replace(" ", "+")
ZILLOW = "https://www.zillow.com/profile/joseL1982"
CALENDLY = ""  # optional: paste a Calendly link here
EXT = 'target="_blank" rel="noopener"'
# Full web address of the site. Change this once the domain is set up.
BASE = "https://example.com/"        # PLACEHOLDER
SHARE_IMAGE = "images/share.jpg"  # picture shown when a page link is texted or posted

# Stats from Jose's Zillow profile (Nov 2026)
YEARS, TOTAL_SALES, LAST_12, AVG_PRICE, RANGE = 5, 51, 24, "$316K", "$35K–$790K"

FEATURED = []  # active listings: (address, city, link, photo)
# Recent sales from Zillow (addresses aren't shown publicly, so cards show price + side)
SOLD = [
  ("Sold for $785,000", "Supply, NC · Represented the seller", ZILLOW, ""),
  ("Sold for $375,000", "Wilmington, NC · Represented the seller", ZILLOW, ""),
  ("Sold for $291,000", "Rocky Point, NC · Represented the buyer", ZILLOW, ""),
  ("Sold for $279,000", "Shallotte, NC · Represented the buyer", ZILLOW, ""),
  ("Sold for $168,000", "Hampstead, NC · Represented the buyer", ZILLOW, ""),
]
AREAS = {
  "wilmington": dict(name="Wilmington", scene="golden", county="New Hanover County",
    short="A historic riverfront city with beaches 20 minutes away.",
    intro="Wilmington sits on the Cape Fear River, with a historic downtown, the Riverwalk, UNC Wilmington and beaches just minutes away. From established neighborhoods like Masonboro to newer communities in Murraysville and Lansdowne, there's a fit for every stage of life.",
    facts=[("New Hanover", "County"), ("~20 min", "To the beach"), ("Cape Fear", "On the river"), ("UNCW", "University town")],
    love=["Historic downtown and the Riverwalk", "Beaches 20 minutes from most neighborhoods", "Neighborhoods like Masonboro, Lansdowne and Murraysville", "Restaurants, breweries and year-round events"]),
  "wrightsville-beach": dict(name="Wrightsville Beach", scene="dawn", county="New Hanover County", video="beach",
    short="Island living just east of Wilmington, with surf, sound and sand.",
    intro="Wrightsville Beach is a small island town just east of Wilmington, between the Atlantic and the Intracoastal Waterway. It's a top pick for buyers who want oceanfront or sound-side living and a quick drive back into the city.",
    facts=[("New Hanover", "County"), ("~20 min", "To downtown Wilmington"), ("Atlantic", "Oceanfront"), ("ICW", "Sound-side homes")],
    love=["Surfing, paddleboarding and boating", "Oceanfront and sound-side homes", "Walkable island lifestyle", "Minutes from Wilmington shopping and jobs"]),
  "carolina-beach": dict(name="Carolina Beach", scene="sunset", county="New Hanover County", video="beach",
    short="A laid-back beach town on Pleasure Island, with a classic boardwalk.",
    intro="Carolina Beach is on Pleasure Island, south of Wilmington, with a classic boardwalk, a fishing pier and Carolina Beach State Park. It offers a more relaxed beach-town feel, from condos to raised beach homes.",
    facts=[("New Hanover", "County"), ("~25 min", "To downtown Wilmington"), ("Pleasure Island", "Beach town"), ("State park", "Trails & marina")],
    love=["Boardwalk, pier and summer events", "Beach homes, condos and investment properties", "Carolina Beach State Park", "Easy drive to Wilmington"]),
  "leland": dict(name="Leland", scene="dusk", county="Brunswick County",
    short="Fast-growing communities just across the river from downtown Wilmington.",
    intro="Leland is in Brunswick County, just across the Cape Fear River from downtown Wilmington. It's one of the fastest-growing towns in the region, with newer master-planned communities, golf, and lower property taxes than New Hanover County.",
    facts=[("Brunswick", "County"), ("~15 min", "To downtown Wilmington"), ("New construction", "Planned communities"), ("Golf", "Course communities")],
    love=["Newer homes and amenity-rich neighborhoods", "Quick commute into Wilmington", "Golf and outdoor space", "Room to grow"]),
  "hampstead": dict(name="Hampstead", scene="mist", county="Pender County",
    short="Coastal living along US-17, close to Topsail Island.",
    intro="Hampstead is in Pender County along US-17, north of Wilmington and close to Topsail Island. It's popular with buyers who want more space, waterfront and golf communities, and a quieter pace while staying near the city.",
    facts=[("Pender", "County"), ("~30 min", "To Wilmington"), ("Topsail", "Island nearby"), ("US-17", "Coastal highway")],
    love=["Close to Topsail Island beaches", "Golf and waterfront communities", "Bigger lots and a quieter pace", "Easy US-17 drive to Wilmington"]),
  "rocky-point": dict(name="Rocky Point", scene="golden", county="Pender County",
    short="Country space off I-40, a short drive north of Wilmington.",
    intro="Rocky Point is a rural community in Pender County along I-40, north of Wilmington. Buyers come here for more land and home for the money, with a straight shot down I-40 into the city.",
    facts=[("Pender", "County"), ("~25 min", "To Wilmington"), ("I-40", "Right off the highway"), ("Acreage", "More land")],
    love=["More home and land for the money", "Quiet, country setting", "Direct I-40 commute to Wilmington", "New construction options"]),
  "supply": dict(name="Supply", scene="dawn", county="Brunswick County", video="beach",
    short="The gateway to Holden Beach, with room to spread out.",
    intro="Supply is a community in Brunswick County just inland from Holden Beach. It's a great fit for buyers who want to be minutes from the sand without paying island prices, from waterfront homes to new builds.",
    facts=[("Brunswick", "County"), ("~15 min", "To Holden Beach"), ("~40 min", "To Wilmington"), ("ICW", "Waterfront nearby")],
    love=["Minutes from Holden Beach", "Waterfront and water-access homes", "More space for the money", "Quiet coastal setting"]),
  "shallotte": dict(name="Shallotte", scene="sunset", county="Brunswick County", video="beach",
    short="A small town on US-17 between Ocean Isle and Holden Beach.",
    intro="Shallotte is a small town in southern Brunswick County on US-17, close to Ocean Isle Beach and Holden Beach. It's the shopping hub for the South Brunswick Islands, with a mix of established neighborhoods and new construction.",
    facts=[("Brunswick", "County"), ("~15 min", "To Ocean Isle Beach"), ("~45 min", "To Wilmington"), ("US-17", "Coastal highway")],
    love=["Close to Ocean Isle and Holden Beach", "Local shopping and dining", "New construction and established neighborhoods", "Small-town coastal feel"]),
}
# Order of towns from north to south (used for "Nearby areas" and the relocation page)
CORRIDOR = ["rocky-point", "hampstead", "wilmington", "wrightsville-beach", "carolina-beach", "leland", "supply", "shallotte"]
HOME_AREAS = ["wilmington", "wrightsville-beach", "hampstead", "leland", "shallotte"]
# Drive times from each town (approximate, normal traffic): (to downtown Wilmington, to the beach)
DRIVE = {"wilmington": ("—", "~20 min"), "wrightsville-beach": ("~20 min", "On the beach"), "carolina-beach": ("~25 min", "On the beach"),
         "leland": ("~15 min", "~35 min"), "hampstead": ("~30 min", "~15 min"), "rocky-point": ("~25 min", "~40 min"),
         "supply": ("~40 min", "~15 min"), "shallotte": ("~45 min", "~15 min")}

# Monthly market update: edit these each month (source + period shown on the page)
MARKET_MONTH = "November 2026"
MARKET = [
  dict(area="Wilmington metro", period="Jan to Jun 2026 average", source="Redfin, via Stacker", url="https://stacker.com/stories/north-carolina/wilmington/wilmington-mid-year-housing-market-review",
       stats=[("$471,799", "Median sale price"), ("+1.4%", "vs. last year"), ("68 days", "Median days on market"), ("4.2 mo", "Supply of homes")]),
]
MARKET_TAKE = [
  ("For buyers", "Homes are taking more than two months to sell and there are over four months of supply. That means more choices and more room to negotiate on price, repairs and closing costs."),
  ("For sellers", "Prices are holding steady, but buyers are patient. Homes priced right from day one and marketed well are the ones that sell fastest."),
  ("City vs. coast", "Moving a little north into Pender County or south into Brunswick County can get you more home or more land for the money, still close to the beach."),
]

NAV = [("about.html", "About"), ("buy.html", "Buying?"), ("sell.html", "Selling?"), ("relocate.html", "Relocating?"), ("listings.html", "Listings")]
TABS = [("about.html", "About"), ("buy.html", "Buy"), ("sell.html", "Sell"), ("relocate.html", "Out of town"), ("listings.html", "Listings")]  # short labels for the phone tab bar

def header(active):
    links = "".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="nav-wrap">
  <nav class="nav-pill"><a href="index.html" class="nav-logo"><img src="images/logo.png" alt="{NAME}, REALTOR®" /></a>{links}</nav>
  <a href="contact.html" class="nav-cta">Let's talk</a>
  <nav class="tabbar" aria-label="Pages">{"".join(f'<a href="{h}"{" class=\"active\"" if (h == active or (h == "index.html" and not active)) else ""}>{t}</a>' for h, t in [("index.html", "Home")] + TABS)}</nav>
</header>'''

FOOTER = f'''<footer class="foot">
  <div class="wrap foot-grid">
    <a href="index.html"><img src="images/logo.png" alt="{NAME}, REALTOR®" /></a>
    <p>{NAME}, REALTOR® · {BROKERAGE}<br />{ADDRESS}</p>
    <div class="soc"><a href="about.html">About</a><a href="buy.html">Buy</a><a href="sell.html">Sell</a><a href="relocate.html">Relocate</a><a href="market.html">Market update</a><a href="listings.html">Listings</a><a href="contact.html">Contact</a></div>
    <div class="soc"><a href="{ZILLOW}" {EXT}>Zillow</a></div>
  </div>
  <div class="wrap foot-areas"><span>Areas I serve</span>{"".join(f'<a href="{k}.html">{AREAS[k]["name"]}</a>' for k in CORRIDOR)}</div>
  <div class="wrap fine eho-line"><svg class="eho" viewBox="0 0 40 40" role="img" aria-label="Equal Housing Opportunity"><path d="M20 3 2 15v4h4v18h28V19h4v-4z" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round"/><rect x="12" y="20" width="16" height="3.4" fill="currentColor"/><rect x="12" y="27" width="16" height="3.4" fill="currentColor"/></svg>
    <span>© <span class="yr">2026</span> {BROKERAGE} · Equal Housing Opportunity · REALTOR®</span></div>
</footer>'''

SCHEMA = json.dumps({
  "@context": "https://schema.org", "@type": "RealEstateAgent",
  "name": f"{NAME}, REALTOR®", "url": BASE, "image": BASE + "images/headshot.jpg", "logo": BASE + "images/logo.png",
  "telephone": TEL, "email": EMAIL,
  "worksFor": {"@type": "RealEstateOrganization", "name": BROKERAGE},
  "address": {"@type": "PostalAddress", "addressLocality": "Wilmington", "addressRegion": "NC", "addressCountry": "US"},
  "areaServed": [{"@type": "City", "name": AREAS[k]["name"] + ", NC"} for k in CORRIDOR],
  "sameAs": [ZILLOW],
}, ensure_ascii=False)

DEFAULT_DESC = f"{NAME}, REALTOR® in Wilmington, NC. Helping buyers and sellers across Wilmington, Wrightsville Beach, Hampstead, Leland and the Brunswick County coast."

def page(fname, title, active, body, curtain=False, desc=DEFAULT_DESC):
    url = BASE + ("" if fname == "index.html" else fname)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{NAME}, REALTOR®" />
<meta property="og:title" content="{E(title)}" />
<meta property="og:description" content="{E(desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}{SHARE_IMAGE}" />
<meta property="og:image:width" content="1200" /><meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">{SCHEMA}</script>
<link rel="icon" href="images/icon.png" /><link rel="apple-touch-icon" href="images/icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="elite.css" />
</head>
<body{"" if curtain else ' class="page-fade"'}>
{'<div class="curtain" aria-hidden="true"><img src="images/logo.png" alt="" /></div>' if curtain else ""}
<div class="cursor-glow" aria-hidden="true"></div>
{header(active)}
{body}
{FOOTER}
<script src="elite.js"></script>
</body>
</html>'''
    open(fname, "w").write(doc)

def bg(scene, photo=None):
    # a real photo (slow zoom) if we have one, otherwise an animated coastal scene
    return f'<div class="photo-bg" style="background-image:url(\'{photo}\')"></div>' if photo else f'<div class="scene" data-scene="{scene}"></div>'

def page_hero(crumb, title_html, sub, scene, photo=None, video=None):
    fog = "" if photo else '<div class="fog f1"></div><div class="fog f2"></div>'
    return f'''<section class="page-hero"><div class="frame">
  {bg(scene, photo)}{(f'<video class="hero-video" data-src="{video if video.startswith("http") else f"videos/{video}.mp4"}" muted loop playsinline autoplay hidden disablepictureinpicture disableremoteplayback preload="metadata" aria-hidden="true"></video>' if video else '')}{fog}<div class="shade"></div>
  <div class="ph-copy"><span class="crumb"><i></i> {crumb}</span><h1 class="split-words">{title_html}</h1><p>{sub}</p></div>
</div></section>'''

# Price, beds, baths and square feet shown on each active listing card.
DETAILS = {}

def card(addr, city, url, photo, sold=False, price=True):
    pic = f'<img src="{photo}" alt="{E(addr)}" />' if photo else '<div class="scene" data-scene="dawn"></div>'
    d = DETAILS.get(addr)
    sub = f"{city} · {d[0]} · {d[1]} bd / {d[2]} ba" if (d and price) else city
    return f'''<a class="home-card" href="{url}" {EXT}><div class="img">{pic}</div>
  <div class="info glass"><span class="badge{" sold" if sold else ""}">{"Sold" if sold else "Featured"}</span><h3>{E(addr)}</h3><p>{sub}</p></div></a>'''

def rail(items, title_html, eyebrow, link=None):
    return f'''<section class="listings">
  <div class="wrap head"><div><p class="eyebrow">{eyebrow}</p><h2>{title_html}</h2></div>
    <div class="arrows">{f'<a class="pill" href="{link}" style="margin-right:.6rem">View all</a>' if link else ""}<button class="arr prev" aria-label="Previous">←</button><button class="arr next" aria-label="Next">→</button></div></div>
  <div class="rail" tabindex="0">{"".join(card(*i[:4], sold=i in SOLD) for i in items)}</div>
  <div class="wrap"><div class="progress"><span></span></div></div>
</section>'''

def panels(keys, title_html="From the river to the <em>coast</em>"):
    out = "".join(f'''<article class="panel{" open" if n == 0 else ""}" data-href="{k}.html">{bg(AREAS[k]["scene"], AREAS[k].get("photo"))}<div class="p-shade"></div>
  <div class="p-copy"><span class="num">0{n+1}</span><h3>{AREAS[k]["name"]}</h3><p>{AREAS[k]["short"]}</p><a class="pill light sm" href="{k}.html">Explore {AREAS[k]["name"]}</a></div></article>''' for n, k in enumerate(keys))
    return f'''<section class="areas"><div class="wrap head"><div><p class="eyebrow">Explore the area</p><h2>{title_html}</h2></div></div>
  <div class="wrap panels">{out}</div></section>'''

VALUE_FORM = '''<form class="line-form stack lead-form" data-subject="Home value request" data-need-contact><input name="address" placeholder="Your home address" autocomplete="street-address" required /><input name="phone" type="tel" placeholder="Phone number" autocomplete="tel" /><input name="email" type="email" placeholder="or email address" autocomplete="email" /><span class="form-note">Phone or email, whichever you prefer.</span><button class="pill solid" type="submit">Get my value</button></form>'''
CONSULT_FORM = '''<form class="line-form stack lead-form" data-subject="Buyer consultation request" data-need-contact><input name="name" placeholder="Your name" autocomplete="name" required /><input name="phone" type="tel" placeholder="Phone number" autocomplete="tel" /><input name="email" type="email" placeholder="or email address" autocomplete="email" /><span class="form-note">Phone or email, whichever you prefer.</span><button class="pill solid" type="submit">Book my consult</button></form>'''

SELL_TOOLS = f'''<section class="tools" id="value">
  <div class="scene" data-scene="night"></div><div class="stars"></div>
  <div class="wrap tools-grid">
    <div class="glass tool reveal"><p class="eyebrow">Free home value report</p><h3>What's your home <em>worth?</em></h3>
      <p>A personalized value report from {FIRST}, not an algorithm. Usually within 24 hours.</p>{VALUE_FORM}</div>
    <div class="glass tool reveal"><p class="eyebrow">My listing plan</p><h3>What you get when you <em>list with me</em></h3>
      <ul class="checks"><li>Pricing based on recent sales near you</li><li>Professional photos and online marketing</li><li>Exposure on the MLS, Zillow and major home sites</li><li>Hands-on negotiation through closing</li></ul></div>
  </div>
</section>'''

# Real quotes from Jose's Zillow reviews
QUOTES = [
  ("Jose listed my house on a Monday and we had a contract by Saturday!", "Amanda M.", "Sold in 2024"),
  ("Jose was phenomenal throughout the entire process of selling our home.", "Zillow reviewer", "Bought &amp; sold in Murraysville"),
  ("Jose did an excellent job with supporting my new home purchase.", "Zillow reviewer", "Bought in 2025"),
  ("Quality at its finest!!", "Zillow reviewer", "Sold in Rocky Point"),
]
FULL_REVIEW = dict(text=["Jose listed my house on a Monday and we had a contract by Saturday!"],
  name="Amanda M.", detail="Seller · Referred by a neighbor · 2024")
FULL_REVIEW_HTML = f'''<figure class="full-review reveal"><div class="fr-stars">★★★★★</div>
  <blockquote>{"".join(f"<p>{E(t)}</p>" for t in FULL_REVIEW["text"])}</blockquote>
  <figcaption><b>{FULL_REVIEW["name"]}</b><span>{FULL_REVIEW["detail"]}</span><a href="{ZILLOW}" {EXT}>Read it on Zillow →</a></figcaption></figure>'''

QUOTE_STRIP = '<section class="quote-strip" aria-label="Client reviews"><div class="wrap qs-inner"><div class="qs-stars">★★★★★ <span>5.0 on Zillow</span></div><div class="qs-stage">' + "".join(
    f'<blockquote class="qs"><p>“{q}”</p><cite>{n} · {w}</cite></blockquote>' for q, n, w in QUOTES) + '</div>' + FULL_REVIEW_HTML + '</div></section>'
REVIEWS = QUOTE_STRIP

SPECIALTIES = ["Buyer's agent", "Listing agent", "Relocation", "First-time homebuyers", "Investment properties", "New construction", "Commercial properties"]
SPECIALTY_SEC = f'''<section class="sec resumes"><div class="wrap">
  <div class="head"><div><p class="eyebrow">Specialties</p><h2>However you're moving, <em>I've got you</em></h2></div></div>
  <ul class="checks" style="columns:2;max-width:760px">{"".join(f"<li>{s}</li>" for s in SPECIALTIES)}</ul>
</div></section>'''

TOOLS = f'''<section class="tools">
  <div class="scene" data-scene="night"></div><div class="stars"></div>
  <div class="wrap tools-grid">
    <div class="glass tool reveal"><p class="eyebrow">Free home value report</p><h3>What's your home <em>worth?</em></h3>
      <p>A personalized value report from {FIRST}, not an algorithm. Usually within 24 hours.</p>{VALUE_FORM}</div>
    <div class="glass tool reveal"><p class="eyebrow">Free buyer consult</p><h3>Thinking about <em>buying?</em></h3>
      <p>A quick call about budget, towns and timing, so you know exactly where to start.</p>{CONSULT_FORM}</div>
  </div>
</section>'''

BOOK = CALENDLY or "contact.html#book"
CTA = f'''<section class="contact">
  <div class="frame small">
    <div class="still-bg" style="background-image:url('images/beach-still.jpg')"></div><div class="shade"></div>
    <div class="c-copy">
      <h2>Ready when <em>you</em> are.</h2>
      <p>Call, text, email, or book a time. I respond fast.</p>
      <div class="hero-btns center">
        <a class="pill solid" href="tel:{TEL}">Call {PHONE}</a><a class="pill light" href="sms:{TEL}">Text {FIRST}</a>
        <a class="pill" href="mailto:{EMAIL}">Email {FIRST}</a><a class="pill" href="{BOOK}">Book a call</a>
      </div>
    </div>
  </div>
</section>'''

MARQUEE = '''<div class="marquee" aria-hidden="true"><div class="track">''' + ("<span>Wilmington</span><i>✦</i><span><em>Wrightsville Beach</em></span><i>✦</i><span>Hampstead</span><i>✦</i><span><em>Leland</em></span><i>✦</i><span>Carolina Beach</span><i>✦</i><span>Shallotte</span><i>✦</i><span><em>Cape Fear</em></span><i>✦</i>" * 2) + "</div></div>"

COUNTERS = f'''<div class="counters reveal">
  <div><b data-count="{TOTAL_SALES}">{TOTAL_SALES}</b><span>Homes sold</span></div>
  <div><b data-count="{LAST_12}">{LAST_12}</b><span>Sales in the last 12 months</span></div>
  <div><b data-count="{YEARS}">{YEARS}</b><span>Years in real estate</span></div>
  <div><b>5.0★</b><span>Every Zillow review</span></div>
</div>'''

# ================= HOME =================
page("index.html", f"{NAME}, REALTOR® | Wilmington, NC Real Estate", "", f'''
<section class="hero" id="top">
  <div class="frame">
    <div class="scene" data-scene="sunset"></div>
    <video class="hero-video" data-src="videos/beach.mp4" muted loop playsinline autoplay hidden disablepictureinpicture disableremoteplayback preload="metadata" aria-hidden="true"></video>
    <div class="fog f1"></div><div class="fog f2"></div><div class="fog f3"></div><div class="shade"></div>
    <div class="trace-line" aria-hidden="true"><span class="chip"><i></i> Serving the Wilmington area</span></div>
    <div class="hero-copy">
      <p class="kicker">{NAME} · REALTOR® · {BROKERAGE}</p>
      <h1 class="split-words">Let's go <em>home.</em></h1>
      <p class="hero-sub">Buying and selling across Wilmington, the beaches, Pender County and the Brunswick County coast, made simple.</p>
      <div class="hero-btns"><a class="pill light" href="listings.html">See my sales</a><a class="pill" href="sell.html#value">What's my home worth?</a></div>
    </div>
    <ul class="hero-stats">
      <li><b data-count="{TOTAL_SALES}">{TOTAL_SALES}</b>homes sold</li>
      <li><b data-count="{LAST_12}">{LAST_12}</b>sales in the last 12 months</li>
      <li><b>5.0★</b>on Zillow</li>
    </ul>
    <aside class="glass-card"><small>Meet {FIRST}</small><p>Five years helping families buy and sell on the Cape Fear coast.</p>
      <img src="images/headshot.jpg" alt="{NAME}" /><a class="pill solid" href="about.html">About me</a></aside>
    <div class="scroll-cue"><span></span></div>
  </div>
</section>
{MARQUEE}
<section class="statement">
  <div class="wrap st-grid">
    <div class="st-photo reveal"><div class="kb"><img src="images/headshot.jpg" alt="{NAME}" /></div><span class="tag-glass">{YEARS} years · {TOTAL_SALES} homes sold</span></div>
    <div>
      <p class="eyebrow reveal">Meet {FIRST}</p>
      <h2 class="words home-story">From first homes in Rocky Point to coastal properties in Brunswick County, I help buyers and sellers move with <em>confidence.</em></h2>
      <p class="body reveal">I'm quick to respond, I know these neighborhoods, and I work to get my clients the best deal whether they're buying, selling, or both.</p>
      <p class="body reveal" style="margin-top:-1rem"><a class="pill solid" href="about.html">More about me</a></p>
      {COUNTERS}
    </div>
  </div>
</section>
{QUOTE_STRIP}
{SPECIALTY_SEC}
{panels(HOME_AREAS)}
{TOOLS}
{rail(FEATURED + SOLD, "Recent <em>wins</em>", "Recently sold", "listings.html")}
{CTA}''', curtain=True, desc=f"{NAME}, REALTOR® in Wilmington, NC. {TOTAL_SALES} homes sold and 5.0 stars on Zillow. Buy, sell or relocate anywhere from Hampstead to Shallotte.")

# ================= ABOUT =================
page("about.html", f"About {NAME} | Wilmington, NC REALTOR®", "about.html", f'''
{page_hero("About", f"Meet <em>{FIRST}.</em>", f"REALTOR® with {BROKERAGE}, serving Wilmington, the beaches, Pender County and the Brunswick County coast.", "golden", video="beach")}
<section class="statement">
  <div class="wrap st-grid">
    <div class="st-photo reveal"><div class="kb"><img src="images/headshot.jpg" alt="{NAME}" /></div><span class="tag-glass">{BROKERAGE}</span></div>
    <div>
      <p class="eyebrow reveal">About me</p>
      <h2 class="words">Five years, {TOTAL_SALES} sales, and a 5-star review from every client who's left <em>one.</em></h2>
      <p class="body reveal">I've spent the last {YEARS} years helping people buy and sell homes across southeastern North Carolina, from Wilmington neighborhoods like Masonboro, Lansdowne and Murraysville to Hampstead, Rocky Point, Supply and Shallotte.</p>
      <p class="body reveal">My clients range from first-time buyers to sellers of coastal homes near $800,000, and I also work with relocation, investment, new construction and commercial clients.</p>
      <p class="body reveal">What my clients say most is that I respond fast and work hard to get them the best deal. Whether you're moving across town or across the country, I'll make the process clear from the first call to closing day.</p>
      {COUNTERS}
    </div>
  </div>
</section>
<section class="sec"><div class="wrap"><p class="eyebrow">Behind the scenes</p><h2>On the <em>job</em></h2>
  <div class="gallery">
    <div class="reveal"><div class="photo-bg" style="background-image:url('https://images.unsplash.com/photo-1741156386380-0236c72eb6f9?w=1600&q=80&auto=format&fit=crop')"></div></div>
    <div class="reveal"><div class="photo-bg" style="background-image:url('https://images.unsplash.com/photo-1793586938427-e8e37441c962?w=1600&q=80&auto=format&fit=crop')"></div></div>
    <div class="reveal"><div class="photo-bg" style="background-image:url('https://images.unsplash.com/photo-1781229771042-2a859f8f8022?w=1600&q=80&auto=format&fit=crop')"></div></div>
    <div class="reveal"><div class="photo-bg" style="background-image:url('https://images.unsplash.com/photo-1772313952254-dae19b91854b?w=1600&q=80&auto=format&fit=crop')"></div></div>
    <div class="reveal"><div class="photo-bg" style="background-image:url('images/beach-still.jpg')"></div></div>
  </div>
  <div class="hero-btns" style="margin-top:2.4rem"><a class="pill solid" href="{ZILLOW}" {EXT}>My Zillow profile</a></div>
</div></section>
<section class="sec sand"><div class="wrap center"><p class="eyebrow">How I work</p><h2>Clear from <em>day one</em></h2>
  <div class="timeline" style="text-align:left">
    <div class="tl reveal"><i>1</i><h3>Listen</h3><p>We talk through your goals, budget and timeline.</p></div>
    <div class="tl reveal"><i>2</i><h3>Plan</h3><p>You get a clear plan: towns, pricing and next steps.</p></div>
    <div class="tl reveal"><i>3</i><h3>Move fast</h3><p>Quick showings, quick answers, strong offers.</p></div>
    <div class="tl reveal"><i>4</i><h3>Close</h3><p>I handle the details all the way to the keys.</p></div>
  </div></div></section>
{REVIEWS}
{CTA}''', desc=f"Meet {NAME}, REALTOR® in Wilmington, NC. {YEARS} years in real estate, {TOTAL_SALES} homes sold and 5.0 stars on Zillow.")

# ================= BUY =================
page("buy.html", f"Buy a Home in the Wilmington Area | {NAME}, REALTOR®", "buy.html", f'''
{page_hero("Buy", "Buy a <em>home.</em>", "From your first showing to closing day, I'll help you find the right home and negotiate the best deal.", "dawn", video="buy")}
<section class="sec"><div class="wrap center"><p class="eyebrow">How it works</p><h2>Your path to the <em>keys</em></h2>
  <div class="steps4" style="text-align:left">
    <div class="step reveal"><h3>Talk</h3><p>A quick call about what you want, where, and your budget.</p></div>
    <div class="step reveal"><h3>Get pre-approved</h3><p>I'll connect you with trusted lenders so you can shop with confidence.</p></div>
    <div class="step reveal"><h3>Tour &amp; offer</h3><p>We tour homes together, then write a strong offer that stands out.</p></div>
    <div class="step reveal"><h3>Close</h3><p>I handle inspections, appraisal, and paperwork right up to closing day.</p></div>
  </div></div></section>
<section class="sec sand" id="calculator"><div class="wrap"><p class="eyebrow">Mortgage calculator</p><h2>What will my <em>payment</em> be?</h2>
  <div class="calc reveal">
    <div class="inputs">
      <label>Home price ($)<input id="c-price" type="number" value="400000" min="0" step="1000" /></label>
      <div class="row2"><label>Down payment (%)<input id="c-down" type="number" value="10" min="0" max="100" /></label><label>Interest rate (%)<input id="c-rate" type="number" value="6.5" min="0" step="0.05" /></label></div>
      <div class="row2"><label>Loan term (years)<input id="c-term" type="number" value="30" min="1" /></label><label>Taxes + insurance / mo ($)<input id="c-extra" type="number" value="450" min="0" step="10" /></label></div>
      <p class="fine">Estimate only. Coastal homes may need flood and wind coverage. Talk to a lender for your exact numbers.</p>
    </div>
    <div class="result"><div class="scene" data-scene="dusk"></div><small style="letter-spacing:.2em;text-transform:uppercase;font-size:.7rem;opacity:.8">Estimated monthly payment</small><div class="pay" id="c-pay">$0</div>
      <div class="bd"><div><span>Principal &amp; interest</span><b id="c-pi">$0</b></div><div><span>Taxes &amp; insurance</span><b id="c-ti">$0</b></div><div><span>Loan amount</span><b id="c-loan">$0</b></div></div></div>
  </div></div></section>
{TOOLS}
{rail(SOLD, "Homes I've helped <em>buy &amp; sell</em>", "Recent sales", "listings.html")}
{REVIEWS}
{CTA}''', desc=f"Buying a home in Wilmington or on the NC coast? Get {FIRST}'s step-by-step plan, a free buyer consult and a mortgage payment calculator.")

# ================= SELL =================
page("sell.html", f"Sell Your Home in the Wilmington Area | {NAME}, REALTOR®", "sell.html", f'''
{page_hero("Sell", "Sell your <em>home.</em>", "Smart pricing, professional photos, and marketing that puts your home in front of the right buyers.", "dusk", video="sell")}
<section class="statement"><div class="wrap">
  <p class="eyebrow reveal">Results</p>
  <h2 class="words" style="max-width:1000px">One recent seller listed on a Monday and had a contract by Saturday. I price it right and market it hard so buyers move <em>fast.</em></h2>
  <div style="margin-top:3rem">{COUNTERS}</div>
</div></section>
<section class="sec dark"><div class="wrap center"><p class="eyebrow">My selling plan</p><h2>How I get your home <em>sold</em></h2>
  <div class="steps4" style="text-align:left">
    <div class="step reveal"><h3>Price it right</h3><p>A detailed look at recent sales so we list at the right number from day one.</p></div>
    <div class="step reveal"><h3>Make it shine</h3><p>Professional photos that make buyers stop scrolling.</p></div>
    <div class="step reveal"><h3>Market everywhere</h3><p>The MLS, Zillow, and the major home search sites.</p></div>
    <div class="step reveal"><h3>Negotiate &amp; close</h3><p>I screen offers, negotiate hard, and handle every detail to closing.</p></div>
  </div></div></section>
{SELL_TOOLS}
{rail(SOLD, "Recently <em>sold</em>", "Results")}
{REVIEWS}
{CTA}''', desc=f"Selling your home in Wilmington, Hampstead or Brunswick County? Get a free home value report from {FIRST} and see his plan to price, market and sell it.")

# ================= LISTINGS =================
featured_html = (f'<div class="grid3">{"".join(card(*l) for l in FEATURED)}</div>' if FEATURED else
  f'<p class="lead" style="max-width:640px">New listings coming soon. See my current homes for sale on Zillow, or reach out and I\'ll send you homes that fit.</p><div class="hero-btns" style="margin-top:1.4rem"><a class="pill solid" href="{ZILLOW}" {EXT}>View on Zillow</a><a class="pill" href="contact.html">Get homes that fit</a></div>')
page("listings.html", f"Listings & Recent Sales | {NAME}, REALTOR®", "listings.html", f'''
{page_hero("Listings", "Featured <em>homes.</em>", "Homes for sale and recent sales across the Wilmington area and the NC coast.", "golden", video="sell")}
<section class="sec dark"><div class="wrap"><div class="head"><div><p class="eyebrow">For sale</p><h2>Featured <em>listings</em></h2></div><a class="pill" href="{ZILLOW}" {EXT}>All on Zillow</a></div>
  {featured_html}</div></section>
<section class="sec"><div class="wrap"><div class="head"><div><p class="eyebrow">Results · {TOTAL_SALES} sales · {RANGE}</p><h2>Recently <em>sold</em></h2></div></div>
  <div class="grid3">{"".join(card(*l, sold=True) for l in SOLD)}</div></div></section>
{CTA}''', desc=f"Homes for sale and recent sales by {NAME}, REALTOR®, across Wilmington, Pender County and the Brunswick County coast.")

# Area pages
for key, a in AREAS.items():
    i = CORRIDOR.index(key)
    others = [k for k in sorted(CORRIDOR, key=lambda k: abs(CORRIDOR.index(k) - i)) if k != key][:4]
    page(f"{key}.html", f"Living in {a['name']}, NC | {NAME}, REALTOR®", "areas.html", f'''
{page_hero(f"Areas / {a['name']}", f"Living in <em>{a['name']}.</em>", a["short"], a["scene"], a.get("photo"), a.get("video"))}
<section class="sec"><div class="wrap split2">
  <div class="reveal"><p class="eyebrow">{a["county"]}</p><h2>Why people love <em>{a["name"]}</em></h2><p class="lead">{a["intro"]}</p>
    <ul class="checks">{"".join(f"<li>{E(x)}</li>" for x in a["love"])}</ul>
    <div class="hero-btns" style="margin-top:2rem"><a class="pill solid" href="contact.html">Find a home in {a["name"]}</a></div></div>
  <div class="area-photo reveal">{bg(a["scene"], a.get("photo"))}</div>
</div>
<div class="wrap"><div class="facts">{"".join(f'<div class="fact reveal"><b>{E(x)}</b><span>{E(y)}</span></div>' for x, y in a["facts"])}</div></div></section>
{panels(others, "Nearby <em>areas</em>")}
{TOOLS}
{CTA}''', desc=f"Thinking about living in {a['name']}, NC? {a['short']} Homes, neighborhoods and local tips from {NAME}, REALTOR®.")

# ================= CONTACT =================
page("contact.html", f"Contact {NAME} | Wilmington, NC REALTOR®", "contact.html", f'''
{page_hero("Contact", "Let's <em>talk.</em>", "Call, text, email, or book a time. I respond fast.", "sunset", video="beach")}
<section class="sec"><div class="wrap split2 top">
  <div class="reveal"><p class="eyebrow">Reach me</p><h2>I'm here to <em>help.</em></h2>
    <div class="contact-list">
      <a class="pill solid" href="tel:{TEL}">Call {PHONE}</a><a class="pill" href="sms:{TEL}">Text {FIRST}</a><a class="pill" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="pill" href="{MAP}" {EXT}>{ADDRESS}</a>
    </div></div>
  <form class="form reveal lead-form" data-subject="Website contact form" data-need-contact style="background:#ebe3d8">
    <div class="row2"><label>Name<input name="name" required /></label><label>Phone<input name="phone" type="tel" /></label></div>
    <label>Email<input name="email" type="email" /></label><span class="form-note dark">Phone or email, whichever you prefer.</span>
    <label>I'm interested in<select name="topic"><option>Buying</option><option>Selling</option><option>Home value report</option><option>Relocating</option><option>Investment property</option><option>Something else</option></select></label>
    <label>Message<textarea name="message" rows="4"></textarea></label>
    <button class="pill solid" type="submit">Send message</button>
  </form></div></section>
<section class="sec tight" id="book"><div class="wrap">
  <div class="booking reveal"><div class="scene" data-scene="night"></div><div class="stars"></div>
    <div><p class="eyebrow" style="color:rgba(255,255,255,.7)">Book a call</p><h2>Pick a <em>time.</em></h2>
      <div class="cal">{"".join(f'<i class="{"sel" if d == 14 else "av" if d in (9,10,15,16,17,21,22) else ""}">{d}</i>' for d in range(5, 26))}</div>
      <a class="pill solid" href="{CALENDLY or "tel:" + TEL}" style="margin-top:1rem">Book a call</a></div></div>
</div></section>''', desc=f"Call, text or email {NAME}, REALTOR® in Wilmington, NC. {PHONE}.")

# ================= RELOCATE =================
def town_card(k):
    a = AREAS[k]; w, b = DRIVE[k]
    return f'''<a class="town reveal" href="{k}.html"><div class="t-top"><h3>{a["name"]}</h3><span>{a["county"]}</span></div>
  <p>{a["short"]}</p><div class="t-drive"><div><b>{w}</b><span>To Wilmington</span></div><div><b>{b}</b><span>To the beach</span></div></div><i>Explore {a["name"]} →</i></a>'''

page("relocate.html", f"Relocating to Wilmington, NC | {NAME}, REALTOR®", "relocate.html", f'''
{page_hero("Relocate", "Moving <em>here?</em>", "From downtown Wilmington to the beach towns of Brunswick County, I'll help you find the right town and the right home, even from out of state.", "golden", video="beach")}
<section class="statement"><div class="wrap">
  <p class="eyebrow reveal">Why people move here</p>
  <h2 class="words" style="max-width:1050px">A historic river city, a string of beach towns, and room to spread out in <em>between.</em></h2>
  <div class="facts" style="margin-top:3rem">
    <div class="fact reveal"><b>{len(CORRIDOR)}</b><span>Towns I cover</span></div>
    <div class="fact reveal"><b>~20 min</b><span>Wilmington to the beach</span></div>
    <div class="fact reveal"><b>3</b><span>Counties: New Hanover, Pender, Brunswick</span></div>
    <div class="fact reveal"><b>5.0★</b><span>On Zillow, including out-of-area buyers</span></div>
  </div>
</div></section>
<section class="sec dark"><div class="wrap center"><p class="eyebrow">How I help from out of town</p><h2>Buy here without <em>flying back and forth</em></h2>
  <div class="steps4" style="text-align:left">
    <div class="step reveal"><h3>Find your town</h3><p>A call about your job, commute, schools and lifestyle, then a short list of towns that fit.</p></div>
    <div class="step reveal"><h3>Live video tours</h3><p>I walk homes and neighborhoods with you on video and point out what photos don't show.</p></div>
    <div class="step reveal"><h3>Local team</h3><p>Trusted lenders, inspectors and closing attorneys, so every step happens on time.</p></div>
    <div class="step reveal"><h3>Close from anywhere</h3><p>I coordinate the details so you can sign remotely if you need to and arrive to your keys.</p></div>
  </div></div></section>
<section class="sec" id="towns"><div class="wrap"><div class="head"><div><p class="eyebrow">Pender to Brunswick</p><h2>Find your <em>town</em></h2></div></div>
  <p class="lead" style="max-width:720px">Listed from north to south. Drive times are approximate, in normal traffic.</p>
  <div class="towns">{"".join(town_card(k) for k in CORRIDOR)}</div></div></section>
{REVIEWS}
<section class="sec sand"><div class="wrap split2 top">
  <div class="reveal"><p class="eyebrow">Relocation plan</p><h2>Tell me about your <em>move.</em></h2>
    <p class="lead">I'll send a short list of towns and homes that fit, plus what to expect on price, commute and timing.</p>
    <ul class="checks"><li>Free relocation consult</li><li>Area tours by video or in person</li><li>Help finding a trusted agent to sell your current home</li></ul></div>
  <form class="form reveal lead-form" data-subject="Relocation request" data-need-contact style="background:#fff">
    <div class="row2"><label>Name<input name="name" required /></label><label>Moving from<input name="moving_from" placeholder="City, state" /></label></div>
    <div class="row2"><label>Phone<input name="phone" type="tel" /></label><label>Email<input name="email" type="email" /></label></div>
    <span class="form-note dark">Phone or email, whichever you prefer.</span>
    <label>When are you moving?<select name="timeline"><option>In the next 3 months</option><option>3 to 6 months</option><option>6 to 12 months</option><option>Just exploring</option></select></label>
    <label>Anything else?<textarea name="message" rows="3" placeholder="Job location, budget, must-haves..."></textarea></label>
    <button class="pill solid" type="submit">Send my relocation plan</button>
  </form></div></section>
{CTA}''', desc=f"Relocating to Wilmington or the NC coast? Compare {len(CORRIDOR)} towns and drive times, and get a free relocation plan from {NAME}, REALTOR®.")

# ================= MARKET UPDATE =================
def market_block(m):
    return f'''<div class="mk reveal"><div class="mk-head"><h3>{m["area"]}</h3><span>{m["period"]}</span></div>
  <div class="facts" style="margin-top:1.2rem">{"".join(f'<div class="fact"><b>{E(x)}</b><span>{E(y)}</span></div>' for x, y in m["stats"])}</div>
  <p class="fine" style="margin-top:.8rem">Source: <a href="{m["url"]}" {EXT} style="text-decoration:underline">{m["source"]}</a></p></div>'''

page("market.html", f"Wilmington Market Update, {MARKET_MONTH} | {NAME}, REALTOR®", "market.html", f'''
{page_hero("Market update", "Market <em>update.</em>", "Home prices, days on market and supply for the Wilmington area, plus what it means if you're buying or selling.", "dusk")}
<section class="sec"><div class="wrap"><p class="eyebrow">{MARKET_MONTH}</p><h2>By the <em>numbers</em></h2>
  {"".join(market_block(m) for m in MARKET)}
</div></section>
<section class="sec dark"><div class="wrap center"><p class="eyebrow">What it means</p><h2>{FIRST}'s <em>take</em></h2>
  <div class="steps4 three" style="text-align:left">{"".join(f'<div class="step reveal"><h3>{E(t)}</h3><p>{E(b)}</p></div>' for t, b in MARKET_TAKE)}</div></div></section>
{SELL_TOOLS}
{CTA}''', desc=f"{MARKET_MONTH} housing market update for Wilmington, NC: median prices, days on market and supply, with what it means for buyers and sellers.")
print("built")
