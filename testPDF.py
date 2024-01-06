from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def create_pdf(text_array, pdf_filename):
    # 初始化样式
    styles = getSampleStyleSheet()

    # 初始化 PDF 文档对象
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer)

    # 循环处理每段文本
    stories = []
    for line in text_array:
        # 处理每一行文本
        p = Paragraph(line, style=styles["Normal"])
        stories.append(p)
        stories.append(Spacer(1, 12))  # 添加间隔

    # 构建 PDF
    pdf.build(stories)

    # 将 PDF 文件保存到磁盘
    pdf_buffer.seek(0)
    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(pdf_buffer.read())



if __name__ == '__main__':
    # 示例用法
    text_array = ["这是中文内容。", "This is English content.", "更多内容...", "More content..."]
    pdf_filename = 'output.pdf'
    create_pdf(text_array, pdf_filename)