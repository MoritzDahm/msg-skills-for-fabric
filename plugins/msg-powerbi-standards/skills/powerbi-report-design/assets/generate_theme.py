# running it as python generate_theme.py NAME_OF_PALETTE

import json, sys, re

PALETTE_NAME = sys.argv[1] if len(sys.argv) > 1 else "msg"

with open("palettes.json") as f:
    palettes = json.load(f)
palette = palettes[PALETTE_NAME]
palette.setdefault("name", f"{PALETTE_NAME} Theme")
palette["dataColors"] = json.dumps(palette["dataColors"])  # for raw array substitution

with open("base.template.json") as f:
    template = f.read()

for key, value in palette.items():
    if isinstance(value, (bool, list)):
        replacement = json.dumps(value)
    else:
        replacement = str(value)
    template = template.replace("{{" + key + "}}", replacement)

unresolved = re.findall(r"\{\{[a-zA-Z0-9_]+\}\}", template)
if unresolved:
    raise ValueError(f"Unresolved placeholders — missing from palette '{PALETTE_NAME}': {sorted(set(unresolved))}")
else:
    theme = json.loads(template)  # validates it's still well-formed JSON
    with open("base.json", "w") as f:
        json.dump(theme, f, indent=2)

    print(f"Generated base.json from palette: {PALETTE_NAME}")