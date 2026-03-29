class PetOwner:
    """Manages multiple pets and provides access to all their tasks."""
    
    def __init__(self, name, daily_hours, years_experience):
        self.name = name
        self.daily_hours = daily_hours
        self.years_experience = years_experience
        self.pets_list = []
    
    def getName(self):
        """Return the owner's name."""
        return self.name
    
    def get_available_time(self):
        """Return available hours per day."""
        return self.daily_hours
    
    def check_experience(self):
        """Return years of experience."""
        return self.years_experience
    
    def add_pet(self, pet):
        """Add a pet to this owner's pet list."""
        pet.set_owner(self)
        self.pets_list.append(pet)
    
    def remove_pet(self, pet):
        """Remove a pet from this owner's pet list."""
        if pet in self.pets_list:
            self.pets_list.remove(pet)
    
    def get_all_pets(self):
        """Return all pets owned by this owner."""
        return self.pets_list
    
    def get_all_tasks(self):
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets_list:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def get_all_pending_tasks(self):
        """Return all pending tasks across all pets."""
        pending_tasks = []
        for pet in self.pets_list:
            pending_tasks.extend(pet.get_pending_tasks())
        return pending_tasks
    
    def get_total_task_time(self):
        """Calculate total time needed for all pending tasks in minutes."""
        total_time = 0
        for task in self.get_all_pending_tasks():
            total_time += task.time_duration()
        return total_time
    
    def __str__(self):
        return f"{self.name} ({self.years_experience} years exp, {self.daily_hours} hrs/day) - {len(self.pets_list)} pets"


class Pet:
    """Stores all pet information and special needs, plus a list of tasks."""
    
    def __init__(self, name, speciesType, foodType, list_special_needs, pet_owner=None):
        self.name = name
        self.speciesType = speciesType
        self.foodType = foodType
        self.list_special_needs = list_special_needs
        self.pet_owner = pet_owner
        self.tasks = []
    
    def getName(self):
        """Return the pet's name."""
        return self.name
    
    def getType(self):
        """Return the pet's species type."""
        return self.speciesType
    
    def getFoodType(self):
        """Return the pet's food type."""
        return self.foodType
    
    def special_needs(self):
        """Return the list of special needs."""
        return self.list_special_needs
    
    def set_owner(self, pet_owner):
        """
        Assign an owner to this pet.
        
        Args:
            pet_owner: The owner object to be assigned to this pet.
        
        Returns:
            None
        """
        """Set the owner of this pet."""
        self.pet_owner = pet_owner
    
    def add_task(self, task):
        """Add a task to this pet's task list."""
        task.set_pet(self)
        self.tasks.append(task)
    
    def remove_task(self, task):
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)
    
    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks
    
    def get_completed_tasks(self):
        """Return only completed tasks."""
        return [task for task in self.tasks if task.is_completed]
    
    def get_pending_tasks(self):
        """Return only pending (incomplete) tasks."""
        return [task for task in self.tasks if not task.is_completed]
    
    def __str__(self):
        return f"{self.name} ({self.speciesType}) - {len(self.tasks)} tasks"


class Task:
    """Represents a single activity (description, time, frequency, completion status)."""
    
    def __init__(self, description, time, frequency, associated_pet=None):
        self.description = description
        self.time = time  # Duration in minutes
        self.frequency = frequency  # Daily, Weekly, etc.
        self.associated_pet = associated_pet
        self.is_completed = False
    
    def time_duration(self):
        """Return the time duration of the task."""
        return self.time
    
    def pet_priority(self):
        """Return priority based on frequency and completion status."""
        priority_map = {"Daily": 3, "Weekly": 2, "Monthly": 1}
        base_priority = priority_map.get(self.frequency, 1)
        return base_priority if not self.is_completed else 0
    
    def set_pet(self, pet):
        """Associate the task with a pet."""
        self.associated_pet = pet
    
    def get_pet(self):
        """Return the associated pet."""
        return self.associated_pet
    
    def mark_completed(self):
        """Mark the task as completed."""
        self.is_completed = True
    
    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.is_completed = False
    
    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.description} ({self.time} min, {self.frequency})"


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    
    def __init__(self, owner, tasks_list=None):
        self.owner = owner
        self.tasks_list = tasks_list if tasks_list is not None else []
    
    @property
    def time_avail(self):
        """Derived from owner's daily_hours (in minutes)."""
        return self.owner.daily_hours * 60 if self.owner else 0
    
    def add_task(self, task):
        """Add a task to the scheduler."""
        self.tasks_list.append(task)
    
    def remove_task(self, task):
        """Remove a task from the scheduler."""
        if task in self.tasks_list:
            self.tasks_list.remove(task)
    
    def retrieve_all_tasks(self):
        """Retrieve all tasks from owner's pets."""
        return self.owner.get_all_tasks() if self.owner else []
    
    def retrieve_pending_tasks(self):
        """Retrieve all pending tasks from owner's pets."""
        return self.owner.get_all_pending_tasks() if self.owner else []
    
    def priority_tasks(self):
        """Return tasks sorted by priority (highest first)."""
        pending_tasks = self.retrieve_pending_tasks()
        # Sort by priority (higher number = higher priority)
        return sorted(pending_tasks, key=lambda t: t.pet_priority(), reverse=True)
    
    def is_feasible(self):
        """Validate if all pending tasks can fit within owner's time constraints."""
        total_time = sum(task.time_duration() for task in self.retrieve_pending_tasks())
        available_minutes = self.time_avail
        return total_time <= available_minutes
    
    def schedule_tasks(self):
        """Organize tasks into a schedule based on priority and availability."""
        prioritized = self.priority_tasks()
        scheduled = []
        remaining_time = self.time_avail
        
        for task in prioritized:
            if task.time_duration() <= remaining_time:
                scheduled.append(task)
                remaining_time -= task.time_duration()
            else:
                break
        
        return scheduled
    
    def generate_plan(self):
        """Generate a readable daily plan for all pets."""
        scheduled_tasks = self.schedule_tasks()
        total_scheduled_time = sum(task.time_duration() for task in scheduled_tasks)
        available_time = self.time_avail
        
        plan = f"\n{'='*60}\n"
        plan += f"DAILY PLAN FOR {self.owner.getName()}\n"
        plan += f"Available Time: {available_time // 60} hours ({available_time} min)\n"
        plan += f"Scheduled Time: {total_scheduled_time} min\n"
        plan += f"{'='*60}\n\n"
        
        if not scheduled_tasks:
            plan += "No tasks scheduled for today.\n"
        else:
            current_time = 0
            for i, task in enumerate(scheduled_tasks, 1):
                pet_name = task.get_pet().getName() if task.get_pet() else "Unknown"
                plan += f"{i}. [{pet_name}] {task.description}\n"
                plan += f"   Duration: {task.time_duration()} min | Frequency: {task.frequency}\n"
                plan += f"   Time slot: {current_time} - {current_time + task.time_duration()} min\n\n"
                current_time += task.time_duration()
        
        plan += f"{'='*60}\n"
        return plan
    
    def __str__(self):
        pending = len(self.retrieve_pending_tasks())
        return f"Scheduler for {self.owner.getName()} ({pending} pending tasks)"
