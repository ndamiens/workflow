
#!/usr/bin/python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import workflow

class Task:
    name: str = None
    done: bool = False

    def __init__(self, name:str):
        self.name = name

    def setDone(self):
        self.done = True

    def isDone(self) -> bool:
        return self.done

    def persist(self):
        with open("/tmp/example_task_%s" % (self.name), "w") as f:
            f.write("done" if self.isDone() else "todo")
            f.close()

    def load(self):
        with open("/tmp/example_task_%s" % (self.name), "r") as f:
            row = f.read()
            self.done = row == "done"

class TaskMaker(workflow.Transition):
    def __init__(self, taskName:str):
        self.name = taskName

    def run(self):
        t = Task(self.name)
        t.persist()
        print("taskmaker : task %s created" % self.name)
        return super().run()

class GetFlour(TaskMaker):
    task_name = "get_flour"
    def __init__(self):
        self.from_state = MyExampleWorkflow.STATE_FLOUR
        self.output_states = [MyExampleWorkflow.STATE_WATER]
        super().__init__(self.task_name)

class GetWater(TaskMaker):
    task_name = "get_water"
    def __init__(self):
        self.from_state = MyExampleWorkflow.STATE_WATER
        self.output_states = [MyExampleWorkflow.STATE_SALT]
        super().__init__(self.task_name)

class GetSalt(TaskMaker):
    task_name = "get_salt"
    def __init__(self):
        self.from_state = MyExampleWorkflow.STATE_SALT
        self.output_states = [MyExampleWorkflow.STATE_WAIT]
        super().__init__(self.task_name)


class Mix(workflow.Transition):
    def __init__(self):
        self.name = "mix"
        self.from_state = MyExampleWorkflow.STATE_MIX
        self.output_states = [MyExampleWorkflow.STATE_COOK]
        super().__init__()

class Cook(workflow.Transition):
    def __init__(self):
        self.name = "cooking"
        self.from_state = MyExampleWorkflow.STATE_COOK
        self.output_states = [MyExampleWorkflow.STATE_FINISHED]

class WaitIngredients(workflow.Transition):
    def __init__(self):
        self.name = "wait"
        self.from_state = MyExampleWorkflow.STATE_WAIT
        self.output_states = [self.from_state, MyExampleWorkflow.STATE_COOK]

    def run(self):
        for task_class in [GetFlour, GetWater, GetSalt]:
            task = Task(task_class.task_name)
            task.load()
            if not task.isDone():
                print("still waiting task %s" % (task.name))
                return self.from_state
        return self.output_states[1]

class SimplePersistWorkflow(workflow.Context):
    PERSISTENT_FILE="current_state"

    def __init__(self):
        super().__init__()
        if os.path.exists(self.PERSISTENT_FILE):
            self.load()
            print("previous state loaded : %s" % (self.state))
        else:
            self.persist()

    def persist(self):
        with open(self.PERSISTENT_FILE, "w") as f:
            f.write(self.state)
            f.close()

    def load(self):
        with open(self.PERSISTENT_FILE, "r") as f:
            self.state = f.read()
            f.close()


class MyExampleWorkflow(SimplePersistWorkflow):
    STATE_FIRST = "need flour"
    STATE_FLOUR = STATE_FIRST
    STATE_WATER = "need_water"
    STATE_SALT = "need_salt"
    STATE_WAIT = "wait_ingredients"
    STATE_MIX = "mix_ingredients"
    STATE_COOK = "cooking"

    def __init__(self):
        super().__init__()
        self.addTransition(GetFlour())
        self.addTransition(GetSalt())
        self.addTransition(GetWater())
        self.addTransition(Mix())
        self.addTransition(Cook())
        self.addTransition(WaitIngredients())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["flour","salt","water"]:
        task = Task("get_%s" % (sys.argv[1]))
        task.setDone()
        task.persist()
    wf = MyExampleWorkflow()
    wf.run()

