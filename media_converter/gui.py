import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from converter import MediaConverter
import keyboard
import winsound
import os

class MediaConverterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Media Converter")
        self.converter = MediaConverter()
        
        # Make window screen reader friendly
        self.root.configure(takefocus=True)
        
        # Register keyboard shortcuts
        keyboard.add_hotkey('ctrl+o', self.select_input)
        keyboard.add_hotkey('ctrl+c', self.start_conversion)
        
        self.setup_ui()
    
    def play_notification(self, success=True):
        if success:
            winsound.MessageBeep(winsound.MB_OK)
        else:
            winsound.MessageBeep(winsound.MB_ICONHAND)
    
    def create_tooltip(self, widget, text):
        widget.bind('<Enter>', lambda e: self.show_tooltip(e, text))
        widget.bind('<Leave>', lambda e: self.hide_tooltip())

    def show_tooltip(self, event, text):
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel(event.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(self.tooltip, text=text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1)
        label.pack()

    def hide_tooltip(self):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
            
    def validate_conversion(self, input_path, output_format):
        input_ext = os.path.splitext(input_path)[1].lower()
        if (input_ext not in self.converter.SUPPORTED_VIDEO_FORMATS and 
            input_ext not in self.converter.SUPPORTED_AUDIO_FORMATS):
            messagebox.showerror("Error", f"Input format {input_ext} is not supported")
            self.play_notification(False)
            return False
        return True
        
    def setup_ui(self):
        # Input file selection
        self.input_frame = ttk.LabelFrame(
            self.root, 
            text="Select Input File",
            padding="10"
        )
        self.input_frame.pack(fill="x", padx=10, pady=5)
        
        self.input_button = ttk.Button(
            self.input_frame,
            text="Browse (Ctrl+O)",
            command=self.select_input
        )
        self.input_button.configure(takefocus=True)
        self.input_button.pack(side="left", padx=5)
        
        self.input_label = ttk.Label(
            self.input_frame,
            text="No file selected"
        )
        self.input_label.pack(side="left", padx=5)
        
        # Output format selection
        self.format_frame = ttk.LabelFrame(
            self.root,
            text="Select Output Format",
            padding="10"
        )
        self.format_frame.pack(fill="x", padx=10, pady=5)
        
        self.format_combo = ttk.Combobox(
            self.format_frame,
            values=self.get_supported_formats(),
            state="readonly",
            takefocus=True
        )
        self.format_combo.set("Select format")
        self.format_combo.pack(fill="x", padx=5)
        
        # Convert button
        self.convert_button = ttk.Button(
            self.root,
            text="Convert (Ctrl+C)",
            command=self.start_conversion
        )
        self.convert_button.pack(pady=10)
        
        # Add tooltips
        self.create_tooltip(self.input_button, "Select input media file (Ctrl+O)")
        self.create_tooltip(self.convert_button, "Start conversion (Ctrl+C)")
        
        # Status area
        self.status_label = ttk.Label(
            self.root,
            text="Ready"
        )
        self.status_label.pack(pady=5)
        
    def get_supported_formats(self):
        formats = []
        formats.extend(self.converter.SUPPORTED_VIDEO_FORMATS)
        formats.extend(self.converter.SUPPORTED_AUDIO_FORMATS)
        return formats
        
    def select_input(self):
        file_path = filedialog.askopenfilename(
            title="Select Media File",
            filetypes=[
                ("Media Files", "*.mp4 *.avi *.mkv *.mov *.wmv *.mp3 *.wav *.aac *.ogg *.flac"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.input_label.config(text=file_path)
            self.root.focus_force()
            
    def start_conversion(self):
        input_path = self.input_label.cget("text")
        if input_path == "No file selected":
            self.play_notification(False)
            messagebox.showerror("Error", "Please select an input file first")
            return
            
        output_format = self.format_combo.get()
        if output_format == "Select format" or not self.validate_conversion(input_path, output_format):
            self.play_notification(False)
            messagebox.showerror("Error", "Please select an output format")
            return
            
        output_path = filedialog.asksaveasfilename(
            defaultextension=output_format,
            filetypes=[(f"{output_format} files", f"*{output_format}")]
        )
        if not output_path:
            return
            
        # Show progress
        self.status_label.config(text="Converting... Please wait")
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate'
        )
        self.progress.pack(pady=5)
        self.progress.start()
        
        # Start conversion
        success = self.converter.convert_media(input_path, output_path)
        
        # Update UI
        self.progress.stop()
        self.progress.destroy()
        
        if success:
            self.status_label.config(text="Conversion completed successfully")
            messagebox.showinfo("Success", "Media conversion completed")
        else:
            self.status_label.config(text="Conversion failed")
            messagebox.showerror("Error", "Media conversion failed")
