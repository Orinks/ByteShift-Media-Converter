# ByteShift Media Converter

A screen reader-friendly desktop application for converting audio and video files between different formats. Built with Python and wxPython, using FFmpeg for media conversion.

## Features

- Convert between a wide range of video and audio formats
- Native Windows controls for optimal accessibility
- Full screen reader support with NVDA and Windows Narrator
- Keyboard shortcuts for all major functions
- Detailed format descriptions and guidance
- Progress tracking during conversion
- Error handling with accessible notifications
- Help system with keyboard navigation guide

## Supported Formats

### Video Formats
- 3GP (.3gp) - Mobile device video format
- AVI (.avi) - Microsoft's Audio Video Interleave format
- FLV (.flv) - Flash Video format
- M4V (.m4v) - Apple's video format
- MKV (.mkv) - Matroska Video format
- MOV (.mov) - Apple QuickTime movie format
- MP4 (.mp4) - Most widely used video format
- MPEG/MPG (.mpeg/.mpg) - Standard video format
- TS (.ts) - Transport Stream format
- VOB (.vob) - DVD Video Object format
- WEBM (.webm) - Open web video format
- WMV (.wmv) - Windows Media Video format

### Audio Formats
- AAC (.aac) - Advanced Audio Coding format
- AC3 (.ac3) - Dolby Digital audio format
- AIFF (.aiff) - Apple's uncompressed audio format
- AMR (.amr) - Adaptive Multi-Rate audio
- FLAC (.flac) - Free Lossless Audio Codec
- M4A (.m4a) - AAC audio in MP4 container
- MP2 (.mp2) - Broadcasting audio format
- MP3 (.mp3) - Most popular compressed audio format
- OGG (.ogg) - Free and open-source audio format
- OPUS (.opus) - Modern audio format for streaming
- WAV (.wav) - Standard uncompressed audio format
- WMA (.wma) - Windows Media Audio format

## Installation

### Option 1: Download Pre-built Binaries (Recommended)
1. Go to the [Releases](https://github.com/Orinks/ByteShift-Media-Converter/releases) page
2. Download the latest release:
   - `ByteShiftMediaConverter-setup.exe` for a full installation
   - `ByteShiftMediaConverter-portable.zip` for portable use

### Option 2: Build from Source
1. Clone the repository:
```bash
git clone https://github.com/Orinks/ByteShift-Media-Converter.git
cd ByteShift-Media-Converter
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH
   - Linux: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`

## Usage

1. Launch ByteShift Media Converter
2. Select an input file using the "Browse" button or press Ctrl+O
3. Choose the desired output format from the dropdown menu
4. Review the format description for compatibility information
5. Click "Convert" or press Ctrl+C to start the conversion
6. Select the output location when prompted
7. Wait for the conversion to complete

### Keyboard Shortcuts

- `Ctrl+O`: Open file selection dialog
- `Ctrl+C`: Start conversion
- `F1`: Show help with keyboard navigation guide
- `Tab`: Navigate between controls
- `Space/Enter`: Activate buttons and controls
- `Escape`: Close dialogs

## Accessibility Features

- Native Windows controls for optimal screen reader compatibility
- Full keyboard navigation support
- Clear focus indicators
- Descriptive format information
- Detailed status announcements
- Help system with navigation guide
- Standard Windows keyboard behavior

## Requirements

- Windows 10 or later
- No additional software required - all codecs included!

## Project Structure

```
media_converter/
├── converter.py     # Core conversion logic
├── gui.py          # User interface implementation
├── main.py         # Application entry point
└── requirements.txt # Project dependencies
```

## Error Handling

The application includes comprehensive error handling for:
- Unsupported file formats
- Invalid input files
- Failed conversions
- FFmpeg errors

All errors are reported through native Windows dialogs for optimal accessibility.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

You are free to:
* Share — copy and redistribute the material in any medium or format
* Adapt — remix, transform, and build upon the material

Under the following terms:
* Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
* NonCommercial — You may not use the material for commercial purposes.

For more details, see the [LICENSE](LICENSE) file or visit the [CC BY-NC 4.0 license page](https://creativecommons.org/licenses/by-nc/4.0/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Make sure to read the license terms before contributing.

## Acknowledgments

- FFmpeg for media conversion capabilities
- wxPython for the accessible GUI framework
