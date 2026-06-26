import zipfile, xml.etree.ElementTree as ET, os

for fname in [
    r'C:\Users\zhang\OneDrive\文档\xwechat_files\wxid_18sxz44d9n5a22_ce2a\msg\file\2026-06\文档.docx',
    r'C:\Users\zhang\OneDrive\文档\xwechat_files\wxid_18sxz44d9n5a22_ce2a\msg\file\2026-06\文档 (1).docx'
]:
    outname = os.path.basename(fname).replace('.docx', '.txt')
    z = zipfile.ZipFile(fname)
    xml_content = z.read('word/document.xml')
    root = ET.fromstring(xml_content)
    paragraphs = []
    for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        texts = []
        for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
            if t.text:
                texts.append(t.text)
        if texts:
            paragraphs.append(''.join(texts))
    with open(os.path.join(r'C:\Users\zhang\OneDrive\Desktop\theo-graph', outname), 'w', encoding='utf-8') as f:
        f.write('\n'.join(paragraphs))
    print('Written:', outname, '-', len(paragraphs), 'paragraphs')
