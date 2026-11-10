# Builds every page of the Elite site. Run: python3 _build/build.py
import os, html
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
E = html.escape

PHONE, TEL, EMAIL = "828-404-5335", "+18284045335", "nolan@nestlewoodrealty.com"
ADDRESS = "825 Highland Ave SE, Hickory, NC 28602"
MAP = "https://www.google.com/maps/search/?api=1&query=" + ADDRESS.replace(" ", "+")
ZILLOW = "https://www.zillow.com/profile/Nolansellnc"
HOMES = "https://www.homes.com/real-estate-agents/nolan-herman/2672vt8/"
INSTAGRAM = "https://www.instagram.com/nolansellsnc/"
FACEBOOK = "https://www.facebook.com/profile.php?id=61578346302536"
CALENDLY = ""  # PLACEHOLDER: paste your Calendly link here
EXT = 'target="_blank" rel="noopener"'

FEATURED = [
  ("5182 Corbin Ln", "Hickory, NC", "https://www.zillow.com/homedetails/5182-Corbin-Ln-Hickory-NC-28601/92556701_zpid/", "images/listings/5182-corbin-ln.jpg"),
  ("1056 Old Hampton Rd", "Boone, NC", "https://www.zillow.com/homedetails/1056-Old-Hampton-Rd-Boone-NC-28607/99379549_zpid/", "images/listings/1056-old-hampton-rd.jpg"),
  ("2137 Olde Farm Rd", "Hudson, NC", "https://www.zillow.com/homedetails/2137-Olde-Farm-Rd-Hudson-NC-28638/70112964_zpid/", "images/listings/2137-olde-farm-rd.jpg"),
]
SOLD = [
  ("7107 Rolling Hills Dr", "Sherrills Ford, NC", "https://www.zillow.com/homedetails/7107-Rolling-Hills-Dr-Sherrills-Ford-NC-28673/71910314_zpid/", "images/listings/7107-rolling-hills-dr.jpg"),
  ("350 14th Ave SW", "Hickory, NC", "https://www.zillow.com/homedetails/350-14th-Ave-SW-Hickory-NC-28602/464120420_zpid/", "images/listings/350-14th-ave-sw.jpg"),
  ("1898 Henry Smith St", "Hickory, NC", "https://www.zillow.com/homedetails/1898-Henry-Smith-St-Hickory-NC-28601/227261430_zpid/", ""),
]
AREAS = {
  "hickory": dict(name="Hickory", scene="golden", county="Catawba County",
    short="Lively downtown, Lake Hickory, and an easy drive to Charlotte and the mountains.",
    intro="Hickory is the largest city in the Catawba Valley, with a lively downtown, Lake Hickory on the Catawba River, and Lenoir-Rhyne University. You get city amenities, lake life, and an easy drive to Charlotte and the mountains.",
    facts=[("Catawba", "County"), ("~1 hr", "To Charlotte"), ("Lake Hickory", "On the water"), ("$XXX,XXX", "Median price*")],
    love=["Downtown restaurants, shops and events", "Lake Hickory for boating and waterfront homes", "Parks, greenways and youth sports", "Quick access to I-40 and US-321"]),
  "newton": dict(name="Newton", scene="dusk", county="Catawba County",
    short="The Catawba County seat, with a historic downtown square and small-town charm.",
    intro="Newton is the county seat of Catawba County, known for its historic courthouse square and small-town feel. It sits just south of Hickory, so you're minutes from shopping, jobs and everything the area offers.",
    facts=[("County Seat", "Catawba County"), ("~15 min", "To Hickory"), ("Historic", "Downtown square"), ("$XXX,XXX", "Median price*")],
    love=["Historic downtown and local events", "More home for your money", "Quiet neighborhoods close to Hickory", "Easy commute in every direction"]),
  "granite-falls": dict(name="Granite Falls", scene="mist", county="Caldwell County",
    short="Quiet living near Lake Rhodhiss, with room to grow and quick trips into town.",
    intro="Granite Falls is a friendly small town in Caldwell County along US-321, between Hickory and Lenoir. It's close to Lake Rhodhiss and Lake Hickory, and a great fit if you want more space and a slower pace without being far from town.",
    facts=[("Caldwell", "County"), ("~15 min", "To Hickory"), ("Lakes", "Rhodhiss & Hickory"), ("$XXX,XXX", "Median price*")],
    love=["Small-town community feel", "Close to lakes and the outdoors", "Larger lots and room to grow", "Quick drive to Hickory and Lenoir"]),
}

