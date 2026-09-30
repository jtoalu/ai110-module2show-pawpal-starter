from dataclasses import dataclass, field


class Owner:
	def __init__(self, owner_id, name, email):
		self.owner_id = owner_id
		self.name = name
		self.email = email
		self.pets = []

	def add_pet(self, pet):
		pass

	def remove_pet(self, pet):
		pass

	def view_tasks(self):
		pass


@dataclass
class Pet:
	pet_id: int
	name: str
	species: str
	breed: str
	age: int
	tasks: list = field(default_factory=list)

	def add_task(self, task):
		pass

	def remove_task(self, task):
		pass

	def get_tasks(self):
		pass


@dataclass
class Task:
	task_id: int
	title: str
	description: str
	due_date: str
	priority: str
	completed: bool = False

	def complete(self):
		pass

	def is_overdue(self):
		pass

	def update_task(self):
		pass


class Scheduler:
	def __init__(self):
		self.tasks = []

	def schedule_task(self, task):
		pass

	def remove_task(self, task):
		pass

	def get_upcoming_tasks(self):
		pass

	def prioritize_tasks(self):
		pass

	def mark_task_complete(self, task):
		pass
