import re

def is_page_end(input_string):
    """
    Checks if the line matches the page end pattern.
    """
    pattern = r"^\s*(\w+)\s+(\d+:\d+)\s+(\d+)\s+(\w+)\s+(\d+:\d+)\s*$"
    return bool(re.match(pattern, input_string))

def parse_columns(my_string):
    """
    Splits a line into left and right columns if it contains more than 3 consecutive spaces.
    """
    if "    " in my_string:  # 4 spaces or more
        parts = my_string.split("    ", 1)
        left = parts[0].strip()
        right = parts[1].strip() if len(parts) > 1 else ""
    else:
        left, right = my_string.strip(), ""
    return left, right

def remove_numbers_after_period(text):
    """
    Removes numbers that start a sentence after a period, exclamation mark, or question mark.
    """
    pattern = r'([.!?])\s*\d+'
    cleaned_text = re.sub(pattern, r'\1', text)
    return cleaned_text

def rearrange_text_file(input_filename, output_filename):
    """
    Processes the input file, splits text into columns, removes numbers starting sentences,
    and removes page markers.
    """
    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    left_column = []
    right_column = []
    combined_lines = []

    for line in lines:
        # Check if the line is a page end marker
        if is_page_end(line):
            # Combine the accumulated lines and reset the columns without writing the marker itself
            combined_lines.extend(left_column + right_column)
            left_column.clear()
            right_column.clear()
            continue

        # Split the current line into left and right columns
        left, right = parse_columns(line)

        # Add the parsed text to the respective columns
        if left:
            left_column.append(left)
        if right:
            right_column.append(right)

    # Append any remaining text after the last page marker
    combined_lines.extend(left_column + right_column)

    # Join the combined lines into a single string
    combined_text = ' '.join(combined_lines)

    # Remove numbers that start after a sentence-ending punctuation
    combined_text = remove_numbers_after_period(combined_text)

    # Replace multiple spaces with a single space
    combined_text = re.sub(r'\s+', ' ', combined_text)

    # Write the cleaned and rearranged text to the output file
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(combined_text)

# Usage example
input_file = 'original.txt'   # Replace with your input file name
output_file = 'cleansed.txt' # Replace with your desired output file name

rearrange_text_file(input_file, output_file)