import streamlit as st
from diagrams.pawpal_system import PetOwner, Pet, Task, Scheduler

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

# Initialize owner in session state (keep simple defaults)
if "owner" not in st.session_state or st.session_state.owner is None:
    st.session_state.owner = None

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

# Note: tasks are stored on each Pet object via Pet.add_task()

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add pet"):
    # create owner if needed
    if st.session_state.owner is None:
        st.session_state.owner = PetOwner(owner_name, years_experience=1, daily_hours=2.0)
    new_pet = Pet(pet_name, species, "Unknown")
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added pet: {new_pet.name}")

# Select which pet to add tasks to
selected_pet = None
if st.session_state.owner is not None and st.session_state.owner.pets:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_name = st.selectbox("Select pet", pet_names)
    # find pet object
    for p in st.session_state.owner.pets:
        if p.name == selected_name:
            selected_pet = p
            break

with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if st.session_state.owner is None or selected_pet is None:
        st.warning("Add a pet first, then select it to add tasks.")
    else:
        # convert minutes to hours
        hours = int(duration) / 60.0
        task_obj = Task(task_title, task_title, hours, frequency="daily", pet=selected_pet)
        selected_pet.add_task(task_obj)
        st.success(f"Added task '{task_obj.name}' to {selected_pet.name}")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("No pets yet. Add a pet above to begin.")
else:
    st.write("Current pets and tasks:")
    for p in st.session_state.owner.pets:
        st.write(f"- {p.name} ({p.getType()})")
        tasks = p.list_tasks(incomplete_only=False)
        if tasks:
            for t in tasks:
                status = "✓" if t.is_completed() else "✗"
                st.write(f"    - {t.name} ({t.time_duration_hours()*60:.0f} min) [{status}]")
        else:
            st.write("    (no tasks)")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if st.session_state.owner is None:
        st.warning("Add an owner and pets first.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        plan = scheduler.generate_plan()
        if not plan:
            st.info("No tasks fit into available time.")
        else:
            st.subheader("Today's Schedule")
            for pet_name, tasks in plan.items():
                st.write(f"- {pet_name}:")
                for task_name in tasks:
                    st.write(f"    - {task_name}")
