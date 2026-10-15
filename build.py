"""Build the Chalant merchant documentation.

Usage: python3 build.py <path to the Chalant theme>

The settings reference is generated from the theme's own schemas and
locale file, so its wording always matches the theme editor. The guides
are written in GUIDES below. Output is plain HTML in this folder, served
by GitHub Pages.
"""
import html
import json
import re
import sys
from pathlib import Path

THEME = Path(sys.argv[1] if len(sys.argv) > 1 else "../plaiter-theme")
OUT = Path(__file__).parent
SUPPORT_EMAIL = "plaiterhq@gmail.com"
SUPPORT_FORM = "https://form.jotform.com/262867756735071"

LOCALE = json.loads((THEME / "locales/en.default.schema.json").read_text())


def t(value):
    """Resolve a t: translation key from the schema locale."""
    if isinstance(value, str) and value.startswith("t:"):
        node = LOCALE
        for key in value[2:].split("."):
            node = node.get(key, {}) if isinstance(node, dict) else {}
        return node if isinstance(node, str) else value
    return value or ""


def schema(path):
    match = re.search(r"{% schema %}(.*){% endschema %}", path.read_text(), re.S)
    return json.loads(match.group(1)) if match else None


def esc(text):
    return html.escape(str(text))


# ---------------------------------------------------------------- reference

SECTION_NOTES = {
    "announcement-bar": "A slim bar above the header for a promotion or shipping news.",
    "header": "Logo, main menu, search, account and cart. The main menu supports three levels, and the header can stay at the top of the screen as visitors scroll.",
    "footer": "Your store description, menu columns, newsletter signup and social media, shown as icons or as a column of links. The bottom bar has the country and language selectors, payment icons, the copyright line and policy links, and your store name can run across the very bottom in the accent color.",
    "image-banner": "A large image with a heading, text and buttons on top. Add a separate mobile image for phones, and a foreground image, such as a product cut out on a transparent background, that moves separately from the image as visitors scroll.",
    "marquee": "A line of short messages that scrolls across the page. It pauses on hover and stays still for visitors who prefer reduced motion.",
    "featured-collection": "A grid of products from one collection. Until you choose a collection, example cards show how it will look.",
    "featured-product": "One product with its gallery, price, options and buy buttons, anywhere on a page.",
    "media-with-text": "An image or a Shopify-hosted video beside your own blocks of text and buttons.",
    "statistics": "Large numbers with short descriptions, such as orders shipped or the share of natural ingredients.",
    "testimonials": "Customer quotes, with an optional photo, name and role. In the stacked layout, on larger screens with animations on, each card slides over the one before it.",
    "faq": "A heading beside numbered questions that open and close.",
    "newsletter": "An email signup form. Subscribers are added to your customer list in Shopify.",
    "product-lineup": "A row of product cutouts standing side by side under an introduction and an optional badge, as on the Chalant demo. Add a product block for each cutout and set its size so smaller products stay smaller. With animations on, the products settle into place as visitors scroll.",
    "routine": "Chalant's routine builder: shoppers pick one product for each step and add the whole routine to the cart. See the Routine builder guide.",
    "section": "An empty section to build your own layout from blocks.",
    "custom-liquid": "Add app snippets or other Liquid code.",
    "product": "The main product page. Each element, such as the title, price or buy buttons, is its own block you can reorder or remove.",
    "product-recommendations": "Related products, chosen automatically by Shopify.",
    "collection": "The product grid for a collection, with filters and sorting.",
    "collections": "A list of all your collections.",
    "search": "Search results with filters and sorting.",
    "cart": "The cart page, with quantities, order note, totals and checkout buttons.",
    "blog": "The list of articles in a blog, with an optional tag filter.",
    "article": "A single article with its image, author, share button and comments.",
    "page": "The content of a page you write in Online Store, Pages.",
    "contact-form": "A contact form. On a page, leave the heading and text blank to use the page's title and content.",
    "404": "The page shoppers see when a link is broken.",
    "password": "The page shown while your store is password protected.",
}

