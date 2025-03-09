#!/usr/bin/env python3
"""
Minivan: A lightweight tool for minifying JavaScript and CSS files.

This module provides functionality to minify JavaScript and CSS files by:
- Removing comments (inline, block, and multi-line).
- Ignoring comments within strings or template literals.
- Preserving "loud" comments (/*! */).
- Stripping unnecessary whitespace, tabs, and line breaks.
- Retaining quoted strings and ensuring code correctness.

Features:
- Can be used as both a standalone script and an importable library.
- Supports command-line arguments for file processing.
- Efficient line-wise processing for performance.

Functions:
- main(args): Entry point for command-line usage.
- minify(src: str, dest: str): Minifies the input file and saves it to the
  specified destination.
- remove_block_comments(lines_list: list[str]): Removes block comments
  while preserving loud comments.
- remove_inline_comments(lines_list: list[str]): Removes inline comments
  while preserving quoted strings.
- handle_file_exception(excp: Exception, fname: str): Handles file-related
  errors gracefully.

Usage:
- As a standalone script:
    $ python minivan.py <source_file> <destination_file>
- As an importable library:
    from minivan import minify
    minify("input.js", "output.min.js")
"""

import argparse


def handle_file_exception(excp: Exception, fname: str) -> None:
    """
    Handles file-related exceptions and prints an appropriate error message.

    Args:
        excp (Exception): The exception object raised during file operations.
        fname (str): The name of the file being processed.
    """
    if isinstance(excp, FileNotFoundError):
        print(f"Error: {fname} not found.")
    elif isinstance(excp, PermissionError):
        print(f"Error: Permission denied when accessing {fname}.")
    else:
        print(f"An error occurred while processing {fname}: {excp}")


def remove_block_comments(lines_list: list[str]) -> list[str]:
    """
    Remove multi-line block comments while preserving loud comments.
    Put extra space before '+' symbol if the line starts with '+'.

    Args:
        lines_list (list[str]): List of lines to process.

    Returns:
        list[str]: Lines with block comments removed and loud comments preserved.
    """
    curated_list = []
    drop_lines = False
    loud_comment = False

    for line in lines_list:
        if loud_comment:
            curated_list.append(line + "\n")
            if line.endswith("*/"):
                loud_comment = False
            continue

        if drop_lines:
            if line.endswith("*/"):
                drop_lines = False
            continue

        if line.startswith("+"):
            line = "".join([" ", line])

        if line.startswith("/*!"):
            curated_list.append(line + "\n")
            if not line.endswith("*/"):
                loud_comment = True
        elif line.startswith("//#"):
            curated_list.append(line + "\n")
            continue
        elif line.startswith("/*") and line.endswith("*/") or line.startswith("//"):
            continue
        elif line.startswith("/*") and not line.endswith("*/"):
            drop_lines = True
        else:
            curated_list.append(line)

    return curated_list


def minify_line(
    line: str,
    matching_char: str | None,
    within_comment: bool,
    loud_comment: bool,
    ext: str,
) -> tuple[str, str | None, bool, bool]:
    """
    Process a single line of code to remove inline comments while
    handling multi-line scenarios.
        * removes all inline comments except those within quoted or format strings
        * fixes one line else statements without curly braces to have an extra space.
    e.g. some code // comment     ==>  some code
         some code /* comment */  ==>  some code
         "some string /* not a comment */ " ==> preserved as is
         else
            statement;      ==>  else statement;

    Args:
        line (str): The line of code to process.
        matching_char (str or None):
            The quote character ('", ', or `` ` ``) being tracked for open strings.
        within_comment (bool):
            Tracks whether processing is within a multi-line comment.
        loud_comment (bool):
            Tracks whether processing is within a loud comment.

    Returns:
        tuple: (processed_line (str), matching_char (str or None),
        within_comment (bool), loud_comment (bool)).
    """
    if line.startswith("//#"):
        curated_line = "\n" + line
        return curated_line, matching_char, within_comment, loud_comment

    chars = tuple(line)
    num_chars = len(chars)
    curated_chars = []
    start_comment = False
    end_comment = False

    for i in range(num_chars):
        c = chars[i]
        if matching_char is not None:
            if c == matching_char:
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
                    if next_char == "*":
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

    # Account for one line else statements that do not have curly braces
    # by adding an extra space after spaces were stripped in a previous step
    if "else" == curated_line:
        curated_line = "".join([curated_line, " "])

    # within backtick or html/tpl files and if line ends with '<' within last 20 chars
    # but does not contain closing '>' then add an extra space
    if matching_char == "`" or ext == "html" or ext == "tpl":
        tail = curated_line[-20:]
        if "<" in tail:
            if tail.rfind("<") > tail.rfind(">"):
                curated_line += " "

    return curated_line, matching_char, within_comment, loud_comment


def smart_strip(input_line: str) -> str:
    """
    Removes leading/trailing whitespace and continuation characters.

    Args:
        input_line (str): A single line of input.

    Returns:
        str: Line stripped of whitespace and trailing backslashes.
    """
    return input_line.strip().strip("\\")


def remove_inline_comments(lines_list: list[str], ext: str) -> list[str]:
    """
    Removes inline comments while handling multi-line contexts and loud comments.

    Args:
        lines_list (list[str]): List of pre-processed lines.

    Returns:
        list[str]: Lines with inline comments removed, preserving loud comments.
    """
    curated_list = []
    # skip_flag = False
    find_char = None
    within_comment = False
    loud_comment = False
    for line in lines_list:
        clean_line, find_char, within_comment, loud_comment = minify_line(
            line, find_char, within_comment, loud_comment, ext
        )
        curated_list.append(clean_line)

    return curated_list


def minify(src: str, dest: str) -> None:
    """
    Minifies a JavaScript or CSS file by removing comments and extra whitespace.

    Args:
        src (str): Path to the source file.
        dest (str): Path to the destination file for the minified output.
    """
    fname = None
    try:
        fname = src
        ext = fname.lower().split(".").pop()
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()

        # splitlines to remove all linebreaks before stripping whitespace, tabs
        # and continuation character '\'
        lines_list = list(map(smart_strip, iter(content.splitlines())))
        lines_list = remove_block_comments(lines_list)
        lines_list = remove_inline_comments(lines_list, ext)
        min_content = "".join(lines_list)

        fname = dest
        with open(dest, "w", encoding="utf-8") as f:
            f.write(min_content)
            f.flush()

    except Exception as e:
        handle_file_exception(e, fname)


def main(args: list[str]) -> None:
    """
    Parses command-line arguments and triggers the minification process.

    Args:
        args (list[str]): List of command-line arguments.
    """
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

    minify(src, dest)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
