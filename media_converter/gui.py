import wx
import os
from converter import MediaConverter

class MediaConverterFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='ByteShift Media Converter')
        self.converter = MediaConverter()
        
        # Set up the main panel
        panel = wx.Panel(self)
        
        # Create a vertical box sizer for layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Input file selection
        input_box = wx.StaticBox(panel, label="Step 1: Select Input File")
        input_sizer = wx.StaticBoxSizer(input_box, wx.HORIZONTAL)
        
        self.browse_btn = wx.Button(panel, label="Browse for File")
        self.browse_btn.SetToolTip("Select input media file (Ctrl+O)")
        input_sizer.Add(self.browse_btn, 0, wx.ALL, 5)
        
        self.file_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.file_text.SetValue("No file selected")
        input_sizer.Add(self.file_text, 1, wx.EXPAND | wx.ALL, 5)
        
        main_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        # Output format selection
        format_box = wx.StaticBox(panel, label="Step 2: Select Output Format")
        format_sizer = wx.StaticBoxSizer(format_box, wx.VERTICAL)
        
        format_panel = wx.Panel(panel)
        format_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        
        format_label = wx.StaticText(format_panel, label="Output Format:")
        format_panel_sizer.Add(format_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        
        self.format_choice = wx.Choice(format_panel, choices=self.get_supported_formats())
        self.format_choice.SetToolTip("Select the output format")
        self.format_choice.SetSelection(0)  # Select first format by default
        self.format_choice.Bind(wx.EVT_SET_FOCUS, self.on_format_focus)
        format_panel_sizer.Add(self.format_choice, 0, wx.EXPAND | wx.ALL, 5)
        
        # Format description
        description_label = wx.StaticText(format_panel, label="Format Description:")
        format_panel_sizer.Add(description_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        
        # Description text control using the same style as help dialog
        self.description_text = wx.TextCtrl(
            format_panel,
            value="Select a format to see its description",
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.BORDER_NONE,
            size=(-1, 60)
        )
        self.description_text.SetBackgroundColour(format_panel.GetBackgroundColour())
        format_panel_sizer.Add(self.description_text, 0, wx.EXPAND | wx.ALL, 5)
        
        format_panel.SetSizer(format_panel_sizer)
        format_sizer.Add(format_panel, 1, wx.EXPAND)
        
        main_sizer.Add(format_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        # Convert button
        convert_box = wx.StaticBox(panel, label="Step 3: Convert File")
        convert_sizer = wx.StaticBoxSizer(convert_box, wx.HORIZONTAL)
        
        self.convert_btn = wx.Button(panel, label="Start Conversion")
        self.convert_btn.SetToolTip("Start conversion (Ctrl+C)")
        convert_sizer.Add(self.convert_btn, 1, wx.EXPAND | wx.ALL, 5)
        
        main_sizer.Add(convert_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        # Status bar
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("Ready - Press F1 for help")
        
        # Make status bar accessible
        self.status_bar.SetName("Status Bar")  # Name for screen readers
        
        # Set sizer and layout
        panel.SetSizer(main_sizer)
        main_sizer.Fit(self)
        
        # Bind events
        self.browse_btn.Bind(wx.EVT_BUTTON, self.on_browse)
        self.convert_btn.Bind(wx.EVT_BUTTON, self.on_convert)
        self.format_choice.Bind(wx.EVT_CHOICE, self.on_format_change)
        
        # Accelerator table for keyboard shortcuts
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('O'), self.browse_btn.GetId()),
            (wx.ACCEL_CTRL, ord('C'), self.convert_btn.GetId()),
            (wx.ACCEL_NORMAL, wx.WXK_F1, wx.ID_HELP)
        ])
        self.SetAcceleratorTable(accel_tbl)
        
        # Bind help event
        self.Bind(wx.EVT_MENU, self.on_help, id=wx.ID_HELP)
        
        # Set initial focus
        self.browse_btn.SetFocus()
    
    def get_supported_formats(self):
        formats = []
        formats.extend([name for name, _, _ in self.converter.SUPPORTED_VIDEO_FORMATS])
        formats.extend([name for name, _, _ in self.converter.SUPPORTED_AUDIO_FORMATS])
        return sorted(formats)
    
    def on_help(self, event):
        help_dialog = wx.Dialog(self, title="Keyboard Shortcuts", size=(400, 300))
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a read-only text control for the help text
        help_text = (
            "Keyboard Shortcuts:\n\n"
            "Ctrl+O: Open file\n"
            "Ctrl+C: Start conversion\n"
            "Tab: Move between controls\n"
            "Space/Enter: Activate button\n"
            "F1: Show this help\n\n"
            "Navigation Instructions:\n\n"
            "1. Use Tab to move between controls\n"
            "2. When in format selection, use Up/Down arrows to choose format\n"
            "3. Press Space or Enter to activate buttons\n"
            "4. Press Escape to close this help window"
        )
        
        text_ctrl = wx.TextCtrl(
            help_dialog, 
            value=help_text,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.BORDER_NONE
        )
        text_ctrl.SetBackgroundColour(help_dialog.GetBackgroundColour())
        dialog_sizer.Add(text_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        # Add OK button at the bottom
        ok_button = wx.Button(help_dialog, wx.ID_OK, "OK")
        ok_button.SetDefault()
        dialog_sizer.Add(ok_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        help_dialog.SetSizer(dialog_sizer)
        
        # Set initial focus to the text control for immediate reading
        text_ctrl.SetFocus()
        
        help_dialog.ShowModal()
        help_dialog.Destroy()

    def on_browse(self, event):
        extensions = [ext[1:] for _, ext, _ in (self.converter.SUPPORTED_VIDEO_FORMATS + self.converter.SUPPORTED_AUDIO_FORMATS)]
        wildcard = "Media Files|*." + ";*.".join(extensions) + "|All files (*.*)|*.*"
        with wx.FileDialog(self, "Choose a file", wildcard=wildcard,
                         style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            
            pathname = fileDialog.GetPath()
            self.file_text.SetValue(pathname)
            self.set_status_text(f"Selected file: {os.path.basename(pathname)}")
            wx.Bell()  # Audible feedback
            self.format_choice.SetFocus()
    
    def on_format_change(self, event):
        selected = self.format_choice.GetString(self.format_choice.GetSelection())
        description = self.converter.get_format_description(selected)
        self.description_text.SetValue(description)
        # Don't steal focus when changing format
        wx.Bell()  # Audible feedback
    
    def on_format_focus(self, event):
        # Ensure a format is selected when the choice gets focus
        if self.format_choice.GetSelection() == wx.NOT_FOUND:
            self.format_choice.SetSelection(0)
            self.on_format_change(None)  # Update description for the selected format
        event.Skip()  # Continue with normal focus handling
    
    def on_convert(self, event):
        input_path = self.file_text.GetValue()
        if input_path == "No file selected":
            wx.MessageBox("Please select an input file first", "Error", 
                         wx.OK | wx.ICON_ERROR)
            self.browse_btn.SetFocus()
            return
        
        if self.format_choice.GetSelection() == wx.NOT_FOUND:
            wx.MessageBox("Please select an output format", "Error",
                         wx.OK | wx.ICON_ERROR)
            self.format_choice.SetFocus()
            return
        
        display_format = self.format_choice.GetString(self.format_choice.GetSelection())
        output_format = self.converter.get_extension_from_display_name(display_format)
        
        if not self.validate_conversion(input_path, display_format):
            self.format_choice.SetFocus()
            return
            
        with wx.FileDialog(self, "Save converted file", 
                          wildcard=f"{display_format}|*{output_format}|All files (*.*)|*.*",
                          style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            
            output_path = fileDialog.GetPath()
            
            # Show progress dialog
            progress_dialog = wx.ProgressDialog("Converting",
                                           "Converting file...",
                                           maximum=100,
                                           parent=self,
                                           style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
            
            # Disable convert button
            self.convert_btn.Enable(False)
            self.status_bar.SetStatusText("Converting... Please wait")
            
            try:
                # Start conversion
                success = self.converter.convert_media(input_path, output_path)
                
                if success:
                    wx.MessageBox("Media conversion completed", "Success",
                                wx.OK | wx.ICON_INFORMATION)
                    self.status_bar.SetStatusText("Conversion completed successfully")
                    wx.Bell()
                else:
                    wx.MessageBox("Media conversion failed", "Error",
                                wx.OK | wx.ICON_ERROR)
                    self.status_bar.SetStatusText("Conversion failed")
            finally:
                progress_dialog.Destroy()
                self.convert_btn.Enable(True)
    
    def validate_conversion(self, input_path, display_format):
        input_ext = os.path.splitext(input_path)[1].lower()
        supported_extensions = [ext for _, ext, _ in (self.converter.SUPPORTED_VIDEO_FORMATS + 
                                                    self.converter.SUPPORTED_AUDIO_FORMATS)]
        if input_ext not in supported_extensions:
            wx.MessageBox(f"Input format {input_ext} is not supported", "Error",
                         wx.OK | wx.ICON_ERROR)
            return False
        return True

    def set_status_text(self, text: str):
        """Set status bar text and ensure it's screen reader friendly"""
        self.status_bar.SetStatusText(text)
        # Force a focus change to trigger screen reader
        self.status_bar.SetFocus()
        self.format_choice.SetFocus()
        
class MediaConverterApp(wx.App):
    def OnInit(self):
        frame = MediaConverterFrame()
        frame.Show()
        return True

if __name__ == "__main__":
    app = MediaConverterApp()
    app.MainLoop()
