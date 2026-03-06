from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

video = cv2.VideoCapture("static/video.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2()

count = 0

def generate_frames():
    global count
    
    while True:
        success, frame = video.read()
        if not success:
            break
        
        mask = fgbg.apply(frame)
        
        # find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                count += 1
        
        cv2.putText(frame, "Count: " + str(count), (20,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)