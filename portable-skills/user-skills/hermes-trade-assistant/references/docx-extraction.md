# .docx 文件提取 — 绕过 python-docx NULL 错误

## 问题

python-docx 库在读取某些 .docx 文件时会抛出 NULL 错误，但实际上文件完好。

## 根因

python-docx 对部分 XML 命名空间或格式处理有缺陷。文件 ZIP 结构 + document.xml 完全正常。

## 解决方案：直接读 ZIP 内的 XML

```python
import zipfile
import xml.etree.ElementTree as ET

def extract_docx_text(filepath):
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(filepath, 'r') as z:
        xml = z.read('word/document.xml')
    root = ET.fromstring(xml)
    paragraphs = []
    for p in root.findall('.//w:p', ns):
        texts = [t.text or '' for t in p.findall('.//w:t', ns)]
        line = ''.join(texts).strip()
        if line:
            paragraphs.append(line)
    return '\n\n'.join(paragraphs)
```

## 验证

2026-06-06 实测：外贸知识库中 14 个"NULL 错误"的 .docx 文件用此法全部成功提取（原来全部是 python-docx 库的 bug，不是文件损坏）。