BLOCK_NOTES = {
    "heading": "A heading. Italic text uses the accent font and bold text is highlighted.",
    "text": "A paragraph of text.",
    "button": "A link styled as a button.",
    "image": "An image, with an optional link.",
    "group": "Holds other blocks in a row or a column.",
    "custom-liquid": "Add app snippets or other Liquid code.",
    "collapsible-content": "A row that opens to show more text, such as ingredients or care details.",
    "routine": "The routine builder. Add it to a product page to suggest a full routine around the product being viewed.",
    "_routine-step": "One step of a routine, such as Cleanse or Treat, with the products to choose from.",
    "product-title": "The product title.",
    "product-price": "The price, sale price and unit price.",
    "product-variant-picker": "Buttons or dropdowns for the product's options, with color swatches where set up.",
    "product-buy-buttons": "Quantity, purchase options for subscriptions, Add to cart, and the accelerated checkout buttons.",
    "product-description": "The product description.",
    "pickup-availability": "Shows whether the product can be picked up in store.",
    "complementary-products": "Products that pair well with this one, set up in the Search and Discovery app.",
    "_product-media-gallery": "The product's images, videos and 3D models.",
    "_footer-menu": "A column of links from one of your menus.",
    "_stat": "One number and its description.",
    "_testimonial": "One customer quote.",
}

SECTION_ORDER = [
    ("Header and footer", ["announcement-bar", "header", "footer"]),
    ("Home page and any page", ["image-banner", "marquee", "featured-collection", "featured-product",
                                "media-with-text", "product-lineup", "routine", "statistics", "testimonials", "faq",
                                "newsletter", "section", "custom-liquid"]),
    ("Product pages", ["product", "product-recommendations"]),
    ("Collections and search", ["collection", "collections", "search"]),
    ("Cart", ["cart"]),
    ("Blog and pages", ["blog", "article", "page", "contact-form"]),
    ("Other pages", ["404", "password"]),
]

BLOCK_ORDER = [
    ("Content blocks", ["heading", "text", "button", "image", "group", "collapsible-content", "custom-liquid"]),
    ("Product page blocks", ["_product-media-gallery", "product-title", "product-price", "product-variant-picker",
                             "product-buy-buttons", "product-description", "pickup-availability",
                             "complementary-products"]),
    ("Routine builder blocks", ["routine", "_routine-step"]),
    ("Blocks inside sections", ["_stat", "_testimonial", "_footer-menu"]),
]

# Used when a setting has no info text of its own, before the type hints below.
ID_HINTS = {
    "routine_step_tag_prefix": "How product tags that name a routine step begin. With step:, a product tagged step:Cleanse shows Cleanse on its product card.",
    "show_routine_step_on_cards": "Shows a product's routine step on product cards across the store.",
    "logo_width": "",
    **{f"social_{n}_link": "The full link to your profile. Leave it blank to hide the icon." for n in
       ["instagram", "facebook", "twitter", "x", "tiktok", "youtube", "pinterest"]},
}

# Used when a setting has no info text of its own.
TYPE_HINTS = {
    "image_picker": "Upload an image or choose one from your files.",
    "video": "Upload a video or choose one hosted on Shopify.",
    "color_scheme": "The color scheme for this area. Edit schemes in Theme settings, Colors.",
    "font_picker": "Choose a font from Shopify's font library.",
    "text": "Text shown to shoppers.",
    "product": "Choose a product.",
    "inline_richtext": "Text shown to shoppers. Italic words use the accent font.",
    "richtext": "Text shown to shoppers.",
    "url": "Where the link goes.",
    "link_list": "Choose a menu from Online Store, Navigation.",
    "collection": "Choose a collection.",
    "product_list": "Choose the products.",
    "checkbox": "Turn this on or off.",
    "liquid": "Liquid code, such as an app snippet.",
    "text_alignment": "Left, center or right.",
}


