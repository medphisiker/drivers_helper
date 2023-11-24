# drivers_helper
Inference class

predict_on_image - predicts on image, as easy as predict_on_image(image)

predict_and_draw_image - draws an image with bboxes, as in previous example, press any key to exit

predict_on_video - predicts on video, predict_on_video(video)

predict_and_display_video - displays video with bboxes, as previous example, press any key to exit

parse_video_detections(detection_results) - counts number of each class instance per frame, static method, needs predict_on_video results
