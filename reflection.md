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

The scheduler considered time, priority, owner experience, pet clustering, priority of tasks, and time of day activities. Time and priority mattered most because pets need to get the care they may need in a certain time or it may lead to bad outcomes. The owners should also have pet experience if they want to work with pets. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler is prioritizing the higher priority tasks first in which it may skip some lower priority tasks. This is reasonable because pet owners might need critical tasks like medications for the pets. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to write my classes to make improvements on the methods. This was more useful when it gave my method names that actually made sense for the class and this also helped me to debug and test code. The prompts were very useful when it was able to write test cases for me. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I did not accept it when it made changes to my code to fix test cases because I was trying this path and the same amount of test cases would pass and fail. I looked and saw the code it was suggesting and it didn't really show the change that would help make my test error disappear. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

1. High Priority tasks are being scheduled first (priority_tasks())
2. Tasks from multiple pets get grouped accordingly (schedule_clustered_by_pet())
3. Cache invalidation if any task changes.(get_cached_total_time())
4. The total scheduled time never goes past owner's available time (is_feasible())

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am like 70% percent sure that my scheudler works correctly. If I had more time, I would have added a bunch more tasks to see if it would do the higher priority tasks first and also test for circular dependency to see if two classes are entirely dependent on each other. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I was satisfied with my UML design in the beginning it was easy to read and understand as well as the methods and classes that were being implemented. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would have studied my test cases and figure out ways to where I can pass all my test cases and make improvements on the UI design as well as it's not fully creative. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned how these 4 classes work with each other to successfully make a pet shop. Users can get pets and learn how to care for the pet and the exercises the pets can do. Working with AI made it much easier to generate methods for each class instead of me having to think about different methods that could be used for each class. 