"""
file taken from https://github.com/stoneyrh/xscripts/blob/master/diff2html.py and modified
Script for convert unified diff text into html
"""

import re
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

separator = "*" * 3


def handleBlock(block):
    """
    Turn a block of lines into a list like this
    - Line 1
    + Line 2
           -> [("Line 1", "Line 2")]
    - Line 1
    - Line 2
           -> [("Line 1", ""), ("Line 2", "")]
    + Line 1
    + Line 2
           -> [("Line 1", ""), ("Line 2", "")]
    - Line 1
    + Line 2
    + Line 3
           -> [("Line 1", "Line 2"), ("", "Line 3")]
    - Line 1
    - Line 2
    + Line 3
           -> [("Line 1", "Line 3"), ("Line 2", "")]
    """
    mlines = list(filter(lambda line: line.startswith("-"), block))
    plines = list(filter(lambda line: line.startswith("+"), block))
    mcount = len(mlines)
    pcount = len(plines)
    if mcount > pcount:
        plines.extend([""] * (mcount - pcount))
    elif pcount > mcount:
        mlines.extend([""] * (pcount - mcount))
    count = max(mcount, pcount)
    return [(mlines[i], plines[i]) for i in range(count)]


def adjust(lines):
    newLines = []
    for line in lines:
        if not line.startswith("\\ No newline at end of file"):
            newLines.append(line)
    return newLines


def makeBlocks(diff):
    blocks = []
    if len(diff) <= 0:
        return
    pattern = re.compile("(\d+)")
    lines = diff.split("\n")
    lines = adjust(lines)
    num = 0
    total = len(lines)
    while num < total:
        line = lines[num]
        if (
            line.startswith("---")
            or line.startswith("+++")
            or line.startswith("===")
            or line.lower().startswith("index")
            or line.lower().startswith("diff")
        ):
            num = num + 1
            continue
        if line.startswith("@@"):
            # Retrieve the line number
            numbers = pattern.findall(line)
            if len(numbers) != 4:
                # TODO: Wrong numbers?
                pass
            numbers = list(map(lambda n: int(n), numbers))
            leftLine = numbers[0]
            rightLine = numbers[2]
            num = num + 1
            if len(blocks) > 0:
                blocks.append((separator, separator, separator, separator))
            while num < total:
                line = lines[num]
                # Leave this line to outside loop
                if (
                    line.startswith("@@")
                    or line.lower().startswith("index")
                    or line.startswith("diff")
                ):
                    break
                # The lines after this line will make a block
                if line.startswith("-") or line.startswith("+"):
                    # Find the next line not start with '-' or '+'
                    block = [line]
                    num = num + 1
                    while num < total:
                        line = lines[num]
                        if line.startswith("-") or line.startswith("+"):
                            block.append(line)
                            num = num + 1
                        else:
                            # When breaking out, line save the current line
                            # This line should be appended to blocks
                            break
                    block = handleBlock(block)
                    for left, right in block:
                        if left and right:
                            blocks.append((str(leftLine), left, str(rightLine), right))
                            leftLine = leftLine + 1
                            rightLine = rightLine + 1
                        elif left:
                            blocks.append((str(leftLine), left, "", right))
                            leftLine = leftLine + 1
                        else:
                            blocks.append(("", left, str(rightLine), right))
                            rightLine = rightLine + 1
                # end if
                if num < total:
                    blocks.append((str(leftLine), line, str(rightLine), line))
                    leftLine = leftLine + 1
                    rightLine = rightLine + 1
                    num = num + 1
        else:  # line.startswith('@@')
            num = num + 1
    return blocks


bg_table = "white"
table = (
    '<table style="width:98%%;border-spacing:1px;text-align=left;background:'
    + bg_table
    + '#eeeeee;padding:0;margin:0;border:1px;cellspacing:0;">\n%s\n</table>'
)
row = '<tr><td style="width:2%%;font-size:12px;font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;color:grey;text-align:center;">%s</td><td class="highlight" style="width:48%%;background:%s;">%s</td><td style="width:2%%;font-size:12px;font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;color:grey;text-align:center;">%s</td><td class="highlight" style="width:48%%;background:%s;">%s</td></tr>'
empty_row = '<tr style="background:purple;"><td style="text-align:center;"><hr/></td><td style="text-align:center;"><hr/></td><td style="text-align:center;"><hr/></td><td style="text-align:center;"><hr/></td></tr>'

color_nor = "black"
color_mod = "black"
color_add = "black"
color_del = "black"
bg_mod = "#ffdea2"
bg_add = "#bef5cb"
bg_del = "#ffdce0"


def text2html(filename, plain):
    try:
        lexer = get_lexer_for_filename(filename)
    except:
        lexer = get_lexer_for_filename("default.txt")
    formatter = HtmlFormatter(nowrap=True)
    return highlight(plain, lexer, formatter)


def makeHTML(blocks, filename):
    # blocks is None
    if not blocks:
        return
    rows = []
    for block in blocks:
        # TODO: Encode block data
        leftLine, left, rightLine, right = block
        if leftLine.startswith(separator):
            rows.append(empty_row)
            continue
        color_left = color_right = color_nor
        bg_left = bg_right = bg_table
        if left.startswith("-"):
            if right.startswith("+"):
                color_left = color_mod
                color_right = color_add
                bg_left = bg_del
                bg_right = bg_add
            else:
                color_left = color_mod
                color_right = color_del
                bg_left = bg_mod
                bg_right = bg_del
        else:
            if right.startswith("+"):
                color_right = color_add
                bg_right = bg_add
                bg_left = bg_mod
        # Remove the first -/+
        if left.startswith("-"):
            left = left[1:]
        if right.startswith("+"):
            right = right[1:]
        rows.append(
            row
            % (
                leftLine,
                bg_left,
                text2html(filename, left),
                rightLine,
                bg_right,
                text2html(filename, right),
            )
        )
    return table % "\n\t".join(rows)


def diff2html(diff, filename):
    blocks = makeBlocks(diff)
    html = makeHTML(blocks, filename)
    return html
