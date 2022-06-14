def is_comment(physical_line: str) -> bool:
    line = physical_line.lstrip()
    if line.startswith("*") or line.startswith("//"):
        return True
    else:
        return False

def is_empty(physical_line: str) -> bool:
    line = physical_line.strip(" */")
    if len(line) == 0:
        return True
    else:
        return False

class Checker:
    
    def backward_slash(physical_line):
        r"""Suggest replacing backward slash with forward slash.
        This ensures portability of the code across different
        operating systems."""

        if "\\" in physical_line:
            msg = "Avoid backward slashes."
            return msg
        else:
            return None


    def maximum_line_length(physical_line):
        r"""Limit all lines to a maximum of 79 characters."""

        MAX_LINE_LENGTH = 79
        line = physical_line.rstrip()
        length = len(line)
        if length > MAX_LINE_LENGTH:
            msg = f"Line too long: {length} > {MAX_LINE_LENGTH} characters."
            return msg
        else:
            return None