NAV = [("about.html", "About"), ("buy.html", "Buy"), ("sell.html", "Sell"), ("listings.html", "Listings"), ("areas.html", "Areas")]

def header(active):
    links = "".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="nav-wrap">
  <nav class="nav-pill"><a href="index.html" class="nav-logo"><img src="images/logo.png" alt="Nestlewood Realty" /></a>{links}</nav>
  <a href="contact.html" class="nav-cta">Let's talk</a>
</header>'''

FOOTER = f'''<footer class="foot">
  <div class="wrap foot-grid">
    <a href="index.html"><img src="images/logo.png" alt="Nestlewood Realty" /></a>
    <p>Nolan Herman, REALTOR® · Nestlewood Realty<br />{ADDRESS}</p>
    <div class="soc"><a href="about.html">About</a><a href="buy.html">Buy</a><a href="sell.html">Sell</a><a href="listings.html">Listings</a><a href="areas.html">Areas</a><a href="contact.html">Contact</a></div>
    <div class="soc"><a href="{INSTAGRAM}" {EXT}>Instagram</a><a href="{FACEBOOK}" {EXT}>Facebook</a><a href="{ZILLOW}" {EXT}>Zillow</a><a href="{HOMES}" {EXT}>Homes.com</a></div>
  </div>
  <div class="wrap fine">© 2026 Nestlewood Realty · Equal Housing Opportunity · REALTOR®</div>
</footer>'''

def page(fname, title, active, body, curtain=False):
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{E(title)}</title>
<meta name="description" content="Nolan Herman, REALTOR® with Nestlewood Realty. Helping buyers and sellers across Hickory, Newton, Granite Falls and the Charlotte area." />
<link rel="icon" href="images/tree-icon.png" />
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

def page_hero(crumb, title_html, sub, scene):
    return f'''<section class="page-hero"><div class="frame">
  <div class="scene" data-scene="{scene}"></div><div class="fog f1"></div><div class="fog f2"></div><div class="shade"></div>
  <div class="ph-copy"><span class="crumb"><i></i> {crumb}</span><h1 class="split-words">{title_html}</h1><p>{sub}</p></div>
</div></section>'''

def card(addr, city, url, photo, sold=False, price=True):
    pic = f'<img src="{photo}" alt="{E(addr)}" />' if photo else '<div class="scene" data-scene="dawn"></div>'
    sub = f"{city} · $XXX,XXX" if (price and not sold) else city
    return f'''<a class="home-card" href="{url}" {EXT}><div class="img">{pic}</div>
  <div class="info glass"><span class="badge{" sold" if sold else ""}">{"Sold" if sold else "Featured"}</span><h3>{E(addr)}</h3><p>{sub}</p></div></a>'''

def rail(items, title_html, eyebrow, link=None):
    return f'''<section class="listings">
  <div class="wrap head"><div><p class="eyebrow">{eyebrow}</p><h2>{title_html}</h2></div>
    <div class="arrows">{f'<a class="pill" href="{link}" style="margin-right:.6rem">View all</a>' if link else ""}<button class="arr prev" aria-label="Previous">←</button><button class="arr next" aria-label="Next">→</button></div></div>
  <div class="rail" tabindex="0">{"".join(card(*i[:4], sold=i in SOLD) for i in items)}</div>
  <div class="wrap"><div class="progress"><span></span></div></div>
