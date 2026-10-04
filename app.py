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

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
    st.session_state.pets = st.session_state.scheduler.load_from_json()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="James")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

breed = st.text_input("Breed", value="Shiba Inu")
age = st.number_input("Age", min_value=0, max_value=30, value=3)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_id=1, name=owner_name, email="owner@example.com"
    )
    for pet in st.session_state.pets:
        if pet.owner_id == 1:
            st.session_state.owner.add_pet(pet)

if st.button("Add pet"):
    pet = Pet(
        pet_id=max((p.pet_id for p in st.session_state.pets), default=0) + 1,
        name=pet_name,
        species=species,
        breed=breed,
        age=age,
        owner_id=1,
    )
    st.session_state.owner.add_pet(pet)
    st.session_state.pets.append(pet)
    st.session_state.scheduler.save_to_json(st.session_state.pets)
    st.success(f"Added pet {pet_name} for owner {owner_name}.")

if st.session_state.owner.pets:
    st.write(f"Current pets for {owner_name}:")
    st.table(
        [
            {
                "Name": f"{pet.name} (Pet ID #{pet.pet_id})",
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

pets_by_id = {pet.pet_id: pet for pet in st.session_state.pets}

if pets_by_id:
    selected_pet_id = st.selectbox(
        "Pet for this task",
        options=list(pets_by_id),
        format_func=lambda pet_id: (
            f"{pets_by_id[pet_id].name} (Pet ID #{pet_id})"
        ),
    )

    if st.button("Add task"):
        task = Task(
            task_id=max(
                (item.task_id for item in st.session_state.scheduler.tasks),
                default=0,
            ) + 1,
            title=task_title,
            description="",
            due_date=datetime.combine(due_date, due_time),
            priority=priority,
            duration_minutes=int(duration),
            pet_id=selected_pet_id,
        )

        if st.session_state.scheduler.schedule_task(task):
            pets_by_id[selected_pet_id].add_task(task)
            st.session_state.scheduler.save_to_json(st.session_state.pets)
            st.success(
                f"Added {task_title} for "
                f"{pets_by_id[selected_pet_id].name}."
            )
        else:
            st.warning(
                f"Could not add {task_title}: it conflicts with a scheduled task."
            )
else:
    st.info("Add a pet before creating a task.")

if st.session_state.scheduler.tasks:
    scheduler = st.session_state.scheduler

    st.subheader("Upcoming tasks")
    upcoming_tasks = scheduler.get_upcoming_tasks()

    if upcoming_tasks:
        st.table(
            [
                {
                    "Task ID": task.task_id,
                    "Pet": f"{pets_by_id[task.pet_id].name} (Pet ID #{task.pet_id})",
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

    incomplete_tasks = [
        task for task in scheduler.tasks if not task.completed
    ]

    st.subheader("Mark a task complete")
    if incomplete_tasks:
        tasks_by_id = {task.task_id: task for task in incomplete_tasks}
        selected_task_id = st.selectbox(
            "Task",
            options=list(tasks_by_id),
            format_func=lambda task_id: (
                f"{tasks_by_id[task_id].title} (Task #{task_id})"
            ),
            key="task_to_complete",
        )

        if st.button("Mark complete", key="mark_task_complete"):
            task = tasks_by_id[selected_task_id]

            try:
                next_task = scheduler.mark_task_complete(task)
            except ValueError as exc:
                st.error(str(exc))
            else:
                # Recurring tasks create a new scheduled occurrence.
                if next_task is not None:
                    pets_by_id[next_task.pet_id].add_task(next_task)

                scheduler.save_to_json(st.session_state.pets)
                st.success(f"Marked “{task.title}” complete and saved.")
    else:
        st.info("There are no incomplete tasks.")

    st.subheader("Completed tasks")
    completed_tasks = [
        task for task in scheduler.tasks if task.completed
    ]

    if completed_tasks:
        st.table(
            [
                {
                    "Task ID": task.task_id,
                    "Pet": f"{pets_by_id[task.pet_id].name} (Pet ID #{task.pet_id})",
                    "Title": task.title,
                    "Due Date": task.due_date,
                    "Completed At": task.completed_at,
                    "Priority": task.priority,
                    "Duration (minutes)": task.duration_minutes,
                }
                for task in completed_tasks
            ]
        )
    else:
        st.info("No completed tasks yet.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule for the next 48 hours.")

if st.button("Generate schedule"):
    now = datetime.now()
    schedule_end = now + timedelta(hours=48)

    scheduled_tasks = [
        task
        for task in st.session_state.scheduler.get_upcoming_tasks()
        if task.due_date <= schedule_end
    ]

    st.write("Scheduled tasks:")
    if scheduled_tasks:
        st.table(
            [
                {
                    "Task ID": task.task_id,
                    "Pet": f"{pets_by_id[task.pet_id].name} (Pet ID #{task.pet_id})",
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