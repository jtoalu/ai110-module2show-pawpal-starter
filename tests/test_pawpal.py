from datetime import datetime, timedelta, timezone

from pawpal_system import Pet, Scheduler, Task, sort_tasks


def test_mark_task_complete_changes_task_status():
	task = Task(
		1,
		"Feed pet",
		"Give the pet dinner",
		datetime.now(timezone.utc) + timedelta(hours=1),
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
		datetime.now(timezone.utc) + timedelta(hours=1),
		"low",
	)

	pet.add_task(task)

	assert len(pet.get_tasks()) == 1

def test_recurring_task_sorts_by_occurrence_not_series_creation_date():
    tasks = [
        Task(
            task_id=1,
            title="Older recurring series",
            description="Recurring task created earlier",
            due_date=datetime(2026, 10, 4, 9),
            priority="medium",
            recurrence="daily",
		),
        Task(
            task_id=2,
            title="Newer task due sooner",
            description="One-time task",
            due_date=datetime(2026, 10, 3, 9),
            priority="medium",
        ),
    ]

    sorted_tasks = sort_tasks(tasks)

    assert [task.task_id for task in sorted_tasks] == [2, 1]

def make_task(task_id, due_date, *, recurrence=None, title="Task"):
    return Task(
        task_id=task_id,
        title=title,
        description="Test task",
        due_date=due_date,
        priority="medium",
        recurrence=recurrence,
	)


def test_sort_tasks_orders_by_due_date():
    later = make_task(1, datetime(2026, 10, 5, 9))
    earlier = make_task(2, datetime(2026, 10, 3, 9))
    middle = make_task(3, datetime(2026, 10, 4, 9))

    result = sort_tasks([later, earlier, middle])

    assert [task.task_id for task in result] == [2, 3, 1]

def test_sort_tasks_returns_empty_list_when_pet_has_no_tasks():
    assert sort_tasks([]) == []


def test_sort_tasks_handles_one_task():
    task = make_task(1, datetime(2026, 10, 3, 9))

    assert sort_tasks([task]) == [task]

def test_sort_tasks_orders_same_due_time_by_task_id():
    later_id = make_task(20, datetime(2026, 10, 3, 9))
    earlier_id = make_task(10, datetime(2026, 10, 3, 9))

    result = sort_tasks([later_id, earlier_id])

    assert [task.task_id for task in result] == [10, 20]

def test_sort_tasks_orders_recurring_tasks_by_due_date():
    recurring = make_task(
        1,
        datetime(2026, 10, 4, 9),
        recurrence="daily",
        title="Daily walk",
    )
    one_time = make_task(
        2,
        datetime(2026, 10, 3, 9),
        title="Vet appointment",
    )

    result = sort_tasks([recurring, one_time])

    assert [task.task_id for task in result] == [2, 1]

def test_sort_tasks_does_not_change_input_list():
    later = make_task(1, datetime(2026, 10, 5, 9))
    earlier = make_task(2, datetime(2026, 10, 3, 9))
    tasks = [later, earlier]

    result = sort_tasks(tasks)

    assert tasks == [later, earlier]
    assert result == [earlier, later]