def settings_table(settings):
    rows = []
    for s in settings:
        kind = s.get("type")
        if kind == "header":
            rows.append(f'<tr class="group"><th colspan="2" scope="colgroup">{esc(t(s.get("content")))}</th></tr>')
            continue
        if kind == "paragraph":
            rows.append(f'<tr class="note"><td colspan="2">{esc(t(s.get("content")))}</td></tr>')
            continue
        label = t(s.get("label")) or {"color_scheme_group": "Color schemes"}.get(kind, "")
        if not label:
            continue
        detail = [t(s.get("info")) or ID_HINTS.get(s.get("id"), "") or TYPE_HINTS.get(kind, "")]
        if s.get("options"):
            detail.append("Options: " + ", ".join(t(o.get("label")) for o in s["options"]) + ".")
        if kind == "range":
            unit = s.get("unit", "")
            detail.append(f'From {s.get("min")}{unit} to {s.get("max")}{unit}.')
        rows.append(f"<tr><th scope=\"row\">{esc(label)}</th><td>{esc(' '.join(d for d in detail if d))}</td></tr>")
    if not rows:
        return '<p class="muted">No settings.</p>'
    return '<div class="table"><table><thead><tr><th scope="col">Setting</th><th scope="col">What it does</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"


def reference():
    parts = ['<h1>Settings reference</h1>',
             '<p class="lede">Every setting in Chalant, using the same names you see in the theme editor. Open the editor from Online Store, Themes, Customize.</p>',
             '<nav class="toc" aria-label="On this page"><a href="#theme-settings">Theme settings</a><a href="#sections">Sections</a><a href="#blocks">Blocks</a></nav>']

    data = json.loads((THEME / "config/settings_schema.json").read_text())
    parts.append('<h2 id="theme-settings">Theme settings</h2>')
    parts.append("<p>Theme settings apply to the whole store. Open them from the gear icon in the theme editor.</p>")
    for group in data[1:]:
        name = t(group["name"])
        parts.append(f'<h3 id="settings-{esc(re.sub("[^a-z]+", "-", name.lower()))}">{esc(name)}</h3>')
        if group["settings"] and group["settings"][0].get("type") == "color_scheme_group":
            roles = [t(r.get("label")) for r in group["settings"][0].get("definition", []) if r.get("label")]
            parts.append("<p>Color schemes set the colors for a section or block. Each scheme has these colors: "
                         + esc(", ".join(roles)) + ". Edit a scheme once and every section using it updates.</p>")
            continue
        parts.append(settings_table(group["settings"]))

    parts.append('<h2 id="sections">Sections</h2>')
    parts.append("<p>Add sections with Add section in the theme editor. Every page that supports sections can also use the Custom Liquid section and app blocks.</p>")
    for heading, handles in SECTION_ORDER:
        parts.append(f"<h3>{esc(heading)}</h3>")
        for handle in handles:
            data = schema(THEME / f"sections/{handle}.liquid")
            parts.append(f'<h4 id="section-{handle}">{esc(t(data["name"]))}</h4>')
            if handle in SECTION_NOTES:
                parts.append(f"<p>{esc(SECTION_NOTES[handle])}</p>")
            parts.append(settings_table(data.get("settings", [])))
            local = [b for b in data.get("blocks", []) if b.get("settings")]
            for block in local:
                parts.append(f"<h5>{esc(t(block.get('name')))} block</h5>")
                parts.append(settings_table(block["settings"]))

    parts.append('<h2 id="blocks">Blocks</h2>')
    parts.append("<p>Blocks are the pieces inside a section. Select a section in the theme editor and choose Add block.</p>")
    for heading, handles in BLOCK_ORDER:
        parts.append(f"<h3>{esc(heading)}</h3>")
        for handle in handles:
            data = schema(THEME / f"blocks/{handle}.liquid")
            parts.append(f'<h4 id="block-{handle.strip("_")}">{esc(t(data["name"]))}</h4>')
            if handle in BLOCK_NOTES:
                parts.append(f"<p>{esc(BLOCK_NOTES[handle])}</p>")
            parts.append(settings_table([s for s in data.get("settings", []) if s.get("type") != "product"]))
    return "\n".join(parts)


# ------------------------------------------------------------------- guides

