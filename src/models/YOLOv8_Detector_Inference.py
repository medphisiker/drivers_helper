import cv2
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class YOLOv8DetectorInference:
    def __init__(self, model_path, font_path):
        self.net = YOLO(model_path, task="detect")
        self.font = font_path
        self.labels_color = (255, 255, 255)

    def predict_on_image(self, img):
        return self.net.predict(img)

    def predict_on_image_and_viz(self, img):
        res = self.net.predict(img)
        some_frame = cv2.imread(img)

        for result in res:
            boxes = result.boxes.cpu().numpy()
            label_num = int(result.boxes.cls.cpu().item())
            xyxys = boxes.xyxy
            for xyxy in xyxys:
                cv2.rectangle(
                    some_frame,
                    (int(xyxy[0]), int(xyxy[1])),
                    (int(xyxy[2]), int(xyxy[3])),
                    (0, 255, 0),
                    3,
                )

                text = result.names[label_num]

                # переводим color из bgr в rgb
                color = self.labels_color[::-1]
                some_frame = self._cv2_img_add_text(
                    some_frame,
                    text,
                    self.font,
                    (int(xyxy[2]), int(xyxy[3])),
                    color,
                    text_size=30,
                    backgrond=True,
                )

        return some_frame

    @staticmethod
    def set_offset(bbox, offset):
        bbox = [
            bbox[x] - offset if x < 2 else bbox[x] + offset for x in range(len(bbox))
        ]
        return bbox

    def _cv2_img_add_text(
        self,
        pil_img,
        text,
        font,
        left_corner,
        text_rgb_color,
        text_size=24,
        backgrond=True,
        **option,
    ):
        """
        cv2_img_add_text(img, '中文', (0, 0), text_rgb_color=(0, 255, 0), text_size=12, font='mingliu.ttc')
        """
        # https://stackoverflow.com/questions/50854235/
        # how-to-draw-chinese-text-on-the-image-using-cv2-puttextcorrectly-pythonopen
        if isinstance(pil_img, np.ndarray):
            pil_img = Image.fromarray(cv2.cvtColor(pil_img, cv2.COLOR_BGR2RGB))

        draw = ImageDraw.Draw(pil_img, "RGBA")
        font_text = ImageFont.truetype(
            font=font, size=text_size, encoding=option.get("encoding", "utf-8")
        )

        # рисуем полупрозрачную подложку
        if backgrond:
            bbox = draw.textbbox(left_corner, text, font=font_text)
            bbox = self.set_offset(bbox, offset=10)
            self._current_text_obj_bbox = bbox
            draw.rectangle(bbox, fill=(38, 38, 38, 170))

        draw.text(left_corner, text, text_rgb_color, font=font_text)
        cv2_img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)

        return cv2_img

    def predict_and_display_video(self, video, frame_stride=10):
        cap = cv2.VideoCapture(video)
        counter = 0
        boxes = []
        xyxys = []
        res = []

        while True:
            ret, frame = cap.read()

            if counter % frame_stride == 0:
                res = self.net.predict(frame, verbose=False)

            for result in res:
                boxes = result.boxes.cpu().numpy()
                xyxys = boxes.xyxy
                for xyxy in xyxys:
                    cv2.rectangle(
                        frame,
                        (int(xyxy[0]), int(xyxy[1])),
                        (int(xyxy[2]), int(xyxy[3])),
                        (0, 255, 0),
                        3,
                    )

            cv2.imshow("video feed", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    image_path = "data/external/autosave01_02_2012_09_22_38.jpg"

    model_path = "models/train2/weights/best.pt"
    model_font_path = "models/fonts/PTSans-Regular.ttf"

    model = YOLOv8DetectorInference(model_path, model_font_path)
    image = model.predict_on_image_and_viz(image_path)
    cv2.imwrite("test.jpg", image)
