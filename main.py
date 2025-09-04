import keyboard
import pyperclip
import json
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional, Callable


class ConfigManager:
    """Handles loading and saving trigger-text mappings from/to config file."""
    
    def __init__(self, config_path: str = "phrases.json"):
        self.config_path = Path(config_path)
    
    def load_trigger_mappings(self) -> Dict[str, str]:
        """Load trigger-text mappings from config file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self._get_default_mappings()
        
        # Create default config if file doesn't exist
        default_mappings = self._get_default_mappings()
        self.save_trigger_mappings(default_mappings)
        return default_mappings
    
    def save_trigger_mappings(self, mappings: Dict[str, str]) -> bool:
        """Save trigger-text mappings to config file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(mappings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def validate_hotkey(self, hotkey: str) -> bool:
        """Validate if hotkey format is correct."""
        try:
            # Test if keyboard library can parse the hotkey
            keyboard.parse_hotkey(hotkey)
            return True
        except ValueError:
            return False
    
    def _get_default_mappings(self) -> Dict[str, str]:
        """Get default trigger-text mappings."""
        return {
            'ctrl+1': '你好，很高兴见到你！',
            'ctrl+2': '谢谢你的帮助',
            'ctrl+3': '我不太明白，能再说一遍吗？',
            'ctrl+4': '没问题，我来帮你',
            'ctrl+5': '游戏愉快！',
            'ctrl+6': '等等我，马上来',
            'ctrl+7': '好的，我知道了',
            'ctrl+8': '抱歉，我要离开一下',
            'ctrl+9': '太厉害了！',
            'ctrl+0': '再见！下次再聊'
        }


class ClipboardExecutor:
    """Handles copying text to clipboard and user feedback."""
    
    def execute(self, text: str) -> None:
        """Execute the clipboard operation with the given text."""
        if self.copy_to_clipboard(text):
            self.notify_user(f"Copied: {text}")
        else:
            self.notify_user("Failed to copy to clipboard")
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to system clipboard."""
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Clipboard error: {e}")
            return False
    
    def notify_user(self, message: str) -> None:
        """Provide user feedback."""
        print(message)


class TriggerDetector:
    """Detects trigger events and emits signals to clipboard executor."""
    
    def __init__(self, trigger_mappings: Dict[str, str], executor: ClipboardExecutor):
        self.trigger_mappings = trigger_mappings
        self.executor = executor
        self.registered_hotkeys = set()
    
    def register_all_hotkeys(self) -> None:
        """Register all hotkeys from the trigger mappings."""
        # Clear existing hotkeys first
        self.clear_hotkeys()
        
        for hotkey in self.trigger_mappings.keys():
            try:
                keyboard.add_hotkey(hotkey, self.on_trigger_fired, args=[hotkey])
                self.registered_hotkeys.add(hotkey)
                print(f"Registered: {hotkey}")
            except ValueError as e:
                print(f"Failed to register hotkey '{hotkey}': {e}")
    
    def on_trigger_fired(self, hotkey: str) -> None:
        """Callback when a trigger is fired."""
        text = self.trigger_mappings.get(hotkey)
        if text:
            self.emit_clipboard_signal(text)
        else:
            print(f"No text found for hotkey: {hotkey}")
    
    def emit_clipboard_signal(self, text: str) -> None:
        """Emit signal to clipboard executor."""
        self.executor.execute(text)
    
    def update_mappings(self, new_mappings: Dict[str, str]) -> None:
        """Update trigger mappings and re-register hotkeys."""
        self.trigger_mappings = new_mappings
        self.register_all_hotkeys()
    
    def clear_hotkeys(self) -> None:
        """Clear all registered hotkeys."""
        for hotkey in self.registered_hotkeys:
            try:
                keyboard.remove_hotkey(hotkey)
            except:
                pass
        self.registered_hotkeys.clear()


class UIManager:
    """Handles user interface and interaction."""
    
    def __init__(self, config_manager: ConfigManager, trigger_detector: TriggerDetector):
        self.config_manager = config_manager
        self.trigger_detector = trigger_detector
    
    def show_current_mappings(self) -> None:
        """Display all current trigger-text mappings."""
        print("\n=== Current Phrases ===")
        for hotkey, text in self.trigger_detector.trigger_mappings.items():
            print(f"{hotkey}: {text}")
        print("========================\n")
    
    def prompt_add_mapping(self) -> Optional[Tuple[str, str]]:
        """Prompt user to add a new mapping."""
        try:
            hotkey = input("Enter hotkey (e.g., ctrl+shift+1): ").strip()
            if not hotkey:
                return None
                
            if not self.config_manager.validate_hotkey(hotkey):
                print("Invalid hotkey format!")
                return None
            
            text = input("Enter text: ").strip()
            if not text:
                return None
                
            return (hotkey, text)
        except KeyboardInterrupt:
            return None
    
    def handle_user_commands(self) -> None:
        """Main command loop for user interaction."""
        print("Chinese Phrase Hotkey Tool Started!")
        print("Commands: 'list', 'add', 'quit'")
        self.show_current_mappings()
        
        while True:
            try:
                cmd = input("Enter command (or press Enter to continue): ").strip().lower()
                
                if not cmd:
                    continue
                elif cmd == 'quit' or cmd == 'q':
                    break
                elif cmd == 'list' or cmd == 'l':
                    self.show_current_mappings()
                elif cmd == 'add' or cmd == 'a':
                    result = self.prompt_add_mapping()
                    if result:
                        hotkey, text = result
                        self._add_mapping(hotkey, text)
                    else:
                        print("Add operation cancelled.")
                else:
                    print("Unknown command. Available: list (l), add (a), quit (q)")
                    
            except KeyboardInterrupt:
                break
        
        print("Shutting down...")
    
    def _add_mapping(self, hotkey: str, text: str) -> None:
        """Add or update a mapping."""
        # Update the current mappings
        current_mappings = self.trigger_detector.trigger_mappings.copy()
        current_mappings[hotkey] = text
        
        # Save to config
        if self.config_manager.save_trigger_mappings(current_mappings):
            # Update trigger detector
            self.trigger_detector.update_mappings(current_mappings)
            print(f"Added/Updated: {hotkey} -> {text}")
        else:
            print("Failed to save mapping!")


class PhraseToolApp:
    """Main application class that coordinates all modules."""
    
    def __init__(self):
        # Initialize modules
        self.config_manager = ConfigManager()
        self.clipboard_executor = ClipboardExecutor()
        
        # Load initial mappings
        trigger_mappings = self.config_manager.load_trigger_mappings()
        
        # Initialize trigger detector with mappings
        self.trigger_detector = TriggerDetector(trigger_mappings, self.clipboard_executor)
        
        # Initialize UI manager
        self.ui_manager = UIManager(self.config_manager, self.trigger_detector)
    
    def run(self) -> None:
        """Start the application."""
        try:
            # Register all hotkeys
            self.trigger_detector.register_all_hotkeys()
            
            # Start UI loop
            self.ui_manager.handle_user_commands()
            
        finally:
            # Cleanup
            self.trigger_detector.clear_hotkeys()


def main():
    """Application entry point."""
    try:
        app = PhraseToolApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have installed required packages:")
        print("pip install keyboard pyperclip")
        sys.exit(1)


if __name__ == "__main__":
    main()
