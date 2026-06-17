#!/usr/bin/env python3
"""
Questionnaire Generator for Academic Research
Generates structured questionnaires from template specifications
"""

import argparse
import json
from pathlib import Path

def load_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(template, output_path):
    """Generate markdown questionnaire from template"""
    
    sections = template.get('sections', [])
    
    output = []
    output.append("# " + template.get('title', 'Survey Questionnaire'))
    output.append("")
    output.append(template.get('cover', ''))
    output.append("")
    
    for section in sections:
        output.append(f"## {section['id']}. {section['title']}")
        output.append("")
        
        if 'intro' in section:
            output.append(section['intro'])
            output.append("")
        
        for q in section.get('questions', []):
            q_id = q.get('id', '')
            q_text = q.get('text', '')
            q_type = q.get('type', 'single')
            options = q.get('options', [])
            table = q.get('table', None)
            
            output.append(f"**{q_id}**. {q_text}")
            output.append("")
            
            if q_type == 'single':
                for opt in options:
                    output.append(f"- [ ] {opt}")
                    
            elif q_type == 'multiple':
                output.append("（可多选）")
                for opt in options:
                    output.append(f"- [ ] {opt}")
                    
            elif q_type == 'fill':
                unit = q.get('unit', '')
                output.append(f"______ {unit}")
                
            elif q_type == 'likert5':
                for i, opt in enumerate(['非常不同意', '比较不同意', '一般', '比较同意', '非常同意'], 1):
                    output.append(f"- [ ] {i}={opt}")
                    
            elif q_type == 'likert7':
                labels = ['非常不同意', '比较不同意', '有点不同意', '一般', '有点同意', '比较同意', '非常同意']
                for i, opt in enumerate(labels, 1):
                    output.append(f"- [ ] {i}={opt}")
            
            elif q_type == 'table':
                if table:
                    headers = table.get('headers', [])
                    output.append("| " + " | ".join(headers) + " |")
                    output.append("| " + " | ".join(['---'] * len(headers)) + " |")
                    for row in table.get('rows', []):
                        output.append("| " + " | ".join(row) + " |")
                        
            elif q_type == 'panel3':
                headers = ['项目', '2023年', '2024年', '2025年', 'Stata变量']
                output.append("| " + " | ".join(headers) + " |")
                output.append("| " + " | ".join(['---'] * len(headers)) + " |")
                for row in table.get('rows', []):
                    output.append("| " + " | ".join(row) + " |")
            
            output.append("")
    
    output.append("---")
    output.append("*感谢您的配合！*")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"Questionnaire generated: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate questionnaire from template')
    parser.add_argument('--template', '-t', required=True, help='Path to template JSON file')
    parser.add_argument('--output', '-o', required=True, help='Output markdown file')
    
    args = parser.parse_args()
    
    template = load_template(args.template)
    generate_markdown(template, args.output)

if __name__ == '__main__':
    main()