GET_STARTED = f"""
<h1>Chalant documentation</h1>
<p class="lede">Chalant is a Shopify theme for skincare and beauty brands. Its routine builder lets shoppers choose one product for each step of a routine and add the whole routine to their cart at once.</p>

<div class="cards">
  <a class="card" href="routine-builder.html"><strong>Routine builder</strong><span>Set up routines on your home page and product pages.</span></a>
  <a class="card" href="products.html"><strong>Products</strong><span>Options and swatches, subscriptions, gift cards, pickup and filters.</span></a>
  <a class="card" href="settings.html"><strong>Settings reference</strong><span>Every section, block and theme setting.</span></a>
  <a class="card" href="faq.html"><strong>FAQ and support</strong><span>Common questions and how to reach us.</span></a>
</div>

<h2 id="install">Install Chalant</h2>
<ol>
  <li>In your Shopify admin, go to Online Store, Themes.</li>
  <li>Add Chalant from the Shopify Theme Store. It appears in your theme library.</li>
  <li>Choose Customize to set it up. Your live store doesn't change until you publish Chalant.</li>
  <li>When you're happy with it, choose Publish.</li>
</ol>

<h2 id="customize">Customize your store</h2>
<p>Everything in Chalant is set up in the theme editor: Online Store, Themes, Customize.</p>
<ul>
  <li><strong>Choose the page to edit</strong> from the menu at the top of the editor: home page, products, collections, cart, blog posts and more.</li>
  <li><strong>Add a section</strong> with Add section. Sections stack from top to bottom.</li>
  <li><strong>Add blocks</strong> inside a section to add headings, text, buttons, images and more. Drag blocks to reorder them.</li>
  <li><strong>Theme settings</strong>, under the gear icon, set your logo, fonts, colors, page width and social media links for the whole store.</li>
</ul>

<h2 id="first-steps">Recommended first steps</h2>
<ol>
  <li><strong>Logo and favicon.</strong> Theme settings, Logo. Tall logos are kept to the height of the header automatically.</li>
  <li><strong>Colors.</strong> Theme settings, Colors. Chalant comes with five color schemes. Edit a scheme once and every section using it updates.</li>
  <li><strong>Fonts.</strong> Theme settings, Typography. The accent font is used for single highlighted words. In any heading, make a word italic to use it.</li>
  <li><strong>Menus.</strong> Online Store, Navigation. The header uses your main menu and supports three levels. Footer columns each use a menu you choose.</li>
  <li><strong>Home page.</strong> Replace the example text in each section with your own, and choose a collection for Featured collection.</li>
  <li><strong>Routine builder.</strong> Follow the <a href="routine-builder.html">routine builder guide</a>.</li>
</ul>

<h2 id="animations">Animations</h2>
<p>Chalant moves gently as visitors scroll: the banner's images drift and fade, sections glide into place, product lineups settle, testimonial cards stack and the footer's store name rises into view. Buttons, links and product cards respond on hover.</p>
<p>To turn animations off, open Theme settings, Layout and turn off <strong>Show animations</strong>. Visitors who turn off motion on their device never see animations, whatever the setting.</p>

<h2 id="templates">Pages in Chalant</h2>
<p>Chalant includes layouts for every page Shopify needs, plus two extra page layouts:</p>
<ul>
  <li><strong>About:</strong> an image or video beside a short introduction, then your page content. Choose it for a page under Theme template, about.</li>
  <li><strong>Contact:</strong> a contact form that uses the page's title and content as its introduction. Choose Theme template, contact.</li>
</ul>

<h2 id="code">Editing the theme code</h2>
<p>Before you edit any theme code, duplicate the theme from Online Store, Themes, so you can go back if something breaks. Code changes aren't covered by support. For custom work, we recommend hiring a <a href="https://www.shopify.com/partners/directory">Shopify Partner</a>.</p>
"""

