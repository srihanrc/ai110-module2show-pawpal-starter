from pawpal_system import PetOwner, Pet, Task, Scheduler
import streamlit as st

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

# Initialize session state variables for PawPal system objects
if "owner" not in st.session_state:
    st.session_state.owner = None

if "pets" not in st.session_state:
    st.session_state.pets = {}

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_hours = st.number_input("Available hours per day", min_value=1, max_value=24, value=4)
years_experience = st.number_input("Years of pet experience", min_value=0, max_value=50, value=2)

# Create or retrieve Owner from session_state
if st.button("Create/Update Owner"):
    # Check if owner already exists in session_state
    if st.session_state.owner is not None:
        st.info(f"Owner '{st.session_state.owner.getName()}' already exists. Updating...")
    
    # Create new owner or update existing
    st.session_state.owner = PetOwner(
        name=owner_name,
        daily_hours=available_hours,
        years_experience=years_experience
    )
    st.success(f"✓ Owner created/updated: {st.session_state.owner}")

# Display current owner if it exists with detailed information
if st.session_state.owner is not None:
    with st.expander(f"👤 Owner: {st.session_state.owner.getName()}", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            # Call get_available_time() method
            st.metric("Available Time", f"{st.session_state.owner.get_available_time()} hrs/day")
        with col2:
            # Call check_experience() method
            st.metric("Years Experience", st.session_state.owner.check_experience())
        with col3:
            # Call get_all_pets() method to count
            num_pets = len(st.session_state.owner.get_all_pets())
            st.metric("Total Pets", num_pets)
        
        # Display experience-based time savings (Improvement #1)
        st.markdown("#### ⚡ Experience-Based Task Speed")
        sample_task_duration = 30
        adjusted = st.session_state.owner.get_adjusted_task_duration(Task("Sample", sample_task_duration, "Daily"))
        time_saved = sample_task_duration - adjusted
        efficiency_gain = (time_saved / sample_task_duration) * 100
        st.write(f"For a 30-minute task:")
        st.write(f"  • Base time: {sample_task_duration} min")
        st.write(f"  • Your adjusted time: {adjusted} min")
        st.write(f"  • **Time saved: {time_saved} min ({efficiency_gain:.0f}% faster)**")
else:
    st.warning("No owner created yet. Click 'Create/Update Owner' above.")

st.markdown("---")

st.subheader("Pet Management")

if st.session_state.owner is not None:
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])
    
    food_type = st.text_input("Food type", value="Kibble")
    special_needs = st.multiselect("Special needs", ["Daily exercise", "Indoor only", "Medication", "Litter box cleaning", "Temperature control"])
    
    if st.button("Add Pet"):
        # Check if pet with same name already exists in session_state
        if pet_name in st.session_state.pets:
            st.warning(f"Pet '{pet_name}' already exists. Skipping...")
        else:
            # Create new pet using Pet constructor
            new_pet = Pet(
                name=pet_name,
                speciesType=species,
                foodType=food_type,
                list_special_needs=special_needs,
                pet_owner=st.session_state.owner
            )
            
            # Store in session_state
            st.session_state.pets[pet_name] = new_pet
            # Add pet to owner using PetOwner.add_pet() method
            st.session_state.owner.add_pet(new_pet)
            st.success(f"✓ Pet added: {new_pet}")
    
