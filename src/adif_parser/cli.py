import argparse
import json
import sys
from .parser import parse_adif, detect_variant


def cmd_parse(args):
    path = args.file
    with open(path, 'r', encoding=args.encoding or 'utf-8', errors='replace') as f:
        text = f.read()
    header, records = parse_adif(text)
    variant = detect_variant(text, header)
    out = {
        'variant': variant,
        'header': header,
        'records': records,
    }
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as fo:
            json.dump(out, fo, indent=2, ensure_ascii=False)
    else:
        json.dump(out, sys.stdout, indent=2, ensure_ascii=False)


def main(argv=None):
    p = argparse.ArgumentParser(description='ADIF 解析与变体检测')
    sub = p.add_subparsers(dest='cmd')
    ps = sub.add_parser('parse', help='解析 ADIF 文件')
    ps.add_argument('file', help='ADIF 文件路径')
    ps.add_argument('-o', '--output', help='输出 JSON 文件路径（默认为 stdout）')
    ps.add_argument('--encoding', help='文件编码，默认 utf-8')
    ps.set_defaults(func=cmd_parse)

    ns = p.parse_args(argv)
    if not hasattr(ns, 'func'):
        p.print_help()
        return 1
    ns.func(ns)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
