from __future__ import annotations
from typing import List, Optional, Dict
from datetime import datetime, timedelta


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

	def __init__(self, name: str, description: str, time_duration: float, frequency: Optional[str] = None, pet: Optional[Pet] = None, last_completed: Optional[datetime] = None) -> None:
		self.name: str = name
		self.description: str = description
		self.time_duration: float = float(time_duration)
		self.frequency: Optional[str] = frequency
		self.completed: bool = False
		self.pet: Optional[Pet] = pet
		self.last_completed: Optional[datetime] = last_completed

	def time_duration_hours(self) -> float:
		return self.time_duration

	def mark_complete(self) -> None:
		self.completed = True
		self.last_completed = datetime.now()
		# If this is a recurring task, create the next occurrence and attach to the same pet
		if self.frequency and self.pet is not None:
			freq = self.frequency.lower()
			if freq == "daily":
				interval = timedelta(days=1)
			elif freq == "weekly":
				interval = timedelta(days=7)
			elif freq == "monthly":
				interval = timedelta(days=30)
			else:
				interval = None
			if interval is not None:
				next_time = self.last_completed + interval
				new_task = Task(self.name, self.description, self.time_duration, frequency=self.frequency, pet=self.pet)
				# attach an explicit time for the next occurrence if a time was present
				if hasattr(self, "time"):
					new_task.time = next_time
				self.pet.add_task(new_task)

	def mark_pending(self) -> None:
		self.completed = False
		self.last_completed = None

	def is_completed(self) -> bool:
		return bool(self.completed)

	def is_due(self, reference: Optional[datetime] = None) -> bool:
		"""Return True if the task should be considered for scheduling now.

		A task is due if it is not completed, or if it is recurring and the last
		completion is older than its recurrence interval.
		"""
		reference = reference or datetime.now()
		if not self.frequency:
			# non-recurring: due if not completed
			return not self.completed

		# recurring tasks: if never completed, it's due
		if self.last_completed is None:
			return True

		freq = self.frequency.lower()
		if freq == "daily":
			interval = timedelta(days=1)
		elif freq == "weekly":
			interval = timedelta(days=7)
		elif freq == "monthly":
			interval = timedelta(days=30)
		else:
			# unknown frequency: treat as non-recurring
			return not self.completed

		return (reference - self.last_completed) >= interval

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

	def sort_by_duration(self, tasks: List[Task], descending: bool = False) -> List[Task]:
		"""Return tasks sorted by their duration (hours)."""
		return sorted(tasks, key=lambda t: t.time_duration, reverse=descending)

	def sort_by_time(self, tasks: List[Task], ascending: bool = True) -> List[Task]:
		"""Sort tasks by a `time` attribute if present, otherwise by duration.

		The `time` attribute may be a datetime or a numeric value; datetimes are
		converted to timestamps for ordering. If no `time` attribute exists the
		task's `time_duration` is used as a fallback.
		"""
		def key_fn(t: Task):
			# prefer tasks with explicit time first (0), then tasks without time (1)
			tval = getattr(t, "time", None)
			if isinstance(tval, datetime):
				return (0, float(tval.timestamp()))
			# numeric times
			if tval is not None:
				try:
					return (0, float(tval))
				except Exception:
					pass
			# fallback: place after timed tasks and sort by duration
			return (1, float(t.time_duration))

		return sorted(tasks, key=key_fn, reverse=not ascending)

	def get_filtered_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None, due_only: bool = False) -> List[Task]:
		"""Return tasks filtered by pet name and/or completion status.

		If `due_only` is True, recurring tasks are evaluated for due-ness.
		"""
		tasks = []
		for p in self.owner.pets:
			if pet_name is not None and p.name != pet_name:
				continue
			for t in p.list_tasks(incomplete_only=False):
				if completed is not None and t.completed != completed:
					continue
				if due_only and not t.is_due():
					continue
				tasks.append(t)
		return tasks

	def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> Dict[str, List]:
		"""Perform basic conflict detection and return buckets of problematic tasks.

		Checks:
		- tasks longer than total available time (cannot fit at all)
		- cumulative overflow when packing by priority/duration
		- duplicate task names for the same pet
		"""
		result: Dict[str, List] = {"too_long": [], "overflow": [], "duplicates": [], "time_conflicts": []}
		all_tasks = tasks if tasks is not None else self.owner.get_all_tasks(incomplete_only=False)

		# too long
		for t in all_tasks:
			if t.time_duration > self.time_avail:
				result["too_long"].append(t)

		# duplicates per pet
		names_by_pet: Dict[str, Dict[str, int]] = {}
		for t in all_tasks:
			pet_name = t.pet.name if t.pet is not None else "(unassigned)"
			names_by_pet.setdefault(pet_name, {})
			names_by_pet[pet_name][t.name] = names_by_pet[pet_name].get(t.name, 0) + 1
		for pet, names in names_by_pet.items():
			for name, count in names.items():
				if count > 1:
					# find task objects to report
					for t in all_tasks:
						if (t.pet and t.pet.name == pet) and t.name == name:
							result["duplicates"].append(t)

		# overflow: simulate greedy packing by priority order and mark tasks that would be left out
		sorted_tasks = sorted(all_tasks, key=lambda t: (self._frequency_rank(t.frequency), t.time_duration))
		remaining = float(self.time_avail)
		for t in sorted_tasks:
			if t.time_duration <= remaining:
				remaining -= t.time_duration
			else:
				result["overflow"].append(t)

		# time-based conflicts: sweep-line style (sort by start, track active tasks)
		timed_tasks = sorted(
			[t for t in all_tasks if hasattr(t, "time") and isinstance(getattr(t, "time"), datetime)],
			key=lambda t: t.time,
		)
		active: List[Task] = []
		for t in timed_tasks:
			start_t = t.time
			end_t = start_t + timedelta(hours=t.time_duration)
			# remove finished tasks from active
			active = [a for a in active if (a.time + timedelta(hours=a.time_duration)) > start_t]
			# any remaining active tasks overlap with t
			for a in active:
				result["time_conflicts"].append((a, t))
			active.append(t)

		return result

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
		"""Return all tasks that are due, ordered by frequency then by duration."""
		# include recurring tasks that are due
		tasks = self.owner.get_all_tasks(incomplete_only=False)
		# filter for due tasks
		due_tasks = [t for t in tasks if t.is_due()]
		tasks_sorted = sorted(due_tasks, key=lambda t: (self._frequency_rank(t.frequency), t.time_duration))
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

	def generate_plan(self, include_conflicts: bool = False) -> Dict[str, List[str]]:
		"""Return a mapping from pet name to list of scheduled task names.

		If `include_conflicts` is True, return a dict with keys `plan` and
		`conflicts` where `conflicts` contains the output of `detect_conflicts`.
		"""
		plan: Dict[str, List[str]] = {}
		selected = self.schedule_tasks()
		for t in selected:
			pet_name = t.pet.name if t.pet is not None else "(unassigned)"
			plan.setdefault(pet_name, []).append(t.name)
		if include_conflicts:
			conflicts = self.detect_conflicts(self.owner.get_all_tasks(incomplete_only=False))
			return {"plan": plan, "conflicts": conflicts}
		return plan

