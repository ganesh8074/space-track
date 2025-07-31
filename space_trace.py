import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Interior Work Tracker", layout="wide")

DATA_FILE = "tracker_data.json"
PHOTO_DIR = "uploads"
os.makedirs(PHOTO_DIR, exist_ok=True)

users = {
    "admin": {"role": "Admin", "password": "admin123"},
    "engineer": {"role": "Engineer", "password": "eng123"},
    "user": {"role": "User", "password": "user123"}
}

section_components = {
    "Wardrobe": ["Loft doors", "Hinges", "Handles", "Expo piece", "Frame-biding"],
    "Cupboard": ["Hinges", "Doors", "Expo piece", "Inner pieces", "Shelves", "Drawers", "Back panelling", "Top piece", "Bottom piece", "Locks", "Handles", "Tower bolt", "Channel", "Mirror"],
    "TV Unit": ["Panelling piece", "Drawers", "Expo piece", "Drawer inner pieces", "Drawer outer box", "Handles", "Channels", "Drawer fixing screws"],
    "Kitchen": ["Loft frame", "Loft doors", "Expo piece", "Hinges", "Tandem basket", "Channels", "Handles", "Doors", "Side frames", "Panelling frames", "Shelves", "Tandem frame pieces"],
    "Middle Box": ["Doors", "Expo piece", "Top piece", "Bottom piece", "Side piece", "Back panelling piece"]
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"flats": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.data = load_data()

if st.session_state.logged_in:
    if st.sidebar.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if not st.session_state.logged_in:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

st.title("📋 Interior Work Tracker Dashboard")
data = st.session_state.data

if st.session_state.role == "Admin":
    st.sidebar.header("➕ Add New Flat")
    new_flat = st.sidebar.text_input("Flat ID (e.g., A1, B2)")
    flat_size = st.sidebar.text_input("Flat Size (L × B)")
    if st.sidebar.button("Add Flat") and new_flat:
        data["flats"][new_flat] = {
            "size": flat_size,
            "sections": {},
            "tasks": [],
            "created_by": st.session_state.username
        }
        save_data(data)
        st.success(f"Flat {new_flat} added!")

flat_ids = list(data["flats"].keys())
if not flat_ids:
    st.warning("Please add at least one flat to continue.")
    st.stop()

selected_flat = st.selectbox("🏠 Select a Flat", flat_ids)

if st.session_state.role == "Admin":
    with st.expander("🧩 Add or Edit Components"):
        section = st.selectbox("Section", list(section_components.keys()))
        component = st.selectbox("Component", section_components[section])
        qty = st.number_input("Quantity", 1)
        length = st.text_input("Length")
        width = st.text_input("Width")
        status = st.selectbox("Status", ["Pending", "Delivered"])
        deadline = st.date_input("Deadline")
        assignee = st.text_input("Assigned Engineer")
        photo = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

        if st.button("Add Component"):
            comp = {
                "component": component,
                "qty": qty,
                "length": length,
                "width": width,
                "status": status,
                "deadline": deadline.strftime("%Y-%m-%d"),
                "assignee": assignee,
                "photo": photo.name if photo else None
            }
            if section not in data["flats"][selected_flat]["sections"]:
                data["flats"][selected_flat]["sections"][section] = []
            data["flats"][selected_flat]["sections"][section].append(comp)

            if photo:
                file_path = os.path.join(PHOTO_DIR, photo.name)
                with open(file_path, "wb") as f:
                    f.write(photo.read())

            save_data(data)
            st.success("Component added")

        st.markdown("---")
        st.markdown("### ✏️ Edit Existing Components")
        for sec, comps in data["flats"][selected_flat]["sections"].items():
            for i, comp in enumerate(comps):
                with st.expander(f"Edit: {sec} → {comp['component']}"):
                    comp["qty"] = st.number_input("Qty", value=int(comp.get("qty", 0)), key=f"qty_{sec}_{i}")
                    comp["length"] = st.text_input("Length", value=comp.get("length", ""), key=f"len_{sec}_{i}")
                    comp["width"] = st.text_input("Width", value=comp.get("width", ""), key=f"wid_{sec}_{i}")
                    comp["status"] = st.selectbox("Status", ["Pending", "Delivered"], index=["Pending", "Delivered"].index(comp.get("status", "Pending")), key=f"stat_{sec}_{i}")
                    comp["deadline"] = st.date_input("Deadline", datetime.strptime(comp.get("deadline", "2025-12-31"), "%Y-%m-%d"), key=f"dd_{sec}_{i}").strftime("%Y-%m-%d")
                    comp["assignee"] = st.text_input("Assignee", value=comp.get("assignee", ""), key=f"asg_{sec}_{i}")
                    if st.button("Update Component", key=f"upd_{sec}_{i}"):
                        save_data(data)
                        st.success("Component updated")

    with st.expander("📝 Task Management"):
        st.markdown("### ➕ Add New Task")
        task_title = st.text_input("Task Title")
        task_desc = st.text_area("Task Description")
        task_eng = st.text_input("Assign to Engineer")
        task_due = st.date_input("Due Date")
        if st.button("Add Task") and task_title:
            data["flats"][selected_flat]["tasks"].append({
                "title": task_title,
                "desc": task_desc,
                "assigned": task_eng,
                "due": task_due.strftime("%Y-%m-%d"),
                "status": "Pending",
                "photo": None
            })
            save_data(data)
            st.success("Task added")

        st.markdown("---")
        st.markdown("### 🛠 Edit Tasks")
        for i, task in enumerate(data["flats"][selected_flat]["tasks"]):
            with st.expander(f"✏️ {task['title']} ({task['status']})"):
                task["title"] = st.text_input("Title", value=task["title"], key=f"tt_{i}")
                task["desc"] = st.text_area("Description", value=task["desc"], key=f"td_{i}")
                task["assigned"] = st.text_input("Engineer", value=task["assigned"], key=f"ta_{i}")
                task["due"] = st.date_input("Due Date", datetime.strptime(task["due"], "%Y-%m-%d"), key=f"tdate_{i}").strftime("%Y-%m-%d")
                task["status"] = st.selectbox("Status", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(task["status"]), key=f"ts_{i}")
                if st.button("Update Task", key=f"tu_{i}"):
                    save_data(data)
                    st.success("Task updated")

if st.session_state.role == "Engineer":
    st.subheader("🛠 My Tasks")
    for flat_id, flat in data["flats"].items():
        for i, task in enumerate(flat.get("tasks", [])):
            if task.get("assigned") == st.session_state.username:
                with st.expander(f"🔧 {flat_id} — {task['title']}"):
                    st.markdown(f"📋 {task['desc']}")
                    st.markdown(f"📅 Due: {task['due']}")
                    st.markdown(f"📌 Status: `{task['status']}`")
                    new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(task["status"]), key=f"ustat_{flat_id}_{i}")
                    img = st.file_uploader("Upload Completion Photo", key=f"uphoto_{flat_id}_{i}")
                    if st.button("Save Task Update", key=f"ustask_{flat_id}_{i}"):
                        task["status"] = new_status
                        if img:
                            img_path = os.path.join(PHOTO_DIR, img.name)
                            with open(img_path, "wb") as f:
                                f.write(img.read())
                            task["photo"] = img.name
                        save_data(data)
                        st.success("Task updated")

