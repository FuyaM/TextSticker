# ocr_handler.py

import objc_util
import re

VNImageRequestHandler = objc_util.ObjCClass('VNImageRequestHandler')
VNRecognizeTextRequest = objc_util.ObjCClass('VNRecognizeTextRequest')

class OCRHandler:
    def process_image(self, image_data, pil_image, target_words):
        detected_positions = {word: None for word in target_words}
        img_data = objc_util.ns(image_data)
        img_height = pil_image.height

        with objc_util.autoreleasepool():
            req = VNRecognizeTextRequest.alloc().init().autorelease()
            req.setRecognitionLanguages_(['ja'])
            req.setRecognitionLevel_(0)

            handler = VNImageRequestHandler.alloc().initWithData_options_(img_data, None).autorelease()
            success = handler.performRequests_error_([req], None)

            if success:
                for result in req.results():
                    text = str(result.text())
                    bounding_box = result.boundingBox()
                    normalized_text = text.replace(" ", "")
                    y_coord = (1 - bounding_box.origin.y) * img_height

                    for word in target_words:
                        if word in normalized_text:
                            if detected_positions[word] is None or y_coord < detected_positions[word][1]:
                                detected_positions[word] = (text, y_coord, bounding_box)
                            break  # マッチしたらループを抜ける
        
        return detected_positions
