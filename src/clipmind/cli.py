"""
Command-line interface for ClipMind.
"""

import sys
import argparse
from .clipboard import ClipboardManager, SystemClipboard
from .tui import launch_tui


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="clipmind",
        description="🧠 ClipMind - Intelligent Terminal Clipboard History Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  clipmind              Launch interactive TUI
  clipmind --add "text" Add text to history
  clipmind --list       List recent entries
  clipmind --search q   Search history
  clipmind --stats      Show usage statistics
  clipmind --clear      Clear all history
  clipmind --monitor    Monitor clipboard in background
        """
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    parser.add_argument(
        "--add", "-a",
        metavar="TEXT",
        help="Add text to clipboard history"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List recent clipboard entries"
    )
    
    parser.add_argument(
        "--search", "-s",
        metavar="QUERY",
        help="Search clipboard history"
    )
    
    parser.add_argument(
        "--type", "-t",
        metavar="TYPE",
        choices=["text", "code", "url", "path", "json", "email"],
        help="Filter by type (text, code, url, path, json, email)"
    )
    
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=20,
        help="Limit number of results (default: 20)"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show usage statistics"
    )
    
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear all clipboard history"
    )
    
    parser.add_argument(
        "--copy", "-c",
        type=int,
        metavar="INDEX",
        help="Copy entry by index to clipboard"
    )
    
    parser.add_argument(
        "--delete", "-d",
        type=int,
        metavar="INDEX",
        help="Delete entry by index"
    )
    
    parser.add_argument(
        "--monitor", "-m",
        action="store_true",
        help="Monitor clipboard changes in background"
    )
    
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Monitor interval in seconds (default: 1.0)"
    )
    
    return parser


def format_entry(index: int, entry, max_width: int = 80) -> str:
    """Format a single entry for display."""
    type_icons = {
        "text": "📄", "code": "💻", "url": "🔗",
        "path": "📁", "json": "📋", "email": "📧"
    }
    
    icon = type_icons.get(entry.entry_type, "📄")
    content = entry.content.replace('\n', '↵')
    
    # Truncate if needed
    max_content = max_width - 20
    if len(content) > max_content:
        content = content[:max_content-3] + "..."
    
    from datetime import datetime
    time_str = datetime.fromtimestamp(entry.timestamp).strftime("%H:%M:%S")
    
    return f"  {index:3d} {icon} {content:<{max_content}} {time_str}"


def handle_list(manager: ClipboardManager, args):
    """Handle --list command."""
    entries = manager.get_history(entry_type=args.type, limit=args.limit)
    
    if not entries:
        print("📭 剪贴板历史为空")
        return
    
    print(f"\n🧠 ClipMind - 最近 {len(entries)} 条记录\n")
    print(f"  {'序号':<5} {'类型':<4} {'内容':<50} {'时间':<10}")
    print("  " + "-" * 75)
    
    for i, entry in enumerate(entries):
        print(format_entry(i, entry))
    
    print()


def handle_search(manager: ClipboardManager, args):
    """Handle --search command."""
    results = manager.search(args.search)
    
    if not results:
        print(f"🔍 未找到匹配 '{args.search}' 的内容")
        return
    
    print(f"\n🔍 搜索 '{args.search}' - 找到 {len(results)} 条结果\n")
    
    for i, entry in enumerate(results[:args.limit]):
        print(format_entry(i, entry))
    
    print()


def handle_stats(manager: ClipboardManager):
    """Handle --stats command."""
    stats = manager.get_stats()
    
    print("\n📊 ClipMind 使用统计\n")
    print(f"  总记录数: {stats.get('total', 0)}")
    print()
    
    type_names = {
        "text": "文本", "code": "代码", "url": "链接",
        "path": "路径", "json": "JSON", "email": "邮箱"
    }
    
    print("  类型分布:")
    for type_key, count in sorted(stats.items()):
        if type_key != "total":
            name = type_names.get(type_key, type_key)
            bar = "█" * (count * 20 // stats["total"])
            print(f"    {name:<6} {bar:<20} {count}")
    
    print()


def handle_monitor(manager: ClipboardManager, args):
    """Handle --monitor command."""
    import time
    
    print("👁️  开始监控剪贴板变化...")
    print("按 Ctrl+C 停止\n")
    
    last_content = ""
    try:
        while True:
            content = SystemClipboard.get()
            if content and content != last_content:
                if manager.add(content):
                    entry_type = manager._detect_type(content)
                    type_names = {
                        "text": "文本", "code": "代码", "url": "链接",
                        "path": "路径", "json": "JSON", "email": "邮箱"
                    }
                    print(f"✅ 捕获 [{type_names.get(entry_type, entry_type)}]: {content[:60]}...")
                last_content = content
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n👋 监控已停止")


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    manager = ClipboardManager()
    
    # Handle commands
    if args.clear:
        manager.clear()
        print("🧹 已清空所有历史记录")
        return
    
    if args.add:
        if manager.add(args.add):
            print("✅ 已添加到历史记录")
        else:
            print("ℹ️ 内容已存在，已更新到顶部")
        return
    
    if args.search:
        handle_search(manager, args)
        return
    
    if args.stats:
        handle_stats(manager)
        return
    
    if args.copy is not None:
        entries = manager.get_history()
        if 0 <= args.copy < len(entries):
            if SystemClipboard.set(entries[args.copy].content):
                print("✅ 已复制到剪贴板")
            else:
                print("❌ 复制失败")
        else:
            print(f"❌ 索引 {args.copy} 超出范围")
        return
    
    if args.delete is not None:
        if manager.delete(args.delete):
            print("🗑️ 已删除")
        else:
            print(f"❌ 索引 {args.delete} 超出范围")
        return
    
    if args.monitor:
        handle_monitor(manager, args)
        return
    
    if args.list:
        handle_list(manager, args)
        return
    
    # Default: launch TUI
    launch_tui(manager)


if __name__ == "__main__":
    main()
