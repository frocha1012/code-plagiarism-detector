import re
from difflib import SequenceMatcher


KEYWORDS = {
    "and", "as", "break", "class", "continue", "def", "elif", "else",
    "false", "for", "from", "if", "import", "in", "is", "not", "or",
    "return", "true", "while", "with",
}


def _normalize_line(line: str) -> str:
    """Normalize a code line so renamed variables/functions can still match."""
    line = re.sub(r"#.*$", "", line)
    line = re.sub(r"(['\"]).*?\1", "str", line)
    line = re.sub(r"\b\d+(\.\d+)?\b", "num", line)
    line = line.lower()

    def replace_identifier(match):
        word = match.group(0)
        return word if word in KEYWORDS else "id"

    line = re.sub(r"[a-z_][a-z0-9_]*", replace_identifier, line)
    return re.sub(r"\s+", " ", line).strip()


def find_similar_lines(
    file1_content: str,
    file2_content: str,
    threshold: float,
) -> list[dict]:
    """Find similar line pairs using simple normalized difflib matching."""
    file1_lines = file1_content.splitlines()
    file2_lines = file2_content.splitlines()
    used_file2_lines = set()
    matches = []

    for index1, text1 in enumerate(file1_lines, start=1):
        normalized1 = _normalize_line(text1)
        if len(normalized1) < 6:
            continue

        best = None

        for index2, text2 in enumerate(file2_lines, start=1):
            if index2 in used_file2_lines:
                continue

            normalized2 = _normalize_line(text2)
            if len(normalized2) < 6:
                continue

            similarity = SequenceMatcher(None, normalized1, normalized2).ratio()

            if similarity >= threshold and (best is None or similarity > best["similarity"]):
                best = {
                    "file1_line": index1,
                    "file1_text": text1,
                    "file2_line": index2,
                    "file2_text": text2,
                    "similarity": round(similarity, 4),
                }

        if best:
            used_file2_lines.add(best["file2_line"])
            matches.append(best)

    return sorted(matches, key=lambda match: match["similarity"], reverse=True)
