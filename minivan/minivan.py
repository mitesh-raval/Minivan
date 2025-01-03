#!/usr/bin/env python3

import argparse


def remove_block_comments(inList):
    """
    remove_block_comments(inList):
        * removes all lines making up multiline comments
        * puts extra space before '+' symbol if the line starts with '+'
        * preserves loud comments
    """
    curatedList = []
    dropLines = False
    loudComment = False

    for line in inList:
        if loudComment:
            curatedList.append(line + "\n")
            if line.endswith("*/"):
                loudComment = False
            continue

        if dropLines:
            if not line.endswith("*/"):
                continue
            else:
                dropLines = False
                continue
        if line.startswith("+"):
            line = "".join([" ", line])
        if line.startswith("/*!"):
            curatedList.append(line + "\n")
            if not line.endswith("*/"):
                loudComment = True
        elif line.startswith("/*") and line.endswith("*/") or line.startswith("//"):
            continue
        elif line.startswith("/*") and not line.endswith("*/"):
            dropLines = True
        else:
            curatedList.append(line)

    return curatedList


def minify_line(line, matching_char, within_comment, loud_comment):
    """
    Process a line character-wise and update flags or var as necessary to
    handle multi-line scenarios
        * removes all inline comments except those within quoted or format strings
        * fixes one line else statements without curly braces to have an extra space.
    e.g. some code // comment     ==>  some code
         some code /* comment */  ==>  some code
         "some string /* not a comment */ " ==> preserved as is
         else
            statement;      ==>  else statement;
    """
    chars = tuple(line)
    num_chars = len(chars)
    curated_chars = []
    start_comment = False
    end_comment = False

    for i in range(num_chars):
        c = chars[i]
        if matching_char is not None:
            if c != matching_char:
                curated_chars.append(c)
            else:
                matching_char = None
                curated_chars.append(c)
            # no further processing required
            continue

        # preserve loud comment whether it is start or end or within
        if loud_comment:
            curated_chars.append(c)

        if start_comment:
            # because '/*' is a 2 char sequence
            # match case below will activate start_comment
            # flag after a lookahead, yet the for loop is 1 char behind
            within_comment = True
            start_comment = False
            continue

        if end_comment:
            # skip the next char '/', similar to start_comment
            # processing, need to discard two char sequence '*/'
            end_comment = False
            loud_comment = False
            continue

        if within_comment:
            next_index = i + 1
            if next_index < num_chars:
                if c == "*" and chars[next_index] == "/":
                    within_comment = False
                    end_comment = True
                # skip c whether inside or at the end of a comment
                continue
            else:
                # just processed last char, so break is fine
                break

        match c:
            case "'":
                matching_char = "'"
                curated_chars.append(c)
            case '"':
                matching_char = '"'
                curated_chars.append(c)
            case "`":
                matching_char = "`"
                curated_chars.append(c)
            case "/":
                next_index = i + 1
                if next_index < num_chars:
                    next_char = chars[next_index]
                    if next_char == "/":
                        # single line comment, skip the rest of the line
                        break
                    elif next_char == "*":
                        next_index = i + 2
                        if next_index < num_chars:
                            next_char = chars[next_index]
                            if next_char == "!":
                                # start of loud comment
                                loud_comment = True
                                # preserve loud comment
                                curated_chars.append(c)
                        # within a comment
                        start_comment = True
                        continue
                # just a division operator or / at the end of a loud comment
                curated_chars.append(c)
            case _:
                curated_chars.append(c)

    curated_line = "".join(curated_chars)

    """
    Account for one line else statements that do not have curly braces
    by adding an extra space after spaces were stripped in a previous step
    """
    if "else" == curated_line:
        curated_line = "".join([curated_line, " "])

    # print(f"curated_line : {curated_line}, {within_comment} {matching_char}")
    return curated_line, matching_char, within_comment, loud_comment


def smart_strip(input_line):
    # removes '\' used in multi-line quoted strings
    return input_line.strip().strip("\\")


def remove_inline_comments(lines_list):
    curated_list = []
    # skip_flag = False
    find_char = None
    within_comment = False
    loud_comment = False
    for line in lines_list:
        clean_line, find_char, within_comment, loud_comment = minify_line(
            line, find_char, within_comment, loud_comment
        )
        curated_list.append(clean_line)

    return curated_list


def minify(args):

    parser = argparse.ArgumentParser(description="Minify .js or .css files")
    parser.add_argument("source", help="(Relative) Path to source file e.g. script.js")
    parser.add_argument(
        "dest",
        help="(Relative) new location/file name \
        e.g. script.min.js.",
    )
    args = parser.parse_args(args)
    src = args.source
    dest = args.dest
    fname = None

    try:
        fname = src
        with open(src, "r") as f:
            content = f.read()

        """
        splitlines to remove all linebreaks before stripping whitespace, tabs
        and continuation character '\'
        """
        linesList = list(map(smart_strip, iter(content.splitlines())))
        linesList = remove_block_comments(linesList)
        linesList = remove_inline_comments(linesList)
        minContent = "".join(linesList)

        fname = dest
        with open(dest, "w") as f:
            f.write(minContent)
            f.flush()

    except Exception as e:
        handle_file_exception(e, fname)


def handle_file_exception(excp, fname):
    if isinstance(excp, FileNotFoundError):
        print(f"Error: {fname} not found.")
    elif isinstance(excp, PermissionError):
        print(f"Error: Permission denied when accessing {fname}.")
    else:
        print(f"An error occurred while processing {fname}: {excp}")


if __name__ == "__main__":
    import sys

    minify(sys.argv[1:])
