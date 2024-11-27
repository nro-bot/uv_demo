"""
Extract gleason scores from health record text (pathology reports).
Uses regex for now.

26 Nov 2024 
nrobot
"""
import pandas as pd
import re
from rich import print

# from rich.traceback import install
# install(show_locals=True)


def find_gl_with_spacy(text: str):
    import spacy
    from spacy.matcher import Matcher

    nlp = spacy.load("en_core_web_sm")
    #matcher = Matcher(nlp.vocab)
    #regex_total_last = get_regexs()["regex_total_last"]
    #matcher.add("GLEASON_TOTAL_LAST", [[{"TEXT": {"regex": regex_total_last}}]])
    results = []
    doc = nlp(text)
    for match in re.finditer(get_regexs()['regex_total_last'], doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        # This is a Span object or None,  if match doesn't map to valid token sequence
        if span is not None:
            print("Found match:", span.text)
            print([span.start, span.end, span.label, span.text])
    return results


def get_regexs() -> dict[str, str]:
    """Return dictionary of regex strings.
    """
    # _3to5_ = '[3-5]'
    _6to10_ = r"\b[6-9]|10\b"
    conjunction = r"&|and|\+"
    regex_total_last = rf"([3-5])\D*([3-5])\D*({_6to10_})"
    regex_total_first = rf"({_6to10_})\D*([3-5])\D*([3-5])"
    regex_no_total = rf"([3-5])\s*({conjunction})\s*([3-5])"

    return {
        "regex_total_last": regex_total_last,
        "regex_total_first": regex_total_first,
        "regex_no_total": regex_no_total,
    }


def find_total_last(text: str) -> list[int] | None:
    """
    Extracts and returns the indices and values of Gleason scores and their total from a given text.

    If the pattern is found, it extracts three numerical values representing two individual Gleason scores and their total, as well as their starting indices in the text. 

    Specifically, this function finds patterns of A + B = C.

    Args:
        text (str): The input text to search for the Gleason score pattern.

    Returns:
        list[int] | None: If a match is found, returns a list of six items: the three string indices and three gleason values. Returns `None` if no match is found.
    """

    m = re.search(get_regexs()["regex_total_last"], text)
    if m:
        gleason1, gleason2, gleason_total = [int(digit) for digit in m.groups()]
        idx1, idx2, idx_total = m.start(1), m.start(2), m.start(3)
        return [idx1, idx2, idx_total, gleason1, gleason2, gleason_total]
    return None


def find_total_first(text: str) -> list[int] | None:
    """
    See find_total_last().
    Specifically, this function finds patterns of C = A + B. 
    """

    m = re.search(get_regexs()["regex_total_first"], text)
    if m:
        gleason_total, gleason1, gleason2 = [int(digit) for digit in m.groups()]
        idx_total, idx1, idx2 = m.start(1), m.start(2), m.start(3)
        return [idx1, idx2, idx_total, gleason1, gleason2, gleason_total]
    return None


def find_no_total(text: str) -> list[int] | None:
    """
    See find_total_last().
    Specifically, this function finds patterns of A + B, A & B, or A and B
    """
    m = re.search(get_regexs()['regex_no_total'], text)
    if m:
        gleason1, gleason2 = int(m.group(1)), int(m.group(3))
        gleason_total = gleason1 + gleason2 # Assumption
        idx1, idx2, idx_total = m.start(1), m.start(3), m.start(3) + 2 # Assumption on last part
        return [idx1, idx2, idx_total, gleason1, gleason2, gleason_total]
    return None

def checksum(a,b,c) -> bool:
    """
    Unused. Can be used in future to sanity check extracted numbers.
    """
    return a+b==c

def find_any_gleason(text: str) -> list[int] | None:
    """
    Attempts to extract Gleason score information from the input text using multiple patterns.

    Three functions are used.
    - `find_total_last()`: Searches for Gleason scores with the total appearing at the end.
    - `find_total_first()`: Searches for Gleason scores with the total appearing at the beginning.
    - `find_no_total()`: Searches for Gleason scores where the total is not explicitly mentioned.

    The function returns the first successful match found from these checks. 

    Args:
        text (str): The input text to search for Gleason score information.

    Returns:
        list[int] | None: The extracted indices and scores from the first
        successful pattern match. List of length 6. Returns `None` if no patterns match.
    """
    if vals := find_total_last(text) \
        or find_total_first(text) \
        or find_no_total(text):
        # if checksum(*vals[3:]):
            return vals
    return None

def find_gleasons(text: str):
    """
    Identifies and extracts Gleason score information from text. Also returns for debugging purposes a window of text around the extract scores. 

    Args:
        text (str): The input text to analyze for Gleason scores.

    Returns:
        list[list[[int, str]]: A list of lists, where each inner list represents a Gleason score match and contains:
            - The starting index of the score in the text.
            - The extracted Gleason score value.
            - A label indicating whether it is "Gleason_1", "Gleason_2", or "Gleason_total".
            - A string representing the context window around the score.

        Returns an empty list if no Gleason scores are found.
    """
    text = text.lower()
    all_matches = []
    for gl in re.finditer("gleason", text):
        start = gl.start()
        context_start, context_end = (
            max(0, gl.start() - 50),
            min(gl.end() + 80, len(text)),
        )
        context = text[context_start:context_end]

        # Cut at next occurence of gleason, in case second one in window
        end = text[gl.start()+1 : context_end].find("gleason")
        if end == -1:
            candidate=text[gl.start() : context_end]
        else:
            end += gl.start()+1
            candidate=text[gl.start() : end]
        gleason_match = find_any_gleason(candidate)

        if gleason_match:
            idx1, idx2, idx_total, gleason1, gleason2, gleason_total = gleason_match
            # start, text, label, context
            all_matches.extend([
                [start+idx1, gleason1, "Gleason_1", context],
                [start+idx2, gleason2, "Gleason_2", context],
                [start+idx_total, gleason_total, "Gleason_total", context]
            ])

    return all_matches


def get_test_strs() -> list[str]:
    """
    Returns a list of example strings found in pathology reports for prostate cancer, including information about gleason scores and biopsy cores.
 
    Used to test regexes in get_regexs().

    Returns:
        list of str: A list containing the sample strings.
    """

    str1A = "gleason score 3+3 = 6; 3 of 3 cores; 40%"
    str1B = "gleason score 4+4=9; one of two; 10%"
    str2 = "gleason 3+4=7/10, involving 5% of 1/2 cores"
    str3 = (
        "gleason grade 3+4 \n\t (combined gleason score 7/10) involving 2 (of 2) cores"
    )
    str4 = "gleason scores 6/10) involving "
    str5A = "gleason score 7 (3+4) in one of one"
    str5B = "gleason score 9 (4+5) in one of one"
    str5C = "adenocarcinoma, grade group 2, gleason score 7 (3+4)"
    str_8 = "gleason pattern 4 is noted"
    str9A = "gleason's score 3+3"
    str9B = "gleason's score 4 + 3"
    str10 = "GLEASON pattern 3+4(10%)=7 (GRADE GROUP 2)."
    strs = [
        str1A, str1B, str2, str3, str4, str5A, str5B, str5C,
        str_8, str9A, str9B, str10,
    ]
    return strs


def main():
    # -- Test using python regex module 
    for sample in get_test_strs():
        print(sample)
        print(find_gleasons(sample))

    # -- Test with spacy and regex
    for sample in get_test_strs():
        print(sample)
        print(find_gl_with_spacy(sample))


if __name__ == "__main__":
    main()