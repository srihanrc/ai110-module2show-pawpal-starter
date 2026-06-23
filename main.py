from diagrams.pawpal_system import PetOwner, Pet, Task, Scheduler


def demo_schedule() -> None:
    owner = PetOwner("Alex", years_experience=3, daily_hours=2.0)

    # Create pets
    dog = Pet("Fido", "Dog", "Kibble", ["none"])
    cat = Pet("Mittens", "Cat", "Wet Food", [])

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks (different durations)
    t1 = Task("Morning Walk", "Walk around the neighborhood", 0.5, frequency="daily", pet=dog)
    t2 = Task("Feed Dog", "Give breakfast and water", 0.15, frequency="daily", pet=dog)
    t3 = Task("Feed Cat", "Serve wet food", 0.1, frequency="daily", pet=cat)

    # Add tasks to pets
    dog.add_task(t1)
    dog.add_task(t2)
    cat.add_task(t3)

    # Create scheduler and produce today's plan
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    print("Today's Schedule:")
    if not plan:
        print("  No tasks fit into available time.")
        return

    for pet_name, tasks in plan.items():
        print(f"- {pet_name}:")
        for task_name in tasks:
            print(f"    - {task_name}")


if __name__ == "__main__":
    demo_schedule()