</section>'''

def panels(keys, title_html="Find your place in the <em>foothills</em>"):
    out = "".join(f'''<article class="panel{" open" if n == 0 else ""}" data-href="{k}.html"><div class="scene" data-scene="{AREAS[k]["scene"]}"></div><div class="p-shade"></div>
  <div class="p-copy"><span class="num">0{n+1}</span><h3>{AREAS[k]["name"]}</h3><p>{AREAS[k]["short"]}</p><a class="pill light sm" href="{k}.html">Explore {AREAS[k]["name"]}</a></div></article>''' for n, k in enumerate(keys))
    return f'''<section class="areas"><div class="wrap head"><div><p class="eyebrow">Explore the area</p><h2>{title_html}</h2></div><a class="under" href="areas.html">All areas →</a></div>
  <div class="wrap panels">{out}</div></section>'''

REVIEWS = '''<section class="reviews">
  <div class="wrap rv-wrap">
    <p class="eyebrow">Client reviews · ★★★★★</p>
    <div class="quotes">
      <blockquote class="q on"><p>“He looked out for our best interests, getting us a fantastic deal. You feel like you're their <em>only client.</em>”</p><cite>Lorena &amp; Martin · Home Buyers</cite></blockquote>
      <blockquote class="q"><p>“His professionalism, deep market knowledge, and ability to communicate clearly made the entire process <em>far less stressful.</em>”</p><cite>Jacopo B. · Home Buyer</cite></blockquote>
      <blockquote class="q"><p>“We couldn't have asked for a better realtor than Nolan. We absolutely <em>love our new home.</em>”</p><cite>Alfred &amp; Rashonda Wingate · First-Time Buyers</cite></blockquote>
    </div>
    <div class="q-bars"><i class="on"></i><i></i><i></i></div>
    <a class="under" href="''' + ZILLOW + '''" target="_blank" rel="noopener">Read every review on Zillow →</a>
  </div>
</section>'''

VALUE_FORM = '''<form class="line-form lead-form" data-subject="Home value request"><input name="address" placeholder="Your home address" required /><button class="pill solid" type="submit">Get my value</button></form>'''
GUIDE_FORM = '''<form class="line-form lead-form" data-subject="Free buyer's guide request" data-guide="Hickory-Area-Home-Buyers-Guide.pdf"><input name="email" type="email" placeholder="Your email" required /><button class="pill solid" type="submit">Send my guide</button></form>'''

TOOLS = f'''<section class="tools">
  <div class="scene" data-scene="night"></div><div class="stars"></div>
  <div class="wrap tools-grid">
    <div class="glass tool reveal"><p class="eyebrow">Free home value report</p><h3>What's your home <em>worth?</em></h3>
      <p>A personalized value report from Nolan, not an algorithm. Usually within 24 hours.</p>{VALUE_FORM}</div>
    <div class="glass tool reveal"><p class="eyebrow">Free download</p><h3>The Hickory Area <em>Buyer's Guide</em></h3>
      <p>Seven steps from budget to keys, plus a home tour checklist. Written in plain English.</p>{GUIDE_FORM}</div>
  </div>
</section>'''

BOOK = CALENDLY or "contact.html#book"
CTA = f'''<section class="contact">
  <div class="frame small">
    <div class="scene" data-scene="sunset"></div><div class="fog f1"></div><div class="shade"></div>
    <div class="c-copy">
      <h2>Ready when <em>you</em> are.</h2>
      <p>Call, text, email, or book a time. I respond fast.</p>
      <div class="hero-btns center">
        <a class="pill solid" href="tel:{TEL}">Call {PHONE}</a><a class="pill light" href="sms:{TEL}">Text Nolan</a>
        <a class="pill" href="mailto:{EMAIL}">Email Nolan</a><a class="pill" href="{BOOK}">Book a call</a>
      </div>
    </div>
  </div>
