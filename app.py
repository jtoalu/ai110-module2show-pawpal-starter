import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

breed = st.text_input("Breed", value="Shiba Inu")
age = st.number_input("Age", min_value=0, max_value=30, value=3)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id=1, name=owner_name, email="owner@example.com")
    st.session_state.pet = Pet(pet_id=1, name=pet_name, species=species, breed=breed, age=age, owner_id=1)
    st.session_state.owner.add_pet(st.session_state.pet)

if st.button("Add pet"):
    st.session_state.pet = Pet(pet_id=1, 
        name=pet_name, species=species, breed=breed, age=age, owner_id=1)
    st.session_state.owner.add_pet(st.session_state.pet)
    st.success(f"Added pet {pet_name} for owner {owner_name}.")

if st.session_state.owner.pets:
    st.write(f"Current pets for {owner_name}:")
    st.table(
        [
            {
                "Name": pet.name,
                "Species": pet.species,
                "Breed": pet.breed,
                "Age": pet.age,
            }
            for pet in st.session_state.owner.pets
        ]
    )

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Outdoor walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

due_date = st.date_input("Due date")
due_time = st.time_input("Due time", value=datetime.now() + timedelta(hours=1))

if st.button("Add task"):
    st.session_state.tasks.append(
        {
            "title": task_title,
            "duration_minutes": int(duration),
            "priority": priority,
            "due_date": datetime.combine(due_date, due_time),
        }
    )

if st.session_state.tasks:
    scheduler = Scheduler()

    for task_id, task_data in enumerate(st.session_state.tasks, start=1):
        task = Task(
            task_id=task_id,
            title=task_data["title"],
            description="",
            due_date=(
                datetime.fromisoformat(task_data["due_date"])
                if isinstance(task_data["due_date"], str)
                else task_data["due_date"]
            ),
            priority=task_data["priority"],
            duration_minutes=task_data["duration_minutes"],
        )

        if not scheduler.schedule_task(task):
            task_end = task.due_date + timedelta(minutes=task.duration_minutes)
            conflict = next(
                (
                    scheduled
                    for scheduled in scheduler.tasks
                    if not scheduled.completed
                    and task.due_date
                    < scheduled.due_date + timedelta(minutes=scheduled.duration_minutes)
                    and scheduled.due_date < task_end
                ),
                None,
            )

            if conflict is not None:
                overlap_start = max(task.due_date, conflict.due_date)
                overlap_end = min(
                    task_end,
                    conflict.due_date + timedelta(minutes=conflict.duration_minutes),
                )
                st.warning(
                    f"Could not schedule **{task.title}**: it overlaps with "
                    f"**{conflict.title}** from {overlap_start:%b %d, %I:%M %p} "
                    f"to {overlap_end:%I:%M %p}."
                )
            else:
                st.warning(
                    f"Could not schedule **{task.title}**. The scheduler rejected it, "
                    f"but no overlapping scheduled task was found."
                )

    st.write("Upcoming tasks:")
    upcoming_tasks = scheduler.get_upcoming_tasks()

    if upcoming_tasks:
        st.table(
            [
                {
                    "Title": task.title,
                    "Due Date": task.due_date,
                    "Priority": task.priority,
                    "Duration (minutes)": task.duration_minutes,
                }
                for task in upcoming_tasks
            ]
        )
    else:
        st.info("No upcoming tasks.")
else:
    st.info("No tasks yet. Add one above.")

open_tasks = [
    task for task in st.session_state.tasks if not task.get("completed", False)
]
task_objects = [
    Task(
        task_id=i,
        title=task["title"],
        description="",
        due_date=(datetime.fromisoformat(task["due_date"])
            if isinstance(task["due_date"], str)
            else task["due_date"]),
        priority=task["priority"],
        duration_minutes=task["duration_minutes"],
    )
    for i, task in enumerate(open_tasks)
]

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    task_objects = [
        Task(
            task_id=i,
            title=task["title"],
            description="",
            due_date=(datetime.fromisoformat(task["due_date"]) 
                if isinstance(task["due_date"], str) 
                else task["due_date"]),
            priority=task["priority"],
            duration_minutes=task["duration_minutes"],
        )
        for i, task in enumerate(st.session_state.tasks)
    ]

    scheduler = Scheduler()
    for task in task_objects:
        scheduler.schedule_task(task)

    st.write("Scheduled tasks:")
    scheduled_tasks = scheduler.get_upcoming_tasks()
    if scheduled_tasks:
        st.table(
            [
                {
                    "Title": task.title,
                    "Due Date": task.due_date,
                    "Priority": task.priority,
                    "Duration (minutes)": task.duration_minutes,
                }
                for task in scheduled_tasks
            ]
        )
    else:
        st.info("No tasks scheduled. Check for conflicts or add more tasks.")

st.divider()

st.markdown(
"""
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
)