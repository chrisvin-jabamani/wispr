"""
Hotkey listener - hold Cmd+Control to record, release to transcribe
"""

from pynput import keyboard

class HotkeyListener:
    def __init__(self, start_callback, stop_callback):
        """
        start_callback: function to call when hotkey is pressed
        stop_callback: function to call when hotkey is released
        """
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.listener = None
        self.pressed_keys = set()
        self.is_recording = False
        
    def _check_hotkey_pressed(self):
        """Check if both Cmd and Control are currently pressed"""
        cmd_pressed = (keyboard.Key.cmd in self.pressed_keys or 
                      keyboard.Key.cmd_r in self.pressed_keys)
        ctrl_pressed = (keyboard.Key.ctrl in self.pressed_keys or 
                       keyboard.Key.ctrl_r in self.pressed_keys or
                       keyboard.Key.ctrl_l in self.pressed_keys)
        return cmd_pressed and ctrl_pressed
        
    def on_press(self, key):
        """Handle key press events"""
        self.pressed_keys.add(key)
        
        # Start recording when both keys are pressed
        if self._check_hotkey_pressed() and not self.is_recording:
            print("✨ Cmd+Control pressed - recording...")
            self.is_recording = True
            self.start_callback()
    
    def on_release(self, key):
        """Handle key release events"""
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
        
        # Stop recording when either key is released
        if key in [keyboard.Key.cmd, keyboard.Key.cmd_r, 
                   keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l]:
            if self.is_recording:
                print("✨ Keys released - stopping...")
                self.is_recording = False
                self.stop_callback()
    
    def start(self):
        """Start listening for hotkeys"""
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        print("🎹 Hotkey listener started (hold Cmd+Control to record)")
    
    def stop(self):
        """Stop listening"""
        if self.listener:
            self.listener.stop()