</section>'''

MARQUEE = '''<div class="marquee" aria-hidden="true"><div class="track">''' + ("<span>Hickory</span><i>✦</i><span><em>Newton</em></span><i>✦</i><span>Granite Falls</span><i>✦</i><span><em>Lake Hickory</em></span><i>✦</i><span>Charlotte</span><i>✦</i><span><em>Blue Ridge</em></span><i>✦</i>" * 2) + "</div></div>"

COUNTERS = '''<div class="counters reveal">
  <div><b data-count="10" data-prefix="$" data-suffix="M+">$10M+</b><span>Total volume</span></div>
  <div><b data-count="7" data-prefix="$" data-suffix="M+">$7M+</b><span>Sold in 2026</span></div>
  <div><b data-count="100" data-suffix="%">100%</b><span>Listings sold</span></div>
  <div><b data-count="600" data-suffix="+">600+</b><span>Families helped by Nestlewood</span></div>
</div>'''

# ================= HOME =================
page("index.html", "Nolan Herman, REALTOR® | Nestlewood Realty | Hickory, NC", "", f'''
<section class="hero" id="top">
  <div class="frame">
    <div class="scene" data-scene="sunset"></div>
    <video class="hero-video" muted loop playsinline autoplay hidden></video>
    <div class="fog f1"></div><div class="fog f2"></div><div class="fog f3"></div><div class="shade"></div>
    <div class="trace-line" aria-hidden="true"><span class="chip"><i></i> Hickory, North Carolina</span></div>
    <div class="hero-copy">
      <p class="kicker">Nolan Herman · REALTOR® · Nestlewood Realty</p>
      <h1 class="split-words">Let's go <em>home.</em></h1>
      <p class="hero-sub">Buying and selling across Hickory, Newton, Granite Falls and the Charlotte area, made simple.</p>
      <div class="hero-btns"><a class="pill light" href="listings.html">Explore listings</a><a class="pill" href="sell.html#value">What's my home worth?</a></div>
    </div>
    <ul class="hero-stats">
      <li><b data-count="10" data-prefix="$" data-suffix="M+">$10M+</b>total sales volume</li>
      <li><b data-count="7" data-prefix="$" data-suffix="M+">$7M+</b>sold in 2026</li>
      <li><b data-count="100" data-suffix="%">100%</b>of listings sold</li>
    </ul>
    <aside class="glass-card"><small>Meet Nolan</small><p>Real estate runs in my family. Let's find yours.</p>
      <img src="images/headshot.jpg" alt="Nolan Herman" /><a class="pill solid" href="about.html">My story</a></aside>
    <div class="scroll-cue"><span></span></div>
  </div>
</section>
{MARQUEE}
<section class="statement">
  <div class="wrap st-grid">
    <div class="st-photo reveal"><div class="kb"><img src="images/headshot.jpg" alt="Nolan Herman" /></div><span class="tag-glass">2 years · $10M+ sold</span></div>
    <div>
      <p class="eyebrow reveal">Meet Nolan</p>
      <h2 class="words">Real estate runs in my family. I bring the same hustle to every client: fast answers, honest advice, and marketing that gets homes <em>seen.</em></h2>
      <p class="body reveal"><a class="pill solid" href="about.html">Read my story</a></p>
      {COUNTERS}
    </div>
  </div>
</section>
{rail(FEATURED + SOLD, "Homes I'm <em>proud</em> to represent", "Featured &amp; sold", "listings.html")}
{panels(list(AREAS))}
{REVIEWS}
{TOOLS}
{CTA}''', curtain=True)

# ================= ABOUT =================
page("about.html", "About Nolan Herman | Nestlewood Realty", "about.html", f'''
{page_hero("About", "Meet <em>Nolan.</em>", "Licensed REALTOR® with Nestlewood Realty, serving Hickory, Newton, Granite Falls and the Charlotte area.", "golden")}
<section class="statement">
  <div class="wrap st-grid">
    <div class="st-photo reveal"><div class="kb"><img src="images/headshot.jpg" alt="Nolan Herman" /></div><span class="tag-glass">Nestlewood Realty</span></div>
    <div>
      <p class="eyebrow reveal">My story</p>
      <h2 class="words">Real estate runs in my family. My grandpa was an investor. I emailed brokers out of high school until one said <em>yes.</em></h2>
      <p class="body reveal">Growing up, I had a front-row seat to how property can change a family's future. Right out of high school I started emailing local brokers asking for a chance to learn. Most didn't answer. One did, and that email turned into an internship, and that internship turned into a career. Two years later, I've helped clients buy and sell over $10 million in homes, and every one of my listings has sold.</p>
      {COUNTERS}
    </div>
  </div>
