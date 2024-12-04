# pip install paddlepaddle
# pip install paddleocr
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import os
import logging
import translate

class ocrApi(object):
    def __init__(self, imgPath, lang="ch", check=True):
        self.imgPath=imgPath
        self.lang=lang
        self.check=check
        self.baseDir = os.path.dirname(os.path.abspath(__file__))
        self.modelPath = os.path.join(self.baseDir, "ocrModel")

    def getTrain(self):
        # 关闭日志打印
        logging.disable(logging.WARNING)
        logging.disable(logging.DEBUG)
        trainResult = []
        if self.check !="false":    
            transObj = translate.Translator()
        # Paddleocr supports Chinese, English, French, German, Korean and Japanese
        # You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
        # to switch the language model in order
        # 如果不指定det_model_dir、rec_model_dir、cls_model_dir，则会下载模型
        ocr = PaddleOCR(use_angle_cls=True, lang=self.lang, 
                        det_model_dir=os.path.join(self.modelPath, "det", "{}".format(self.lang), "ch_PP-OCRv4_det_infer"),
                        rec_model_dir=os.path.join(self.modelPath, "rec", "{}".format(self.lang), "ch_PP-OCRv4_rec_infer"),
                        cls_model_dir=os.path.join(self.modelPath, "cls", "ch_ppocr_mobile_v2.0_cls_infer"),
                        ) # need to run only once to download and load model into memory
        self.result = ocr.ocr(self.imgPath, cls=True)
        for idx in range(len(self.result)):
            res = self.result[idx]
            for line in res:
                # print(line)
                # 只输出预测结果
                trainResult.append(line[1][0])
                if self.check != "false":
                    trans = transObj.trans(line[1][0], lang=self.lang)
                    trainResult.append(trans)
        return trainResult

    def drawshow(self):
        # draw result
        result = self.result[0]
        image = Image.open(self.imgPath).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path=os.path.join(self.baseDir,'fonts\\simfang.ttf'))
        im_show = Image.fromarray(im_show)
        im_show.save(os.path.join(self.baseDir, "result.jpg"))
        im_show.show()

if __name__=="__main__":
    ocr = ocrApi("E:\\POPO-20241128-154641.jpg")
    result = ocr.getTrain()
