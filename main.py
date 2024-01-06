# -*- coding: utf-8 -*-
import zipfile

from flask import Flask, request, render_template, send_file
# 导入翻译模块
from googletrans import Translator
# 导入PDF模块
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from datetime import datetime
import requests
import medium
import getTop10
# 创建Flask应用对象
app = Flask(__name__)




# 封装请求详情URL的函数
def requstdetail(url):
    payload = {}
    headers = {
        'authority': 'medium.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'apollographql-client-name': 'lite',
        'apollographql-client-version': 'main-20240105-172446-fe9cfbd9ba',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'g_state={"i_p":1704455237812,"i_l":1}; nonce=P3c1t73h; _gid=GA1.2.2112381953.1704448772; lightstep_guid/medium-web=f3b9693f8bde2f27; lightstep_session_id=f84398ff9f5599d8; sz=1857; pr=1; tz=-480; _ga=GA1.1.1497685297.1704448036; uid=lo_c6ef3fe43d07; sid=1:Qt7/wieRK466cilqWXaj/B7rIM0e4oHNdRtwsmyub6m/qHmh+VwP0Rq/2y8wTHAc; _dd_s=rum=0&expire=1704517310272; _ga_7JY7T788PK=GS1.1.1704512059.10.1.1704516410.0.0.0',
        'graphql-operation': 'PostPageQuery',
        'medium-frontend-app': 'lite/main-20240105-172446-fe9cfbd9ba',
        'medium-frontend-path': '/wise-well/the-four-stages-of-sleep-and-what-they-actually-do-d7c03ae2eb11',
        'medium-frontend-route': 'post',
        'origin': 'https://medium.com',
        'ot-tracer-sampled': 'true',
        'ot-tracer-spanid': '422769e0366a3c2c',
        'ot-tracer-traceid': '2976f285490f01a6',
        'pragma': 'no-cache',
        'referer': 'https://medium.com/wise-well/the-four-stages-of-sleep-and-what-they-actually-do-d7c03ae2eb11',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    return response.text



# 定义翻译函数
def translate(text, dest='zh-cn'):
    # 创建翻译器对象
    translator = Translator()
    # 调用翻译方法
    result = translator.translate(text, dest=dest, src='en')
    # print(result.text)
    return result.text

def generate_pdf(content, filename):
    # 使用reportlab生成PDF文件
    content.split('\n')
    create_pdf(content, filename)

# 定义创建PDF文件函数
def create_pdf(text, filename):
    # 注册字体
    pdfmetrics.registerFont(TTFont('SourceHanSansSC-VF', 'SourceHanSansSC-VF.ttf'))
    pdf = SimpleDocTemplate(filename, pagesize=letter)

    stories = []
    styles = getSampleStyleSheet()

    for line in text:
        p = Paragraph(line, style=styles["Normal"])
        stories.append(p)
        stories.append(Spacer(1, 20))
        # print('输出PDF时候的内容：'+line)
        # 写入 TXT
        with open(filename+'.txt', 'a', encoding='utf-8') as f:
            f.write(line + '\n')

    pdf.build(stories)

def create_by_url(url):
    d = medium.Demo()
    innercontent = d.get_detail_url(url)[0]
    # 遍历innercontent数组，每个元素都调用翻译函数，并将翻译后的结果和翻译前的结果合并追加到一个text,并且每个元素后面都加上一个换行符
    text = []
    for i in range(len(innercontent)):
        text.append(innercontent[i])
        text.append(translate(innercontent[i]))
    return text



# 定义路由和视图函数
@app.route('/', methods=['GET', 'POST'])
def index():
    # 定义一个数组存放文件名称
    filenames = []
    # 如果是GET请求，渲染模板
    if request.method == 'GET':
        return render_template('index.html')
    # 如果是POST请求，获取表单数据
    elif request.method == 'POST':
        # 获取英文输入框的内容
        english = request.form.get('english')
        # 获取按钮的值
        button = request.form.get('button')
        fanyi2 = request.form.get('test-url')
        # 如果点击的是翻译按钮
        if button == 'Translate':
            # 调用翻译函数
            chinese = translate(english)
            # 渲染模板，传递参数
            return render_template('index.html', english=english, chinese=chinese)
        # 如果点击的是创建PDF文件按钮
        elif button == 'Create pdf files':
            top10 = getTop10.get_top10_all()[0]
            losercount = getTop10.get_top10_all()[1]

            # 遍历top10数组
            for i in range(len(top10)):
                # 获取top10数组中的元素
                article = top10[i]
                # 获取文章的url
                url = article[0]
                print(url)
                # 调用medium模块的get_detail_url函数，获取文章的内容
                d = medium.Demo()
                like_count = d.get_detail_url(url)[1]
                if like_count == -1:
                    continue
                innercontent = d.get_detail_url(url)[0]
                # innercontent = requstdetail(url)
                # 定义一个数组装载每次循环取得的数据
                text = []
                # 遍历innercontent数组，每个元素都调用翻译函数，并将翻译后的结果和翻译前的结果合并追加到一个text,并且每个元素后面都加上一个换行符
                for i in range(len(innercontent)):
                    try:
                        text.append(innercontent[i])
                        text.append(translate(innercontent[i]))
                    except Exception as e:
                        print(f"An error occurred while translating text: {e}")

                # 调用创建PDF文件函数
                # 文件名用时间戳
                # 获取当前时间
                now = datetime.now()
                # 将当前时间转换为字符串，格式为年月日时分秒
                timestamp_str = now.strftime("%Y%m%d%H%M%S")
                # 使用时间戳作为文件名
                filename = "file_" + timestamp_str + ".pdf"
                filenames.append(filename)
                create_pdf(text, filename)

            # 渲染模板，传递参数
            return render_template('index.html', english=english, message='访问接口失败笔数:'+str(losercount))
        # 如果点击的是下载按钮
        elif button == 'Download':
            # 读取同级目录下的fileNames[]文件,把这些文件全部压缩到一个zip文件中
            # 遍历当前目录下的所有文件，后缀是TXT和PDF的文件都添加到zip文件中
            import os
            filenames_txt = []
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.startswith("file") and (file.endswith(".txt") or file.endswith(".pdf")):
                        filenames_txt.append(file)

            # 生成zip文件
            # 创建一个新的ZIP文件，用时间戳做名字
            now = datetime.now()
            # 将当前时间转换为字符串，格式为年月日时分秒
            timestamp_str = now.strftime("%Y%m%d%H%M%S")
            # 使用时间戳作为文件名
            zipname = "file_" + timestamp_str + ".zip"
            with zipfile.ZipFile(zipname, "w") as zipf:
                # 遍历文件名数组
                for fileName in filenames_txt:
                    # 将文件添加到ZIP文件中
                    zipf.write(fileName)
            # 发送文件
            return send_file(zipname, as_attachment=True)
        # 如果点击的是翻译2
        elif button == 'Translate2':
            # 判断参数是否为空
            if fanyi2 == '':
                return render_template('index.html', message='请输入文章链接')
            urltext = create_by_url(fanyi2)
            # 把urltext写入pdf，
            # 文件名用时间戳
            # 获取当前时间
            now = datetime.now()
            # 将当前时间转换为字符串，格式为年月日时分秒
            timestamp_str = now.strftime("%Y%m%d%H%M%S")
            # 使用时间戳作为文件名
            filename = "file_" + timestamp_str + ".pdf"
            create_pdf(urltext, filename)
            # 发送文件
            send_file(filename, as_attachment=True)
            # 渲染模板，传递参数
            return render_template('index.html', articlechinese=urltext, message='翻译保存下载成功')

# 运行Flask应用
if __name__ == '__main__':
    app.run(debug=True, port=8080)