ROUTINE = """
<h1>Routine builder</h1>
<p class="lede">The routine builder lets shoppers build a routine one step at a time, such as Cleanse, Treat and Protect, choosing one product for each. They see a running total and add the whole routine to their cart with one button.</p>

<h2 id="where">Where you can use it</h2>
<ul>
  <li><strong>Any page, as a section.</strong> Add the Routine builder section, for example to your home page.</li>
  <li><strong>Product pages, as a block.</strong> In the Product information section, add the Routine builder block. When a shopper views a product that's part of a step, that product is chosen for them in its step.</li>
</ul>

<h2 id="set-up">Set up a routine</h2>
<ol>
  <li>In the theme editor, add the Routine builder section, or select the Routine builder block on a product page.</li>
  <li>Give the routine a <strong>Routine name</strong>, such as Morning routine. Shoppers see it in the cart next to each product from the routine.</li>
  <li>Add a <strong>Step</strong> block for each step. Give it a <strong>Step name</strong>, such as Cleanse, and an optional <strong>Description</strong>.</li>
  <li>In each step, choose the <strong>Products to choose from</strong>. Shoppers pick one of them.</li>
  <li>Turn on <strong>Optional step</strong> for steps shoppers can skip. They see a Skip this step choice and the total updates.</li>
  <li>Choose a <strong>Layout</strong> and change the <strong>Button label</strong> if you like.</li>
</ol>
<p>Steps with no products are hidden from shoppers. A routine with no steps is hidden too, so you can set it up in the editor before anyone sees it.</p>

<h2 id="cart">In the cart</h2>
<p>Each product from a routine is added as its own cart line, labeled with the routine name, for example Part of Morning routine. Shoppers can change quantities or remove items like any other line. If a product can't be added, for example because it just sold out, the shopper sees a message explaining why.</p>
<p>Products with several options, such as size, show a dropdown once chosen, so the shopper picks the exact variant.</p>

<h2 id="tags">Show the step on product cards</h2>
<p>Product cards across your store can show which step a product belongs to, as a small label such as Cleanse.</p>
<ol>
  <li>Add a tag to the product that starts with the step tag prefix, for example <code>step:Cleanse</code>.</li>
  <li>In Theme settings, Routines, check that <strong>Show routine step on product cards</strong> is on. Change the <strong>Step tag prefix</strong> if you already use step: for something else.</li>
</ol>

<h2 id="ideas">Ideas</h2>
<ul>
  <li>A morning routine and an evening routine on the home page, as two sections.</li>
  <li>A routine block on every serum's product page, suggesting the cleanser before it and the moisturizer after.</li>
  <li>A gift set builder: Choose a scent, Choose a body lotion, Add a candle.</li>
</ul>
"""

PRODUCTS = """
<h1>Products</h1>
<p class="lede">How Chalant shows product features that you set up in your Shopify admin.</p>

<h2 id="options">Options and color swatches</h2>
<p>Product options show as buttons or a dropdown. Choose the style in the Variant picker block. Options with no available variant stay selectable and are struck through, so shoppers can see what exists.</p>
<p>To show color swatches, set the product's category in the product page of your admin, then link the color option to the category's color metafield. Each value can have a color or an image. Chalant shows the swatch on the product page and in collection filters.</p>

<h2 id="media">Images and video</h2>
<p>Add images, videos and 3D models to a product in your admin. When a shopper picks a variant that has its own image, the gallery moves to it. Set a focal point on an image in your admin to keep the important part in view when it's cropped.</p>

<h2 id="subscriptions">Subscriptions</h2>
<p>Install a subscription app, such as Shopify Subscriptions, and add a subscription plan to a product. Chalant shows the plans under Purchase options, with the subscription price, and the cart shows the plan the shopper chose. Products that can only be bought on subscription preselect the first plan.</p>

<h2 id="gift-cards">Gift cards</h2>
<p>Create a gift card product in Products, Gift cards. On its product page, shoppers can choose to send it to someone else, with the recipient's email, name, a message and a send date. What they type is kept if they change the amount.</p>

<h2 id="pairs">Pairs well with</h2>
<p>Install Shopify's free Search and Discovery app and add complementary products to a product. In the theme editor, add the Complementary products block to the product page. Products without complementary products don't show the block.</p>
<p>The Related products section below the product page works on its own. Shopify chooses related products automatically.</p>

<h2 id="pickup">Local pickup</h2>
<p>Turn on local pickup for a location in Settings, Shipping and delivery. The Pickup availability block shows whether the product can be picked up and opens store details.</p>

<h2 id="filters">Filters and sorting</h2>
<p>Install the Search and Discovery app to choose which filters appear on collection and search pages, such as availability, price, product type or color. Turn filtering and sorting on or off in the Collection and Search results sections, and choose whether filters show in a sidebar or a drawer on large screens.</p>

<h2 id="unit-price">Unit prices and Shop Pay Installments</h2>
<p>Unit prices you set on a variant, such as $93.30 / 100 ml, show on product cards, the product page and in the cart. When Shop Pay Installments is turned on for your store, the installment message shows under the price on the product page.</p>
"""

