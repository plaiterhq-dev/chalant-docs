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
    "header": "Logo, search, account, cart and the main menu, in one of two layouts. The floating pill shows your element symbols and opens into a panel with the main menu and the formula table. The bar puts the main menu across the top, with three levels. Either can stay at the top of the screen as visitors scroll.",
    "footer": "Your store description, menu columns, newsletter signup and social media, shown as icons or as a column of links. The formula index shows your element tiles above the bottom bar, which has the country and language selectors, payment icons, the copyright line and policy links.",
    "image-banner": "A large image with a heading, text and buttons on top. Add Element pin blocks to pin element tiles to the photo, such as Vitamin C on the cheek. Add a separate mobile image for phones, and a foreground image, such as a product cut out on a transparent background, that moves separately from the image as visitors scroll.",
    "marquee": "A line of short messages that scrolls across the page. It pauses on hover and stays still for visitors who prefer reduced motion.",
    "featured-collection": "A grid of products from one collection. Until you choose a collection, example cards show how it will look.",
    "featured-product": "One product with its gallery, price, options and buy buttons, anywhere on a page.",
    "media-with-text": "An image or a Shopify-hosted video beside your own blocks of text and buttons.",
    "statistics": "Large numbers with short descriptions, such as orders shipped or the share of natural ingredients.",
    "testimonials": "Customer quotes, with an optional photo, name and role. In the stacked layout, on larger screens with animations on, each card slides over the one before it.",
    "faq": "A heading beside numbered questions that open and close.",
    "newsletter": "An email signup form. Subscribers are added to your customer list in Shopify.",
    "formula-table": "Your actives as a periodic table. Pointing at a tile opens that element: its photo, description, first products with their formulas, and a link to its collection. See the Formula guide.",
    "strength-story": "One product that comes in strengths. A slider moves through them; the gauge fills, the strength shows large, the advice for that strength lists below and the button adds that strength to the cart.",
    "face-map": "A full-width portrait with face zones. Pointing at a zone rings it and shows its note and products. Add a zone block for each area and set its position on the photo.",
    "feel-finder": "Texture swatches in a row. Picking one places it on two scales, light to rich and matte to dewy, and links to that texture's collection. Add a block for each texture.",
    "formula-compare": "Two products side by side as labels, with the same lines in the same order: lead active, support ingredient, pH, type and price.",
    "section": "An empty section to build your own layout from blocks.",
    "custom-liquid": "Add app snippets or other Liquid code.",
    "product-formula": "Every ingredient of the product in order of amount, with a bar to scale and its percentage. Pointing at a line shows why the ingredient is there. When the product has strengths, the list follows the strength the shopper picks.",
    "product-pairs": "What to layer the product with and what to use at another time of day, from the product's Pairs well with and Keep apart metafields. Hidden when the product has neither.",
    "cart-formula": "The formula check under the cart: the actives in the bag, products that should be used at different times, and products that pair with the bag, each with an add button. Hidden when the cart is empty.",
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
    "heading": "A heading. Italic words show in the accent color.",
    "text": "A paragraph of text.",
    "button": "A link styled as a button.",
    "image": "An image, with an optional link.",
    "group": "Holds other blocks in a row or a column.",
    "custom-liquid": "Add app snippets or other Liquid code.",
    "collapsible-content": "A row that opens to show more text, such as ingredients or care details.",
    "element-pin": "An element tile pinned to the banner photo, with a dot and a line, such as Vitamin C on the cheek. Set its position as a percentage of the photo, with a separate position for phones.",
    "product-title": "The product title, with the product's element tile beside it.",
    "product-price": "The price, sale price and unit price.",
    "product-variant-picker": "Buttons or dropdowns for the product's options, with color swatches where set up. The strength option shows as large strengths beside a vial that fills to the one chosen.",
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
                                "media-with-text", "statistics", "testimonials", "faq", "newsletter", "section",
                                "custom-liquid"]),
    ("Formula sections", ["formula-table", "strength-story", "face-map", "feel-finder", "formula-compare"]),
    ("Product pages", ["product", "product-formula", "product-pairs", "product-recommendations"]),
    ("Collections and search", ["collection", "collections", "search"]),
    ("Cart", ["cart", "cart-formula"]),
    ("Blog and pages", ["blog", "article", "page", "contact-form"]),
    ("Other pages", ["404", "password"]),
]

BLOCK_ORDER = [
    ("Content blocks", ["heading", "text", "button", "image", "group", "collapsible-content", "element-pin",
                        "custom-liquid"]),
    ("Product page blocks", ["_product-media-gallery", "product-title", "product-price", "product-variant-picker",
                             "product-buy-buttons", "product-description", "pickup-availability",
                             "complementary-products"]),
    ("Blocks inside sections", ["_stat", "_testimonial", "_footer-menu"]),
]

