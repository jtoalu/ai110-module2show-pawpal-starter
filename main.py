from datetime import date, datetime, time

from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner(1, "Jamie", "jamie@example.com")

buddy = Pet(1, "Buddy", "Dog", "Labrador", 4)
whiskers = Pet(2, "Whiskers", "Cat", "Tabby", 3)
owner.add_pet(buddy)
owner.add_pet(whiskers)

today = date.today()
tasks = [
	(buddy, Task(1, "Morning walk", "Walk around the neighborhood", datetime.combine(today, time(9, 0)), "medium", 30)),
	(whiskers, Task(2, "Vet checkup", "Annual wellness visit", datetime.combine(today, time(13, 30)), "high", 45)),
	(buddy, Task(3, "Evening feeding", "Serve dinner", datetime.combine(today, time(18, 0)), "low", 15)),
]

scheduler = Scheduler()
for pet, task in tasks:
	pet.add_task(task)
	scheduler.schedule_task(task)

pet_names = {pet.pet_id: pet.name for pet in owner.pets}
print("Today's Schedule")
for task in scheduler.get_upcoming_tasks():
	print(f"{task.due_date:%I:%M %p} - {task.title} ({pet_names[task.pet_id]})")
