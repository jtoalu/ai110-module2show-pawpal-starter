from datetime import datetime, timedelta

from pawpal_system import Pet, Scheduler, Task


def test_mark_task_complete_changes_task_status():
	task = Task(
		1,
		"Feed pet",
		"Give the pet dinner",
		datetime.now() + timedelta(hours=1),
		"medium",
	)
	scheduler = Scheduler()
	scheduler.schedule_task(task)

	scheduler.mark_task_complete(task)

	assert task.completed is True


def test_adding_task_increases_pet_task_count():
	pet = Pet(1, "Buddy", "Dog", "Labrador", 4)
	task = Task(
		1,
		"Morning walk",
		"Walk around the neighborhood",
		datetime.now() + timedelta(hours=1),
		"low",
	)

	pet.add_task(task)

	assert len(pet.get_tasks()) == 1
