from dataclasses import dataclass


@dataclass
class Paper:
    title: str
    authors: str
    url: str
    filepath_local: str | None = None
    text: str | None = None
    tags: list[str] | None = None
    summary: str | None = None
