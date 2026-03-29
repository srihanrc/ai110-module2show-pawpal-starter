# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    - PetOwner class
        - Stores the owner of pets information (name, daily hours, years of experience)
        - Responsibilities: Look at time constraints so the tasks can fit the owner's timing.
        - Attributes: name, years_experience, daily_hours
        - Methods: getName(), get_available_time(), check_experience()

    - Pet class
        - Stores all pet information (name, type, food, special needs)
        - Responsibilities: Allows for people to select pet preference.
        - Attributes: name, speciesType, foodType, list_special_needs
        - Methods: getName(), getType(), getFoodType(), special_needs()

    - Task class
        - Stores all task details for the pet (duration, priority)
        - Responsibilities: Represents pet care activities like walking or feeding.
        - Attributes: time, priorTasks
        - Methods: time_duration(), pet_priority()

    - Scheduler class
        - Stores references to petOwner, pet and list of tasks.
        - Responsibilities: Generate the daily plan for pets by prioritizing tasks within time constraints.
        - Attributes: owner, pet, prior_tasks, time_avail
        - Methods: priority_tasks(), schedule-tasks(), generate_plan()


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---
    Yes my design did change during implementation. One change that was made was adding or removing pets and making a list for this because the pet owner can decide when to add pets to the shop and when to remove them.

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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
