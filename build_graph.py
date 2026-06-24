#!/usr/bin/env python3
"""Build concept network graph from [[wiki link]] cross-references."""

import os
import re
from collections import defaultdict

edges = set()
node_files = {}  # name -> path

for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f).replace(os.sep, '/').lstrip('./')
            name = os.path.splitext(f)[0]
            node_files[name] = path

# Collect edges from [[概念/xxx]] links
for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            src_name = os.path.splitext(f)[0]
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
            except:
                continue
            # Match [[概念/xxx]] and [[概念/xxx|alias]]
            for m in re.finditer(r'\[\[概念/([^\]|#]+)(?:\|[^\]]+)?\]\]', content):
                target = m.group(1)
                edges.add((src_name, target))

# Also collect edges from [[system links]]
for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            src_name = os.path.splitext(f)[0]
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
            except:
                continue
            for m in re.finditer(r'\[\[(system/[^\]|#]+)(?:\|[^\]]+)?\]\]', content):
                target = m.group(1).split('/')[-1]
                edges.add((src_name, target))

# Generate Mermaid graph (focus on concepts -> concepts edges)
concept_edges = set()
concept_nodes = set()
for a, b in edges:
    # Check if both are concept files (exist in concepts/ dir)
    a_is_concept = os.path.exists(os.path.join('concepts', a + '.md'))
    b_is_concept = os.path.exists(os.path.join('concepts', b + '.md'))
    if a_is_concept and b_is_concept:
        concept_edges.add((a, b))
        concept_nodes.add(a)
        concept_nodes.add(b)

print(f"Concept-only graph: {len(concept_nodes)} nodes, {len(concept_edges)} edges")
print(f"Full graph: {len(set())}")

# Write Mermaid file
with open('concept_graph.mmd', 'w', encoding='utf-8') as out:
    out.write('graph LR\n')
    out.write('    %% TheoGraph Concept Network\n')
    out.write('    %% Auto-generated from [[wiki link]] cross-references\n\n')
    # Style
    for node in sorted(concept_nodes):
        safe = node.replace(' ', '_').replace('·','').replace('·','').replace(':','')
        out.write(f'    {safe}["`**{node}**`"]\n')
    out.write('\n')
    for a, b in sorted(concept_edges):
        sa = a.replace(' ', '_').replace('·','').replace('·','').replace(':','')
        sb = b.replace(' ', '_').replace('·','').replace('·','').replace(':','')
        out.write(f'    {sa} --> {sb}\n')

print("Written concept_graph.mmd")

# Print stats
print(f"\n=== Top concepts by inbound links ===")
inbound = defaultdict(int)
for a, b in concept_edges:
    inbound[b] += 1
for name, count in sorted(inbound.items(), key=lambda x: -x[1])[:10]:
    print(f"  {count} ← {name}")

print(f"\n=== Top concepts by outbound links ===")
outbound = defaultdict(int)
for a, b in concept_edges:
    outbound[a] += 1
for name, count in sorted(outbound.items(), key=lambda x: -x[1])[:10]:
    print(f"  {name} → {count}")
