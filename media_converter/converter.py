from pathlib import Path
import ffmpeg  # We'll use ffmpeg-python for conversions

class MediaConverter:
    SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
    SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.aac', '.ogg', '.flac']
    
    def __init__(self):
        self.input_path = None
        self.output_path = None
        
    def validate_format(self, file_path: str, target_format: str) -> bool:
        """Validate if the input file and target format are supported"""
        input_path = Path(file_path)
        if not input_path.exists():
            return False
            
        input_suffix = input_path.suffix.lower()
        target_format = target_format.lower()
        
        return (input_suffix in self.SUPPORTED_VIDEO_FORMATS or 
                input_suffix in self.SUPPORTED_AUDIO_FORMATS)
        
    def convert_media(self, input_path: str, output_path: str) -> bool:
        """Convert media file using ffmpeg"""
        try:
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(stream, output_path)
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            return True
        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
            return False