</section>
<section class="sec sand"><div class="wrap center"><p class="eyebrow">How I got here</p><h2>From emails to <em>$10M+</em></h2>
  <div class="timeline" style="text-align:left">
    <div class="tl reveal"><i>1</i><h3>Growing up</h3><p>Learned the business watching my grandpa invest in real estate.</p></div>
    <div class="tl reveal"><i>2</i><h3>The emails</h3><p>Out of high school, I emailed brokers asking for a shot.</p></div>
    <div class="tl reveal"><i>3</i><h3>The internship</h3><p>One broker said yes, and I learned every part of the business.</p></div>
    <div class="tl reveal"><i>4</i><h3>REALTOR®</h3><p>Two years in: $10M+ sold and 100% of my listings sold.</p></div>
  </div></div></section>
<section class="sec"><div class="wrap"><p class="eyebrow">Behind the scenes</p><h2>On the <em>job</em></h2>
  <div class="gallery">
    <div class="reveal"><div class="scene" data-scene="golden"></div><span class="label">Action shot: you at a closing</span></div>
    <div class="reveal"><div class="scene" data-scene="dusk"></div><span class="label">Action shot: showing a home</span></div>
    <div class="reveal"><div class="scene" data-scene="mist"></div><span class="label">Action shot: with clients</span></div>
    <div class="reveal"><div class="scene" data-scene="dawn"></div><span class="label">Action shot: open house</span></div>
    <div class="reveal"><div class="scene" data-scene="sunset"></div><span class="label">Action shot: around Hickory</span></div>
  </div>
  <div class="hero-btns" style="margin-top:2.4rem"><a class="pill solid" href="{ZILLOW}" {EXT}>My Zillow profile</a><a class="pill" style="color:var(--ink);border-color:rgba(0,0,0,.25)" href="{HOMES}" {EXT}>My Homes.com profile</a></div>
</div></section>
{REVIEWS}
{CTA}''')

# ================= BUY =================
page("buy.html", "Buy a Home | Nolan Herman, REALTOR®", "buy.html", f'''
{page_hero("Buy", "Buy a <em>home.</em>", "From your first showing to closing day, I'll help you find the right home and negotiate the best deal.", "dawn")}
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
      <label>Home price ($)<input id="c-price" type="number" value="350000" min="0" step="1000" /></label>
      <div class="row2"><label>Down payment (%)<input id="c-down" type="number" value="10" min="0" max="100" /></label><label>Interest rate (%)<input id="c-rate" type="number" value="6.5" min="0" step="0.05" /></label></div>
      <div class="row2"><label>Loan term (years)<input id="c-term" type="number" value="30" min="1" /></label><label>Taxes + insurance / mo ($)<input id="c-extra" type="number" value="350" min="0" step="10" /></label></div>
      <p class="fine">Estimate only. Talk to a lender for your exact numbers.</p>
    </div>
    <div class="result"><div class="scene" data-scene="dusk"></div><small style="letter-spacing:.2em;text-transform:uppercase;font-size:.7rem;opacity:.8">Estimated monthly payment</small><div class="pay" id="c-pay">$0</div>
      <div class="bd"><div><span>Principal &amp; interest</span><b id="c-pi">$0</b></div><div><span>Taxes &amp; insurance</span><b id="c-ti">$0</b></div><div><span>Loan amount</span><b id="c-loan">$0</b></div></div></div>
  </div></div></section>
