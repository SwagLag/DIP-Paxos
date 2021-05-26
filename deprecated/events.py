# class EventWrapper():
#     """Wrapper class for containing multiple events. Used in the simulation function
#     for getting new events."""
#     def __init__(self,events:list):
#         """Initialises a event sequence, using a list containing all the event
#         objects."""
#         self.events = events
#
#     def add_event(self,event):
#         self.events.append(event)
#
#     def get_event(self,tick):
#         for event in self.events:
#             if event.tick == tick:
#                 return event
#         return None

# class Event():
#     """Defines actions which happen independently from a user's input, albeit
#     defined before the simulation begins."""
#     def __init__(self, tick:int, failed:list, repaired:list, proposerc: int, proposerv):
#         """Creates an event. This method should only be called by the parser."""
#         self.tick = tick
#         self.failed = failed
#         self.repaired = repaired
#         self.proposercomputer = proposerc
#         self.proposervalue = proposerv
#
#     def get_eventinfo(self):
#         return self.tick, self.failed, self.repaired, self.proposercomputer, self.proposervalue
