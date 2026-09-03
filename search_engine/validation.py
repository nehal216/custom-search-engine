import re


def extract_citations(answer):
    """
    Find citations such as [1], [2], [3] in the answer.
    """

    citations = re.findall(r"\[(\d+)\]", answer)

    return [int(citation) for citation in citations]


def validate_citations(answer, sources):
    """
    Check whether every citation in the answer
    corresponds to an actual source.
    """

    citations = extract_citations(answer)

    valid_citations = []
    invalid_citations = []

    for citation in citations:
        if 1 <= citation <= len(sources):
            valid_citations.append(citation)
        else:
            invalid_citations.append(citation)

    return valid_citations, invalid_citations


def remove_invalid_citations(answer, sources):
    """
    Remove citations that do not correspond
    to an available source.
    """

    def replace_citation(match):
        citation_number = int(match.group(1))

        if 1 <= citation_number <= len(sources):
            return match.group(0)

        return ""

    return re.sub(
        r"\[(\d+)\]",
        replace_citation,
        answer
    )