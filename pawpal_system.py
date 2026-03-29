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
    
    def get_adjusted_task_duration(self, task):
        """Calculate task duration adjusted for owner experience (Improvement #1)."""
        base_duration = task.time_duration()
        # Experienced owners complete tasks faster: 5% reduction per year, min 50%
        experience_factor = 1 - (self.years_experience * 0.05)
        experience_factor = max(0.5, experience_factor)
        return int(base_duration * experience_factor)
    
    def get_fatigue_adjusted_capacity(self, hours_worked=0):
        """Get available time adjusted for fatigue (Improvement #12)."""
        base_capacity = self.daily_hours * 60  # in minutes
        
        # Efficiency drops after 2-3 hours of continuous work
        if hours_worked >= 6:
            fatigue_factor = 0.7  # 30% efficiency loss
        elif hours_worked >= 3:
            fatigue_factor = 0.85  # 15% efficiency loss
        else:
            fatigue_factor = 1.0  # No loss
        
        return int(base_capacity * fatigue_factor)
    
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
    
    def __init__(self, description, time, frequency, associated_pet=None, criticality="normal", dependencies=None):
        self.description = description
        self.time = time  # Duration in minutes
        self.frequency = frequency  # Daily, Weekly, etc.
        self.associated_pet = associated_pet
        self.is_completed = False
        self.criticality = criticality  # "low", "normal", "high", "critical"
        self.dependencies = dependencies or []  # List of task descriptions that must complete first
        self.last_completed_date = None
        from datetime import datetime
        self.created_date = datetime.now()
    
    def time_duration(self):
        """Return the time duration of the task."""
        return self.time
    
    def pet_priority(self):
        """Return priority based on frequency, criticality, and days overdue (Improvement #9, #11)."""
        from datetime import datetime, timedelta
        
        priority_map = {"Daily": 3, "Weekly": 2, "Monthly": 1}
        base_priority = priority_map.get(self.frequency, 1)
        
        # Don't prioritize completed tasks
        if self.is_completed:
            return 0
        
        # Add criticality boost (Improvement #9)
        criticality_boost = {"critical": 5, "high": 3, "normal": 0, "low": -1}
        priority_score = base_priority + criticality_boost.get(self.criticality, 0)
        
        # Add days overdue penalty (Improvement #11)
        if self.last_completed_date:
            days_since_completion = (datetime.now() - self.last_completed_date).days
            if self.frequency == "Daily" and days_since_completion > 0:
                priority_score += days_since_completion * 2
            elif self.frequency == "Weekly" and days_since_completion > 7:
                priority_score += (days_since_completion - 7)
        
        return priority_score
    
    def set_pet(self, pet):
        """Associate the task with a pet."""
        self.associated_pet = pet
    
    def get_pet(self):
        """Return the associated pet."""
        return self.associated_pet
    
    def mark_completed(self):
        """Mark the task as completed and create next occurrence for recurring tasks."""
        # FIX #1: Only mark completed if not already completed (prevents double creation)
        if self.is_completed:
            return
        
        self.is_completed = True
        from datetime import datetime
        self.last_completed_date = datetime.now()
        
        # Auto-create next occurrence for recurring tasks (Daily, Weekly)
        if self.frequency in ["Daily", "Weekly"]:
            self.create_next_occurrence()
    
    def create_next_occurrence(self):
        """Create a new task for the next occurrence of this recurring task.
        
        For Daily tasks: creates a task for tomorrow
        For Weekly tasks: creates a task for next week
        
        Returns:
            Task: A new Task instance for the next occurrence, or None if not a recurring task
        """
        if self.frequency not in ["Daily", "Weekly"]:
            return None
        
        # Create new task with same properties
        next_task = Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            associated_pet=self.associated_pet,
            criticality=self.criticality,
            dependencies=self.dependencies.copy() if self.dependencies else []
        )
        
        # Add the new task to the pet if it exists
        if self.associated_pet:
            self.associated_pet.add_task(next_task)
        
        return next_task
    
    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.is_completed = False
    
    def has_dependencies_met(self, scheduled_tasks):
        """Check if all dependent tasks have been scheduled (Improvement #6)."""
        scheduled_descriptions = [t.description for t in scheduled_tasks]
        return all(dep in scheduled_descriptions for dep in self.dependencies)
    
    def __str__(self):
        status = "✓" if self.is_completed else "○"
        criticality_str = f" [{self.criticality.upper()}]" if self.criticality != "normal" else ""
        return f"{status} {self.description} ({self.time} min, {self.frequency}){criticality_str}"


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    
    def __init__(self, owner, tasks_list=None):
        self.owner = owner
        self.tasks_list = tasks_list if tasks_list is not None else []
        self._cached_total_time = None
        self._cache_valid = False
    
    @property
    def time_avail(self):
        """Derived from owner's daily_hours (in minutes)."""
        return self.owner.daily_hours * 60 if self.owner else 0
    
    def _invalidate_cache(self):
        """Invalidate cache when tasks change (Improvement #7)."""
        self._cache_valid = False
        self._cached_total_time = None
    
    def add_task(self, task):
        """Add a task to the scheduler."""
        self.tasks_list.append(task)
        self._invalidate_cache()
    
    def remove_task(self, task):
        """Remove a task from the scheduler."""
        if task in self.tasks_list:
            self.tasks_list.remove(task)
            self._invalidate_cache()
    
    def retrieve_all_tasks(self):
        """Retrieve all tasks from owner's pets."""
        return self.owner.get_all_tasks() if self.owner else []
    
    def retrieve_pending_tasks(self):
        """Retrieve all pending tasks from owner's pets."""
        # FIX #2: Invalidate cache when retrieving pending tasks
        self._invalidate_cache()
        return self.owner.get_all_pending_tasks() if self.owner else []
    
    def priority_tasks(self):
        """Return tasks sorted by priority (highest first) using improved scoring."""
        pending_tasks = self.retrieve_pending_tasks()
        # Sort by new priority scoring algorithm (Improvements #9, #11)
        return sorted(pending_tasks, key=lambda t: t.pet_priority(), reverse=True)
    
    def sort_by_time(self, ascending=True):
        """Sort pending tasks by duration/time (Improvement #3 enhancement).
        
        Args:
            ascending (bool): If True, sorts shortest tasks first (ascending).
                            If False, sorts longest tasks first (descending).
        
        Returns:
            list: Sorted list of pending tasks
        """
        # FIX #3: Implement sort_by_time() method
        pending_tasks = self.retrieve_pending_tasks()
        return sorted(pending_tasks, key=lambda t: t.time_duration(), reverse=not ascending)
    
    def filter_tasks(self, status=None, pet_name=None):
        """Filter tasks by completion status or pet name.
        
        Args:
            status (str): Filter by task status. Options: "completed", "pending", or None (all tasks)
            pet_name (str): Filter by pet name. If None, includes all pets.
        
        Returns:
            list: Filtered list of tasks matching the criteria
        
        Examples:
            # Get all completed tasks
            completed = scheduler.filter_tasks(status="completed")
            
            # Get pending tasks for a specific pet
            max_pending = scheduler.filter_tasks(status="pending", pet_name="Max")
            
            # Get all tasks for a pet regardless of status
            all_pet_tasks = scheduler.filter_tasks(pet_name="Whiskers")
        """
        all_tasks = self.retrieve_all_tasks()
        filtered = all_tasks
        
        # Filter by status
        if status == "completed":
            filtered = [t for t in filtered if t.is_completed]
        elif status == "pending":
            filtered = [t for t in filtered if not t.is_completed]
        
        # Filter by pet name
        if pet_name is not None:
            filtered = [t for t in filtered if t.get_pet() and t.get_pet().getName() == pet_name]
        
        return filtered
    
    def get_recurring_tasks(self):
        """Get all recurring tasks (Daily or Weekly) that will auto-generate next occurrences.
        
        Returns:
            list: List of recurring tasks
        """
        all_tasks = self.retrieve_all_tasks()
        return [t for t in all_tasks if t.frequency in ["Daily", "Weekly"]]
    
    def mark_task_complete_with_auto_create(self, task):
        """Mark a task as complete and trigger auto-creation of next occurrence if recurring.
        
        Args:
            task (Task): The task to mark as completed
        
        Returns:
            dict: Information about the completion and any new task created
                {
                    "completed_task": task,
                    "next_occurrence": next_task or None,
                    "is_recurring": bool,
                    "created_new": bool
                }
        """
        is_recurring = task.frequency in ["Daily", "Weekly"]
        next_task = None
        created_new = False
        
        # Mark task as completed (this also auto-creates next occurrence)
        task.mark_completed()
        
        # Check if new task was created
        if is_recurring and task.associated_pet:
            pending_tasks = task.associated_pet.get_pending_tasks()
            # The next occurrence should be the most recently added pending task
            if pending_tasks:
                next_task = pending_tasks[-1]
                created_new = (next_task is not None and next_task != task)
        
        return {
            "completed_task": task,
            "next_occurrence": next_task,
            "is_recurring": is_recurring,
            "created_new": created_new
        }
    
    def detect_time_conflicts(self, scheduled_tasks=None):
        """Detect if two or more tasks are scheduled at the same time.
        
        Args:
            scheduled_tasks (list): List of tasks to check for conflicts. 
                                  If None, uses the current schedule.
        
        Returns:
            list: List of conflict groups. Each group contains:
                {
                    "tasks": [list of overlapping tasks],
                    "conflicting_pets": [list of pet names],
                    "start_time": start_minute,
                    "end_time": end_minute,
                    "overlap_duration": duration in minutes,
                    "same_pet": bool (True if all tasks are for same pet)
                }
        """
        # FIX #4: Detect time conflicts properly
        if scheduled_tasks is None:
            scheduled_tasks = self.schedule_tasks()
        
        conflicts = []
        
        # Filter out None tasks
        scheduled_tasks = [t for t in scheduled_tasks if t is not None]
        
        if len(scheduled_tasks) < 2:
            return conflicts
        
        # Build time slots for each task
        time_slots = []
        current_time = 0
        for task in scheduled_tasks:
            task_start = current_time
            task_end = current_time + task.time_duration()
            time_slots.append({
                "task": task,
                "start": task_start,
                "end": task_end,
                "pet": task.get_pet()
            })
            current_time = task_end
        
        # Check for overlaps between each pair of tasks
        for i in range(len(time_slots)):
            for j in range(i + 1, len(time_slots)):
                slot_i = time_slots[i]
                slot_j = time_slots[j]
                
                # Check if time ranges overlap
                if slot_i["start"] < slot_j["end"] and slot_j["start"] < slot_i["end"]:
                    # Calculate overlap
                    overlap_start = max(slot_i["start"], slot_j["start"])
                    overlap_end = min(slot_i["end"], slot_j["end"])
                    overlap_duration = overlap_end - overlap_start
                    
                    # Check if both tasks are for same pet
                    same_pet = slot_i["pet"] == slot_j["pet"]
                    
                    pet_names = []
                    if slot_i["pet"]:
                        pet_names.append(slot_i["pet"].getName())
                    if slot_j["pet"] and slot_j["pet"] != slot_i["pet"]:
                        pet_names.append(slot_j["pet"].getName())
                    
                    conflict = {
                        "tasks": [slot_i["task"], slot_j["task"]],
                        "conflicting_pets": pet_names,
                        "start_time": overlap_start,
                        "end_time": overlap_end,
                        "overlap_duration": overlap_duration,
                        "same_pet": same_pet
                    }
                    
                    conflicts.append(conflict)
        
        return conflicts
    
    def find_overlapping_tasks_for_pet(self, pet_name, scheduled_tasks=None):
        """Find all tasks scheduled at overlapping times for a specific pet.
        
        Args:
            pet_name (str): The name of the pet to check
            scheduled_tasks (list): List of tasks to check. If None, uses current schedule.
        
        Returns:
            list: List of dictionaries with overlapping task info for the specified pet
                {
                    "task1": Task,
                    "task2": Task,
                    "start_time": minute,
                    "end_time": minute,
                    "duration": minutes
                }
        """
        if scheduled_tasks is None:
            scheduled_tasks = self.schedule_tasks()
        
        conflicts = self.detect_time_conflicts(scheduled_tasks)
        pet_conflicts = []
        
        for conflict in conflicts:
            # Include conflicts if the pet is involved
            if pet_name in conflict["conflicting_pets"]:
                pet_conflicts.append({
                    "task1": conflict["tasks"][0],
                    "task2": conflict["tasks"][1],
                    "start_time": conflict["start_time"],
                    "end_time": conflict["end_time"],
                    "duration": conflict["overlap_duration"],
                    "same_pet": conflict["same_pet"],
                    "other_pet": conflict["conflicting_pets"][0] if len(conflict["conflicting_pets"]) > 0 else None
                })
        
        return pet_conflicts
    
    def has_scheduling_conflicts(self, scheduled_tasks=None):
        """Quick check to see if any scheduling conflicts exist.
        
        Args:
            scheduled_tasks (list): List of tasks to check. If None, uses current schedule.
        
        Returns:
            bool: True if any conflicts found, False otherwise
        """
        conflicts = self.detect_time_conflicts(scheduled_tasks)
        return len(conflicts) > 0
    
    def _get_pet_name(self, task):
        """Helper method to safely extract pet name from task (simplifies repeated logic)."""
        if task and task.get_pet():
            return task.get_pet().getName()
        return "Unknown"
    
    def _format_conflict_detail(self, idx, conflict):
        """Helper method to format a single conflict (improves readability)."""
        task1, task2 = conflict["tasks"]
        pet1 = self._get_pet_name(task1)
        pet2 = self._get_pet_name(task2)
        
        same_pet_indicator = " (same pet)" if conflict["same_pet"] else ""
        
        return (
            f"Conflict #{idx}:\n"
            f"  • Time: {conflict['start_time']}-{conflict['end_time']} min "
            f"(overlap: {conflict['overlap_duration']} min)\n"
            f"  • Task 1: [{pet1}] {task1.description}\n"
            f"  • Task 2: [{pet2}] {task2.description}{same_pet_indicator}\n"
        )
    
    def get_conflict_summary(self, scheduled_tasks=None):
        """Get a human-readable summary of scheduling conflicts (simplified & optimized).
        
        Args:
            scheduled_tasks (list): List of tasks to check. If None, uses current schedule.
        
        Returns:
            str: Formatted summary of conflicts
        """
        conflicts = self.detect_time_conflicts(scheduled_tasks)
        
        if not conflicts:
            return "✓ No scheduling conflicts detected!"
        
        # Build summary using list of conflict details (more efficient than repeated concatenation)
        conflict_details = [self._format_conflict_detail(idx, conflict) for idx, conflict in enumerate(conflicts, 1)]
        
        summary = f"⚠️  Found {len(conflicts)} scheduling conflict(s):\n\n"
        summary += "\n".join(conflict_details)
        
        return summary
    
    def lightweight_conflict_check(self, scheduled_tasks=None):
        """Lightweight conflict detection with graceful error handling.
        
        This method safely checks for conflicts without crashing, returning warnings
        instead of raising exceptions. Ideal for production/UI use.
        
        Args:
            scheduled_tasks (list): List of tasks to check. If None, uses current schedule.
        
        Returns:
            dict: Status information
                {
                    "success": bool,
                    "has_conflicts": bool,
                    "warning_count": int,
                    "critical_count": int,
                    "warnings": [list of warning messages],
                    "conflicts": [list of conflict details or empty],
                    "status_message": str (human-readable summary)
                }
        """
        # FIX #5: Enhanced conflict checking with proper warnings
        result = {
            "success": True,
            "has_conflicts": False,
            "warning_count": 0,
            "critical_count": 0,
            "warnings": [],
            "conflicts": [],
            "status_message": "✓ Schedule validated successfully"
        }
        
        try:
            # Get scheduled tasks safely
            if scheduled_tasks is None:
                try:
                    scheduled_tasks = self.schedule_tasks()
                except Exception as e:
                    result["success"] = False
                    result["warnings"].append(f"⚠️ Could not generate schedule: {str(e)}")
                    result["status_message"] = "⚠️ Schedule generation failed with warning"
                    return result
            
            # Validate input
            if not scheduled_tasks or len(scheduled_tasks) == 0:
                result["status_message"] = "ℹ️ No tasks scheduled"
                return result
            
            # Filter out None tasks
            scheduled_tasks = [t for t in scheduled_tasks if t is not None]
            
            # Check for basic data integrity issues
            for task in scheduled_tasks:
                if task is None:
                    result["warnings"].append("⚠️ Null task found in schedule")
                    result["warning_count"] += 1
                elif task.time_duration() <= 0:
                    result["warnings"].append(f"⚠️ Task '{task.description}' has invalid duration: {task.time_duration()}")
                    result["warning_count"] += 1
                elif task.time_duration() > 1440:  # More than 24 hours
                    result["warnings"].append(f"⚠️ Task '{task.description}' duration ({task.time_duration()} min) exceeds 24 hours")
                    result["warning_count"] += 1
            
            if len(scheduled_tasks) < 2:
                result["status_message"] = "ℹ️ Only one task scheduled - no conflicts possible"
                return result
            
            # Detect actual time conflicts
            try:
                conflicts = self.detect_time_conflicts(scheduled_tasks)
                
                if conflicts:
                    result["has_conflicts"] = True
                    result["critical_count"] = len(conflicts)
                    result["conflicts"] = conflicts
                    
                    # Build warning messages for each conflict
                    for idx, conflict in enumerate(conflicts, 1):
                        try:
                            task1, task2 = conflict.get("tasks", [None, None])
                            
                            if task1 is None or task2 is None:
                                result["warnings"].append(f"⚠️ Conflict #{idx}: Invalid task reference")
                                continue
                            
                            pet1_name = task1.get_pet().getName() if task1.get_pet() else "Unknown"
                            pet2_name = task2.get_pet().getName() if task2.get_pet() else "Unknown"
                            overlap_duration = conflict.get("overlap_duration", 0)
                            
                            same_pet = conflict.get("same_pet", False)
                            pet_info = " (SAME PET - double booking!)" if same_pet else ""
                            
                            warning_msg = (
                                f"🔴 Conflict #{idx}: [{pet1_name}] {task1.description} "
                                f"overlaps with [{pet2_name}] {task2.description} "
                                f"by {overlap_duration} min{pet_info}"
                            )
                            result["warnings"].append(warning_msg)
                        except Exception as e:
                            result["warnings"].append(f"⚠️ Error processing conflict #{idx}: {str(e)}")
                    
                    result["status_message"] = f"🔴 Schedule has {len(conflicts)} conflict(s)"
                else:
                    result["status_message"] = "✓ No scheduling conflicts detected"
            
            except Exception as e:
                result["warnings"].append(f"⚠️ Conflict detection error: {str(e)}")
                result["warning_count"] += 1
                result["status_message"] = "⚠️ Conflict check completed with warnings"
        
        except Exception as e:
            result["success"] = False
            result["warnings"].append(f"❌ Unexpected error during conflict check: {str(e)}")
            result["status_message"] = "❌ Conflict check failed"
        
        return result
    
    def get_lightweight_report(self, scheduled_tasks=None):
        """Get a formatted report from lightweight conflict check.
        
        Args:
            scheduled_tasks (list): List of tasks to check. If None, uses current schedule.
        
        Returns:
            str: Formatted report for display
        """
        check_result = self.lightweight_conflict_check(scheduled_tasks)
        
        report = f"\n{'='*70}\n"
        report += f"SCHEDULE VALIDATION REPORT\n"
        report += f"{'='*70}\n\n"
        
        report += f"Status: {check_result['status_message']}\n"
        report += f"Success: {'✓ Yes' if check_result['success'] else '✗ No'}\n"
        report += f"Conflicts Found: {check_result['critical_count']}\n"
        report += f"Warnings: {check_result['warning_count']}\n\n"
        
        if check_result["warnings"]:
            report += f"{'='*70}\n"
            report += "WARNINGS & ISSUES:\n"
            report += f"{'='*70}\n"
            for warning in check_result["warnings"]:
                report += f"{warning}\n"
        else:
            report += "✓ No warnings or issues detected\n"
        
        report += f"\n{'='*70}\n"
        return report
    
    def is_feasible(self):
        """Validate if all pending tasks can fit within owner's time constraints."""
        total_time = sum(task.time_duration() for task in self.retrieve_pending_tasks())
        available_minutes = self.time_avail
        return total_time <= available_minutes
    
    def get_cached_total_time(self):
        """Return cached total time calculation (Improvement #7)."""
        # FIX #6: Recalculate cache when invalid
        if not self._cache_valid:
            self._cached_total_time = sum(task.time_duration() for task in self.retrieve_pending_tasks())
            self._cache_valid = True
        return self._cached_total_time
    
    def _schedule_with_gap_filling(self, prioritized_tasks):
        """Schedule large tasks first, then fill gaps with small ones (Improvement #3)."""
        # Separate tasks by size
        large_tasks = [t for t in prioritized_tasks if t.time_duration() > 20]
        small_tasks = [t for t in prioritized_tasks if t.time_duration() <= 20]
        
        scheduled = []
        remaining_time = self.time_avail
        
        # First, schedule large tasks
        for task in large_tasks:
            if task.time_duration() <= remaining_time:
                scheduled.append(task)
                remaining_time -= task.time_duration()
        
        # Then fill gaps with small tasks
        for task in small_tasks:
            if task.time_duration() <= remaining_time:
                scheduled.append(task)
                remaining_time -= task.time_duration()
        
        return scheduled, remaining_time
    
    def _schedule_clustered_by_pet(self, prioritized_tasks):
        """Schedule tasks grouped by pet for efficiency (Improvement #2)."""
        # Group tasks by pet
        pet_tasks = {}
        for task in prioritized_tasks:
            pet = task.get_pet()
            if pet not in pet_tasks:
                pet_tasks[pet] = []
            pet_tasks[pet].append(task)
        
        # Schedule pet clusters
        scheduled = []
        remaining_time = self.time_avail
        
        for pet, tasks in pet_tasks.items():
            for task in tasks:
                if task.time_duration() <= remaining_time:
                    scheduled.append(task)
                    remaining_time -= task.time_duration()
        
        return scheduled
    
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
    
    def schedule_tasks_with_breaks(self):
        """Schedule with automatic breaks every 60 minutes (Improvement #4)."""
        scheduled_tasks = self.schedule_tasks()
        total_work_time = sum(t.time_duration() for t in scheduled_tasks)
        
        # Calculate break time needed
        num_breaks = max(0, total_work_time // 60)
        break_duration = num_breaks * 10
        
        feasible_with_breaks = (total_work_time + break_duration) <= self.time_avail
        
        return scheduled_tasks, num_breaks, break_duration, feasible_with_breaks
    
    def get_parallelizable_tasks(self):
        """Return groups of tasks that can be done simultaneously (Improvement #10)."""
        pending = self.retrieve_pending_tasks()
        parallelizable_groups = []
        
        # Group tasks from different pets that can happen at same time
        used = set()
        for i, task1 in enumerate(pending):
            if i in used:
                continue
            group = [task1]
            for j, task2 in enumerate(pending[i+1:], i+1):
                if j in used:
                    continue
                # Can parallelize if different pets
                if task1.get_pet() != task2.get_pet():
                    group.append(task2)
                    used.add(j)
            if len(group) > 1:
                parallelizable_groups.append(group)
            used.add(i)
        
        return parallelizable_groups
    
    def get_unscheduled_tasks_with_reasons(self):
        """Return unscheduled tasks with reasons why (Improvement #8)."""
        scheduled = self.schedule_tasks()
        pending = self.retrieve_pending_tasks()
        unscheduled = [t for t in pending if t not in scheduled]
        
        reasons = []
        remaining_time = self.time_avail - sum(t.time_duration() for t in scheduled)
        
        for task in unscheduled:
            if task.time_duration() > remaining_time:
                reason = f"Insufficient time ({task.time_duration()} min needed, {remaining_time} min available)"
            elif task.dependencies and not task.has_dependencies_met(scheduled):
                reason = "Dependent tasks not scheduled"
            else:
                reason = "Lower priority than scheduled tasks"
            
            reasons.append({
                "task": task,
                "reason": reason,
                "pet": task.get_pet().getName() if task.get_pet() else "Unknown"
            })
        
        return reasons
    
    def get_priority_by_time_of_day(self, hour=0):
        """Adjust task priority based on time of day (Improvement #5)."""
        # Morning (0-12): Exercise and training priority
        # Afternoon (12-18): Mixed tasks
        # Evening (18-24): Feeding and grooming priority
        
        morning_boost = ["walk", "exercise", "training", "play"]
        evening_boost = ["feed", "eating", "groom", "clean"]
        
        time_of_day_adjustments = []
        for task in self.retrieve_pending_tasks():
            desc_lower = task.description.lower()
            adjustment = 0
            
            if hour < 12:  # Morning
                if any(keyword in desc_lower for keyword in morning_boost):
                    adjustment = 2
            elif hour >= 18:  # Evening
                if any(keyword in desc_lower for keyword in evening_boost):
                    adjustment = 2
            
            time_of_day_adjustments.append({
                "task": task,
                "adjustment": adjustment,
                "adjusted_priority": task.pet_priority() + adjustment
            })
        
        return sorted(time_of_day_adjustments, key=lambda x: x["adjusted_priority"], reverse=True)
    
    def generate_plan(self):
        """Generate a readable daily plan for all pets."""
        scheduled_tasks = self.schedule_tasks()
        total_scheduled_time = sum(task.time_duration() for task in scheduled_tasks)
        available_time = self.time_avail
        
        plan = f"\n{'='*70}\n"
        plan += f"DAILY PLAN FOR {self.owner.getName()}\n"
        plan += f"Available Time: {available_time // 60} hours ({available_time} min)\n"
        plan += f"Scheduled Time: {total_scheduled_time} min | Remaining: {available_time - total_scheduled_time} min\n"
        plan += f"{'='*70}\n\n"
        
        if not scheduled_tasks:
            plan += "No tasks scheduled for today.\n"
        else:
            current_time = 0
            for i, task in enumerate(scheduled_tasks, 1):
                pet_name = task.get_pet().getName() if task.get_pet() else "Unknown"
                plan += f"{i}. [{pet_name}] {task.description}\n"
                plan += f"   Duration: {task.time_duration()} min | Frequency: {task.frequency} | Priority: {task.pet_priority()}\n"
                plan += f"   Time slot: {current_time} - {current_time + task.time_duration()} min\n\n"
                current_time += task.time_duration()
        
        # Show unscheduled tasks with reasons
        unscheduled = self.get_unscheduled_tasks_with_reasons()
        if unscheduled:
            plan += f"\n{'='*70}\n"
            plan += "⚠️  UNSCHEDULED TASKS (Could not fit in schedule):\n"
            plan += f"{'='*70}\n\n"
            for item in unscheduled:
                plan += f"• [{item['pet']}] {item['task'].description}\n"
                plan += f"  Reason: {item['reason']}\n\n"
        
        plan += f"{'='*70}\n"
        return plan
    
    def __str__(self):
        pending = len(self.retrieve_pending_tasks())
        return f"Scheduler for {self.owner.getName()} ({pending} pending tasks)"
    
 
