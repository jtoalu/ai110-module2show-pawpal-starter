from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections.abc import Iterable

class Owner:
	def __init__(self, owner_id, name, email):
		"""Initialize an owner and an empty pet list."""
		self.owner_id = owner_id
		self.name = name
		self.email = email
		self.pets = []

	def add_pet(self, pet):
		"""Add a pet to this owner and assign its owner ID."""
		if pet not in self.pets:
			self.pets.append(pet)
			pet.owner_id = self.owner_id

	def remove_pet(self, pet):
		"""Remove a pet from this owner and clear its owner ID."""
		if pet in self.pets:
			self.pets.remove(pet)
			pet.owner_id = None

	def view_tasks(self):
		"""Return the tasks belonging to all of this owner's pets."""
		return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Pet:
	pet_id: int
	name: str
	species: str
	breed: str
	age: int
	owner_id: int | None = None
	tasks: list = field(default_factory=list)

	def add_task(self, task):
		"""Add a task to this pet and assign its pet ID."""
		if task not in self.tasks:
			self.tasks.append(task)
			task.pet_id = self.pet_id

	def remove_task(self, task):
		"""Remove a task from this pet and clear its pet ID."""
		if task in self.tasks:
			self.tasks.remove(task)
			task.pet_id = None

	def get_tasks(self):
		"""Return this pet's task list."""
		return self.tasks


@dataclass
class Task:
	task_id: int
	title: str
	description: str
	due_date: datetime
	priority: str
	duration_minutes: int = 30
	completed: bool = False
	pet_id: int | None = None
	recurrence: str | None = None  # "daily", "weekly", or None
	completed_at: datetime | None = None

	def complete(self, completed_at: datetime | None = None):
		"""Mark this task as completed and record when it was completed."""
		self.completed = True
		self.completed_at = completed_at or datetime.now()

	def is_overdue(self):
		"""Return whether this incomplete task is past its due date."""
		return not self.completed and self.due_date < datetime.now()

	def update_task(self):
		"""Return this task after an update."""
		return self

def sort_tasks(tasks: Iterable[Task]) -> list[Task]:
		return sorted(tasks, key=lambda task: (task.due_date, task.task_id))


class Scheduler:
	def __init__(self):
		"""Initialize an empty task scheduler."""
		self.tasks = []

	def schedule_task(self, task):
		"""Add a task unless it conflicts; warn instead of raising an error."""
		if task in self.tasks:
			return True
		
		conflict = self._find_conflict(task)
		if conflict is not None:
			print(
                f"Warning: {task.title!r} conflicts with "
                f"{conflict.title!r}; task was not scheduled."
            )
			return False
		self.tasks.append(task)
		return True
		
	def _find_conflict(self, task):
		"""Return an existing incomplete task that overlaps this task."""
		new_end = task.due_date + timedelta(minutes=task.duration_minutes)
		
		for existing_task in self.tasks:
			if existing_task.completed:
				continue
			existing_end = existing_task.due_date + timedelta(
                minutes=existing_task.duration_minutes
            )
			if task.due_date < existing_end and existing_task.due_date < new_end:
				return existing_task
				
			return None

	def remove_task(self, task):
		"""Remove a task from the schedule if it is present."""
		if task in self.tasks:
			self.tasks.remove(task)

	def get_upcoming_tasks(self):
		"""Return incomplete scheduled tasks ordered by due date."""
		return sorted(
			(task for task in self.tasks 
				if not task.completed and task.due_date >= datetime.now()
			),
			key=lambda task: task.due_date,
		)

	def get_overdue_tasks(self):
		"""Return incomplete scheduled tasks that are past their due date."""
		now = datetime.now()
		return sorted(
			[task for task in self.tasks 
				if task.is_overdue()], key=lambda task: task.due_date
		)

	def prioritize_tasks(self):
		"""Return scheduled tasks ordered by priority and due date."""
		priority_order = {"high": 0, "medium": 1, "low": 2}
		return sorted(
			self.tasks,
			key=lambda task: (priority_order.get(task.priority.lower(), 1), task.due_date),
		)

	def mark_task_complete(self, task):
		"""Complete a task and schedule its next daily or weekly occurrence."""
		if task not in self.tasks or task.completed:
			return None
			
		recurrence = (task.recurrence or "").lower()
		if recurrence not in {"daily", "weekly"}:
			task.complete()
			return None

		completed_at = datetime.now()

		if recurrence == "daily":
			next_due_date = completed_at + timedelta(days=1)
		else:  # weekly
			next_due_date = task.due_date + timedelta(days=7)

		next_task = Task(
            task_id=max((item.task_id for item in self.tasks), default=0) + 1,
            title=task.title,
            description=task.description,
            due_date=next_due_date,
            priority=task.priority,
            duration_minutes=task.duration_minutes,
            pet_id=task.pet_id,
            recurrence=recurrence,
        )
		
		if not self.schedule_task(next_task):
			raise ValueError(
				f"Could not schedule the next occurrence of {task.title!r}: "
				"it conflicts with another task."
            )
			
		task.complete()
		return next_task

	def _conflicts_with_existing(self, task):
		"""Return whether the task overlaps an existing scheduled task."""
		new_end = task.due_date + timedelta(minutes=task.duration_minutes)
		for existing_task in self.tasks:
			existing_end = existing_task.due_date + timedelta(
				minutes=existing_task.duration_minutes
			)
			if task.due_date < existing_end and existing_task.due_date < new_end:
				return True
		return False
