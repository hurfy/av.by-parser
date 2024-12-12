def remove_html_chars(text: str) -> str:
    """Removes all HTML and garbage characters"""
    return text.replace(" ·", "").replace("\xa0", " ").replace("\u2009", " ")