# Used when a setting has no info text of its own, before the type hints below.
ID_HINTS = {
    "formula_collections": "The collections that are your elements, in the order they're numbered. See the Formula guide.",
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
    "inline_richtext": "Text shown to shoppers. Italic words show in the accent color.",
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
<p class="lede">Chalant is a Shopify theme for skincare brands that sell on what's in the bottle. Your actives become elements in a formula table, and every product shows its percentages and pH: on cards, on the product page, in the cart and in search.</p>

<div class="cards">
  <a class="card" href="formula.html"><strong>Formula</strong><span>Set up your elements, product formulas, strengths and pairings.</span></a>
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
  <li><strong>Fonts.</strong> Theme settings, Typography. Headings and body text use the heading and body fonts. The accent font is kept for single large words, such as the faint word behind Shop by feel. In any heading, make a word italic to show it in the accent color.</li>
  <li><strong>Menus.</strong> Online Store, Navigation. The header uses your main menu and supports three levels. Footer columns each use a menu you choose.</li>
  <li><strong>Home page.</strong> Replace the example text in each section with your own, and choose a collection for Featured collection.</li>
  <li><strong>Formula.</strong> Follow the <a href="formula.html">Formula guide</a> to set up your elements and product formulas. Most of Chalant reads from them.</li>
</ul>

<h2 id="animations">Animations</h2>
<p>Chalant moves with your content. The menu opens out of the header pill and its links rise in one after another, element pins draw onto the banner photo, large photos drift a little slower than the page, formula bars fill as they come into view, and sections fade and rise into place as they reach the screen, with headings coming up word by word. On larger screens the formula table holds in place while its tiles fly into position (turn off <strong>Assemble the table on scroll</strong> on the section to keep it still). With the banner's <strong>Centered statement</strong> layout, the headline rises in as the page loads and grows and fades as visitors scroll on. On hover, element tiles fill with their color, product cards turn their photo into a formula label (or print their formula line, for products without an active) and buttons fill from the left. Mouse wheel scrolling eases to a stop.</p>
<p>To turn animations off, open Theme settings, Layout and turn off <strong>Show animations</strong>. Turn off <strong>Smooth scrolling</strong> on its own to keep the other animations. Visitors who turn off motion on their device never see animations, whatever the settings.</p>

<h2 id="templates">Pages in Chalant</h2>
<p>Chalant includes layouts for every page Shopify needs, plus two extra page layouts:</p>
<ul>
  <li><strong>About:</strong> an image or video beside a short introduction, then your page content. Choose it for a page under Theme template, about.</li>
  <li><strong>Contact:</strong> a contact form that uses the page's title and content as its introduction. Choose Theme template, contact.</li>
</ul>

<h2 id="code">Editing the theme code</h2>
<p>Before you edit any theme code, duplicate the theme from Online Store, Themes, so you can go back if something breaks. Code changes aren't covered by support. For custom work, we recommend hiring a <a href="https://www.shopify.com/partners/directory">Shopify Partner</a>.</p>
"""

FORMULA = """
<h1>Formula</h1>
<p class="lede">Chalant is built around your formulas. Your actives are elements, shown as tiles in a formula table, and each product carries its ingredients with their percentages and pH. You set this up once, in your admin, and every page reads from it.</p>

<h2 id="elements">1. Choose your elements</h2>
<p>An element is a collection of the products built around one active, such as Vitamin C or Retinol.</p>
<ol>
  <li>In Products, Collections, create a collection for each active and add its products. A product can be in several.</li>
  <li>In the theme editor, open Theme settings, <strong>Formula table</strong>, and choose up to 12 collections as your <strong>Element collections</strong>. Their order sets their numbers, 01, 02 and so on.</li>
</ol>
<p>Each tile shows the first two letters of the collection's title as its symbol, and a color from Chalant's palette. To choose them yourself, add these collection metafields in Settings, Custom data, Collections:</p>
<div class="table"><table><thead><tr><th scope="col">Name and key</th><th scope="col">Type</th><th scope="col">Example</th></tr></thead><tbody>
<tr><th scope="row">Symbol, <code>chalant.symbol</code></th><td>Single line text</td><td>Vc</td></tr>
<tr><th scope="row">Strength range, <code>chalant.range</code></th><td>Single line text</td><td>10&ndash;20%</td></tr>
<tr><th scope="row">Tint, <code>chalant.tint</code></th><td>Color</td><td>#f6e3cf</td></tr>
</tbody></table></div>
<p>The collection's image and description are shown when its tile is opened in the formula table.</p>

<h2 id="formula">2. Add each product's formula</h2>
<p>In Settings, Custom data, Products, add these metafield definitions, then fill them in on each product:</p>
<div class="table"><table><thead><tr><th scope="col">Name and key</th><th scope="col">Type</th><th scope="col">What it holds</th></tr></thead><tbody>
<tr><th scope="row">Formula, <code>chalant.formula</code></th><td>JSON</td><td>The ingredients, as described below.</td></tr>
<tr><th scope="row">pH, <code>chalant.ph</code></th><td>Decimal</td><td>5.5</td></tr>
<tr><th scope="row">Strength advice, <code>chalant.strength_advice</code></th><td>JSON</td><td>Advice for each strength (step 3).</td></tr>
<tr><th scope="row">Pairs well with, <code>chalant.pairs_with</code></th><td>Product (list)</td><td>Products to layer it with (step 4).</td></tr>
<tr><th scope="row">Keep apart, <code>chalant.keep_apart</code></th><td>Product (list)</td><td>Products to use at another time (step 4).</td></tr>
</tbody></table></div>
<p>The formula is a list of ingredients. Each has a <code>name</code>, a <code>role</code> (<code>active</code>, <code>support</code> or <code>base</code>) and a <code>percent</code>. Optionally add <code>why</code>, a sentence on what it does, and <code>label</code>, shown instead of the percentage, such as SPF 50. The base, such as water, has no percentage.</p>
<pre><code>[
  {"name": "Water", "role": "base", "why": "Carries everything else."},
  {"name": "Ascorbic acid", "percent": 15, "role": "active",
   "why": "Vitamin C. Brightens and fades marks."},
  {"name": "Vitamin E", "percent": 1, "role": "support",
   "why": "Keeps the vitamin C stable."}
]</code></pre>
<p>Product cards show the lead active, the first support ingredient and the pH. To hide this line, turn off <strong>Show the formula on product cards</strong> in Theme settings, Formula table.</p>

<h2 id="strengths">3. Sell strengths</h2>
<p>For a product that comes in strengths, such as a retinol at 0.1%, 0.3% and 1%, name the option <strong>Strength</strong> and give each value a percentage. If you use another name, set it in Theme settings, Formula table, <strong>Strength option name</strong>.</p>
<p>The strength option shows as large strengths beside a vial that fills to the one chosen, the full formula follows the chosen strength, and the Strength story section steps through them. Its advice comes from the strength advice metafield, a list of label and text pairs for each strength:</p>
<pre><code>{
  "0.1%": [["For", "First time on retinol"], ["Use", "2 nights a week"]],
  "0.3%": [["For", "After 6 weeks at 0.1%"], ["Use", "Every other night"]]
}</code></pre>

<h2 id="pairs">4. Pairs well with and keep apart</h2>
<p>Choose the products a product layers well with, and the ones to use at another time of day, such as vitamin C in the morning and retinol at night. The product page shows both in the Pairs well with section, and the cart's formula check warns when two products to keep apart are in the bag and suggests products that pair with it.</p>

<h2 id="where">Where your formulas show</h2>
<ul>
  <li><strong>Header:</strong> the element symbols in the pill, and the formula table in the menu panel.</li>
  <li><strong>Home page:</strong> the Formula table, Strength story, Face map, Shop by feel and Compare formulas sections, and element pins on the banner.</li>
  <li><strong>Product cards:</strong> the element tile and the formula line.</li>
  <li><strong>Product page:</strong> the element beside the title, the strength picker, the formula label on the photo, the full formula and Pairs well with.</li>
  <li><strong>Collection pages:</strong> the formula table as the header, with a ledger view that lists each product's formula in a table.</li>
  <li><strong>Cart:</strong> each line's element and formula, and the formula check.</li>
  <li><strong>Search:</strong> searching an element's name or symbol shows its tile and its products on a strength scale; searching a strength or pH, such as 10% or pH 3, lists the products that match.</li>
  <li><strong>Footer:</strong> the formula index, a row of your element tiles.</li>
</ul>
<p>A product without a formula still shows everywhere, without the formula line. In the theme editor, sections without data show example tiles so you can see the layout while you set things up.</p>
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
    ("Why doesn't a section show on my store?", "Statistics, Testimonials and FAQ sections with no blocks, Pairs well with on a product with no pairings, the cart's formula check on an empty cart, and a Featured collection whose collection is empty are hidden from shoppers. They still show in the theme editor so you can finish setting them up."),
    ("Why doesn't a product show its formula?", "Check that the product has the Formula metafield (chalant.formula) filled in with at least one ingredient whose role is active. See the Formula guide."),
    ("Why doesn't a product show its element tile?", "The product needs to be in one of the collections chosen as Element collections in Theme settings, Formula table."),
    ("How do I change an element's symbol or color?", "Add the Symbol and Tint metafields to the collection. Without them, the symbol is the first two letters of the title and the color comes from Chalant's palette."),
    ("How do I show subscriptions?", "Install a subscription app and add a subscription plan to the product. Purchase options appear on the product page automatically."),
    ("How do I set up filters?", "Install Shopify's Search and Discovery app and choose your filters there. Turn filtering on in the Collection and Search results sections."),
    ("Can I use a different layout for one page?", "Yes. In the theme editor, create a template from the page menu at the top, set it up, then choose it for the page in your admin under Theme template."),
    ("How do I translate the theme?", "Go to Online Store, Themes, then the menu next to Customize, Edit default theme content. Add languages in Settings, Languages, and use the Translate and Adapt app for content."),
    ("Does Chalant work with apps?", "Yes. Product pages, featured products and most sections accept app blocks. Choose Add block, Apps in the theme editor. Apps that need code changes may need help from the app developer."),
    ("How do I turn off animations?", "In Theme settings, Layout, turn off Show animations, or only Smooth scrolling. Visitors who reduce motion on their device never see animations."),
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
    ("formula.html", "Formula", FORMULA),
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
