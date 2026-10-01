# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design separated pet-care data from scheduling logic. A **PetOwner** stores owner information and manages the owner’s pets, while a **Pet** stores details about an animal and its care needs. A **Service** represents the type of care requested, such as grooming or walking, and an **Appointment** connects a pet, service, date, and time. A **Scheduler** checks availability, applies priorities and preferences, and creates a schedule without overlapping appointments.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Findings

High: Task has no link to its Pet.
Pet.tasks and Scheduler.tasks are separate lists, so the same task could be missing from one collection or appear inconsistently. Add a pet or pet_id field to Task, or make Scheduler the single source of truth. See pawpal_system.py.

Medium: Pet has no relationship to Owner.
Owner.pets tracks pets in one direction, but a Pet cannot identify its owner. This may make owner-specific task views difficult to implement. See pawpal_system.py and pawpal_system.py.

High: scheduling data is too limited for conflict detection.
Task.due_date is only a string, with no start time, duration, or recurring schedule. The scheduler therefore cannot reliably detect overlapping tasks or check availability. See pawpal_system.py.

Medium: completion logic has unclear ownership.
Task.complete() and Scheduler.mark_task_complete() may eventually implement the same behavior. Choose whether the task changes its own state or the scheduler coordinates that change. See pawpal_system.py and pawpal_system.py.

Low: priority is an unrestricted string.
Values such as "high", "High", and "urgent" could be treated inconsistently by prioritize_tasks(). An enum or validated set of priority values would make sorting more reliable.

Assumption

The file is intentionally a skeleton, so the empty methods are expected. The most important design decision before implementation is whether Scheduler.tasks or each Pet.tasks list should be the authoritative task collection.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I am amazed how AI (Copilot) can do a lot of things which I learned from my Object-Oriented Programming course/class in the past.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

In some occassions, I allow the AI to write codes or comments into a file. I then review the new lines or comments and decide whether to keep or undo. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
