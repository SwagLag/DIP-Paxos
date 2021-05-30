from typing import Any

class Message():
    """A message to be sent."""
    def __init__(self,source,destination,typestr: str,value: Any):
        self.src = source  # Computer die het bericht verstuurd heeft.
        self.dst = destination  # Computer waarnaar het bericht verstuurd moet worden.
        if typestr.upper() in ["PROPOSE","PREPARE","PROMISE","ACCEPT","ACCEPTED","SUCCESS","PREDICTED","REJECTED"]:
            self.type = typestr.upper()
        else:
            raise NotImplementedError
        self.value = value  # Value that the message carries.
