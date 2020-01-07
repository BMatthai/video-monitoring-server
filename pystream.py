from flask import Flask, render_template, Response
from video import Video

app = Flask(__name__)
vid=Video()

def gen():
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video():
	return render_template('index.html')

@app.route('/video_feed')
def video_feed():
	return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)