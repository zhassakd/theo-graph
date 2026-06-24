"""Convert summa.json ALL.json to individual Markdown files for RAG."""
import json, os

src = r'C:\Users\zhang\OneDrive\Desktop\theo-graph\_data\summa.json\json\ALL.json'
dst = r'C:\Users\zhang\OneDrive\Desktop\theo-graph\_data\rag-ready\summa'

os.makedirs(dst, exist_ok=True)

with open(src, 'r', encoding='utf-8') as f:
    data = json.load(f)

parts_map = {
    'FP': '第一部',
    'FS': '第一部第二卷',
    'SS': '第二部第二卷',
    'TP': '第三部',
    'SP': '补编',
}

count = 0
for part_key, part_data in data.items():
    if not isinstance(part_data, dict):
        continue
    part_name = parts_map.get(part_key, part_key)
    questions = part_data.get('questions', {})
    if not isinstance(questions, dict):
        continue

    for q_num, q_data in questions.items():
        if not isinstance(q_data, dict):
            continue
        q_title = q_data.get('title', '')
        articles = q_data.get('article', {})
        if not isinstance(articles, dict):
            continue

        for a_num, a_data in articles.items():
            if not isinstance(a_data, dict):
                continue
            a_title = a_data.get('title', '')
            if isinstance(a_title, list):
                a_title = a_title[0] if a_title else ''
            body = a_data.get('body', '')
            if isinstance(body, list):
                body = '\n\n'.join(body)
            objections = a_data.get('objections', {})
            replies = a_data.get('replies', {})

            if not body.strip():
                continue

            md_lines = []
            md_lines.append(f'# 神学大全 · {part_name} · 第{q_num}题 · 第{a_num}条')
            md_lines.append('')
            md_lines.append(f'**{a_title}**')
            md_lines.append('')
            md_lines.append(body)
            md_lines.append('')

            # Handle objections (dict or list)
            if isinstance(objections, dict) and objections:
                md_lines.append('## 异议')
                md_lines.append('')
                for i, (o_num, o_data) in enumerate(objections.items(), 1):
                    o_text = ''
                    if isinstance(o_data, str):
                        o_text = o_data
                    elif isinstance(o_data, dict):
                        o_text = o_data.get('text', '')
                        if isinstance(o_text, list):
                            o_text = ' '.join(o_text)
                    elif isinstance(o_data, list):
                        o_text = ' '.join(str(x) for x in o_data)
                    if o_text.strip():
                        md_lines.append(f'**异议{i}：** {o_text}')
                        md_lines.append('')

            if isinstance(replies, dict) and replies:
                md_lines.append('## 答复')
                md_lines.append('')
                for i, (r_num, r_data) in enumerate(replies.items(), 1):
                    r_text = ''
                    if isinstance(r_data, str):
                        r_text = r_data
                    elif isinstance(r_data, dict):
                        r_text = r_data.get('text', '')
                        if isinstance(r_text, list):
                            r_text = ' '.join(r_text)
                    elif isinstance(r_data, list):
                        r_text = ' '.join(str(x) for x in r_data)
                    if r_text.strip():
                        md_lines.append(f'**答复{i}：** {r_text}')
                        md_lines.append('')

            fname = f'{part_key}_Q{q_num}_A{a_num}.md'
            fname = fname.replace('/', '_').replace('\\', '_').replace(' ', '_')
            filepath = os.path.join(dst, fname)
            with open(filepath, 'w', encoding='utf-8') as fout:
                fout.write('\n'.join(md_lines))
            count += 1

# Write index
with open(os.path.join(dst, '_index.md'), 'w', encoding='utf-8') as f:
    f.write('# 神学大全（Summa Theologiae）\n\n')
    f.write('托马斯·阿奎那 著\n\n')
    f.write(f'共 {count} 条论题，已拆分为独立 Markdown 文件，适用于 RAG 检索和知识库导入。\n')

print(f'Done: {count} articles written to {dst}')