FAQ_ITEMS = [
    ("How do I change the colors?", "In the theme editor, open Theme settings, Colors. Edit a color scheme and every section using it updates. Each section has a Color scheme setting to pick which scheme it uses."),
    ("Why doesn't a section show on my store?", "Statistics, Testimonials and FAQ sections with no blocks, a Routine builder with no products, and a Featured collection whose collection is empty are hidden from shoppers. They still show in the theme editor so you can finish setting them up."),
    ("How do I add the routine builder to my product pages?", "Open a product page in the theme editor, select the Product information section and add the Routine builder block. See the routine builder guide."),
    ("Why isn't the routine step showing on my product cards?", "Tag the product with the step tag prefix and a step name, such as step:Cleanse, and check that Show routine step on product cards is on in Theme settings, Routines."),
    ("How do I show subscriptions?", "Install a subscription app and add a subscription plan to the product. Purchase options appear on the product page automatically."),
    ("How do I set up filters?", "Install Shopify's Search and Discovery app and choose your filters there. Turn filtering on in the Collection and Search results sections."),
    ("Can I use a different layout for one page?", "Yes. In the theme editor, create a template from the page menu at the top, set it up, then choose it for the page in your admin under Theme template."),
    ("How do I translate the theme?", "Go to Online Store, Themes, then the menu next to Customize, Edit default theme content. Add languages in Settings, Languages, and use the Translate and Adapt app for content."),
    ("Does Chalant work with apps?", "Yes. Product pages, featured products and most sections accept app blocks. Choose Add block, Apps in the theme editor. Apps that need code changes may need help from the app developer."),
    ("How do I turn off animations?", "In Theme settings, Layout, turn off Show animations. Visitors who reduce motion on their device never see animations."),
    ("How do I make the banner's product move separately?", "In the Image banner section, add a Foreground image: a transparent PNG the same size as the main image, with only the product on it. It drifts at its own speed as visitors scroll."),
    ("How do I update Chalant?", "When a new version is released, Shopify shows it in your theme library. Updating adds the new version as a copy with your settings, so you can check it before publishing."),
]

FAQ = "<h1>FAQ and support</h1>\n<p class=\"lede\">Answers to common questions, and how to get help with Chalant.</p>\n<h2 id=\"faq\">Frequently asked questions</h2>\n" + "\n".join(
    f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ_ITEMS
) + f"""
<h2 id="support">Support</h2>
<p><a class="button" href="{SUPPORT_FORM}">Contact Chalant support</a></p>
<p>The support form asks for your store URL, a description of the problem and any screenshots, so we can help quickly. You'll get an email confirming we have your request. You can also email <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>.</p>

<h2 id="policy">Support policy</h2>
<ul>
  <li>We reply within two business days, Monday to Friday.</li>
  <li>Support covers setting up and using Chalant's features and settings, and fixing anything in the theme that doesn't work as described here.</li>
  <li>Support doesn't cover changes to the theme code, design work, or problems caused by third-party apps or code edits. For custom work, we recommend a <a href="https://www.shopify.com/partners/directory">Shopify Partner</a>.</li>
  <li>We fix critical bugs as soon as we find them and release updates through the Shopify Theme Store.</li>
</ul>
"""

PAGES = [
    ("index.html", "Get started", GET_STARTED),
    ("routine-builder.html", "Routine builder", ROUTINE),
    ("products.html", "Products", PRODUCTS),
    ("settings.html", "Settings reference", None),
    ("faq.html", "FAQ and support", FAQ),
]

