import os
import pathlib
import google.generativeai as genai
from pytube import YouTube
import time


def upload_and_wait_for_processing(path: str, sleep_interval: int = 10):
    """
    Uploads a file and polls its status until it's 'ACTIVE' or fails.

    Args:
        path: The local path to the file to upload.
        sleep_interval: The number of seconds to wait between status checks.

    Returns:
        The file object once it is ready.
    
    Raises:
        Exception: If the file processing fails.
    """
    genai.configure(api_key='AIzaSyB4vtrhMzjG7J_qLb1YobTe6UcSEQaiN74')
    print(f"Uploading file: {path}...")
    video_file = genai.upload_file(path=path)
    print(f"File '{video_file.display_name}' uploaded. Initial state: {video_file.state.name}")

    # Poll the file's status until it is no longer PROCESSING
    while video_file.state.name == "PROCESSING":
        print(f"⏳ Waiting for processing... sleeping for {sleep_interval} seconds.")
        time.sleep(sleep_interval)
        
        # Fetch the latest status of the file
        video_file = genai.get_file(name=video_file.name)
        print(f"Current file state: {video_file.state.name}")

    if video_file.state.name != "ACTIVE":
        raise Exception(f"File processing failed with final state: {video_file.state.name}")
    
    print(f"✅ File '{video_file.display_name}' is now ACTIVE and ready to use.")
    return video_file

# --- 2. Download the YouTube Video ---
# The Gemini API needs the actual video file, not just a URL.
def summary_youtube_video(video_url: str):
    # Upload to Gemini
    print("Uploading video to Gemini")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, "video.mp4")
    video_file = upload_and_wait_for_processing(video_path)
    print(f"Completed file upload. File status: {video_file.state.name}")

    model = genai.GenerativeModel("models/gemini-2.5-pro")
    promt = "Please provide a detailed summary of this video. Describe the main characters, and the key points of their argument. Description language is Vietnamese please"
    print("Generating summary...")
    try:
        # Call the API to get the summary
        response = model.generate_content([promt, video_file])

        print("\n--- Video summarized ---")
        return response.text
    except Exception as e:
        print(f"An error occurred during summary generation: {e}")
    finally:
        print("\nCleaning up files...")
        genai.delete_file(video_file)
        # print("\nDeleted remote file: {video_file.name}")
        # os.remove(video_file_path)
        # print(f"Deleted local file: {video_file_path}")
