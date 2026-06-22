from __future__ import annotations
from typing import List, Optional, Dict


class PetOwner:
	"""Stores owner information and availability."""

	def __init__(self, name: str, years_experience: int, daily_hours: float) -> None:
		self.name: str = name
		self.years_experience: int = years_experience
		self.daily_hours: float = daily_hours

	def getName(self) -> str:
		raise NotImplementedError()

	def get_available_time(self) -> float:
		raise NotImplementedError()

	def check_experience(self) -> bool:
		raise NotImplementedError()


class Pet:
	"""Represents a pet and its basic properties."""

	def __init__(self, name: str, speciesType: str, foodType: str, list_special_needs: Optional[List[str]] = None) -> None:
		self.name: str = name
		self.speciesType: str = speciesType
		self.foodType: str = foodType
		self.list_special_needs: List[str] = list_special_needs or []

	def getName(self) -> str:
		raise NotImplementedError()

	def getType(self) -> str:
		raise NotImplementedError()

	def getFoodType(self) -> str:
		raise NotImplementedError()

	def special_needs(self) -> List[str]:
		raise NotImplementedError()


class Task:
	"""A task for a pet (duration and priority)."""

	def __init__(self, name: str, time_duration: float, priority: int, pet: Optional[Pet] = None) -> None:
		self.name: str = name
		self.time_duration_val: float = time_duration
		self.priority: int = priority
		self.pet: Optional[Pet] = pet

	def time_duration(self) -> float:
		raise NotImplementedError()

	def pet_priority(self) -> int:
		raise NotImplementedError()


class Scheduler:
	"""Generates daily plans by prioritizing tasks within time constraints."""

	def __init__(self, owner: PetOwner, pets: Optional[List[Pet]] = None, prior_tasks: Optional[List[Task]] = None, time_avail: Optional[float] = None) -> None:
		self.owner: PetOwner = owner
		self.pets: List[Pet] = pets or []
		self.prior_tasks: List[Task] = prior_tasks or []
		self.time_avail: float = time_avail if time_avail is not None else owner.daily_hours

	def priority_tasks(self) -> List[Task]:
		"""Return tasks ordered by priority (stub)."""
		raise NotImplementedError()

	def schedule_tasks(self) -> List[Task]:
		"""Schedule tasks to fit within available time (stub)."""
		raise NotImplementedError()

	def generate_plan(self) -> Dict[str, List[str]]:
		"""Return a human-readable plan (stub)."""
		raise NotImplementedError()

