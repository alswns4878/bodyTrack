import cv2
import mediapipe as mp

# MediaPipe 초기화
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()

sec = 3

# OpenCV 초기화
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # 비디오에서 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        continue
    
    # RGB로 변환
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # MediaPipe Holistic을 사용하여 사람 감지
    results = holistic.process(rgb_frame)
    
    # 결과가 있을 경우
    if results.pose_landmarks:
        # 사용할 포즈 랜드마크 선택 (여기서는 어깨, 엉덩이, 목을 사용)
        landmarks_to_use = [11, 12, 23]

        # 사람의 bounding box 계산
        bbox_coor = [frame.shape[1], frame.shape[0], 0, 0]  # [xmin, ymin, xmax, ymax]

        for idx in landmarks_to_use:
            landmark = results.pose_landmarks.landmark[idx]
            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])

            # bbox_coor 업데이트
            bbox_coor[0] = min(bbox_coor[0], x)
            bbox_coor[1] = min(bbox_coor[1], y)
            bbox_coor[2] = max(bbox_coor[2], x)
            bbox_coor[3] = max(bbox_coor[3], y)

        # bounding box 크기 조절
        bbox_width = int((bbox_coor[2] - bbox_coor[0]) * 1.5)
        bbox_height = int((bbox_coor[3] - bbox_coor[1]) * 1.5)

        bbox_coor[0] = max(0, bbox_coor[0] - (bbox_width - (bbox_coor[2] - bbox_coor[0])) // 2)
        bbox_coor[1] = max(0, bbox_coor[1] - (bbox_height - (bbox_coor[3] - bbox_coor[1])) // 2)
        bbox_coor[2] = min(frame.shape[1], bbox_coor[0] + bbox_width)
        bbox_coor[3] = min(frame.shape[0], bbox_coor[1] + bbox_height)

        # bounding box 그리기
        cv2.rectangle(frame, (bbox_coor[0], bbox_coor[1]), (bbox_coor[2], bbox_coor[3]), (0, 255, 0), 2)

    # 화면에 출력
    cv2.imshow("Holistic Model", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 시 리소스 해제
cap.release()
cv2.destroyAllWindows()