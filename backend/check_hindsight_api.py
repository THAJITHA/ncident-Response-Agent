import inspect
from hindsight_client import Hindsight

print(Hindsight)
print([a for a in dir(Hindsight) if not a.startswith("_")][:80])
for name in ["retain", "recall", "list_memories", "__init__"]:
    if hasattr(Hindsight, name):
        try:
            print(name, inspect.signature(getattr(Hindsight, name)))
        except Exception as exc:
            print(name, "sig-error", exc)
