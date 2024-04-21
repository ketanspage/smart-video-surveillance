from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import base64
import requests
def analyze_video(video_path,candidate_labels):
  # Open the video capture object
  cap = cv2.VideoCapture(video_path)

  # Check if video opened successfully
  if not cap.isOpened():
    print("Error opening video!")
    return "Error processing video"

  # target frame
  target_frame = 30

  # Move to the target frame
  cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame - 1)

  # Capture the frame
  ret, frame = cap.read()

  # If the frame is not read successfully exit
  if not ret:
    print(f"Couldn't read frame {target_frame}. Exiting...")
    return "Error processing video"

  # Encode frame as base64 string (for API)
  _, buffer = cv2.imencode('.jpg', frame)
  image_data = base64.b64encode(buffer).decode("utf-8")

  # Define API details (replace with your API details)
  API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-large-patch14"
  headers = {"Authorization": "Bearer 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"}

  def query(data):
    payload = {
      "parameters": data["parameters"],
      "inputs": image_data
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

  # Define parameters for the query
  try:
    output = query({
    "parameters": {"candidate_labels": candidate_labels},
    "inputs": image_data
  })

    # Process output as before
  except requests.exceptions.RequestException as e:
    return f"Error analyzing video: {str(e)}"


  # Process and format analysis result
  if len(output) > 0:
    val = output[0]['label']
    score = output[0]['score']*100
    result_string = f"{val} detected with a confidence score of {score}"
  else:
    result_string = "No matching labels found in the analyzed frame."

  # Release the video capture object
  cap.release()
  cv2.destroyAllWindows()

  return result_string