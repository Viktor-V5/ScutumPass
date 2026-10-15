from dataclasses import dataclass



@dataclass
class ContainerRow:
    key_bytes: str
    db_location : str

class ContainerRowContainer:
    session: ContainerRow | None = None

    @classmethod
    def set_session(cls, session_data: ContainerRow):
        if not isinstance(session_data, ContainerRow):
            raise TypeError("Invalid SessionWalletData")
        cls.session = session_data

    @classmethod
    def get_session(cls):
        return cls.session

    @classmethod
    def clear_session(cls):
        cls.session = None

