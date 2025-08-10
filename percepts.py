from dataclasses import dataclass

@dataclass
class Percept:
    stench: bool
    breeze: bool
    glitter: bool
    bump: bool
    scream: bool

    def to_dict(self):
        return {
            "stench": self.stench,
            "breeze": self.breeze,
            "glitter": self.glitter,
            "bump": self.bump,
            "scream": self.scream
        }
