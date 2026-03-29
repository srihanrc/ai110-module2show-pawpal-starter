"""
PawPal Main Script - Demonstrates the pet care scheduling system
"""

from pawpal_system import PetOwner, Pet, Task, Scheduler


def main():
    print("🐾 Welcome to PawPal - Your Pet Care Scheduler 🐾\n")
    
    # Create a Pet Owner
    owner = PetOwner(name="Sarah", daily_hours=4, years_experience=5)
    print(f"Owner Created: {owner}\n")
    
    # Create Pet 1 - Dog
    dog = Pet(
        name="Max",
        speciesType="Dog",
        foodType="Kibble",
        list_special_needs=["Daily exercise", "Medication at 8am"],
        pet_owner=owner
    )
    
    # Create Pet 2 - Cat
    cat = Pet(
        name="Whiskers",
        speciesType="Cat",
        foodType="Wet food",
        list_special_needs=["Indoor only", "Litter box cleaning"],
        pet_owner=owner
    )
    
    # Create Pet 3 - Rabbit
    rabbit = Pet(
        name="Fluffy",
        speciesType="Rabbit",
        foodType="Hay and vegetables",
        list_special_needs=["Temperature control", "Social interaction"],
        pet_owner=owner
    )
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    owner.add_pet(rabbit)
    
    print(f"Pets Created and Added:\n  - {dog}\n  - {cat}\n  - {rabbit}\n")
    
    # Create Tasks for Max (Dog)
    task1 = Task(
        description="Morning walk",
        time=30,
        frequency="Daily",
        associated_pet=dog
    )
    
    task2 = Task(
        description="Evening walk",
        time=30,
        frequency="Daily",
        associated_pet=dog
    )
    
    task3 = Task(
        description="Training session",
        time=20,
        frequency="Daily",
        associated_pet=dog
    )
    
    # Create Tasks for Whiskers (Cat)
    task4 = Task(
        description="Clean litter box",
        time=10,
        frequency="Daily",
        associated_pet=cat
    )
    
    task5 = Task(
        description="Feeding",
        time=15,
        frequency="Daily",
        associated_pet=cat
    )
    
    # Create Tasks for Fluffy (Rabbit)
    task6 = Task(
        description="Feed vegetables and hay",
        time=15,
        frequency="Daily",
        associated_pet=rabbit
    )
    
    task7 = Task(
        description="Cage cleaning",
        time=25,
        frequency="Weekly",
        associated_pet=rabbit
    )
    
    # Create conflicting tasks for DEMO - these will overlap!
    # Task 8: Grooming for Max (will cause time conflict)
    task8 = Task(
        description="Grooming session",
        time=25,
        frequency="Daily",
        associated_pet=dog,
        criticality="high"
    )
    
    # Task 9: Playtime for Max (will also create conflicts)
    task9 = Task(
        description="Playtime with Max",
        time=20,
        frequency="Daily",
        associated_pet=dog
    )
    
    # Add tasks to pets
    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task3)
    dog.add_task(task8)  # Add conflicting task
    dog.add_task(task9)  # Add another conflicting task
    
    cat.add_task(task4)
    cat.add_task(task5)
    
    rabbit.add_task(task6)
    rabbit.add_task(task7)
    
    print("Tasks Created and Added to Pets:\n")
    for pet in owner.get_all_pets():
        print(f"  {pet.getName()}:")
        for task in pet.get_tasks():
            print(f"    - {task}")
        print()
    
    # Create Scheduler
    scheduler = Scheduler(owner)
    
    print(f"\n{scheduler}")
    print(f"Total pending tasks: {len(scheduler.retrieve_pending_tasks())}")
    print(f"Total time required: {owner.get_total_task_time()} minutes")
    print(f"Available time: {scheduler.time_avail} minutes\n")
    
    # Check if schedule is feasible
    if scheduler.is_feasible():
        print("✓ All tasks fit within the available time!\n")
    else:
        print("✗ Warning: Not all tasks fit within the available time.\n")
    
    # Print priority-sorted tasks
    print("Tasks by Priority:")
    for i, task in enumerate(scheduler.priority_tasks(), 1):
        pet_name = task.get_pet().getName()
        print(f"  {i}. [{pet_name}] {task.description} (Priority: {task.pet_priority()})")
    
    # Generate and print the daily schedule
    print(scheduler.generate_plan())
    
    # Test lightweight conflict detection
    print("\n" + "="*70)
    print("CONFLICT DETECTION TEST")
    print("="*70)
    print("\nRunning lightweight conflict check...\n")
    
    # Get lightweight report (handles errors gracefully)
    report = scheduler.get_lightweight_report()
    print(report)
    
    # Get detailed conflict info
    conflict_check = scheduler.lightweight_conflict_check()
    
    print("\nDetailed Conflict Information:")
    print(f"  • Total warnings: {conflict_check['warning_count']}")
    print(f"  • Critical conflicts: {conflict_check['critical_count']}")
    print(f"  • Check successful: {conflict_check['success']}")
    
    if conflict_check['has_conflicts']:
        print("\n⚠️  CONFLICTS DETECTED!")
        for warning in conflict_check['warnings']:
            print(f"    {warning}")
    else:
        print("\n✓ No conflicts found!")
    
    # Mark one task as completed and show updated schedule
    print("\n" + "="*70)
    print("--- Marking 'Morning walk' as completed and auto-creating next occurrence ---")
    print("="*70 + "\n")
    task1.mark_completed()
    print(scheduler.generate_plan())
    
    # Check for conflicts after marking task complete
    print("\n" + "="*70)
    print("CONFLICT CHECK AFTER COMPLETION")
    print("="*70 + "\n")
    updated_report = scheduler.get_lightweight_report()
    print(updated_report)


if __name__ == "__main__":
    main()
