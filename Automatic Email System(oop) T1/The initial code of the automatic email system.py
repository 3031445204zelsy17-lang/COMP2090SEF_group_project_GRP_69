class AbstractEmail(ABC):
    """Abstract base class for email"""

    def __init__(self, id: str, subject: str, body: str, sender: AbstractPerson):
        self.__id = id
        self.__subject = subject
        self.__body = body
        self.__sender = sender
        self.__timestamp = datetime.now()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def body(self) -> str:
        return self.__body

    @property
    def sender(self) -> AbstractPerson:
        return self.__sender




class Category:
    """Email Classification"""

    def __init__(self, id: str, name: str, priority: int):
        self.__id = id
        self.__name = name
        self.__priority = priority

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def priority(self) -> int:
        return self.__priority

    def __lt__(self, other: 'Category') -> bool:
        return self.__priority < other.__priority



class Professor(AbstractPerson):
    """Professor category"""

    def __init__(self, name: str, email: str, department: str):
        super().__init__(name, email)
        self.__department = department
        self.__inbox = []  

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        return True

    def receive_email(self) -> list:
        return self.__inbox

    def approve_reply(self, reply: Reply) -> bool:
        reply.approved = True
        return True