<section class="tools">
  <div class="scene" data-scene="night"></div><div class="stars"></div>
  <div class="wrap tools-grid">
    <div class="glass tool reveal"><p class="eyebrow">Free download</p><h3>The Hickory Area <em>Buyer's Guide</em></h3>
      <p>Seven steps from budget to keys, plus a home tour checklist. Written in plain English.</p>{GUIDE_FORM}</div>
    <div class="glass tool reveal"><p class="eyebrow">What's inside</p><h3>Everything you need to <em>buy smart</em></h3>
      <ul class="checks"><li>How much home you can really afford</li><li>Getting pre-approved (and why it wins offers)</li><li>How to make an offer that stands out</li><li>Due diligence, inspections and closing, explained</li></ul></div>
  </div>
</section>
{rail(FEATURED, "Homes for <em>sale</em>", "Featured listings", "listings.html")}
{CTA}''')

# ================= SELL =================
page("sell.html", "Sell Your Home | Nolan Herman, REALTOR®", "sell.html", f'''
{page_hero("Sell", "Sell your <em>home.</em>", "Smart pricing, professional photos, and social media marketing that puts your home in front of the right buyers.", "dusk")}
<section class="statement"><div class="wrap">
  <p class="eyebrow reveal">Results</p>
  <h2 class="words" style="max-width:1000px">Every one of my listings has sold. I launch your home like a product, so buyers compete for <em>it.</em></h2>
  <div style="margin-top:3rem">{COUNTERS}</div>
</div></section>
<section class="sec dark"><div class="wrap center"><p class="eyebrow">My selling plan</p><h2>How I get your home <em>sold</em></h2>
  <div class="steps4" style="text-align:left">
    <div class="step reveal"><h3>Price it right</h3><p>A detailed look at recent sales so we list at the right number from day one.</p></div>
    <div class="step reveal"><h3>Make it shine</h3><p>Professional photos and video that make buyers stop scrolling.</p></div>
    <div class="step reveal"><h3>Market everywhere</h3><p>The MLS, Zillow, Homes.com, plus targeted Instagram and Facebook ads.</p></div>
    <div class="step reveal"><h3>Negotiate &amp; close</h3><p>I screen offers, negotiate hard, and handle every detail to closing.</p></div>
  </div></div></section>
<section class="sec sand" id="value"><div class="wrap split2">
  <div class="reveal"><p class="eyebrow">Free home value report</p><h2>What's your home <em>worth?</em></h2>
    <p class="lead">Tell me a little about your home and I'll send a personalized value report, usually within 24 hours.</p>
    <ul class="checks"><li>Based on real recent sales near you</li><li>Prepared by me, not a computer</li><li>No pressure and no obligation</li></ul></div>
  <form class="form reveal lead-form" data-subject="Home value report request">
    <label>Property address<input name="address" required /></label>
    <div class="row2"><label>Beds<input name="beds" /></label><label>Baths<input name="baths" /></label></div>
    <div class="row2"><label>Name<input name="name" required /></label><label>Phone<input name="phone" type="tel" /></label></div>
    <label>Email<input name="email" type="email" required /></label>
    <label>Timeline<select name="timeline"><option>Just curious</option><option>Within 3 months</option><option>3–6 months</option><option>6+ months</option></select></label>
    <button class="pill solid" type="submit">Get my free report</button>
  </form></div></section>
{rail(SOLD, "Recently <em>sold</em>", "Results")}
{REVIEWS}
{CTA}''')

# ================= LISTINGS =================
page("listings.html", "Listings | Nolan Herman, REALTOR®", "listings.html", f'''
{page_hero("Listings", "Featured <em>homes.</em>", "My featured homes and recent sales across the Catawba Valley and beyond.", "golden")}
<section class="sec dark"><div class="wrap"><div class="head"><div><p class="eyebrow">For sale</p><h2>Featured <em>listings</em></h2></div><a class="pill" href="{ZILLOW}" {EXT}>All on Zillow</a></div>
  <div class="grid3">{"".join(card(*l) for l in FEATURED)}</div></div></section>
