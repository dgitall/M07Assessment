from dataclasses import dataclass, field

@dataclass
class ApplicationState:
    HasUnsavedChanges: bool = False,
    