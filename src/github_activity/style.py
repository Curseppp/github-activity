from rich.text import Text


def gradient_text(
    text: str, start: tuple[int, int, int], end: tuple[int, int, int]
) -> Text:
    result = Text()

    for i, char in enumerate(text):
        ratio = i / max(len(text) - 1, 1)

        r = int(start[0] + (end[0] - start[0]) * ratio)
        g = int(start[1] + (end[1] - start[1]) * ratio)
        b = int(start[2] + (end[2] - start[2]) * ratio)

        result.append(char, style=f"rgb({r},{g},{b})")

    return result
