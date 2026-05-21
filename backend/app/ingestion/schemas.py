from dataclasses import dataclass, asdict


@dataclass
class Chunk:
    id: str
    text: str
    source: str
    chunk_index: int

    def to_dict(self):
        return asdict(self)