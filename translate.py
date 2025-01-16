import requests
import re
import html
import unicodedata


def clean_text(text):
    # 移除特殊字符，但保留基本标点符号
    cleaned = re.sub(r'[^\w\s,.!?，。！？、]', '', text)
    return cleaned

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")

# bing翻译
class BingTranslator(object):
    def __init__(self):
        self.url = 'https://cn.bing.com/translator'
        self.gi = requests.get(self.url).text
        self.ig = re.search(r'IG:"(.*?)"', self.gi).group(1)
        self.iid = re.search(r'data-iid=\"(.*?)\"', self.gi).group(1)
        self.token = re.search(r'params_AbusePreventionHelper = (.*?);', self.gi).group(1)
        self.tokens = self.token.replace("[", "")
        self.js = self.tokens.split(',')
        self.t = self.js[1][1:33]
    
    # 调用bing的翻译功能
    def translate(self, word, lang="en", num=3):
        word = word[:1000]
        # 清理文本中的特殊字符
        word = clean_text(word)
        url = 'https://cn.bing.com/ttranslatev3?isVertical=1&&IG={}&IID={}'.format(self.ig, self.iid)
        data = {
            'text': word,
            'token': self.t,
            'key': self.js[0],
            'tryFetchingGenderDebiasedTranslations': 'true'
        }
        if lang.strip() == 'en':
            data['fromLang'] = 'en'
            data['to'] = 'zh-Hans'
        elif lang.strip() == 'ch':
            data['fromLang'] = 'zh-Hans'
            data['to'] = 'en'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        for i in range(num):
            response = requests.post(url, data=data, headers=headers)
            # raise_for_status() 方法会检查响应的状态码，如果状态码不是 200，则会引发一个 HTTPError 异常
            response.raise_for_status()
            try:
                translations = response.json()[0]['translations']
                translated_text = "译文: " + translations[0]['text']
                break
            except Exception as e:
                print("error: 请求数据：" + word + " 返回内容：" + response.text)
                if lang.strip() == 'en':
                    translated_text = 'translation failure'
                elif lang.strip() == 'ch':
                    translated_text = '翻译失败'
        return translated_text
    


# 谷歌翻译
class GoogleTranslator():
    def __init__(self):
        super().__init__()
        self.endpoint = "http://translate.google.com/m"
        self.headers = {
            "User-Agent": "Mozilla/4.0 (compatible;MSIE 6.0;Windows NT 5.1;SV1;.NET CLR 1.1.4322;.NET CLR 2.0.50727;.NET CLR 3.0.04506.30)"  # noqa: E501
        }

    def translate(self, word, lang="en", num=3):
        if lang.strip() == 'en':
            lang_out = "zh-CN"
            lang_in = "en"
        elif lang.strip() == 'ch':
            lang_out = "en"
            lang_in = "zh-CN"
        word = word[:5000]  # google translate max length
        word = clean_text(word)
        for i in range(num):
            response = requests.get(self.endpoint, params={"tl": lang_out, "sl": lang_in, "q": word}, headers=self.headers)
            re_result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', response.text)
            response.raise_for_status()
            try:
                translated_text = "译文: " + html.unescape(re_result[0])
                break
            except Exception as e:
                print("error: 请求数据：" + word + " 返回内容：" + response.text)
                if lang.strip() == 'en':
                    translated_text = 'translation failure'
                elif lang.strip() == 'ch':
                    translated_text = '翻译失败'
        return remove_control_characters(translated_text)
    
if __name__ == '__main__':
    o = GoogleTranslator()
    a= o.translate('2.CnOCR推荐指数', "ch")
    print(a)
