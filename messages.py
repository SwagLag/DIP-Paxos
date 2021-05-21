from computer import Computer

class Message():
    """A message to be sent."""
    def __init__(self,source: Computer,destination: Computer,typestr,content):
        self.src = source  # Computer die het bericht verstuurd heeft.
        self.dst = destination  # Computer waarnaar het bericht verstuurd moet worden.
        if typestr.upper() in ["PROPOSE","PREPARE","PROMISE","ACCEPT","ACCEPTED","REJECTED"]:
            self.type = typestr.upper()
        self.cnt = content  # Value that the message carries.

