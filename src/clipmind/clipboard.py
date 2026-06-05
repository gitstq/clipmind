"""
Clipboard monitoring and history management module.
"""

import os
import json
import time
import hashlib
import platform
import subprocess
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path


class ClipboardEntry:
    """Represents a single clipboard entry."""
    
    def __init__(self, content: str, entry_type: str = "text"):
        self.content = content
        self.entry_type = entry_type
        self.timestamp = time.time()
        self.hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:12]
        self.tags = []
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "type": self.entry_type,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClipboardEntry':
        entry = cls(data["content"], data.get("type", "text"))
        entry.timestamp = data.get("timestamp", time.time())
        entry.hash = data.get("hash", "")
        entry.tags = data.get("tags", [])
        return entry


class ClipboardManager:
    """Manages clipboard history and persistence."""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.history: List[ClipboardEntry] = []
        self.config_dir = self._get_config_dir()
        self.history_file = self.config_dir / "history.json"
        self.config_file = self.config_dir / "config.json"
        self._ensure_dirs()
        self._load_history()
        
    def _get_config_dir(self) -> Path:
        """Get platform-specific config directory."""
        system = platform.system()
        if system == "Windows":
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
        elif system == "Darwin":  # macOS
            base = Path.home() / "Library/Application Support"
        else:  # Linux and others
            base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        return base / "clipmind"
    
    def _ensure_dirs(self):
        """Ensure configuration directories exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_history(self):
        """Load history from disk."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = [ClipboardEntry.from_dict(e) for e in data]
            except (json.JSONDecodeError, KeyError):
                self.history = []
    
    def save_history(self):
        """Save history to disk."""
        data = [e.to_dict() for e in self.history]
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _detect_type(self, content: str) -> str:
        """Detect content type."""
        content = content.strip()
        
        # Check for URL
        if content.startswith(('http://', 'https://', 'ftp://')):
            return "url"
        
        # Check for file path
        if content.startswith(('/', './', '../', '~')) or (len(content) > 2 and content[1] == ':'):
            if os.path.exists(os.path.expanduser(content)):
                return "path"
        
        # Check for code (contains common code patterns)
        code_indicators = ['def ', 'class ', 'import ', 'from ', 'function', 'const ', 'let ', 'var ', '<?php', '#!/']
        if any(indicator in content for indicator in code_indicators):
            return "code"
        
        # Check for JSON
        if content.startswith('{') and content.endswith('}'):
            try:
                json.loads(content)
                return "json"
            except:
                pass
        
        # Check for email
        if '@' in content and '.' in content.split('@')[-1]:
            return "email"
        
        return "text"
    
    def add(self, content: str) -> bool:
        """Add content to history. Returns True if added, False if duplicate."""
        if not content or not content.strip():
            return False
            
        content = content.strip()
        
        # Check for duplicates (most recent 50 entries)
        for entry in self.history[:50]:
            if entry.content == content:
                # Move to top
                self.history.remove(entry)
                entry.timestamp = time.time()
                self.history.insert(0, entry)
                self.save_history()
                return False
        
        entry_type = self._detect_type(content)
        entry = ClipboardEntry(content, entry_type)
        self.history.insert(0, entry)
        
        # Trim to max_history
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
        
        self.save_history()
        return True
    
    def get_history(self, entry_type: Optional[str] = None, limit: int = 50) -> List[ClipboardEntry]:
        """Get history entries, optionally filtered by type."""
        entries = self.history
        if entry_type:
            entries = [e for e in entries if e.entry_type == entry_type]
        return entries[:limit]
    
    def search(self, query: str) -> List[ClipboardEntry]:
        """Search history with fuzzy matching."""
        query = query.lower()
        results = []
        
        for entry in self.history:
            score = 0
            content_lower = entry.content.lower()
            
            # Exact match gets highest score
            if query == content_lower:
                score = 1000
            # Contains query
            elif query in content_lower:
                score = 500
            # Word match
            elif any(query == word for word in content_lower.split()):
                score = 300
            # Character match (fuzzy)
            else:
                # Simple fuzzy scoring
                query_chars = list(query)
                content_chars = list(content_lower)
                matches = 0
                ci = 0
                for qc in query_chars:
                    while ci < len(content_chars) and content_chars[ci] != qc:
                        ci += 1
                    if ci < len(content_chars):
                        matches += 1
                        ci += 1
                if matches == len(query_chars):
                    score = 100 + matches
            
            if score > 0:
                results.append((score, entry))
        
        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in results]
    
    def delete(self, index: int) -> bool:
        """Delete entry by index."""
        if 0 <= index < len(self.history):
            self.history.pop(index)
            self.save_history()
            return True
        return False
    
    def clear(self):
        """Clear all history."""
        self.history = []
        self.save_history()
    
    def get_stats(self) -> Dict[str, int]:
        """Get usage statistics."""
        stats = {"total": len(self.history)}
        for entry in self.history:
            stats[entry.entry_type] = stats.get(entry.entry_type, 0) + 1
        return stats


class SystemClipboard:
    """Interface to system clipboard."""
    
    @staticmethod
    def get() -> str:
        """Get content from system clipboard."""
        system = platform.system()
        try:
            if system == "Windows":
                result = subprocess.run(
                    ["powershell", "-command", "Get-Clipboard"],
                    capture_output=True, text=True, timeout=5
                )
                return result.stdout
            elif system == "Darwin":  # macOS
                result = subprocess.run(
                    ["pbpaste"],
                    capture_output=True, text=True, timeout=5
                )
                return result.stdout
            else:  # Linux
                # Try wl-copy first (Wayland), then xclip (X11)
                for cmd in [["wl-paste"], ["xclip", "-selection", "clipboard", "-o"]]:
                    try:
                        result = subprocess.run(
                            cmd,
                            capture_output=True, text=True, timeout=5
                        )
                        if result.returncode == 0:
                            return result.stdout
                    except FileNotFoundError:
                        continue
                return ""
        except Exception:
            return ""
    
    @staticmethod
    def set(content: str) -> bool:
        """Set content to system clipboard."""
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.run(
                    ["powershell", "-command", f"Set-Clipboard -Value '{content}'"],
                    capture_output=True, timeout=5
                )
                return True
            elif system == "Darwin":  # macOS
                proc = subprocess.Popen(
                    ["pbcopy"],
                    stdin=subprocess.PIPE,
                    text=True
                )
                proc.communicate(input=content, timeout=5)
                return True
            else:  # Linux
                for cmd in [["wl-copy"], ["xclip", "-selection", "clipboard"]]:
                    try:
                        proc = subprocess.Popen(
                            cmd,
                            stdin=subprocess.PIPE,
                            capture_output=True,
                            text=True
                        )
                        proc.communicate(input=content, timeout=5)
                        if proc.returncode == 0:
                            return True
                    except FileNotFoundError:
                        continue
                return False
        except Exception:
            return False
