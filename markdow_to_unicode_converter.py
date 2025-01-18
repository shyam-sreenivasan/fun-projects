import sys
import re

# Unicode mappings for different styles
BOLD_UNICODE_MAP = {chr(i): chr(0x1D400 + i - ord('A')) for i in range(ord('A'), ord('Z') + 1)}
BOLD_UNICODE_MAP.update({chr(i): chr(0x1D41A + i - ord('a')) for i in range(ord('a'), ord('z') + 1)})

ITALIC_UNICODE_MAP = {chr(i): chr(0x1D434 + i - ord('A')) for i in range(ord('A'), ord('Z') + 1)}
ITALIC_UNICODE_MAP.update({chr(i): chr(0x1D44E + i - ord('a')) for i in range(ord('a'), ord('z') + 1)})
ITALIC_UNICODE_MAP.update({'h': chr(0x210F)})

MONOSPACE_UNICODE_MAP = {chr(i): chr(0x1D670 + i - ord('A')) for i in range(ord('A'), ord('Z') + 1)}
MONOSPACE_UNICODE_MAP.update({chr(i): chr(0x1D68A + i - ord('a')) for i in range(ord('a'), ord('z') + 1)})
MONOSPACE_UNICODE_MAP.update({chr(i): chr(0x1D7F6 + i - ord('0')) for i in range(ord('0'), ord('9') + 1)})

# Function to convert text to Unicode
def convert_to_unicode(text, style_map):
    return ''.join(style_map.get(char, char) for char in text)

# Function to convert Markdown to Unicode
def convert_markdown_to_unicode(markdown):
    def replace_with_unicode(match):
        tag = match.group(1)
        text = match.group(2)

        if tag == '**':  # Bold
            return convert_to_unicode(text, BOLD_UNICODE_MAP)
        elif tag == '*':  # Italic
            return convert_to_unicode(text, ITALIC_UNICODE_MAP)
        elif tag == '`':  # Code snippet
            # Add as many '|' as spaces in the start of each line
            lines = text.splitlines()
            updated_lines = [line.replace(' ', '|', 1) if line.startswith(' ') else line for line in lines]
            text = '\n'.join(updated_lines)
            return convert_to_unicode(text, MONOSPACE_UNICODE_MAP)
        else:
            return text

    # Regex to find Markdown syntax
    pattern = re.compile(r'(\*\*|`|\*)(.+?)\1', re.DOTALL)  # Matches **bold**, *italic*, and `code`
    result = re.sub(pattern, replace_with_unicode, markdown)

    return result

# Get filename from command line arguments
if len(sys.argv) > 1:
    filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
else:
    print("Usage: python markdown_to_unicode.py <filename>")
    sys.exit(1)

# Convert Markdown to Unicode
unicode_result = convert_markdown_to_unicode(markdown_content)
print(unicode_result)
