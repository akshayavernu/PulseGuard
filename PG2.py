import cv2
import time
from vitallens import VitalLens

# Use full path for the video file
VIDEO_PATH = "/Users/input_username/Desktop/face_video.mp4"

# Step 1: Record 15 seconds of video
print("Recording 15 seconds... look at the camera!")
camera = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(VIDEO_PATH, fourcc, 30.0, (640, 480))

start = time.time()
while time.time() - start < 15:
    ret, frame = camera.read()
    if ret:
        out.write(frame)
        cv2.imshow("Recording - look at camera!", frame)
        seconds_left = 15 -int(time.time() - start)
        print(f"Recording... {seconds_left}s left", end='\r')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
out.release()
cv2.destroyAllWindows()
print("\nRecording done! Analyzing...")

# Step 2: Analyze the video
vl = VitalLens(method="vitallens", api_key="input_vitallens_api_key")
results = vl(VIDEO_PATH)

if results:
    vitals = results[0].get('vitals', {})
    if 'heart_rate' in vitals and vitals['heart_rate']['value'] is not None:
        bpm = vitals['heart_rate']['value']
        confidence = vitals['heart_rate']['confidence']
        print(f"BPM: {bpm:.1f}  (confidence: {confidence:.2f})")
    else:
        print("Could not detect heart rate. Make sure your face was visible.")
else:
    print("No results returned.")