st.subheader("📦 Section Overview")
flat = data["flats"][selected_flat]

for sec, comps in flat["sections"].items():
    st.markdown(f"### {sec}")
    for i, comp in enumerate(comps):
        st.markdown(f"🔹 {comp.get('component', 'N/A')} — {comp.get('qty', 'N/A')} pcs — {comp.get('length', '-') }×{comp.get('width', '-') } — `{comp.get('status', 'N/A')}`")
        st.markdown(f"🧑 Assigned to: {comp.get('assignee', '-')}, ⏳ Deadline: {comp.get('deadline', '-')}")
        if comp.get("photo"):
            path = os.path.join(PHOTO_DIR, comp["photo"])
            if os.path.exists(path):
                st.image(path, width=120)

        if st.session_state.role == "Engineer" and comp.get("assignee") == st.session_state.username:
            new_status = st.selectbox("Update Status", ["Pending", "Delivered"], index=["Pending", "Delivered"].index(comp["status"]), key=f"status_{sec}_{i}")
            new_img = st.file_uploader("Upload Completion Photo", key=f"img_{sec}_{i}")
            if st.button("Update Component", key=f"update_{sec}_{i}"):
                comp["status"] = new_status
                if new_img:
                    path = os.path.join(PHOTO_DIR, new_img.name)
                    with open(path, "wb") as f:
                        f.write(new_img.read())
                    comp["photo"] = new_img.name
                save_data(data)
                st.success("Component Updated")

if st.session_state.role == "Admin":
    st.subheader("📊 Multi-Flat Dashboard")
    flat_rows = []
    for flat_id, flat in data["flats"].items():
        total = delivered = 0
        for comps in flat["sections"].values():
            for comp in comps:
                total += 1
                if comp.get("status") == "Delivered":
                    delivered += 1
        flat_rows.append({"Flat": flat_id, "Total": total, "Delivered": delivered, "Pending": total - delivered})

    df = pd.DataFrame(flat_rows)
    st.dataframe(df)

    if st.download_button("📥 Export CSV", df.to_csv(index=False).encode(), "interior_report.csv", "text/csv"):
        st.success("CSV downloaded")

    json_data = json.dumps(data, indent=2)
    st.download_button("📥 Export JSON", json_data.encode(), "interior_data.json", "application/json")
