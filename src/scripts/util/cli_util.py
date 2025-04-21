def get_preview(text: str) -> str:
    if len(text) <= 200:
        return text
    return (
        f"{text[:100]}\n\n"
        f"[...]\n\n"
        f"{text[-100:]}"
    )
