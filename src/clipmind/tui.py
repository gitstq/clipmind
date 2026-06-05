"""
Terminal User Interface for ClipMind using only standard library.
"""

import os
import sys
import shutil
import signal
from typing import List, Optional, Callable
from .clipboard import ClipboardManager, ClipboardEntry


class Colors:
    """ANSI color codes."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class Terminal:
    """Terminal control utilities."""
    
    @staticmethod
    def clear():
        """Clear the terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    @staticmethod
    def get_size() -> tuple:
        """Get terminal size (columns, rows)."""
        return shutil.get_terminal_size()
    
    @staticmethod
    def hide_cursor():
        """Hide terminal cursor."""
        print("\033[?25l", end="", flush=True)
    
    @staticmethod
    def show_cursor():
        """Show terminal cursor."""
        print("\033[?25h", end="", flush=True)
    
    @staticmethod
    def move_cursor(row: int, col: int):
        """Move cursor to position."""
        print(f"\033[{row};{col}H", end="", flush=True)
    
    @staticmethod
    def clear_line():
        """Clear current line."""
        print("\033[2K\r", end="", flush=True)


class ClipMindTUI:
    """Terminal User Interface for ClipMind."""
    
    TYPE_ICONS = {
        "text": "📄",
        "code": "💻",
        "url": "🔗",
        "path": "📁",
        "json": "📋",
        "email": "📧",
    }
    
    TYPE_COLORS = {
        "text": Colors.WHITE,
        "code": Colors.BRIGHT_CYAN,
        "url": Colors.BRIGHT_BLUE,
        "path": Colors.BRIGHT_YELLOW,
        "json": Colors.BRIGHT_GREEN,
        "email": Colors.BRIGHT_MAGENTA,
    }
    
    def __init__(self, manager: ClipboardManager):
        self.manager = manager
        self.entries: List[ClipboardEntry] = []
        self.selected = 0
        self.scroll_offset = 0
        self.search_query = ""
        self.mode = "list"  # list, search, preview
        self.running = True
        self.message = ""
        self.message_timeout = 0
        
    def _get_icon(self, entry_type: str) -> str:
        return self.TYPE_ICONS.get(entry_type, "📄")
    
    def _get_color(self, entry_type: str) -> str:
        return self.TYPE_COLORS.get(entry_type, Colors.WHITE)
    
    def _format_time(self, timestamp: float) -> str:
        from datetime import datetime
        dt = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        diff = now - dt
        
        if diff.days == 0:
            if diff.seconds < 60:
                return "刚刚"
            elif diff.seconds < 3600:
                return f"{diff.seconds // 60}分钟前"
            else:
                return f"{diff.seconds // 3600}小时前"
        elif diff.days == 1:
            return "昨天"
        elif diff.days < 7:
            return f"{diff.days}天前"
        else:
            return dt.strftime("%m-%d")
    
    def _truncate(self, text: str, max_len: int) -> str:
        """Truncate text to fit within max_len."""
        if len(text) <= max_len:
            return text
        return text[:max_len-3] + "..."
    
    def _draw_header(self, cols: int):
        """Draw the header bar."""
        title = "🧠 ClipMind - 智能剪贴板管理器"
        subtitle = f" [{len(self.entries)} 项]"
        
        header_text = title + subtitle
        padding = cols - len(header_text) - 2
        
        print(f"{Colors.BG_BLUE}{Colors.BRIGHT_WHITE}{Colors.BOLD} {header_text}{' ' * padding}{Colors.RESET}")
    
    def _draw_search_bar(self, cols: int):
        """Draw search bar."""
        if self.mode == "search":
            search_text = f" 搜索: {self.search_query}_"
        else:
            search_text = " 按 / 搜索 | ↑↓ 选择 | Enter 复制 | d 删除 | q 退出"
        
        padding = max(0, cols - len(search_text) - 2)
        print(f"{Colors.BG_BLACK}{Colors.BRIGHT_BLACK}{search_text}{' ' * padding}{Colors.RESET}")
    
    def _draw_entries(self, cols: int, rows: int):
        """Draw clipboard entries."""
        content_rows = rows - 4  # Header + search + status + padding
        
        if not self.entries:
            empty_msg = "📭 剪贴板历史为空"
            padding = (cols - len(empty_msg)) // 2
            print(f"\n{' ' * padding}{Colors.DIM}{empty_msg}{Colors.RESET}")
            return
        
        # Adjust scroll offset
        if self.selected < self.scroll_offset:
            self.scroll_offset = self.selected
        elif self.selected >= self.scroll_offset + content_rows:
            self.scroll_offset = self.selected - content_rows + 1
        
        visible_entries = self.entries[self.scroll_offset:self.scroll_offset + content_rows]
        
        for i, entry in enumerate(visible_entries):
            actual_idx = self.scroll_offset + i
            is_selected = actual_idx == self.selected
            
            # Format line
            icon = self._get_icon(entry.entry_type)
            color = self._get_color(entry.entry_type)
            time_str = self._format_time(entry.timestamp)
            
            # Calculate available width for content
            time_width = 10
            prefix_width = 6  # icon + spaces
            suffix_width = time_width + 4  # time + padding
            content_width = cols - prefix_width - suffix_width - 2
            
            content = self._truncate(entry.content.replace('\n', '↵'), content_width)
            
            if is_selected:
                line = f"{Colors.BG_BLUE}{Colors.BRIGHT_WHITE} ❯ {icon} {content}{' ' * (content_width - len(content))} {time_str} {Colors.RESET}"
            else:
                line = f"   {icon} {color}{content}{Colors.RESET}{' ' * (content_width - len(content))} {Colors.DIM}{time_str}{Colors.RESET}"
            
            print(line)
        
        # Fill remaining space
        for _ in range(content_rows - len(visible_entries)):
            print()
    
    def _draw_status(self, cols: int):
        """Draw status bar."""
        if self.message and time.time() < self.message_timeout:
            status = f" {self.message}"
            color = Colors.BRIGHT_GREEN
        else:
            if self.entries and self.selected < len(self.entries):
                entry = self.entries[self.selected]
                type_label = {
                    "text": "文本", "code": "代码", "url": "链接",
                    "path": "路径", "json": "JSON", "email": "邮箱"
                }.get(entry.entry_type, entry.entry_type)
                status = f" [{type_label}] {len(entry.content)} 字符"
            else:
                status = " 就绪"
            color = Colors.BRIGHT_BLACK
        
        padding = max(0, cols - len(status) - 2)
        print(f"{Colors.BG_BLACK}{color}{status}{' ' * padding}{Colors.RESET}")
    
    def draw(self):
        """Redraw the entire UI."""
        Terminal.clear()
        cols, rows = Terminal.get_size()
        
        self._draw_header(cols)
        self._draw_search_bar(cols)
        print()
        self._draw_entries(cols, rows)
        self._draw_status(cols)
    
    def show_message(self, msg: str, duration: float = 2.0):
        """Show a temporary message."""
        self.message = msg
        self.message_timeout = time.time() + duration
    
    def handle_input(self) -> bool:
        """Handle user input. Returns False to quit."""
        try:
            import tty
            import termios
            
            # Save terminal settings
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
            
            char = sys.stdin.read(1)
            
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            
        except (ImportError, AttributeError):
            # Windows fallback
            import msvcrt
            char = msvcrt.getch().decode('utf-8', errors='ignore')
        
        if char == '\x03' or char == 'q':  # Ctrl+C or q
            return False
        
        elif char == 'j' or char == '\x1b[B':  # Down arrow
            if self.selected < len(self.entries) - 1:
                self.selected += 1
        
        elif char == 'k' or char == '\x1b[A':  # Up arrow
            if self.selected > 0:
                self.selected -= 1
        
        elif char == 'g':  # Go to top
            self.selected = 0
        
        elif char == 'G':  # Go to bottom
            self.selected = max(0, len(self.entries) - 1)
        
        elif char == '\r' or char == '\n':  # Enter - copy to clipboard
            if self.entries and self.selected < len(self.entries):
                entry = self.entries[self.selected]
                from .clipboard import SystemClipboard
                if SystemClipboard.set(entry.content):
                    self.show_message(f"✅ 已复制到剪贴板!")
                else:
                    self.show_message("❌ 复制失败")
        
        elif char == 'd':  # Delete entry
            if self.entries and self.selected < len(self.entries):
                if self.manager.delete(self.selected):
                    self.entries = self.manager.get_history()
                    if self.selected >= len(self.entries):
                        self.selected = max(0, len(self.entries) - 1)
                    self.show_message("🗑️ 已删除")
        
        elif char == '/':  # Search mode
            self.mode = "search"
            self.search_query = ""
            self._handle_search()
            self.mode = "list"
        
        elif char == 'c':  # Clear all
            self.manager.clear()
            self.entries = []
            self.selected = 0
            self.show_message("🧹 已清空历史")
        
        elif char == '\x12':  # Ctrl+R - refresh
            self.entries = self.manager.get_history()
            self.show_message("🔄 已刷新")
        
        return True
    
    def _handle_search(self):
        """Handle search input."""
        while True:
            self.draw()
            
            try:
                import tty
                import termios
                old_settings = termios.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin.fileno())
                char = sys.stdin.read(1)
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except:
                break
            
            if char == '\x1b':  # Escape - cancel search
                self.search_query = ""
                self.entries = self.manager.get_history()
                break
            
            elif char == '\r' or char == '\n':  # Enter - confirm search
                break
            
            elif char == '\x7f':  # Backspace
                self.search_query = self.search_query[:-1]
                if self.search_query:
                    self.entries = self.manager.search(self.search_query)
                else:
                    self.entries = self.manager.get_history()
            
            elif char.isprintable():
                self.search_query += char
                self.entries = self.manager.search(self.search_query)
                self.selected = 0
    
    def run(self):
        """Run the TUI main loop."""
        self.entries = self.manager.get_history()
        
        # Setup signal handler for clean exit
        def signal_handler(sig, frame):
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        
        Terminal.hide_cursor()
        
        try:
            while self.running:
                self.draw()
                if not self.handle_input():
                    break
        finally:
            Terminal.show_cursor()
            Terminal.clear()
            print("👋 感谢使用 ClipMind!")


def launch_tui(manager: ClipboardManager):
    """Launch the TUI interface."""
    tui = ClipMindTUI(manager)
    tui.run()
