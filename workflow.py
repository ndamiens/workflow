#!/usr/bin/python3

class Context:
    STATE_FIRST = None
    STATE_FINISHED = "finished"

    def __init__(self, init_state:str=None):
        self.state = self.STATE_FIRST
        self.transitions: "list[Transition]" = []

    def addTransition(self, tr:"Transition"):
        tr.setContext(self)
        self.transitions.append(tr)

    def setState(self, state:str):
        self.state = state

    def run(self):
        if self.state == self.STATE_FINISHED:
            print("workflow completed")
            return
        for tr in self.transitions:
            if tr.from_state == self.state:
                print("wf run transition %s" % (tr.name))
                new_state = tr.run()
                if new_state == self.state:
                    return
                print("new state : %s" % (new_state))
                self.state = new_state
                self.persist()
                return self.run()
        print("no transition found")
        return

    def persist(self):
        raise Exception("implement me")

    def load(self):
        raise Exception("implement me")

class Transition:
    from_state: str = None
    output_states: "list[str]"  = []
    context: Context = None

    def setContext(self, context:Context):
        self.context = context

    def run(self):
        return self.output_states[0]