<section class="sec"><div class="wrap"><div class="head"><div><p class="eyebrow">Results</p><h2>Recently <em>sold</em></h2></div></div>
  <div class="grid3">{"".join(card(*l, sold=True) for l in SOLD)}</div></div></section>
{TOOLS}
{CTA}''')

# ================= AREAS =================
page("areas.html", "Areas I Serve | Nolan Herman, REALTOR®", "areas.html", f'''
{page_hero("Areas", "Find your <em>place.</em>", "Local guides to help you find the right town, the right neighborhood, and the right home.", "mist")}
{panels(list(AREAS), "Hickory, Newton &amp; <em>Granite Falls</em>")}
<section class="sec tight"><div class="wrap center"><p class="lead">Also serving Charlotte, Conover, Lenoir, Hudson, Sherrills Ford, Boone and the surrounding area.</p></div></section>
{CTA}''')

for key, a in AREAS.items():
    others = [k for k in AREAS if k != key]
    page(f"{key}.html", f"Living in {a['name']}, NC | Nolan Herman, REALTOR®", "areas.html", f'''
{page_hero(f"Areas / {a['name']}", f"Living in <em>{a['name']}.</em>", a["short"], a["scene"])}
<section class="sec"><div class="wrap split2">
  <div class="reveal"><p class="eyebrow">{a["county"]}</p><h2>Why people love <em>{a["name"]}</em></h2><p class="lead">{a["intro"]}</p>
    <ul class="checks">{"".join(f"<li>{E(x)}</li>" for x in a["love"])}</ul>
    <div class="hero-btns" style="margin-top:2rem"><a class="pill solid" href="contact.html">Find a home in {a["name"]}</a></div></div>
  <div class="area-photo reveal"><div class="scene" data-scene="{a["scene"]}"></div><span class="tag-glass">Photo of {a["name"]} goes here</span></div>
</div>
<div class="wrap"><div class="facts">{"".join(f'<div class="fact reveal"><b>{E(x)}</b><span>{E(y)}</span></div>' for x, y in a["facts"])}</div>
  <p class="fine" style="margin-top:1rem">*Market numbers are placeholders. Update with current local data.</p></div></section>
{panels(others, "Nearby <em>areas</em>")}
{TOOLS}
{CTA}''')

# ================= CONTACT =================
page("contact.html", "Contact Nolan Herman | Nestlewood Realty", "contact.html", f'''
{page_hero("Contact", "Let's <em>talk.</em>", "Call, text, email, or book a time. I respond fast.", "sunset")}
<section class="sec"><div class="wrap split2 top">
  <div class="reveal"><p class="eyebrow">Reach me</p><h2>I'm here to <em>help.</em></h2>
    <div class="contact-list">
      <a class="pill solid" href="tel:{TEL}">Call {PHONE}</a><a class="pill" href="sms:{TEL}">Text Nolan</a><a class="pill" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="pill" href="{MAP}" {EXT}>{ADDRESS}</a>
    </div></div>
  <form class="form reveal lead-form" data-subject="Website contact form" style="background:#ebe3d8">
    <div class="row2"><label>Name<input name="name" required /></label><label>Phone<input name="phone" type="tel" /></label></div>
    <label>Email<input name="email" type="email" required /></label>
    <label>I'm interested in<select name="topic"><option>Buying</option><option>Selling</option><option>Home value report</option><option>Something else</option></select></label>
    <label>Message<textarea name="message" rows="4"></textarea></label>
    <button class="pill solid" type="submit">Send message</button>
  </form></div></section>
<section class="sec tight" id="book"><div class="wrap">
  <div class="booking reveal"><div class="scene" data-scene="night"></div><div class="stars"></div>
    <div><p class="eyebrow" style="color:rgba(255,255,255,.7)">Book a call</p><h2>Pick a <em>time.</em></h2>
      <div class="cal">{"".join(f'<i class="{"sel" if d == 14 else "av" if d in (9,10,15,16,17,21,22) else ""}">{d}</i>' for d in range(5, 26))}</div>
      <p class="fine" style="color:rgba(255,255,255,.7)">PLACEHOLDER: your Calendly calendar goes here.</p></div></div>
</div></section>''')
print("built")
