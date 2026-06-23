from datetime import datetime, timedelta

import pytest

from diagrams.pawpal_system import Pet, Task, PetOwner, Scheduler


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


def test_sort_by_time_and_duration():
    owner = PetOwner("A", 1, daily_hours=2.0)
    p = Pet("P", "dog", "kibble")
    owner.add_pet(p)

    t1 = Task("t1", "first", 0.5, pet=p)
    t2 = Task("t2", "second", 0.25, pet=p)
    t3 = Task("t3", "third", 0.1, pet=p)

    # explicit times
    base = datetime(2026, 6, 23, 7, 0, 0)
    t1.time = base.replace(hour=9)
    t2.time = base.replace(hour=8)
    # t3 has no time

    p.add_task(t1)
    p.add_task(t2)
    p.add_task(t3)

    s = Scheduler(owner)
    by_time = s.sort_by_time(owner.get_all_tasks(incomplete_only=False))
    assert [t.name for t in by_time][:3] == ["t2", "t1", "t3"]

    by_dur = s.sort_by_duration(owner.get_all_tasks(incomplete_only=False))
    assert [t.name for t in by_dur] == ["t3", "t2", "t1"]


def test_recurring_due_and_mark_complete_creates_next():
    owner = PetOwner("B", 1, daily_hours=2.0)
    p = Pet("P", "cat", "wet")
    owner.add_pet(p)

    t = Task("feed", "feed cat", 0.1, frequency="daily", pet=p)
    # make last completed 2 days ago
    t.last_completed = datetime(2026, 6, 20, 8, 0, 0)
    p.add_task(t)

    s = Scheduler(owner)
    # due because last_completed older than 1 day
    assert t.is_due(reference=datetime(2026, 6, 23, 9, 0, 0))

    # mark complete should append a new task for next occurrence
    before = len(p.list_tasks(incomplete_only=False))
    t.mark_complete()
    after = len(p.list_tasks(incomplete_only=False))
    assert after == before + 1
    # newest task should have same name and frequency
    names = [x.name for x in p.list_tasks(incomplete_only=False)]
    assert names.count("feed") >= 2


def test_time_conflict_detection():
    owner = PetOwner("C", 1, daily_hours=2.0)
    p1 = Pet("A", "dog", "k")
    p2 = Pet("B", "cat", "w")
    owner.add_pet(p1)
    owner.add_pet(p2)

    # overlapping tasks
    t1 = Task("walk", "morning", 1.0, pet=p1)
    t2 = Task("vet", "check", 0.5, pet=p2)
    t1.time = datetime(2026, 6, 23, 8, 0, 0)
    t2.time = datetime(2026, 6, 23, 8, 30, 0)  # overlaps with t1 (8:00-9:00)

    p1.add_task(t1)
    p2.add_task(t2)

    s = Scheduler(owner)
    conflicts = s.detect_conflicts()
    tc = conflicts.get("time_conflicts", [])
    # should detect at least one overlapping pair involving walk and vet
    pairs = {(a.name, b.name) for a, b in tc}
    assert ("walk", "vet") in pairs or ("vet", "walk") in pairs


def test_too_long_and_overflow_and_duplicates():
    owner = PetOwner("D", 1, daily_hours=0.5)  # 30 minutes
    p = Pet("P", "dog", "k")
    owner.add_pet(p)

    t_long = Task("long", "too long", 1.0, pet=p)
    t_a = Task("a", "a", 0.25, pet=p)
    t_b = Task("a", "a duplicate", 0.25, pet=p)

    p.add_task(t_long)
    p.add_task(t_a)
    p.add_task(t_b)

    s = Scheduler(owner)
    conflicts = s.detect_conflicts()
    assert any(t.name == "long" for t in conflicts.get("too_long", []))
    # overflow should include the task that cannot fit (the long one)
    overflow_names = [t.name for t in conflicts.get("overflow", [])]
    assert "long" in overflow_names
    # duplicates should include both with name "a"
    dup_names = [t.name for t in conflicts.get("duplicates", [])]
    assert dup_names.count("a") >= 2


def test_get_filtered_tasks_and_priority():
    owner = PetOwner("E", 1, daily_hours=1.0)
    p = Pet("P", "dog", "k")
    owner.add_pet(p)

    t1 = Task("daily", "d", 0.25, frequency="daily", pet=p)
    t2 = Task("once", "o", 0.25, frequency=None, pet=p)
    # t1 never completed -> due
    p.add_task(t1)
    p.add_task(t2)

    s = Scheduler(owner)
    filtered = s.get_filtered_tasks(pet_name="P", due_only=True)
    assert any(t.name == "daily" for t in filtered)
    # priority_tasks should include daily first
    pr = s.priority_tasks()
    assert pr and pr[0].frequency == "daily"

