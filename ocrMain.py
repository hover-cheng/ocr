from bottle import Bottle, route, run, request, static_file, HTTPResponse
import ocrApi
import os
import time

app = Bottle()
baseDir = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    filePath = os.path.join(baseDir, 'templates')
    return static_file('ocr.html', root=filePath)

@app.route("/upload",  method="POST")
def saveFile():
    nowData = time.strftime("%Y%m%d", time.localtime())
    upload = request.files.get('image')
    imgname = request.forms.get('name')
    lang = request.forms.get('lang')
    checked = request.forms.get('checked')
    print("checked", checked)
    _, ext = os.path.splitext(imgname)
    if ext not in ('.png', '.jpg', '.jpeg'):
        request.body.close()
        return HTTPResponse(status=403)

    savePath = os.path.join(baseDir, 'uploads', nowData)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    filePath = os.path.join(savePath, imgname)
    upload.save(filePath, overwrite=True)
    request.body.close()
    ocrObj = ocrApi.ocrApi(filePath, lang, checked)
    result = ocrObj.getTrain()
    return {'result': result}

# 设置css文件访问方法
@app.route('/static/css/<cssFile>')
def serverCss(cssFile):
    filePath = os.path.join(baseDir, 'static/css')
    return static_file(cssFile, root=filePath)


# 设置js文件访问方法
@app.route('/static/js/<jsFile>')
def serverJs(jsFile):
    filePath = os.path.join(baseDir, 'static/js')
    return static_file(jsFile, root=filePath)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
else:
    application = app