from PyPDF2 import PdfReader
import re

def extract_experiment_four(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    
    # 查找实验四相关内容
    exp4_pattern = r'实验四[\s\S]*?(?=实验五|附录|参考文献|$)'
    match = re.search(exp4_pattern, text)
    
    if match:
        exp4_content = match.group(0)
        print("===实验四内容===")
        print(exp4_content)
        return exp4_content
    else:
        print("未找到实验四内容")
        return None

if __name__ == "__main__":
    pdf_path = "写作/手机备忘录/智慧银行实验讲义_v3.0.pdf"
    extract_experiment_four(pdf_path)