# Display existing pets from session_state with detailed information
    if st.session_state.pets:
        st.write("**Current Pets:**")
        for pet_name, pet in st.session_state.pets.items():
            with st.expander(f"📄 {pet.getName()}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    # Call Pet.getType() method
                    st.write(f"**Type:** {pet.getType()}")
                with col2:
                    # Call Pet.getFoodType() method
                    st.write(f"**Food:** {pet.getFoodType()}")
                with col3:
                    # Call Pet.getName() method
                    st.write(f"**Tasks:** {len(pet.get_tasks())}")
                
                # Call special_needs() method
                special_needs = pet.special_needs()
                if special_needs:
                    st.write(f"**Special Needs:** {', '.join(special_needs)}")
                else:
                    st.write("**Special Needs:** None")
else:
    st.info("Create an owner first to add pets.")

st.markdown("---")

st.markdown("### Tasks")
st.caption("Add tasks to your pets. These will be managed in session_state.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if st.session_state.pets:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_pet = st.selectbox("Select Pet", list(st.session_state.pets.keys()))
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
    
    col5, col6 = st.columns(2)
    with col5:
        criticality = st.selectbox("Criticality", ["normal", "low", "high", "critical"], help="Priority level")
    with col6:
        dependencies = st.multiselect("Dependencies", [t.description for t in st.session_state.tasks], help="Tasks that must be completed first")
    
    if st.button("Add task"):
        new_task = Task(
            description=task_title,
            time=int(duration),
            frequency=frequency,
            associated_pet=st.session_state.pets[selected_pet],
            criticality=criticality,
            dependencies=dependencies
        )
        # Add task to pet using Pet.add_task() method
        st.session_state.pets[selected_pet].add_task(new_task)
        st.session_state.tasks.append(new_task)
        st.success(f"✓ Task added to {selected_pet}: {task_title} ({duration} min, {frequency}, {criticality})")
    
    if st.session_state.tasks:
        st.write("**Current Tasks:**")
        for idx, task in enumerate(st.session_state.tasks):
            if task.get_pet():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    # Display task using __str__ method
                    st.write(f"  • [{task.get_pet().getName()}] {task}")
                with col2:
                    # Display priority using pet_priority() method
                    st.write(f"Priority: {task.pet_priority()}")
                with col3:
                    # Button to mark task as completed
                    if st.button(f"✓ Done##task_{idx}", key=f"complete_{idx}"):
                        task.mark_completed()
                        st.rerun()
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first to create tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Click below to generate a schedule based on all created tasks and owner constraints.")

if st.button("Generate schedule"):
    # Check if owner exists in session_state
    if st.session_state.owner is None:
        st.error("❌ No owner found in session. Please create an owner first.")
    # Check if there are pets
    elif not st.session_state.pets:
        st.error("❌ No pets found in session. Please add at least one pet.")
    # Check if there are tasks
    elif not st.session_state.tasks:
        st.warning("⚠️ No tasks found. Add some tasks to generate a schedule.")
    else:
        # Create scheduler from session_state objects
        # Check if scheduler already exists
        if st.session_state.scheduler is None or st.session_state.scheduler.owner != st.session_state.owner:
            st.session_state.scheduler = Scheduler(st.session_state.owner, st.session_state.tasks)
            st.info("✓ Scheduler created from existing session objects.")
        else:
            st.info("✓ Using existing scheduler from session.")
        
        # Display schedule information using various Phase 2 methods
        st.markdown("### 📋 Schedule Summary")
        # Get pending tasks using retrieve_pending_tasks() method
        pending_tasks = st.session_state.scheduler.retrieve_pending_tasks()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tasks", len(st.session_state.tasks))
        with col2:
            st.metric("Pending Tasks", len(pending_tasks))
        with col3:
            # Call get_total_task_time() method
            st.metric("Time Required", f"{st.session_state.owner.get_total_task_time()} min")
        with col4:
            # time_avail property implementation from Phase 2
            st.metric("Available Time", f"{st.session_state.scheduler.time_avail} min")
        
        # Check feasibility using is_feasible() method
        if st.session_state.scheduler.is_feasible():
            st.success("✓ All pending tasks fit within the available time!")
        else:
            st.error("✗ Warning: Not all pending tasks fit within the available time. Some tasks may not be scheduled.")
        
        # Display priority-sorted tasks using priority_tasks() method
        st.markdown("### 🎯 Tasks by Priority")
        priority_tasks = st.session_state.scheduler.priority_tasks()
        if priority_tasks:
            task_data = []
            for i, task in enumerate(priority_tasks, 1):
                pet_name = task.get_pet().getName() if task.get_pet() else "Unknown"
                # Call time_duration() and pet_priority() methods
                task_data.append({
                    "#": i,
                    "Pet": pet_name,
                    "Task": task.description,
                    "Duration (min)": task.time_duration(),
                    "Priority": task.pet_priority(),
                    "Frequency": task.frequency,
                    "Criticality": task.criticality
                })
            st.dataframe(task_data, use_container_width=True)
        else:
            st.info("No pending tasks to schedule.")
        
        # Display tasks sorted by duration (Improvement #3)
        st.markdown("### ⏱️ Tasks Sorted by Duration")
        sort_order = st.radio("Sort order", ("Shortest first", "Longest first"))
        ascending = sort_order == "Shortest first"
        sorted_by_time = st.session_state.scheduler.sort_by_time(ascending=ascending)
        if sorted_by_time:
            time_sort_data = []
            for i, task in enumerate(sorted_by_time, 1):
                pet_name = task.get_pet().getName() if task.get_pet() else "Unknown"
                time_sort_data.append({
                    "#": i,
                    "Pet": pet_name,
                    "Task": task.description,
                    "Duration (min)": task.time_duration(),
                    "Frequency": task.frequency
                })
            st.dataframe(time_sort_data, use_container_width=True)
        else:
            st.info("No tasks to sort.")
        
        # Filter tasks by pet and status (Improvement #2)
        st.markdown("### 🔍 Filter Tasks")
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            filter_pet = st.selectbox("Filter by Pet", ["All"] + list(st.session_state.pets.keys()))
        with col_filter2:
            filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
        
        pet_name_filter = None if filter_pet == "All" else filter_pet
        status_filter = None if filter_status == "All" else filter_status.lower()
        
        filtered_tasks = st.session_state.scheduler.filter_tasks(status=status_filter, pet_name=pet_name_filter)
        if filtered_tasks:
            filter_data = []
            for task in filtered_tasks:
                pet_name = task.get_pet().getName() if task.get_pet() else "Unknown"
                filter_data.append({
                    "Pet": pet_name,
                    "Task": task.description,
                    "Duration (min)": task.time_duration(),
                    "Status": "✓ Completed" if task.is_completed else "○ Pending",
                    "Priority": task.pet_priority()
                })
            st.dataframe(filter_data, use_container_width=True)
            st.write(f"📊 Showing {len(filtered_tasks)} task(s)")
        else:
            st.info("No tasks match the selected filters.")
        
        # Display time-of-day optimization (Improvement #5)
        st.markdown("### 🕐 Tasks by Optimal Time")
        time_of_day_hour = st.slider("Select time of day", 0, 23, 9, help="9 = 9 AM, 18 = 6 PM")
        time_optimized = st.session_state.scheduler.get_priority_by_time_of_day(time_of_day_hour)
        if time_optimized:
            time_data = []
            for item in time_optimized[:10]:  # Show top 10
                task = item['task']
                time_data.append({
                    "Task": task.description,
                    "Pet": task.get_pet().getName() if task.get_pet() else "Unknown",
                    "Base Priority": task.pet_priority(),
                    "Time Adjustment": item['adjustment'],
                    "Optimized Priority": item['adjusted_priority']
                })
            st.dataframe(time_data, use_container_width=True)
        
        # Display scheduled tasks
        st.markdown("### ✅ Scheduled Tasks")
        scheduled = st.session_state.scheduler.schedule_tasks()
        if scheduled:
            for i, task in enumerate(scheduled, 1):
                with st.expander(f"{i}. {task.description}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Pet:** {task.get_pet().getName() if task.get_pet() else 'Unknown'}")
                        st.write(f"**Duration:** {task.time_duration()} minutes")
                    with col2:
                        st.write(f"**Frequency:** {task.frequency}")
                        st.write(f"**Status:** {'✓ Completed' if task.is_completed else '○ Pending'}")
        else:
            st.warning("No tasks could be scheduled within the time constraints.")
        
        # Display conflict detection (Improvements #4, #5)
        st.markdown("### 🚨 Scheduling Conflicts & Warnings")
        conflict_check = st.session_state.scheduler.lightweight_conflict_check(scheduled)
        
        if conflict_check["success"]:
            if conflict_check["has_conflicts"]:
                st.error(f"⚠️ {conflict_check['critical_count']} conflict(s) detected!")
                for warning in conflict_check["warnings"]:
                    st.warning(warning)
                
                # Show detailed conflict info
                st.markdown("#### Conflict Details:")
                for idx, conflict in enumerate(conflict_check["conflicts"], 1):
                    task1, task2 = conflict["tasks"]
                    pet1 = task1.get_pet().getName() if task1.get_pet() else "Unknown"
                    pet2 = task2.get_pet().getName() if task2.get_pet() else "Unknown"
                    
                    if conflict["same_pet"]:
                        st.error(f"**🔴 DOUBLE BOOKING**: [{pet1}] {task1.description} conflicts with {task2.description}")
                    else:
                        st.warning(f"**⚠️ Overlap**: [{pet1}] {task1.description} overlaps with [{pet2}] {task2.description}")
            else:
                st.success("✓ No scheduling conflicts detected!")
            
            if conflict_check["warning_count"] > 0:
                st.info(f"📋 {conflict_check['warning_count']} warning(s) found during validation")
        else:
            st.error(f"❌ Conflict check failed: {conflict_check['status_message']}")
        
        # Display unscheduled tasks with reasons (Improvement #8)
        unscheduled = st.session_state.scheduler.get_unscheduled_tasks_with_reasons()
        if unscheduled:
            st.markdown("### ⚠️ Unscheduled Tasks (Could not fit)")
            for item in unscheduled:
                with st.expander(f"[{item['pet']}] {item['task'].description}"):
                    st.error(f"Reason: {item['reason']}")
        
        # Display break recommendations (Improvement #4)
        st.markdown("### ☕ Break Scheduling")
        scheduled_tasks, num_breaks, break_time, feasible_with_breaks = st.session_state.scheduler.schedule_tasks_with_breaks()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Recommended Breaks", num_breaks)
        with col2:
            st.metric("Break Time", f"{break_time} min")
        with col3:
            if feasible_with_breaks:
                st.metric("Feasible?", "✓ Yes")
            else:
                st.metric("Feasible?", "✗ No")
        
        # Display parallelizable tasks (Improvement #10)
        st.markdown("### 🔄 Tasks That Can Run in Parallel")
        parallel_groups = st.session_state.scheduler.get_parallelizable_tasks()
        if parallel_groups:
            for idx, group in enumerate(parallel_groups, 1):
                task_names = " + ".join([f"[{t.get_pet().getName()}] {t.description}" for t in group])
                st.info(f"Group {idx}: {task_names}")
        else:
            st.info("No parallelizable tasks found (all tasks are for same pet or no combinations available).")
        
        # Display final schedule
        st.markdown("### 📅 Daily Schedule")
        schedule_plan = st.session_state.scheduler.generate_plan()
        st.code(schedule_plan)
