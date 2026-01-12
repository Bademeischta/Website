import os
import shutil

# Configuration for the 7 websites
websites = [
    {
        "folder": "neumann",
        "company_name": "Dachdecker Neumann",
        "address": "De-Neufville-Str. 27, 60596 Frankfurt am Main",
        "hero_title": "Dachdecker Neumann - Ihr Traditionsbetrieb in Frankfurt"
    },
    {
        "folder": "voelker",
        "company_name": "Heinrich Völker GmbH",
        "address": "Oberschelder Weg 20, 60439 Frankfurt am Main",
        "hero_title": "Völkerdach - Qualität seit Generationen"
    },
    {
        "folder": "hohl",
        "company_name": "Franz Hohl GmbH",
        "address": "Friesstraße 17, 60388 Frankfurt am Main",
        "hero_title": "Franz Hohl GmbH - Ihr Dach-Experte"
    },
    {
        "folder": "lerch",
        "company_name": "Lerch, Mull & Co GmbH",
        "address": "Alt Harheim 35, 60437 Frankfurt am Main",
        "hero_title": "Lerch, Mull & Co - Meisterhafte Bedachungen"
    },
    {
        "folder": "nagel",
        "company_name": "Nagel Bedachung",
        "address": "Buchwaldstraße 38, 60385 Frankfurt am Main",
        "hero_title": "Nagel Bedachung - Sicher unter einem guten Dach"
    },
    {
        "folder": "limbacher",
        "company_name": "Limbacher Dach",
        "address": "Bornheimer Landstr. 29, 60316 Frankfurt am Main",
        "hero_title": "Limbacher Dach - Ihr Partner in Bornheim"
    },
    {
        "folder": "guenes",
        "company_name": "Günes Dachdecker",
        "address": "Münzenbergerstr. 2, 60389 Frankfurt am Main",
        "hero_title": "Günes Dachdecker - Schnell & Zuverlässig"
    }
]

SOURCE_FILE = "index.html"
OUTPUT_DIR = "kunden_websites"

def generate():
    # Read the template
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for site in websites:
        print(f"Generating site for {site['company_name']} in /{site['folder']}...")

        # Create site specific directory
        site_dir = os.path.join(OUTPUT_DIR, site['folder'])
        if not os.path.exists(site_dir):
            os.makedirs(site_dir)

        content = template_content

        # 1. Address Replacement (Before global Musterstadt replacement to be safe)
        # The template has "Dachstraße 1, 12345 Musterstadt"
        content = content.replace("Dachstraße 1, 12345 Musterstadt", site['address'])

        # 2. Global "Musterstadt" -> "Frankfurt am Main"
        content = content.replace("Musterstadt", "Frankfurt am Main")

        # 3. Form Action and Hidden Fields
        # Replace action
        # Old: <form action="https://formsubmit.co/silasboch15@gmail.com" method="POST" class="space-y-6">
        # Or generic: <form action="#" ...> -> We need to find the form tag.
        # In the provided index.html: <form action="https://formsubmit.co/silasboch15@gmail.com" method="POST" class="space-y-6">
        # I'll just replace the whole opening tag and add the hidden fields immediately after.

        form_search = '<form action="https://formsubmit.co/silasboch15@gmail.com" method="POST" class="space-y-6">'
        form_replace = f'''<form action="https://formsubmit.co/silasboch15@gmail.com" method="POST" class="space-y-6">
                        <input type="hidden" name="_subject" value="Anfrage Demo-Seite: {site['company_name']}">
                        <input type="hidden" name="_captcha" value="false">'''

        content = content.replace(form_search, form_replace)

        # 4. Hero Title Replacement
        # The template has:
        # <h1 class="text-3xl md:text-6xl font-bold text-white leading-tight mb-6 shadow-sm">
        #     Ihr zuverlässiger <span class="text-brand-orange">Dachdecker</span> in Musterstadt
        # </h1>
        # Note: "Musterstadt" is already replaced by "Frankfurt am Main" in step 2.
        # So we search for "Ihr zuverlässiger <span class="text-brand-orange">Dachdecker</span> in Frankfurt am Main"
        # Or better, we identify the H1 block and replace the content.

        # Since I'm using string replacement, exact match is tricky with whitespace.
        # Let's try to match the surrounding tags.

        # Original (after step 2):
        # <h1 class="text-3xl md:text-6xl font-bold text-white leading-tight mb-6 shadow-sm">
        #     Ihr zuverlässiger <span class="text-brand-orange">Dachdecker</span> in Frankfurt am Main
        # </h1>

        # I will construct the regex or just replace the inner part if I can match it exactly.
        # The source file has newlines.

        # Let's use a simpler approach. I know the structure.
        # I'll replace the whole H1 block with the new H1 block.
        # I need to know what the template looks like *exactly* after step 2.
        # Step 2 replaced "Musterstadt" with "Frankfurt am Main".

        # Search block (Original content in variable, but "Musterstadt" is "Frankfurt am Main")
        h1_search = '''<h1 class="text-3xl md:text-6xl font-bold text-white leading-tight mb-6 shadow-sm">
                    Ihr zuverlässiger <span class="text-brand-orange">Dachdecker</span> in Frankfurt am Main
                </h1>'''

        h1_replace = f'''<h1 class="text-3xl md:text-6xl font-bold text-white leading-tight mb-6 shadow-sm">
                    {site['hero_title']}
                </h1>'''

        if h1_search in content:
            content = content.replace(h1_search, h1_replace)
        else:
             # Fallback if whitespace is different, try to find unique substrings
             # "Ihr zuverlässiger <span class="text-brand-orange">Dachdecker</span>"
             # This part shouldn't have changed except maybe context.
             pass

        # Also update <title> tag
        # <title>Dachdecker Frankfurt am Main - Ihr zuverlässiger Partner</title> (After step 2)
        title_search = "<title>Dachdecker Frankfurt am Main - Ihr zuverlässiger Partner</title>"
        title_replace = f"<title>{site['hero_title']}</title>"
        content = content.replace(title_search, title_replace)

        # Write file
        output_path = os.path.join(site_dir, "index.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Created {output_path}")

if __name__ == "__main__":
    generate()
