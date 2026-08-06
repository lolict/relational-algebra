#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地文档关系代数处理 CLI
用法:
    python local_cli.py scan <目录>           # 扫描文档
    python local_cli.py filter <目录> --min-freq 3  # 筛选高频词
    python local_cli.py watch <目录>           # 监控变化
    python local_cli.py export <目录> --format md  # 导出报告
"""

import sys
import os
import argparse
import json
from pathlib import Path

# 引入本地处理器
from . import 局部文件系统关系代数处理器


def cmd_scan(args):
    """扫描目录，输出词频统计"""
    print(f"[扫描] 目录: {args.directory}")
    print(f"[扫描] 最低频次阈值: {args.min_freq}")

    处理器 = 局部文件系统关系代数处理器(args.directory)
    处理器.扫描()

    词种数 = 处理器.词种数()
    总频次 = 处理器.总频次()
    文档数 = 处理器.文档数()

    print(f"\n[结果]")
    print(f"  文档数: {文档数}")
    print(f"  词种数: {词种数}")
    print(f"  总频次: {总频次}")

    # 过滤高频词
    高频词表 = 处理器.漏斗(最小频次=args.min_freq)
    print(f"\n[高频词] (频次 >= {args.min_freq})")
    for 词, 频次 in sorted(高频词表.items(), key=lambda x: -x[1])[:20]:
        print(f"  {词}: {频次}")

    return 0


def cmd_filter(args):
    """按条件筛选文档"""
    print(f"[筛选] 目录: {args.directory}")
    print(f"[筛选] 最低频次: {args.min_freq}")

    处理器 = 局部文件系统关系代数处理器(args.directory)
    处理器.扫描()

    高频词表 = 处理器.漏斗(最小频次=args.min_freq)
    # 筛选包含高频词的文档
    匹配文档 = {}
    for 节点 in 处理器.文件列表:
        命中词 = [词 for 词 in 高频词表 if 词 in 节点.内容]
        if 命中词:
            匹配文档[节点.路径] = 命中词

    print(f"\n[结果] 匹配文档: {len(匹配文档)}")
    for 路径, 词 in list(匹配文档.items())[:10]:
        print(f"  {路径}")
        print(f"    命中词: {', '.join(词[:5])}{'...' if len(词) > 5 else ''}")

    return 0


def cmd_watch(args):
    """监控目录变化"""
    import time

    print(f"[监控] 目录: {args.directory}")
    print(f"[监控] 间隔: {args.interval} 秒")
    print("[监控] 按 Ctrl+C 停止")

    处理器 = 局部文件系统关系代数处理器(args.directory)
    处理器.扫描()

    上次词种 = set()
    try:
        while True:
            处理器.扫描()
            当前词种 = set(处理器.词频表.keys())

            新增 = 当前词种 - 上次词种
            删除 = 上次词种 - 当前词种

            if 新增 or 删除:
                print(f"\n[{时间戳()}] 变化检测")
                if 新增:
                    print(f"  新增词: {', '.join(list(新增)[:5])}{'...' if len(新增) > 5 else ''}")
                if 删除:
                    print(f"  删除词: {', '.join(list(删除)[:5])}{'...' if len(删除) > 5 else ''}")
                print(f"  当前: {处理器.词种数()} 词种 / {处理器.文档数()} 文档")

            上次词种 = 当前词种
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[监控] 已停止")
        return 0

    return 0


def cmd_export(args):
    """导出统计报告"""
    print(f"[导出] 目录: {args.directory}")
    print(f"[导出] 格式: {args.format}")

    处理器 = 局部文件系统关系代数处理器(args.directory)
    处理器.扫描()

    报告 = {
        '扫描时间': 时间戳(),
        '目录': args.directory,
        '文档数': 处理器.文档数(),
        '词种数': 处理器.词种数(),
        '总频次': 处理器.总频次(),
        '高频词': dict(sorted(处理器.漏斗(最小频次=3).items(), key=lambda x: -x[1])[:50]),
    }

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(报告, f, ensure_ascii=False, indent=2)
        print(f"[导出] 已保存: {args.output}")
    else:
        print(json.dumps(报告, ensure_ascii=False, indent=2))

    return 0


def 时间戳():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    parser = argparse.ArgumentParser(
        description='本地文档关系代数处理 CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s scan ./文档
  %(prog)s scan ./文档 --min-freq 5
  %(prog)s filter ./文档 --min-freq 3
  %(prog)s watch ./文档 --interval 30
  %(prog)s export ./文档 --format md --output report.json
        """
    )

    sub = parser.add_subparsers(dest='command', help='子命令')

    # scan
    p_scan = sub.add_parser('scan', help='扫描目录，输出词频统计')
    p_scan.add_argument('directory', help='要扫描的目录路径')
    p_scan.add_argument('--min-freq', type=int, default=1, help='最低频次阈值 (默认: 1)')

    # filter
    p_filter = sub.add_parser('filter', help='按条件筛选文档')
    p_filter.add_argument('directory', help='要筛选的目录路径')
    p_filter.add_argument('--min-freq', type=int, default=3, help='最低频次阈值 (默认: 3)')

    # watch
    p_watch = sub.add_parser('watch', help='监控目录变化')
    p_watch.add_argument('directory', help='要监控的目录路径')
    p_watch.add_argument('--interval', type=int, default=60, help='检查间隔(秒) (默认: 60)')

    # export
    p_export = sub.add_parser('export', help='导出统计报告')
    p_export.add_argument('directory', help='要导出的目录路径')
    p_export.add_argument('--format', choices=['json', 'md', 'csv'], default='json', help='输出格式')
    p_export.add_argument('--output', help='输出文件路径 (默认: stdout)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        'scan': cmd_scan,
        'filter': cmd_filter,
        'watch': cmd_watch,
        'export': cmd_export,
    }

    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())
