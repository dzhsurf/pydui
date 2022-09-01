from dataclasses import dataclass


@dataclass(frozen=True)
class PyDuiAttributeString:
    pass


def parse_attribute_string(desc: str) -> PyDuiAttributeString:
    pass