STYLE = """
:root{--bg:#fff;--fg:#18181b;--muted:#5f5f68;--surface:#f4f4f5;--blush:#fff7f7;--line:#e4e4e7;--accent:#0a11cf;
--body:"Libre Franklin","Helvetica Neue",Arial,sans-serif;--display:"Cormorant",Georgia,serif}
@media (prefers-color-scheme:dark){:root{--bg:#0d0d10;--fg:#f4f4f5;--muted:#a8a8b3;--surface:#1b1b20;--blush:#1f1618;--line:#2c2c33;--accent:#9da1ff;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:400 17px/1.6 var(--body)}
a{color:var(--accent)}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:16px;background:var(--bg);padding:8px 12px;z-index:2}
.top{border-bottom:1px solid var(--line);padding:0 20px}
.top-inner{max-width:72rem;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:8px 24px;min-height:64px}
.brand{font:italic 700 28px/1 var(--display);color:var(--accent);text-decoration:none;margin-right:auto}
.brand span{font:500 14px var(--body);color:var(--muted);font-style:normal;margin-left:6px}
.top nav{display:flex;flex-wrap:wrap;gap:4px 16px}
.top nav a{color:var(--fg);text-decoration:none;font-size:15px;padding:10px 0}
.top nav a[aria-current=page]{text-decoration:underline;text-underline-offset:6px}
.top nav a:hover{color:var(--accent)}
main{max-width:46rem;margin:0 auto;padding:40px 20px 80px}
main.wide{max-width:60rem}
h1{font-size:clamp(2rem,1.6rem + 2vw,2.75rem);line-height:1.05;letter-spacing:-.04em;margin:0 0 12px;text-wrap:balance}
h2{font-size:1.6rem;letter-spacing:-.03em;margin:48px 0 12px;line-height:1.15}
h3{font-size:1.25rem;letter-spacing:-.02em;margin:36px 0 8px}
h4{font-size:1.05rem;margin:28px 0 6px}
h5{font-size:.95rem;margin:16px 0 6px;color:var(--muted)}
.lede{font-size:1.2rem;color:var(--muted);margin:0 0 24px}
.muted{color:var(--muted)}
li{margin:4px 0}
code{background:var(--surface);padding:1px 6px;font-size:.9em}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:24px 0}
@media (max-width:560px){.cards{grid-template-columns:1fr}}
.card{display:flex;flex-direction:column;gap:4px;padding:18px;background:var(--blush);color:var(--fg);text-decoration:none}
.card span{color:var(--muted);font-size:15px}
.card:hover strong{color:var(--accent)}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 8px}
.toc a{background:var(--surface);color:var(--fg);text-decoration:none;padding:8px 14px;border-radius:999px;font-size:15px}
.table{overflow-x:auto;margin:8px 0 16px}
table{border-collapse:collapse;width:100%;font-size:15px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
thead th{font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
tbody th{font-weight:600;width:34%}
tr.group th{background:var(--surface);font-size:13px;text-transform:uppercase;letter-spacing:.05em}
tr.note td{color:var(--muted)}
details{border-bottom:1px solid var(--line);padding:4px 0}
summary{cursor:pointer;font-weight:600;min-height:44px;display:flex;align-items:center}
summary:hover{color:var(--accent)}
details p{margin:0 0 14px;color:var(--muted)}
footer{border-top:1px solid var(--line);padding:24px 20px;color:var(--muted);font-size:14px;text-align:center}
"""


def page(filename, title, body):
    current = ' aria-current="page"'
    nav = "".join(
        f'<a href="{f}"{current if f == filename else ""}>{esc(n)}</a>' for f, n, _ in PAGES
    )
    wide = ' class="wide"' if filename == "settings.html" else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} – Chalant documentation</title>
<meta name="description" content="Documentation for Chalant, a Shopify theme for skincare and beauty brands.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@1,700&family=Libre+Franklin:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="top"><div class="top-inner"><a class="brand" href="index.html">Chalant<span>documentation</span></a><nav aria-label="Documentation">{nav}</nav></div></header>
<main id="content"{wide}>
{body}
</main>
<footer>Chalant by Plaiter. Questions? <a href="{SUPPORT_FORM}">Contact support</a>.</footer>
</body>
</html>
"""


def main():
    (OUT / "style.css").write_text(STYLE.strip() + "\n")
    for filename, title, body in PAGES:
        (OUT / filename).write_text(page(filename, title, body if body is not None else reference()))
    print("built", ", ".join(f for f, _, _ in PAGES))


if __name__ == "__main__":
    main()
