from pathlib import Path
import ffmpeg  # We'll use ffmpeg-python for conversions

class MediaConverter:
    # Format tuples: (Display Name, Extension, Description)
    SUPPORTED_VIDEO_FORMATS = [
        ('3GP (.3gp)', '.3gp', 'Mobile device video format, commonly used in older phones and basic multimedia devices'),
        ('AVI (.avi)', '.avi', 'Microsoft\'s Audio Video Interleave format, widely supported with good compatibility'),
        ('FLV (.flv)', '.flv', 'Flash Video format, previously popular for web videos and streaming'),
        ('M4V (.m4v)', '.m4v', 'Apple\'s video format, similar to MP4 with optional DRM support'),
        ('MKV (.mkv)', '.mkv', 'Matroska Video, supports multiple audio/subtitle tracks and high-quality video'),
        ('MOV (.mov)', '.mov', 'Apple QuickTime movie format, commonly used in video editing'),
        ('MP4 (.mp4)', '.mp4', 'Most widely used video format, excellent compatibility across devices'),
        ('MPEG (.mpeg)', '.mpeg', 'Standard video format, good compatibility with DVD players and older devices'),
        ('MPG (.mpg)', '.mpg', 'Alternative extension for MPEG format, commonly used in DVD video'),
        ('TS (.ts)', '.ts', 'Transport Stream format, used in broadcasting and Blu-ray discs'),
        ('VOB (.vob)', '.vob', 'DVD Video Object format, used on DVD discs'),
        ('WEBM (.webm)', '.webm', 'Open web video format, optimized for streaming and web playback'),
        ('WMV (.wmv)', '.wmv', 'Windows Media Video, good compatibility with Windows systems')
    ]
    
    SUPPORTED_AUDIO_FORMATS = [
        ('AAC (.aac)', '.aac', 'Advanced Audio Coding, high-quality compressed audio used in digital music'),
        ('AC3 (.ac3)', '.ac3', 'Dolby Digital audio format, commonly used in DVDs and digital TV'),
        ('AIFF (.aiff)', '.aiff', 'Apple\'s uncompressed audio format, high quality for professional use'),
        ('AMR (.amr)', '.amr', 'Adaptive Multi-Rate audio, optimized for speech recording in mobile phones'),
        ('FLAC (.flac)', '.flac', 'Free Lossless Audio Codec, high-quality compressed audio without quality loss'),
        ('M4A (.m4a)', '.m4a', 'AAC audio in MP4 container, commonly used for music and podcasts'),
        ('MP2 (.mp2)', '.mp2', 'Older audio format, still used in some broadcasting applications'),
        ('MP3 (.mp3)', '.mp3', 'Most popular compressed audio format, widely supported across all devices'),
        ('OGA (.oga)', '.oga', 'Ogg audio container format, free and open standard'),
        ('OGG (.ogg)', '.ogg', 'Free and open audio format, popular in gaming and open-source software'),
        ('OPUS (.opus)', '.opus', 'Modern audio format, excellent quality for voice and music streaming'),
        ('WAV (.wav)', '.wav', 'Standard uncompressed audio format, high quality for professional use'),
        ('WMA (.wma)', '.wma', 'Windows Media Audio, good compatibility with Windows systems')
    ]
    
    def __init__(self):
        self.input_path = None
        self.output_path = None
    
    def get_extension_from_display_name(self, display_name: str) -> str:
        """Get the file extension from a display name (e.g., 'MP3 (.mp3)' -> '.mp3')"""
        for formats in [self.SUPPORTED_VIDEO_FORMATS, self.SUPPORTED_AUDIO_FORMATS]:
            for name, ext, _ in formats:
                if name == display_name:
                    return ext
        return None
    
    def get_format_description(self, display_name: str) -> str:
        """Get the description for a format from its display name"""
        for formats in [self.SUPPORTED_VIDEO_FORMATS, self.SUPPORTED_AUDIO_FORMATS]:
            for name, _, desc in formats:
                if name == display_name:
                    return desc
        return "Format description not available"
        
    def validate_format(self, file_path: str, display_format: str) -> bool:
        """Validate if the input file and target format are supported"""
        input_path = Path(file_path)
        if not input_path.exists():
            return False
            
        input_suffix = input_path.suffix.lower()
        target_format = self.get_extension_from_display_name(display_format)
        if not target_format:
            return False
            
        supported_extensions = [ext for _, ext, _ in self.SUPPORTED_VIDEO_FORMATS + self.SUPPORTED_AUDIO_FORMATS]
        return input_suffix in supported_extensions
        
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
