from moviepy.video.io.VideoFileClip import VideoFileClip

def extract_audio(input_video, output_audio):
    video_clip = VideoFileClip(input_video)
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(output_audio, codec='libmp3lame')

if __name__ == "__main__":
    input_video = "input.mp4"  # Input MP4 file
    output_audio = "output_audio.mp3"  # Output MP3 file

    extract_audio(input_video, output_audio)