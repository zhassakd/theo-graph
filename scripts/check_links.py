#!/usr/bin/env python3
"""Check that all [[wiki links]] in Markdown files point to existing files."""
import os, re, sys

errors = []
md_files = {}

for root, dirs, files in os.walk('.'):
    if '.git' in root or '_data' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            rel = os.path.join(root, f).replace(os.sep, '/').lstrip('./')
            md_files[os.path.splitext(f)[0]] = rel

for name, full in list(md_files.items()):
    try:
        with open(full, 'r', encoding='utf-8') as fh:
            content = fh.read()
    except Exception:
        continue
    # Remove code blocks (```...``` spanning multiple lines)
    content_no_code = re.sub(r'```[\s\S]*?```', '', content)
    # Remove inline code (`...`)
    content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
    for m in re.finditer(r'\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]', content_no_code):
        target = m.group(1).split('/')[-1]
        if target not in md_files:
            errors.append((full, m.group(1)))

if errors:
    with open('link_errors.log', 'w', encoding='utf-8') as f:
        for full, target in errors:
            f.write('  {}  ->  [[{}]]  (target not found)\n'.format(full, target))
        f.write('\n{} broken internal links found.\n'.format(len(errors)))
    print('{} broken links found. See link_errors.log for details.'.format(len(errors)))
    sys.exit(1)
else:
    print('All internal [[wiki]] links are valid!')
