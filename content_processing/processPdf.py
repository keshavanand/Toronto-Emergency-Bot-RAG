from pypdf import PdfReader
import re
from itertools import tee

def get_chunks(path: str, content_page_no: int, page_1_index: int, pattern: re =r"([\w\s\-?']+)\.*\s*(\d+)") -> dict:
    '''
     Extracts chunks of heading-page pairs from the content of a file starting from a specified page number.

    Args:
        path (str): The file path to the content (e.g., a text file or document).
        content_page_no (int): The starting page number from which the headings and page numbers will be extracted.
        page_1_index (int): The index to map the first page number (used for adjusting the page number logic if necessary).
        pattern (str, optional): The regular expression pattern used to match headings and page numbers. Defaults to matching headings and page numbers (e.g., "Heading... 1").

    Returns:
        dict: A dictionary with headings as keys and their respective page content as values. The page numbers are adjusted based on the `content_page_no` and `page_1_index`.

    Example:
        get_chunks('file.txt', 2, 1)
        # Returns a dictionary like:
        # {'Preparing for an Emergency': "content......", 'Make a Plan': "content......", 'The importance of insurance': "content......", ...}
    '''
    print("\n............................Reading PDF file............................\n")
    # read pdf with pydf
    reader = PdfReader(path)

    # get contents page text to store contet and page number
    page = reader.pages[content_page_no]
    contents = page.extract_text()

    print(f"\nOriginal Content page text:\n{contents}\n")

    # Merge into a single line
    single_line_contents = " ".join(contents.splitlines())

    # General regex pattern for headings and page numbers
    pattern = pattern

    # Find all matches
    matches = re.findall(pattern, single_line_contents)

    # Convert matches into a dictionary
    toc_dict = {heading.strip(): int(page) for heading, page in matches}

    print(f"\nConverted content page text:\n{toc_dict}\n")

    # Function to pair current and next items
    def pair_with_next(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    # iterate to get text for each heading
    for current, next_key in pair_with_next(toc_dict.keys()):
        page_number = toc_dict[current] 

        while True:
            page = reader.pages[page_number + page_1_index] # for correct index 
            toc_dict[current] = str(toc_dict[current] ) + page.extract_text() 
            page_number +=1
            
            if page_number < toc_dict[next_key]:
                continue
            break
    print("\n............................Done storing headings and there contents in dict............................\n")        
    return toc_dict


