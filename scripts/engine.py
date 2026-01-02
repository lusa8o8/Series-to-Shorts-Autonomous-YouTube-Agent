import os
import json
import subprocess
import re
from supabase import create_client, Client
from huggingface_hub import InferenceClient

# Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
HF_TOKEN = os.environ.get('HF_TOKEN')
OUTPUT_DIR = '/home/node/output'

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Hugging Face
huggingface = InferenceClient(token=HF_TOKEN)

def get_next_video():
    # Fetch from Supabase 'videos' table where status is 'Pending'
    response = supabase.table('videos').select('*').eq('status', 'Pending').limit(1).execute()
    if response.data:
        return response.data[0]
    return None

def update_status(video_id, status):
    supabase.table('videos').update({'status': status}).eq('id', video_id).execute()

def analyze_transcript(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()
    
    prompt = f"""
    Analyze the following 45-minute transcript and identify the 5 most "viral/high-tension" segments.
    Output ONLY a JSON array of objects with "start", "end", and "title" keys.
    Format timestamps as HH:MM:SS or MM:SS.
    
    Transcript:
    {transcript[:15000]} # Smaller limit for HF Inference API stability
    """
    
    # Using Mistral as a reliable instruct model
    response = huggingface.text_generation(
        prompt, 
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_new_tokens=500
    )
    
    try:
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        print(f"Error parsing HF response: {e}")
    return []

def process_clip(video_path, start_time, end_time, output_name):
    filter_complex = (
        f"[0:v]scale=ih*9/16:ih:force_original_aspect_ratio=decrease,crop=ih*9/16:ih,hflip,zoompan=z='1.05':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',eq=saturation=1.1:contrast=1.05[main];"
        f"[0:v]scale=ih*9/16:ih:force_original_aspect_ratio=increase,crop=ih*9/16:ih,boxblur=20:10[bg];"
        f"[bg][main]overlay=(W-w)/2:(H-h)/2[v]"
    )
    audio_filters = "asetrate=44100*1.03,atempo=1/1.03"
    
    cmd = [
        'ffmpeg', '-ss', start_time, '-to', end_time, '-i', video_path,
        '-filter_complex', filter_complex, '-map', '[v]', '-map', '0:a',
        '-af', audio_filters, '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast',
        '-c:a', 'aac', '-b:a', '128k', output_name
    ]
    subprocess.run(cmd)

def main():
    video = get_next_video()
    if not video:
        print("No videos to process.")
        return

    video_id = video['id']
    youtube_url = video['url']
    
    update_status(video_id, 'Processing')
    
    # Download video and subs
    # subprocess.run(['yt-dlp', '-f', 'bestvideo+bestaudio', '--write-subs', '-o', 'input.mp4', youtube_url])
    
    print(f"Processing video {video_id} from {youtube_url}...")
    
    # clips = analyze_transcript('subs.vtt')
    # for i, clip in enumerate(clips):
    #     process_clip('input.mp4', clip['start'], clip['end'], f'clip_{i}.mp4')
    
    update_status(video_id, 'Completed')

if __name__ == "__main__":
    main()
