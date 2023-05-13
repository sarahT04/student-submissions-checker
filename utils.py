from difflib import SequenceMatcher

def sanitize_string(string: str) -> str:
    # Lowercase the string, replace every whitespace with nothing, 
    return string.replace(' ', '').replace(".", '').lower()

def change_name(string: str) -> str:
    return string.replace('muhammad', '').replace('moh', '')

def string_comparisor(in_csv: str, in_gc: str) -> int:
    # Converts the ratio to be in percentage, then round it downwards.
    return round(SequenceMatcher(None, change_name(sanitize_string(in_csv)), sanitize_string(in_gc)).ratio() * 100)

def name_matches(in_csv: str, in_gc: str) -> bool:
    if string_comparisor(in_csv, in_gc) > 60:
        return True
    return False
