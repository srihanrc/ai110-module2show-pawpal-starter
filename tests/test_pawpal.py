from diagrams.pawpal_system import Pet, Task


def test_task_completion():
    t = Task("test", "do something", 0.25)
    assert not t.is_completed()
    t.mark_complete()
    assert t.is_completed()


def test_task_addition_to_pet():
    p = Pet("Buddy", "Dog", "Kibble")
    assert len(p.list_tasks(incomplete_only=False)) == 0
    t = Task("feed", "feed the pet", 0.1, pet=p)
    p.add_task(t)
    assert len(p.list_tasks(incomplete_only=False)) == 1
