from __future__ import annotations
from typing import List, Optional, Dict


class PetOwner:
	"""Stores owner information and manages multiple pets.

	Attributes:
		name: Owner's name.
		years_experience: Years of pet experience.
		daily_hours: Available hours per day for pet care.
		pets: List of `Pet` instances owned by this owner.
	"""

	def __init__(self, name: str, years_experience: int, daily_hours: float) -> None:
		self.name: str = name
		self.years_experience: int = years_experience
		self.daily_hours: float = daily_hours
		self.pets: List[Pet] = []

	def getName(self) -> str:
		return self.name

	def get_available_time(self) -> float:
		return float(self.daily_hours)

	def check_experience(self) -> bool:
		return self.years_experience >= 0

	def add_pet(self, pet: "Pet") -> None:
		self.pets.append(pet)

	def remove_pet(self, pet_name: str) -> bool:
		for i, p in enumerate(self.pets):
			if p.name == pet_name:
				del self.pets[i]
				return True
		return False

	def get_all_tasks(self, incomplete_only: bool = True) -> List["Task"]:
		"""Return all tasks across all owned pets.

		If `incomplete_only` is True, only returns tasks where `completed` is False.
		"""
		tasks: List[Task] = []
		for p in self.pets:
			tasks.extend(p.list_tasks(incomplete_only=incomplete_only))
		return tasks


class Pet:
	"""Represents a pet and its basic properties and tasks."""

	def __init__(self, name: str, speciesType: str, foodType: str, list_special_needs: Optional[List[str]] = None) -> None:
		self.name: str = name
		self.speciesType: str = speciesType
		self.foodType: str = foodType
		self.list_special_needs: List[str] = list_special_needs or []
		self.tasks: List[Task] = []

	def getName(self) -> str:
		return self.name

	def getType(self) -> str:
		return self.speciesType

	def getFoodType(self) -> str:
		return self.foodType

	def special_needs(self) -> List[str]:
		return list(self.list_special_needs)

	def add_task(self, task: "Task") -> None:
		self.tasks.append(task)

	def remove_task(self, task_name: str) -> bool:
		for i, t in enumerate(self.tasks):
			if t.name == task_name:
				del self.tasks[i]
				return True
		return False

	def list_tasks(self, incomplete_only: bool = True) -> List["Task"]:
		if incomplete_only:
			return [t for t in self.tasks if not t.completed]
		return list(self.tasks)


class Task:
	"""Represents a single activity for a pet.

	Attributes:
		name: Short identifier for the task.
		description: Human-friendly description.
		time_duration: Hours required to complete the task.
		frequency: e.g. "daily", "weekly", or None.
		completed: Completion flag.
		pet: Optional back-reference to the Pet this task belongs to.
	"""

	def __init__(self, name: str, description: str, time_duration: float, frequency: Optional[str] = None, pet: Optional[Pet] = None) -> None:
		self.name: str = name
		self.description: str = description
		self.time_duration: float = float(time_duration)
		self.frequency: Optional[str] = frequency
		self.completed: bool = False
		self.pet: Optional[Pet] = pet

	def time_duration_hours(self) -> float:
		return self.time_duration

	def mark_complete(self) -> None:
		self.completed = True

	def mark_pending(self) -> None:
		self.completed = False

	def is_completed(self) -> bool:
		return bool(self.completed)

	def to_dict(self) -> Dict[str, object]:
		return {
			"name": self.name,
			"description": self.description,
			"time_duration": self.time_duration,
			"frequency": self.frequency,
			"completed": self.completed,
		}


class Scheduler:
	"""The scheduling brain: retrieves, organizes, and manages tasks across pets.

	This implementation keeps the logic simple: it collects incomplete tasks from the
	owner's pets, sorts them by frequency (daily first) and duration, and picks
	tasks until the owner's available time is consumed.
	"""

	def __init__(self, owner: PetOwner, time_avail: Optional[float] = None) -> None:
		self.owner: PetOwner = owner
		self.time_avail: float = time_avail if time_avail is not None else owner.get_available_time()

	def _frequency_rank(self, freq: Optional[str]) -> int:
		if not freq:
			return 10
		f = freq.lower()
		if f == "daily":
			return 0
		if f == "weekly":
			return 1
		if f == "monthly":
			return 2
		return 5

	def priority_tasks(self) -> List[Task]:
		"""Return all incomplete tasks ordered by frequency then by duration."""
		tasks = self.owner.get_all_tasks(incomplete_only=True)
		tasks_sorted = sorted(tasks, key=lambda t: (self._frequency_rank(t.frequency), t.time_duration))
		return tasks_sorted

	def schedule_tasks(self) -> List[Task]:
		"""Select tasks to fit within `self.time_avail` using a simple greedy approach."""
		selected: List[Task] = []
		remaining = float(self.time_avail)
		for t in self.priority_tasks():
			if t.time_duration <= remaining:
				selected.append(t)
				remaining -= t.time_duration
				if remaining <= 1e-6:
					break
		return selected

	def generate_plan(self) -> Dict[str, List[str]]:
		"""Return a mapping from pet name to list of scheduled task names."""
		plan: Dict[str, List[str]] = {}
		for t in self.schedule_tasks():
			pet_name = t.pet.name if t.pet is not None else "(unassigned)"
			plan.setdefault(pet_name, []).append(t.name)
		return plan

