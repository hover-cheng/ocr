import requests
import re


def clean_text(text):
    # 移除特殊字符，但保留基本标点符号
    cleaned = re.sub(r'[^\w\s,.!?，。！？、]', '', text)
    return cleaned


class Translator(object):
    def __init__(self):
        self.url = 'https://cn.bing.com/translator'
        self.gi = requests.get(self.url).text
        self.ig = re.search(r'IG:"(.*?)"', self.gi).group(1)
        self.token = re.search(r'params_AbusePreventionHelper = (.*?);', self.gi).group(1)
        self.tokens = self.token.replace("[", "")
        self.js = self.tokens.split(',')
        self.t = self.js[1][1:33]
    
    # 调用bing的翻译功能
    def trans(self, word, lang="en"):
        # 清理文本中的特殊字符
        word = clean_text(word)
        url = 'https://cn.bing.com/ttranslatev3?isVertical=1&&IG={}&IID=translator.5027'.format(self.ig)
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
        response = requests.post(url, data=data, headers=headers)
        # raise_for_status() 方法会检查响应的状态码，如果状态码不是 200，则会引发一个 HTTPError 异常
        response.raise_for_status()
        try:
            translations = response.json()[0]['translations']
            translated_text = "译文: " + translations[0]['text']
        except:
            if lang.strip() == 'en':
                translated_text = 'translation failure'
            elif lang.strip() == 'ch':
                translated_text = '翻译失败'
        return translated_text
    
if __name__ == '__main__':
    o = Translator()
    a= o.trans('开始', "zh")
    print(a)