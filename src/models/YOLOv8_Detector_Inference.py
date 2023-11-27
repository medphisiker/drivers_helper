import cv2
from ultralytics import YOLO


class YOLOv8_Detector_Inference:
    def __init__(self, model_path):
        self.net = YOLO(model_path, task="detect")

    def predict_on_image(self, img):
        return self.net.predict(img)

    def predict_and_draw_image(self, img):
        res = self.net.predict(img)
        some_frame = cv2.imread(img)

        for result in res:
            boxes = result.boxes.cpu().numpy()
            xyxys = boxes.xyxy
            for xyxy in xyxys:
                cv2.rectangle(
                    some_frame,
                    (int(xyxy[0]), int(xyxy[1])),
                    (int(xyxy[2]), int(xyxy[3])),
                    (255, 0, 0),
                    3,
                )

        return some_frame

    def predict_on_video(self, video):
        return self.net.predict(video)

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
                        (255, 0, 0),
                        3,
                    )

            cv2.imshow("video feed", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def parse_video_detections(detection_results):
        dict_of_frames_detections = {}
        frame_counter = 0
        classes_names = detection_results[0].names
        for result in detection_results:
            dict_of_frames_detections[f"frame_{frame_counter}"] = {}
            detected_classes_instances = result.boxes.data[:, 5].to(int)
            for class_instance_label in detected_classes_instances:
                if (
                    result.names[int(class_instance_label)]
                    in dict_of_frames_detections[f"frame_{frame_counter}"].keys()
                ):
                    dict_of_frames_detections[f"frame_{frame_counter}"][
                        result.names[int(class_instance_label)]
                    ] += 1
                else:
                    dict_of_frames_detections[f"frame_{frame_counter}"][
                        result.names[int(class_instance_label)]
                    ] = 1
            frame_counter += 1
        return dict_of_frames_detections
