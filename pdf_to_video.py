#!/usr/bin/env python3
"""
PDF to MP4 Slideshow Converter
A production-ready desktop application for converting PDF files into loopable MP4 videos.
"""

import os
import sys
import tempfile
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Optional, Tuple
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PDFToVideoConverter(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("PDF to MP4 Slideshow Converter")
        self.geometry("700x650")
        self.resizable(False, False)
        
        self.pdf_path = None
        self.mp3_path = None
        self.output_path = str(Path.home() / "Desktop")
        self.is_processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame, 
            text="PDF to Video Converter", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        self.pdf_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        self.pdf_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.pdf_frame, text="PDF File:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.pdf_label = ctk.CTkLabel(self.pdf_frame, text="No file selected", text_color="gray")
        self.pdf_label.pack(side="left", padx=10, expand=True, fill="x")
        self.pdf_button = ctk.CTkButton(
            self.pdf_frame, 
            text="Browse", 
            command=self.select_pdf,
            width=80
        )
        self.pdf_button.pack(side="right", padx=10, pady=10)
        
        self.mp3_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        self.mp3_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.mp3_frame, text="MP3 File (Optional):", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.mp3_label = ctk.CTkLabel(self.mp3_frame, text="No file selected", text_color="gray")
        self.mp3_label.pack(side="left", padx=10, expand=True, fill="x")
        self.mp3_button = ctk.CTkButton(
            self.mp3_frame, 
            text="Browse", 
            command=self.select_mp3,
            width=80
        )
        self.mp3_button.pack(side="right", padx=10, pady=10)
        
        self.output_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        self.output_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.output_frame, text="Output Folder:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.output_label = ctk.CTkLabel(self.output_frame, text="Desktop", text_color="white")
        self.output_label.pack(side="left", padx=10, expand=True, fill="x")
        self.output_button = ctk.CTkButton(
            self.output_frame, 
            text="Browse", 
            command=self.select_output_folder,
            width=80
        )
        self.output_button.pack(side="right", padx=10, pady=10)
        
        settings_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        settings_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        duration_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        duration_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(duration_frame, text="Seconds per slide:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.duration_entry = ctk.CTkEntry(duration_frame, width=60, placeholder_text="2")
        self.duration_entry.pack(side="left")
        self.duration_entry.insert(0, "2")
        
        resolution_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        resolution_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(resolution_frame, text="Output Resolution:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.resolution_menu = ctk.CTkOptionMenu(
            resolution_frame,
            values=["720p (1280x720)", "1080p (1920x1080)", "4K (3840x2160)"],
            width=200
        )
        self.resolution_menu.pack(side="left")
        self.resolution_menu.set("1080p (1920x1080)")
        
        layout_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        layout_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(layout_frame, text="Page Layout:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.layout_menu = ctk.CTkOptionMenu(
            layout_frame,
            values=["Single Page", "Book Mode (2 pages)"],
            width=200
        )
        self.layout_menu.pack(side="left")
        self.layout_menu.set("Single Page")
        
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=400)
        self.progress_bar.pack(pady=(20, 10))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(main_frame, text="Ready to convert", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=(0, 20))
        
        self.convert_button = ctk.CTkButton(
            main_frame,
            text="Create Video",
            command=self.start_conversion,
            width=300,
            height=60,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=10,
            text_color="white",
            hover_color=("gray70", "gray30")
        )
        self.convert_button.pack(pady=(15, 25))
        
    def select_pdf(self):
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.pdf_path = filename
            self.pdf_label.configure(text=Path(filename).name, text_color="white")
            
    def select_mp3(self):
        filename = filedialog.askopenfilename(
            title="Select MP3 file (optional)",
            filetypes=[("MP3 files", "*.mp3"), ("All audio files", "*.mp3;*.wav;*.m4a"), ("All files", "*.*")]
        )
        if filename:
            self.mp3_path = filename
            self.mp3_label.configure(text=Path(filename).name, text_color="white")
            
    def select_output_folder(self):
        folder = filedialog.askdirectory(
            title="Select output folder",
            initialdir=self.output_path
        )
        if folder:
            self.output_path = folder
            folder_name = Path(folder).name
            if len(folder_name) > 20:
                folder_name = folder_name[:17] + "..."
            self.output_label.configure(text=folder_name, text_color="white")
            
    def get_resolution(self) -> Tuple[int, int]:
        resolution_map = {
            "720p (1280x720)": (1280, 720),
            "1080p (1920x1080)": (1920, 1080),
            "4K (3840x2160)": (3840, 2160)
        }
        return resolution_map[self.resolution_menu.get()]
    
    def update_status(self, message: str, progress: float = None):
        self.status_label.configure(text=message)
        if progress is not None:
            self.progress_bar.set(progress)
        self.update()
        
    def disable_controls(self):
        self.pdf_button.configure(state="disabled")
        self.mp3_button.configure(state="disabled")
        self.output_button.configure(state="disabled")
        self.duration_entry.configure(state="disabled")
        self.resolution_menu.configure(state="disabled")
        self.layout_menu.configure(state="disabled")
        self.convert_button.configure(state="disabled")
        
    def enable_controls(self):
        self.pdf_button.configure(state="normal")
        self.mp3_button.configure(state="normal")
        self.output_button.configure(state="normal")
        self.duration_entry.configure(state="normal")
        self.resolution_menu.configure(state="normal")
        self.layout_menu.configure(state="normal")
        self.convert_button.configure(state="normal")
        
    def start_conversion(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Please select a PDF file first!")
            return
            
        if self.is_processing:
            return
            
        self.is_processing = True
        self.disable_controls()
        
        thread = threading.Thread(target=self.convert_pdf_to_video)
        thread.start()
        
    def check_ffmpeg(self) -> bool:
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def convert_pdf_to_video(self):
        temp_dir = None
        try:
            if not self.check_ffmpeg():
                self.after(0, lambda: messagebox.showerror(
                    "Error", 
                    "FFmpeg is not installed or not found in PATH.\n"
                    "Please install FFmpeg to use this application."
                ))
                return
                
            duration = float(self.duration_entry.get() or "2")
            if duration <= 0:
                raise ValueError("Duration must be positive")
                
            self.after(0, lambda: self.update_status("Creating temporary directory...", 0.1))
            temp_dir = tempfile.mkdtemp()
            
            self.after(0, lambda: self.update_status("Converting PDF pages to images...", 0.2))
            try:
                print(f"Converting PDF: {self.pdf_path}")
                images = convert_from_path(self.pdf_path, dpi=150, poppler_path='/opt/homebrew/bin' if sys.platform == 'darwin' else None)
                print(f"Successfully converted {len(images)} pages")
            except Exception as e:
                print(f"PDF conversion error: {str(e)}")
                raise Exception(f"Failed to convert PDF: {str(e)}\n\nMake sure poppler is installed:\n- macOS: brew install poppler\n- Ubuntu: sudo apt-get install poppler-utils\n- Windows: Download from GitHub")
                
            if not images:
                raise Exception("No pages found in PDF")
                
            width, height = self.get_resolution()
            book_mode = self.layout_menu.get() == "Book Mode (2 pages)"
            
            total_pages = len(images)
            processed_frames = []
            
            if book_mode:
                # Process pages in pairs for book mode
                for i in range(0, total_pages, 2):
                    progress = 0.2 + (0.4 * (i / total_pages))
                    self.after(0, lambda p=progress, i=i, t=total_pages: self.update_status(
                        f"Processing pages {i+1}-{min(i+2, t)} of {t} (Book mode)...", p
                    ))
                    print(f"Processing pages {i+1}-{min(i+2, total_pages)}/{total_pages} (Book mode)")
                    
                    # Create a frame with two pages side by side
                    background = Image.new('RGB', (width, height), (0, 0, 0))
                    
                    # Calculate size for each page (half width minus gap)
                    gap = 20  # pixels between pages
                    page_width = (width - gap) // 2
                    
                    # Process left page
                    left_page = images[i]
                    left_aspect = left_page.size[0] / left_page.size[1]
                    
                    if left_aspect > page_width / height:
                        left_new_width = page_width
                        left_new_height = int(page_width / left_aspect)
                    else:
                        left_new_height = height
                        left_new_width = int(height * left_aspect)
                        
                    left_resized = left_page.resize((left_new_width, left_new_height), Image.Resampling.LANCZOS)
                    left_x = (page_width - left_new_width) // 2
                    left_y = (height - left_new_height) // 2
                    background.paste(left_resized, (left_x, left_y))
                    
                    # Process right page if exists
                    if i + 1 < total_pages:
                        right_page = images[i + 1]
                        right_aspect = right_page.size[0] / right_page.size[1]
                        
                        if right_aspect > page_width / height:
                            right_new_width = page_width
                            right_new_height = int(page_width / right_aspect)
                        else:
                            right_new_height = height
                            right_new_width = int(height * right_aspect)
                            
                        right_resized = right_page.resize((right_new_width, right_new_height), Image.Resampling.LANCZOS)
                        right_x = page_width + gap + (page_width - right_new_width) // 2
                        right_y = (height - right_new_height) // 2
                        background.paste(right_resized, (right_x, right_y))
                    
                    frame_index = i // 2
                    output_path = os.path.join(temp_dir, f"page_{frame_index:04d}.png")
                    background.save(output_path, "PNG")
                    processed_frames.append(frame_index)
            else:
                # Single page mode (original logic)
                for i, image in enumerate(images):
                    progress = 0.2 + (0.4 * (i / total_pages))
                    self.after(0, lambda p=progress, i=i, t=total_pages: self.update_status(
                        f"Processing page {i+1} of {t}...", p
                    ))
                    print(f"Processing page {i+1}/{total_pages}")
                    
                    img_width, img_height = image.size
                    aspect_ratio = img_width / img_height
                    
                    if aspect_ratio > width / height:
                        new_width = width
                        new_height = int(width / aspect_ratio)
                    else:
                        new_height = height
                        new_width = int(height * aspect_ratio)
                        
                    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    background = Image.new('RGB', (width, height), (0, 0, 0))
                    x = (width - new_width) // 2
                    y = (height - new_height) // 2
                    background.paste(resized, (x, y))
                    
                    output_path = os.path.join(temp_dir, f"page_{i:04d}.png")
                    background.save(output_path, "PNG")
                    processed_frames.append(i)
                
            self.after(0, lambda: self.update_status("Creating video with FFmpeg...", 0.7))
            
            output_path = Path(self.output_path)
            pdf_name = Path(self.pdf_path).stem
            output_file = output_path / f"{pdf_name}_slideshow.mp4"
            
            counter = 1
            while output_file.exists():
                output_file = output_path / f"{pdf_name}_slideshow_{counter}.mp4"
                counter += 1
                
            framerate = 1 / duration
            
            ffmpeg_cmd = [
                "ffmpeg",
                "-framerate", str(framerate),
                "-i", os.path.join(temp_dir, "page_%04d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "medium",
                "-crf", "23",
                "-r", "30",
            ]
            
            if self.mp3_path:
                ffmpeg_cmd.extend([
                    "-stream_loop", "-1",
                    "-i", self.mp3_path,
                    "-shortest",
                    "-c:a", "aac",
                    "-b:a", "192k"
                ])
                
            ffmpeg_cmd.extend([
                "-movflags", "+faststart",
                "-y",
                str(output_file)
            ])
            
            process = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            
            if process.returncode != 0:
                raise Exception(f"FFmpeg error: {process.stderr}")
                
            self.after(0, lambda: self.update_status("Video created successfully!", 1.0))
            self.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"Video saved to:\n{output_file}\n\n"
                f"Duration: {duration}s per slide\n"
                f"Resolution: {self.resolution_menu.get()}\n"
                f"Layout: {self.layout_menu.get()}"
            ))
            
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self.update_status("Error occurred", 0))
            self.after(0, lambda msg=error_msg: messagebox.showerror("Error", f"Conversion failed:\n{msg}"))
            
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                
            self.after(0, self.enable_controls)
            self.is_processing = False
            self.after(0, lambda: self.progress_bar.set(0))


def main():
    app = PDFToVideoConverter()
    app.mainloop()


if __name__ == "__main__":
    main()