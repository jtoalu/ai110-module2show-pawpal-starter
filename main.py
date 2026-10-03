from datetime import date, datetime, time, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task

owner = Owner(1, "James", "james@example.com")

buddy = Pet(1, "Buddy", "Dog", "Labrador", 4)
whiskers = Pet(2, "Whiskers", "Cat", "Tabby", 3)
owner.add_pet(buddy)
owner.add_pet(whiskers)

now = datetime.now().replace(second=0, microsecond=0)
print(f"Current date and time: {now:%B %d, %Y at %I:%M %p}\n")

tasks = [
    # Overdue tasks (intentionally listed out of order)
    (buddy, Task(1, "Medication", "Give evening medication",
        now - timedelta(hours=2), "high", 15)),
    (whiskers, Task(2, "Brush coat", "Brush Whiskers",
        now - timedelta(hours=6), "low", 30)),
    (buddy, Task(3, "Outdoor walk", "Walk around the park",
        now - timedelta(hours=4), "medium", 30)),
	
	# Upcoming tasks (intentionally listed out of order)
    (whiskers, Task(4, "Vet checkup", "Annual wellness visit",
        now + timedelta(hours=5), "high", 45)),
    (buddy, Task(5, "Feeding", "Serve dinner",
        now + timedelta(hours=1), "low", 15)),
    (buddy, Task(6, "Playtime", "Play fetch",
        now + timedelta(hours=3), "medium", 30)),

	# Completed tasks
    (whiskers, Task(7, "Nail trim", "Trim claws",
        now - timedelta(days=1, hours=2), "low", 15)),
    (buddy, Task(8, "Morning feeding", "Serve breakfast",
        now - timedelta(days=1, hours=6), "low", 15)),
    (whiskers, Task(9, "Grooming", "Brush and groom",
        now - timedelta(days=1, hours=4), "medium", 30)),
]

recurring_tasks = [
    (
        buddy,
        Task(
            10,
            "Daily medication",
            "Give Buddy his medication",
            now + timedelta(hours=2),
            "high",
            15,
            recurrence="daily",
        ),
    ),
	(
		whiskers,
		Task(
			11,
			"Weekly grooming",
			"Brush Whiskers thoroughly",
			now - timedelta(days=4),
			"medium",
			30,
			recurrence="weekly",
		),
	),
]

# Mark the three completed tasks before adding them to the scheduler.
for _, task in tasks[6:]:
    task.complete()

scheduler = Scheduler()
for pet, task in tasks:
	pet.add_task(task)
	if not scheduler.schedule_task(task):
		pet.remove_task(task)

# Run the recurring-task demo only after scheduler has been created.
print("Recurring Tasks")
for pet, task in recurring_tasks:
    if not scheduler.schedule_task(task):
        continue  # Skip if the task is already scheduled
    pet.add_task(task)
    next_task = scheduler.mark_task_complete(task)
    if next_task is not None:
        pet.add_task(next_task)
        if task.recurrence == "daily":
            completed_display = task.completed_at
        elif task.recurrence == "weekly":
            completed_display = task.due_date
        else:
            raise ValueError(f"Unsupported recurrence: {task.recurrence}")

        if completed_display is None:
            raise ValueError(f"No completion date recorded for {task.title}")
        print(
			f"{pet.name} - completed: {task.title} at "
			f"{completed_display:%b %d, %I:%M %p}; " 
			f"next occurrence: "
            f"{next_task.due_date:%b %d, %I:%M %p} "
            f"({task.recurrence})"
        )

print("\nConflict Detection Demo")

conflict_time = now + timedelta(days=2)
first_demo_id = max(
    (task.task_id for task in scheduler.tasks),
    default=0,
) + 1

buddy_task = Task(
    first_demo_id,
    "Outdoor walk [conflict demo]",
    "First task in the conflict demo",
    conflict_time,
    "medium",
    30,
)

whiskers_task = Task(
    first_demo_id + 1,
    "Whiskers appointment [conflict demo]",
    "Overlaps Buddy's walk",
    conflict_time + timedelta(minutes=10),
    "medium",
    30,
)

buddy.add_task(buddy_task)
if scheduler.schedule_task(buddy_task):
    print(f"- Scheduling {buddy_task.title} for {buddy.name}.")

whiskers.add_task(whiskers_task)
candidate_end = whiskers_task.due_date + timedelta(
    minutes=whiskers_task.duration_minutes
)

conflict = next(
    (
        scheduled
        for scheduled in scheduler.tasks
        if not scheduled.completed
        and whiskers_task.due_date
        < scheduled.due_date + timedelta(minutes=scheduled.duration_minutes)
        and scheduled.due_date < candidate_end
    ),
    None,
)

if conflict is not None:
    print("Conflict detected:")
    print(
        f"  Existing: {conflict.title} ({buddy.name}) at "
        f"{conflict.due_date:%B %d, %Y at %I:%M %p} "
        f"for {conflict.duration_minutes} minutes"
    )
    print(
        f"  Proposed: {whiskers_task.title} ({whiskers.name}) at "
        f"{whiskers_task.due_date:%B %d, %Y at %I:%M %p} "
        f"for {whiskers_task.duration_minutes} minutes"
    )
    print("  They overlap and are for different pets; proposed task not scheduled.")
    whiskers.remove_task(whiskers_task)
elif scheduler.schedule_task(whiskers_task):
    print(f"Scheduled {whiskers_task.title} for {whiskers.name}.")

pet_names = {pet.pet_id: pet.name for pet in owner.pets}

print("\nOverdue Tasks")
overdue_tasks = scheduler.get_overdue_tasks()
if overdue_tasks:
    for task in overdue_tasks:
        print(
            f"OVERDUE - {task.due_date:%B %d, %Y at %I:%M %p} - "
            f"{task.title} ({pet_names[task.pet_id]})"
        )
else:
    print("No overdue tasks.")

print("\nUpcoming Tasks")
upcoming_tasks = scheduler.get_upcoming_tasks()
if upcoming_tasks:
    for task in upcoming_tasks:
        print(
            f"{task.due_date:%B %d, %Y at %I:%M %p} - "
            f"{task.title} ({pet_names[task.pet_id]})"
        )
else:
    print("No upcoming tasks.")

print("\nCompleted Tasks")
completed_tasks = sorted(
    (task for task in scheduler.tasks if task.completed),
    key=lambda task: task.due_date,
)

if completed_tasks:
    for task in completed_tasks:
        print(
            f"{task.due_date:%B %d, %Y at %I:%M %p} - "
            f"{task.title} ({pet_names[task.pet_id]})"
        )
else:
    print("No completed tasks.")