from flask import Flask, render_template, request, redirect, url_for
import os
from analyse import analyze_video
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["UPLOAD_FOLDER"] = os.path.join(basedir, "static/videos")

@app.route("/")
def auth():
  return render_template("auth.html")

@app.route("/home")
def home():
  return render_template("index.html")

@app.route("/home", methods=["POST"])
def upload():
  if request.method == "POST":
    f = request.files["video"]
    candidate_labels_str = request.form["candidate_labels"] 
    if f:
      # Validate file extension
      if not f.filename.lower().endswith(".mp4"):
        return "Invalid video file format. Only MP4 is allowed."
      # Save the file
      filename = f.filename
      filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
      f.save(filepath)
      # Split comma-separated labels into a list
      candidate_labels = candidate_labels_str.split(",")
      candidate_labels = [label.strip() for label in candidate_labels]  
      # Analyze the video and get results
      analysis_result = analyze_video(filepath,candidate_labels)
      # Redirect to preview page with analysis result
      return render_template("preview.html", filename=filename, analysis_result=analysis_result)
    else:
      return "No video file chosen."
  return redirect(url_for("home"))

@app.route("/preview/<filename>")
def preview(filename, analysis_result=None):
  return render_template("preview.html", filename=filename, analysis_result=analysis_result)



if __name__ == "__main__":
  app.config["UPLOAD_FOLDER"] = os.path.join(basedir, "static/videos")
  app.run(debug=True)
