import os
import re
import sys


HEADING = re.compile(r'^\s*(#{1,6}) (.*)')
SYSFILES = re.compile(r'^\..*')


def _headings(lines):
    lineno = 0

    for l in lines:
        lineno += 1
        m = HEADING.match(l)
        if not m:
            continue

        level, title = m.groups()
        yield lineno, len(level), title


def _extract(stack, filename, lines, depth=6):
    currentlevel = len(stack)

    for lineno, level, title in _headings(lines):
        if level > depth:
            continue

        # is level changed ?
        step = level - currentlevel
        if step:
            # level gap
            # ensure at least one item is exists in current container and
            # next level is not too far from current position.
            if not stack[-1] or step > 1:
                print(f'warn: {filename}:{lineno} -- level gap found: '
                      f'{level * "#"} {title}',
                      file=sys.stderr)
                continue

            if step > 0:
                # forward
                stack.append(stack[-1][-1]['children'])
                currentlevel += 1
            else:
                # backward
                while step:
                    stack.pop()
                    currentlevel -= 1
                    step += 1

        bookmark = re.sub(r'\s+', '-', re.sub(r'[:)(><]*', '', title.lower()))
        current = dict(
            title=title,
            level=level,
            children=[],
            href=f'{filename}#{bookmark}',
            bookmark=bookmark
        )
        stack[-1].append(current)


def extract(filename, lines, depth=6):
    headings = []
    stack = [headings]

    _extract(stack, filename, lines, depth)
    return headings


def extractdir(root, directory, depth=6):
    headings = []
    stack = [headings]
    subdirs = []
    root = os.path.abspath(root)

    # FIXME: prevent to traverse up
    dirpath = os.path.join(root, directory)
    for item in sorted(os.listdir(dirpath)):
        if SYSFILES.match(item):
            continue

        filepath = os.path.join(dirpath, item)
        if os.path.isdir(filepath):
            subdirs.append(item)
            continue

        if not item.endswith('.md'):
            continue

        print(f'Extractig headings from {filepath}')
        with open(filepath) as file:
            _extract(
                stack,
                os.path.relpath(filepath, root),
                file,
                depth
            )

    return headings, subdirs
