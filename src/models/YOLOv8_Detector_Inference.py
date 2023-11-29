import json
from collections import deque

import cv2
import numpy as np
import tqdm
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO


class YOLOv8DetectorInference:
    def __init__(self, model_path, font_path, messages_path):
        self.net = YOLO(model_path, task="detect")
        self.font = font_path
        self.messages_texts = self.read_json(messages_path)

        # время показа сообщения в секундах
        self.message_life = 3
        self.messages_number = 3
        self.labels_color = (255, 255, 255)
        self.signs_deque = deque()

    @staticmethod
    def read_json(filename: str):
        with open(filename) as f_in:
            dct_data = json.load(f_in)

        return dct_data

    def predict_on_image(self, img):
        return self.net.predict(img)

    def predict_on_image_and_viz(self, img):
        res = self.net.predict(img)
        frame = cv2.imread(img)

        for result in res:
            boxes = result.boxes.cpu().numpy()
            label_nums = result.boxes.cls.int().cpu().numpy()
            xyxys = boxes.xyxy
            for xyxy, label_num in zip(xyxys, label_nums):
                # рисуем прямоугольник детекции
                cv2.rectangle(
                    frame,
                    (int(xyxy[0]), int(xyxy[1])),
                    (int(xyxy[2]), int(xyxy[3])),
                    (0, 255, 0),
                    3,
                )

                text = result.names[label_num]

                # печатаем надпись с названием класс в рамке
                color = self.labels_color[::-1]
                frame = self._cv2_img_add_text(
                    frame,
                    text,
                    self.font,
                    (int(xyxy[2]), int(xyxy[3])),
                    color,
                    text_size=30,
                    backgrond=True,
                )

        return frame

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

    @staticmethod
    def _runOnVideo(video, maxFrames):
        """Генератор кадров из видео. Продолжает генерировать кадры
        пока не достигнуто количество кадров maxFrames.
        """

        readFrames = 0
        while True:
            hasFrame, frame = video.read()
            if not hasFrame:
                break

            yield frame

            readFrames += 1
            if readFrames > maxFrames:
                break

    def predict_on_video_and_viz(self, path_video, path_out_video, num_frames=None):
        # Extract video properties
        video = cv2.VideoCapture(path_video)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = video.get(cv2.CAP_PROP_FPS)
        self.message_life *= frames_per_second
        self.message_life = int(self.message_life)

        if num_frames is None:
            num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Initialize video writer
        # fourcc = cv2.VideoWriter_fourcc(*"avc1")
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")

        video_writer = cv2.VideoWriter(
            path_out_video,
            fourcc=fourcc,
            fps=float(frames_per_second),
            frameSize=(width, height),
            isColor=True,
        )

        new_ids = set()

        # Enumerate the frames of the video
        video_frames_gen = self._runOnVideo(video, num_frames)
        for frame in tqdm.tqdm(video_frames_gen, total=num_frames):
            results = self.net.track(frame, persist=True)
            for result in results:
                boxes = result.boxes.cpu().numpy()
                label_nums = result.boxes.cls.int().cpu().numpy()

                if result.boxes.id is not None:
                    track_ids = result.boxes.id.int().cpu().tolist()
                    xyxys = boxes.xyxy

                    for xyxy, label_num, track_id in zip(xyxys, label_nums, track_ids):
                        # рисуем прямоугольник детекции
                        cv2.rectangle(
                            frame,
                            (int(xyxy[0]), int(xyxy[1])),
                            (int(xyxy[2]), int(xyxy[3])),
                            (0, 255, 0),
                            3,
                        )

                        text = f"id={track_id}, {result.names[label_num]}"

                        # печатаем надпись с названием класс в рамке
                        color = self.labels_color[::-1]
                        frame = self._cv2_img_add_text(
                            frame,
                            text,
                            self.font,
                            (int(xyxy[2]), int(xyxy[3])),
                            color,
                            text_size=30,
                            backgrond=True,
                        )

                        # выдаем водителю уведомление о знаках
                        if track_id not in new_ids:
                            new_ids.add(track_id)
                            message_text = self.messages_texts[result.names[label_num]]
                            self.signs_deque.append([message_text, self.message_life])

                        if self.signs_deque:
                            # печатаем уведомления водителю
                            msg_idx = 0
                            y_start = 50
                            while (
                                msg_idx < len(self.signs_deque)
                                and msg_idx < self.messages_number
                            ):
                                text = f"Уведомление: {self.signs_deque[msg_idx][0]}"

                                color = self.labels_color[::-1]
                                height, width, chan = frame.shape
                                frame = self._cv2_img_add_text(
                                    frame,
                                    text,
                                    self.font,
                                    ((50, height - y_start)),
                                    color,
                                    text_size=30,
                                    backgrond=True,
                                )

                                self.signs_deque[msg_idx][1] += -1
                                if self.signs_deque[msg_idx][1] < 1:
                                    self.signs_deque.popleft()

                                msg_idx += 1
                                y_start += 50

            # Write to video file
            video_writer.write(frame)

        # Release resources
        self.mot_tracker = None

        video.release()
        video_writer.release()


if __name__ == "__main__":
    image_path = "data/external/autosave01_02_2012_09_22_38.jpg"
    video_path = "data/external/test_rain_video_1.mp4"

    model_path = "models/train/weights/best.pt"
    model_font_path = "models/fonts/PTSans-Regular.ttf"
    messages_path = "models/messages/messages_for_signs.json"

    model = YOLOv8DetectorInference(model_path, model_font_path, messages_path)

    # Предсказать на картинке и визуализировать предсказания
    image = model.predict_on_image_and_viz(image_path)
    cv2.imwrite("test.jpg", image)

    model.predict_on_video_and_viz(video_path, "output_video.mp4", num_frames=None)
