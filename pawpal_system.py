from dataclasses import dataclass, field
from datetime import datetime, timedelta


class Owner:
	def __init__(self, owner_id, name, email):
		self.owner_id = owner_id
		self.name = name
		self.email = email
		self.pets = []

	def add_pet(self, pet):
		if pet not in self.pets:
			self.pets.append(pet)
			pet.owner_id = self.owner_id

	def remove_pet(self, pet):
		if pet in self.pets:
			self.pets.remove(pet)
			pet.owner_id = None

	def view_tasks(self):
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
		if task not in self.tasks:
			self.tasks.append(task)
			task.pet_id = self.pet_id

	def remove_task(self, task):
		if task in self.tasks:
			self.tasks.remove(task)
			task.pet_id = None

	def get_tasks(self):
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

	def complete(self):
		self.completed = True

	def is_overdue(self):
		return not self.completed and self.due_date < datetime.now()

	def update_task(self):
		return self


class Scheduler:
	def __init__(self):
		self.tasks = []

	def schedule_task(self, task):
		if task not in self.tasks and not self._conflicts_with_existing(task):
			self.tasks.append(task)
		return task in self.tasks

	def remove_task(self, task):
		if task in self.tasks:
			self.tasks.remove(task)

	def get_upcoming_tasks(self):
		return sorted(
			(task for task in self.tasks if not task.completed),
			key=lambda task: task.due_date,
		)

	def prioritize_tasks(self):
		priority_order = {"high": 0, "medium": 1, "low": 2}
		return sorted(
			self.tasks,
			key=lambda task: (priority_order.get(task.priority.lower(), 1), task.due_date),
		)

	def mark_task_complete(self, task):
		if task in self.tasks:
			task.complete()

	def _conflicts_with_existing(self, task):
		new_end = task.due_date + timedelta(minutes=task.duration_minutes)
		for existing_task in self.tasks:
			existing_end = existing_task.due_date + timedelta(
				minutes=existing_task.duration_minutes
			)
			if task.due_date < existing_end and existing_task.due_date < new_end:
				return True
		return False
