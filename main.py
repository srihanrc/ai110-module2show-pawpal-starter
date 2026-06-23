from diagrams.pawpal_system import PetOwner, Pet, Task, Scheduler


def demo_schedule() -> None:
    """Demo the scheduling features in the terminal.

    Sets up a `PetOwner` with two `Pet` instances and several `Task` objects
    (added out-of-order). Some tasks are given explicit `time` attributes and
    one recurring task is back-dated so it is due. This function exercises the
    `Scheduler` methods (`sort_by_duration`, `sort_by_time`,
    `get_filtered_tasks`, `priority_tasks`, `generate_plan(include_conflicts=True)`)
    and prints human-readable summaries and detected conflicts to stdout.

    Intended for manual verification and debugging; it has no return value and
    writes its results to the console.
    """
    owner = PetOwner("Alex", years_experience=3, daily_hours=2.0)

    # Create pets
    dog = Pet("Fido", "Dog", "Kibble", ["none"])
    cat = Pet("Mittens", "Cat", "Wet Food", [])

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks out-of-order and with optional time attributes
    from datetime import datetime, timedelta

    # Task created first but scheduled later
    t_feed_cat = Task("Feed Cat", "Serve wet food", 0.1, frequency="daily", pet=cat)
    # Task created second but earlier in time
    t_play = Task("Play Time", "15 minutes of play", 0.25, frequency=None, pet=dog)
    # Task created last but has an explicit time (morning)
    t_walk = Task("Morning Walk", "Walk around the neighborhood", 0.5, frequency="daily", pet=dog)

    # use a single reference 'now' to avoid microsecond drift
    now = datetime.now().replace(microsecond=0)
    # assign explicit times to test sort_by_time (times are illustrative)
    t_play.time = now.replace(hour=20, minute=0, second=0)
    t_feed_cat.time = now.replace(hour=8, minute=0, second=0)
    t_walk.time = now.replace(hour=7, minute=0, second=0)

    # mark one recurring task as last completed 2 days ago to make it due
    t_walk.last_completed = now - timedelta(days=2)

    # Add tasks to pets in an out-of-order fashion
    dog.add_task(t_play)
    cat.add_task(t_feed_cat)
    dog.add_task(t_walk)

    # Create scheduler and produce today's plan
    scheduler = Scheduler(owner)

    # Print unsorted task list (use helpers for clarity)
    def format_task(t: Task) -> str:
        pet_name = t.pet.name if t.pet else "(unassigned)"
        time_attr = getattr(t, "time", None)
        return f"{t.name} (pet={pet_name}, dur={t.time_duration}h, freq={t.frequency}, time={time_attr})"

    all_tasks = owner.get_all_tasks(incomplete_only=False)
    print("Unsorted tasks:")
    for t in all_tasks:
        print(f" - {format_task(t)}")

    # Sort by duration
    print("\nSorted by duration:")
    for t in scheduler.sort_by_duration(all_tasks):
        print(f" - {t.name}: {t.time_duration}h")

    # Sort by explicit time (falls back to duration)
    print("\nSorted by time:")
    for t in scheduler.sort_by_time(all_tasks):
        print(f" - {t.name}: time={getattr(t, 'time', None)}, dur={t.time_duration}h")

    # Filter tasks for dog and due-only recurring tasks
    print("\nFiltered (pet=Fido, due_only=True):")
    for t in scheduler.get_filtered_tasks(pet_name="Fido", due_only=True):
        print(f" - {t.name}: due={t.is_due()}, freq={t.frequency}")

    # Priority tasks (due + sorted)
    print("\nPriority (due) tasks:")
    for t in scheduler.priority_tasks():
        pet_name = t.pet.name if t.pet else "(unassigned)"
        print(f" - {t.name} (pet={pet_name}, dur={t.time_duration}h, freq={t.frequency})")

    # Generate plan and show conflicts
    result = scheduler.generate_plan(include_conflicts=True)
    plan = result.get("plan")
    conflicts = result.get("conflicts")

    print("\nGenerated Plan:")
    if not plan:
        print("  No tasks fit into available time.")
    else:
        for pet_name, tasks in plan.items():
            print(f"- {pet_name}:")
            for task_name in tasks:
                print(f"    - {task_name}")

    print("\nConflicts:")
    def format_conflict_entry(item) -> str:
        if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[0], Task) and isinstance(item[1], Task):
            a, b = item
            return f"{a.name} (pet={a.pet.name if a.pet else '(unassigned)'}) <-> {b.name} (pet={b.pet.name if b.pet else '(unassigned)'})"
        if isinstance(item, Task):
            return item.name
        return str(item)

    for k, items in conflicts.items():
        formatted = [format_conflict_entry(it) for it in items]
        print(f" {k}: {formatted}")


if __name__ == "__main__":
    demo_schedule()
