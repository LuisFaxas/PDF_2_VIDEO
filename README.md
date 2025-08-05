# PDF to MP4 Slideshow Converter

A production-ready Python desktop application that converts PDF files into MP4 slideshow videos with optional background music. Perfect for artists, comic book lovers, and creators who want to display their PDFs as looping videos on Apple TV or any media device.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🎨 **Modern GUI** - Clean, dark-themed interface built with CustomTkinter
- 📄 **PDF to Video** - Convert any PDF into a high-quality MP4 video
- 🎵 **Background Music** - Add optional MP3 background music to your slideshow
- 📖 **Book Mode** - Display pages side-by-side like an open book
- 🎯 **Multiple Resolutions** - Support for 720p, 1080p, and 4K output
- ⏱️ **Customizable Timing** - Set your own duration for each slide
- 📁 **Flexible Output** - Choose where to save your video files
- 🔄 **Progress Tracking** - Real-time progress bar and status updates
- 🎬 **Loopable Videos** - Perfect for continuous display

## Requirements

### System Requirements
- Python 3.8 or higher
- FFmpeg (for video encoding)
- Poppler (for PDF rendering)

### Python Dependencies
- customtkinter
- pdf2image
- Pillow

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/LuisFaxas/PDF_2_VIDEO.git
cd PDF_2_VIDEO
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install system dependencies:**

**macOS:**
```bash
brew install ffmpeg poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg poppler-utils
```

**Windows:**
- Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
- Download Poppler from [GitHub](https://github.com/oschwartz10612/poppler-windows/releases/)
- Add both to your system PATH

## Usage

Run the application:
```bash
python pdf_to_video.py
```

1. **Select PDF** - Click "Browse" to choose your PDF file
2. **Add Music (Optional)** - Select an MP3 file for background audio
3. **Choose Output Folder** - Select where to save the video (defaults to Desktop)
4. **Configure Settings:**
   - Set seconds per slide (default: 2 seconds)
   - Choose output resolution (720p, 1080p, or 4K)
   - Select page layout (Single Page or Book Mode)
5. **Create Video** - Click the button and watch the progress

## Features in Detail

### Book Mode
When enabled, displays two pages side-by-side like an open book, perfect for:
- Comic books
- Art portfolios
- Photo albums
- Presentations

### Resolution Options
- **720p (1280x720)** - Good for smaller files and web sharing
- **1080p (1920x1080)** - Standard HD quality (default)
- **4K (3840x2160)** - Ultra-high definition for large displays

### Video Output
- Format: MP4 (H.264/AAC)
- Compatible with all major media players
- Optimized for streaming devices like Apple TV
- Includes proper metadata for looping playback

## Building Standalone Application

To create a standalone executable that doesn't require Python:

**Using PyInstaller:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "*.png:." pdf_to_video.py
```

The executable will be in the `dist` folder.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI
- Uses [pdf2image](https://github.com/Belval/pdf2image) for PDF processing
- Powered by [FFmpeg](https://ffmpeg.org/) for video encoding

## Author

Created by Luis Faxas

---

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
