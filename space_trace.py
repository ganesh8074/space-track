
import streamlit as st
from utils.auth import require_login, logout_button, get_current_role
from utils.layout import set_custom_theme


# --- Global Vibrant & Professional UI Styling ---
st.set_page_config(page_title="Interior Design Automation", layout="wide", page_icon="🛋️")
set_custom_theme()
st.markdown('''
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #f8fafc 0%, #e0e7ef 100%) !important;
    }
    .stApp {
        background: none !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(120deg, #e0e7ef 0%, #a5b4fc 100%) !important;
        color: #1a202c !important;
        border-radius: 0 24px 24px 0 !important;
        box-shadow: 2px 0 16px #a5b4fc33;
    }
    [data-testid="stSidebar"] * {
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    /* Only minimal selectbox/input color fix, no font-size, no text-shadow, no background override */
    .stSelectbox span, .stSelectbox .css-1uccc91-singleValue, .stSelectbox .css-1dimb5e-singleValue {
        color: #000 !important;
    }
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] select, [data-testid="stSidebar"] textarea {
        color: #000 !important;
        background: #fff !important;
    }
    .stHeader, .stSubheader, h1, h2, h3, h4, h5, h6 {
        color: #1a202c !important;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        letter-spacing: 0.5px;
        font-weight: 800 !important;
    }
    .stDataFrame, .stTable {
        background: #fff !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 8px #e0e7ef !important;
        padding: 0.5em 1em 1em 1em !important;
        margin-bottom: 1.5em !important;
        color: #1a202c !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #38bdf8 0%, #6366f1 100%) !important;
        color: #fff !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.1em !important;
        box-shadow: 0 2px 8px #a5b4fc;
        border: none !important;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #6366f1 0%, #38bdf8 100%) !important;
    }
    .stExpanderHeader {
        font-size: 1.2em !important;
        color: #1a202c !important;
        font-weight: 700 !important;
    }
    .stInfo, .stWarning, .stSuccess {
        border-radius: 10px !important;
        font-size: 1.05em !important;
        background: #e0f2fe !important;
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    .stCheckbox > label {
        font-size: 1.05em !important;
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #38bdf8 0%, #6366f1 100%) !important;
    }
    .stDivider {
        border-top: 2px solid #a5b4fc !important;
        margin: 2em 0 1.5em 0 !important;
    }
    /* Card style for all major sections */
    .stMarkdown > div, .stMarkdown > p, .stMarkdown > span {
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        color: #1a202c !important;
    }
    /* Section headers and labels */
    .stMarkdown strong, .stMarkdown b, .stMarkdown span, .stMarkdown label {
        color: #1a202c !important;
        font-weight: 700 !important;
    }
    </style>
''', unsafe_allow_html=True)

require_login()
role = get_current_role()


# Hide only the default Streamlit navigation, not the entire sidebar content
st.markdown("""
    <style>
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavItems"],
    .css-1v0mbdj.e1fqkh3o4 { display: none !important; }
    </style>
""", unsafe_allow_html=True)

import pandas as pd
import os
flats_path = "data/flats.csv"
project_list = ["Project 1"]

with st.sidebar:
    st.success(f"Current Role: {role}")
    logout_button()
    if role == "Customer":
        # Ensure project_list is always a list of strings
        project_list_path = "data/projects.csv"
        import csv
        if os.path.exists(project_list_path):
            with open(project_list_path, newline='') as f:
                reader = csv.reader(f)
                project_list = [row[0] for row in reader if row]
        else:
            project_list = ["No Projects"]
        project_list = [str(p) for p in project_list if p and str(p).strip() != ""]
        if not project_list:
            project_list = ["No Projects"]
        selected_project = st.selectbox("Select Project", project_list, key="customer_project")
        import re
        def safe_project_name(name):
            return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
        project_file = f"data/flats_{safe_project_name(selected_project)}.csv"
        if os.path.exists(project_file):
            df = pd.read_csv(project_file)
            # Always treat FlatID as string and strip whitespace
            df["FlatID"] = df["FlatID"].astype(str).str.strip()
            flat_list = [f for f in df["FlatID"].tolist() if f and f.strip() != ""]
            if not flat_list:
                flat_list = ["No Flats"]
            selected_flat = st.selectbox("Select Flat", flat_list, key="customer_flat")
            st.session_state["customer_selected_flat"] = selected_flat
        else:
            st.warning("No flats found for this project. Please ask the engineer to add a flat.")
            st.session_state["customer_selected_flat"] = None
    elif role == "Engineer":
        st.header("Engineer Navigation")
        # Project management (CRUD)
        with st.expander("Manage Projects"):
            project_list_path = "data/projects.csv"
            import csv
            if os.path.exists(project_list_path):
                with open(project_list_path, newline='') as f:
                    reader = csv.reader(f)
                    project_list = [row[0] for row in reader if row]
            else:
                project_list = ["Project 1"]
                with open(project_list_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Project 1"])
            new_project = st.text_input("Add New Project", key="engineer_new_project")
            if st.button("Add Project", key="engineer_add_project") and new_project:
                if new_project not in project_list:
                    project_list.append(new_project)
                    with open(project_list_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        for p in project_list:
                            writer.writerow([p])
                    st.success(f"Project '{new_project}' added.")
                    st.rerun()
            del_project = st.selectbox("Delete Project", [None] + project_list, key="engineer_del_project") if project_list else None
            if del_project and del_project != None:
                confirm_proj = st.checkbox(f"Are you sure you want to delete project '{del_project}'?", key="confirm_proj")
                if st.button("Delete Project", key="engineer_delete_project", type="primary", help="This will permanently delete the project.", use_container_width=True):
                    if confirm_proj:
                        project_list = [p for p in project_list if p != del_project]
                        with open(project_list_path, 'w', newline='') as f:
                            writer = csv.writer(f)
                            for p in project_list:
                                writer.writerow([p])
                        st.success(f"Project '{del_project}' deleted.")
                        st.rerun()
            st.markdown("""
                <style>
                button[data-testid=\"baseButton-engineer_delete_project\"] {
                    background-color: #ff4b4b !important;
                    color: white !important;
                }
                </style>
            """, unsafe_allow_html=True)
        # Ensure project_list is always a list of non-empty, stripped strings
        project_list = [str(p).strip() for p in project_list if p and str(p).strip() != "" and str(p).strip().lower() != "none"]
        if not project_list:
            project_list = ["No Projects"]
        selected_project = st.selectbox("Select Project", project_list, key="engineer_project")
        # Flat management (per project)
        import re
        def safe_project_name(name):
            return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
        project_file = f"data/flats_{safe_project_name(selected_project)}.csv"
        if os.path.exists(project_file):
            df = pd.read_csv(project_file, dtype={"FlatID": str})
            df["FlatID"] = df["FlatID"].astype(str).str.strip()
            flat_list = [f for f in df["FlatID"].tolist() if f and f.strip() != "" and f.strip().lower() != "none"]
        else:
            df = pd.DataFrame(columns=["FlatID","Owner","Designer","Engineer","Status"])
            flat_list = []
        # Add/delete flat
        with st.expander("Manage Flats"):
            new_flat = st.text_input("Add New Flat (FlatID)", key="engineer_new_flat")
            if st.button("Add Flat", key="engineer_add_flat") and new_flat:
                if new_flat not in flat_list:
                    df = pd.concat([df, pd.DataFrame([[new_flat, '', '', '', 'Design']], columns=df.columns)], ignore_index=True)
                    df.to_csv(project_file, index=False)
                    st.rerun()
            del_flat = st.selectbox("Delete Flat", [None] + flat_list, key="engineer_del_flat") if flat_list else None
            if del_flat and del_flat != None:
                confirm_flat = st.checkbox(f"Are you sure you want to delete flat '{del_flat}'?", key="confirm_flat")
                if st.button("Delete Flat", key="engineer_delete_flat", type="primary", help="This will permanently delete the flat.", use_container_width=True):
                    if confirm_flat:
                        df = df[df["FlatID"] != del_flat]
                        df.to_csv(project_file, index=False)
                        st.success(f"Flat '{del_flat}' deleted.")
                        st.rerun()
            st.markdown("""
                <style>
                button[data-testid=\"baseButton-engineer_delete_flat\"] {
                    background-color: #ff4b4b !important;
                    color: white !important;
                }
                </style>
            """, unsafe_allow_html=True)
        # Only add None if there are valid flats
        if flat_list:
            select_flat_options = [None] + flat_list
        else:
            select_flat_options = [None]
        selected_flat = st.selectbox("Select Flat", select_flat_options, key="engineer_flat")
        st.session_state["engineer_selected_flat"] = selected_flat


import numpy as np
# Main area content per role
if role == "Engineer":
    st.markdown("<span style='color:#2563eb;font-size:2.1em;font-weight:800;'>Engineer Project Dashboard</span>", unsafe_allow_html=True)
    # Project-specific flats file
    import re
    def safe_project_name(name):
        return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
    project_file = f"data/flats_{safe_project_name(selected_project)}.csv"
    if os.path.exists(project_file):
        df = pd.read_csv(project_file, dtype={"FlatID": str})
        df["FlatID"] = df["FlatID"].astype(str).str.strip()
        # Project dashboard: progress for each flat
        st.subheader("Project Progress (All Flats)")
        status_counts = df['Status'].str.lower().value_counts()
        total_flats = len(df)
        completed = status_counts.get('completed', 0)
        pending = total_flats - completed
        st.markdown(f"**Total Flats:** {total_flats}")
        st.markdown(f"**Completed:** {completed}")
        st.markdown(f"**Pending:** {pending}")
        st.progress(completed / total_flats if total_flats else 0)
        # Per-flat, per-unit progress table
        st.markdown("### Flat-wise Progress")
        unit_cols = ["Wardrobe_Status", "TV_Unit_Status", "Kitchen_Status", "Cupboard_Status"]
        for col in unit_cols:
            if col not in df.columns:
                df[col] = "Not Started"
        show_df = df[['FlatID'] + unit_cols].copy()
        st.dataframe(show_df)
        # Dropdown-based unit status update
        st.markdown("**Update Unit Status**")
        if len(df) > 0:
            flat_options = [str(f).strip() for f in df['FlatID'].tolist() if f and str(f).strip() != "" and str(f).strip().lower() != "none"]
            selected_flat_for_update = st.selectbox("Select Flat to Update Units", [None] + flat_options, key="unit_update_flat")
            if selected_flat_for_update and selected_flat_for_update != None:
                idxs = df.index[df['FlatID'] == selected_flat_for_update]
                if len(idxs) == 0:
                    st.warning(f"Selected flat '{selected_flat_for_update}' not found in data. Please check your data.")
                else:
                    idx = idxs[0]
                    current_statuses = {col: df.at[idx, col] if col in df.columns else "Not Started" for col in unit_cols}
                    new_statuses = {}
                    for unit, col in zip(["Wardrobe", "TV Unit", "Kitchen", "Cupboard"], unit_cols):
                        new_statuses[col] = st.selectbox(f"{unit} Status", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(current_statuses[col]) if current_statuses[col] in ["Not Started", "In Progress", "Completed"] else 0, key=f"update_{selected_flat_for_update}_{col}")
                    if any(new_statuses[col] != current_statuses[col] for col in unit_cols):
                        confirm = st.checkbox(f"Confirm update unit statuses for Flat {selected_flat_for_update}", key=f"confirm_update_{selected_flat_for_update}")
                        if st.button("Update Unit Statuses", key=f"update_units_{selected_flat_for_update}", type="primary"):
                            if confirm:
                                for col in unit_cols:
                                    df.at[idx, col] = new_statuses[col]
                                df.to_csv(project_file, index=False)
                                st.success(f"Unit statuses for Flat {selected_flat_for_update} updated.")
                                st.rerun()
        # Tasks summary for all flats
        all_tasks = []
        for flat in df['FlatID']:
            task_path = f"data/flat_{flat}_tasks.csv"
            if os.path.exists(task_path):
                task_df = pd.read_csv(task_path)
                all_tasks.append(task_df)
        if all_tasks:
            all_tasks_df = pd.concat(all_tasks, ignore_index=True)
            total_tasks = len(all_tasks_df)
            completed_tasks = (all_tasks_df['Status'].str.lower() == 'completed').sum()
            st.markdown(f"**Total Tasks:** {total_tasks}")
            st.markdown(f"**Completed Tasks:** {completed_tasks}")
            st.markdown(f"**Pending Tasks:** {total_tasks - completed_tasks}")
            st.progress(completed_tasks / total_tasks if total_tasks else 0)
        # Total material size for all flats
        total_size = 0
        for flat in df['FlatID']:
            mat_path = f"data/flat_{flat}_materials.csv"
            if os.path.exists(mat_path):
                mat_df = pd.read_csv(mat_path)
                if 'Size' in mat_df.columns:
                    total_size += mat_df['Size'].replace(np.nan, 0).astype(float).sum()
        st.markdown(f"**Total Material Size (All Flats):** {total_size}")
        # If a flat is selected, show its details
        selected_flat = st.session_state.get("engineer_selected_flat")
        if selected_flat and selected_flat != None:


            st.divider()
            st.subheader(f"Details for Flat {selected_flat}")
            # --- Materials Required (CRUD + Duplicate), split by 4 sections ---
            mat_path = f"data/flat_{selected_flat}_materials.csv"
            mat_columns = ["Section","Material","L","B","H","Size"]
            if os.path.exists(mat_path):
                mat_df = pd.read_csv(mat_path)
                # Ensure all required columns exist
                for col in mat_columns:
                    if col not in mat_df.columns:
                        mat_df[col] = ""
                mat_df = mat_df[mat_columns]
            else:
                mat_df = pd.DataFrame(columns=mat_columns)
            st.markdown("### Materials Required")
            section_materials = {
                "Wardrobe": ["Loft Doors", "Hinges", "Handles (Qty Only)", "Expo Piece", "Frame-Biding"],
                "Cupboard": ["Hinges", "Doors", "Expo Piece", "Inner Pieces", "Shelves", "Draws", "Back Panelling", "Top and Bottom Piece", "Locks", "Handles", "Tower Bolt", "Channel", "Mirror"],
                "TV Unit": ["Panelling Piece", "Draws Expo Piece", "Draw Inner Pieces", "Draw Outer Box", "Handles", "Channels", "Draw Fixing Screws"],
                "Kitchen": ["Loft Frame", "Loft Doors", "Expo Piece", "Hinges", "Tandem Basket & Channels", "Handles", "Doors", "Side Frames", "Panelling Frames", "Shelves", "Tandem Frame Pieces"]
            }
            # Unified add material form
            with st.expander("Add Material"):
                st.markdown("""
                <style>
                .stNumberInput > div > input {
                    background-color: #f0f7fa !important;
                    border-radius: 10px !important;
                    font-size: 1.1em !important;
                    color: #22223b !important;
                    box-shadow: 0 2px 8px #e0e7ef;
                    border: 1.5px solid #a5b4fc !important;
                    padding: 0.5em 1em !important;
                }
                .stSelectbox > div > div {
                    background-color: #f0f7fa !important;
                    border-radius: 10px !important;
                    font-size: 1.1em !important;
                    color: #22223b !important;
                    border: 1.5px solid #a5b4fc !important;
                }
                .stButton > button {
                    background: linear-gradient(90deg, #38bdf8 0%, #6366f1 100%) !important;
                    color: white !important;
                    border-radius: 10px !important;
                    font-weight: 700 !important;
                    font-size: 1.1em !important;
                    box-shadow: 0 2px 8px #a5b4fc;
                    border: none !important;
                    transition: background 0.2s;
                }
                .stButton > button:hover {
                    background: linear-gradient(90deg, #6366f1 0%, #38bdf8 100%) !important;
                }
                .stExpanderHeader {
                    font-size: 1.2em !important;
                    color: #2563eb !important;
                }
                </style>
                """, unsafe_allow_html=True)
                section = st.selectbox("Section", list(section_materials.keys()), key="mat_section_unified")
                material = st.selectbox("Material", section_materials[section], key="mat_material_unified")
                l = st.number_input("Length (L) in mm", min_value=0.0, value=1.0, step=0.1, format="%.1f", key="mat_l_unified")
                b = st.number_input("Breadth (B) in mm", min_value=0.0, value=1.0, step=0.1, format="%.1f", key="mat_b_unified")
                h = st.number_input("Height (H) in mm", min_value=0.0, value=1.0, step=0.1, format="%.1f", key="mat_h_unified")
                size = round(l * b * h, 1) if (l and b and h) else 0.0
                st.markdown(f"<span style='font-weight:600;font-size:1.1em;'>Calculated Size: <span style='color:#2563eb;font-size:1.15em'>{size}</span></span>", unsafe_allow_html=True)
                if st.button("Add Material", key=f"add_mat_btn_unified_{section}_{material}_{l}_{b}_{h}"):
                    new_row = pd.DataFrame([[section, material, l, b, h, size]], columns=["Section","Material","L","B","H","Size"])
                    mat_df = pd.concat([mat_df, new_row], ignore_index=True)
                    mat_df.to_csv(mat_path, index=False)
                    st.rerun()
            # Filterable display of all materials with delete button per row
            st.markdown("**All Materials**")
            filter_section = st.selectbox("Filter by Section", ["All"] + list(section_materials.keys()), key="mat_filter_section")
            filtered_df = mat_df.copy()
            if filter_section != "All":
                filtered_df = filtered_df[filtered_df['Section'] == filter_section]
            if not filtered_df.empty:
                st.markdown("""
                <style>
                .material-table {
                    background: #f8fafc;
                    border-radius: 16px;
                    box-shadow: 0 2px 8px 0 #e0e7ef;
                    padding: 0.5em 1em 1em 1em;
                    margin-bottom: 1.5em;
                }
                .material-table-header {
                    font-weight: 700;
                    color: #2563eb;
                    background: #e0f2fe;
                    border-radius: 12px 12px 0 0;
                    padding: 0.5em 0;
                }
                .material-table-row {
                    background: #f0f7fa;
                    border-radius: 8px;
                    margin-bottom: 0.2em;
                    transition: background 0.2s;
                }
                .material-table-row:hover {
                    background: #dbeafe;
                }
                </style>
                <div class='material-table'>
                <div class='material-table-header'>
                <div style='display:flex;gap:1em;'>
                    <div style='flex:2;'>Section</div>
                    <div style='flex:2;'>Material</div>
                    <div style='flex:1;'>L</div>
                    <div style='flex:1;'>B</div>
                    <div style='flex:1;'>H</div>
                    <div style='flex:1;'>Size</div>
                    <div style='flex:1;'></div>
                </div>
                </div>
                </div>
                """, unsafe_allow_html=True)
                import math
                for i, row in filtered_df.iterrows():
                    cols = st.columns([2,2,1,1,1,1,1])
                    def fmt(val, is_num=False):
                        if pd.isna(val) or val == '' or (isinstance(val, float) and math.isnan(val)):
                            return ""
                        if is_num:
                            try:
                                return f"{float(val):.1f}"
                            except:
                                return str(val)
                        return str(val)
                    with cols[0]:
                        st.markdown(f"<div class='material-table-row'>{fmt(row['Section'])}</div>", unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown(f"<div class='material-table-row'>{fmt(row['Material'])}</div>", unsafe_allow_html=True)
                    with cols[2]:
                        st.markdown(f"<div class='material-table-row'>{fmt(row['L'], True)}</div>", unsafe_allow_html=True)
                    with cols[3]:
                        st.markdown(f"<div class='material-table-row'>{fmt(row['B'], True)}</div>", unsafe_allow_html=True)
                    with cols[4]:
                        st.markdown(f"<div class='material-table-row'>{fmt(row['H'], True)}</div>", unsafe_allow_html=True)
                    with cols[5]:
                        st.markdown(f"<div class='material-table-row'>{fmt(row['Size'], True)}</div>", unsafe_allow_html=True)
                    with cols[6]:
                        if st.button("Delete", key=f"delete_mat_{row['Section']}_{row['Material']}_{row['L']}_{row['B']}_{row['H']}_{row['Size']}_{i}"):
                            idx = mat_df.index[(mat_df['Section'] == row['Section']) & (mat_df['Material'] == row['Material']) & (mat_df['L'] == row['L']) & (mat_df['B'] == row['B']) & (mat_df['H'] == row['H']) & (mat_df['Size'] == row['Size'])]
                            if not idx.empty:
                                mat_df = mat_df.drop(idx[0]).reset_index(drop=True)
                                mat_df.to_csv(mat_path, index=False)
                                st.rerun()
            else:
                st.info("No materials to display for this filter.")
            # Per-section total size
            for section in ["Kitchen", "Wardrobe", "TV Unit", "Cupboard"]:
                section_df = mat_df[mat_df['Section'].str.lower() == section.lower()] if not mat_df.empty else pd.DataFrame(columns=["Section","Material","L","B","H","Size"])
                st.markdown(f"**Total Size for {section}:** {section_df['Size'].replace(np.nan, 0).astype(float).sum() if 'Size' in section_df.columns else 0}")
            # Duplicate materials from another flat
            if len(df['FlatID']) > 1:
                st.markdown("**Duplicate Materials from Another Flat**")
                dup_flat = st.selectbox("Select Flat to Copy Materials From", [f for f in df['FlatID'] if f != selected_flat], key="dup_mat_flat")
                if st.button("Duplicate Materials", key="dup_mat_btn"):
                    src_path = f"data/flat_{dup_flat}_materials.csv"
                    if os.path.exists(src_path):
                        src_df = pd.read_csv(src_path)
                        src_df.to_csv(mat_path, index=False)
                        st.success(f"Materials duplicated from {dup_flat} to {selected_flat}")
                        st.rerun()

            # --- Flat Task Progress (Card CRUD) ---
            st.markdown("<hr style='border:1.5px solid #a5b4fc;margin:1.5em 0 1em 0;'>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:1.3em;font-weight:700;color:#2563eb;'>Tasks</span>", unsafe_allow_html=True)
            task_path = f"data/flat_{selected_flat}_tasks.csv"
            task_columns = ["Task","Details","AssignedTo","Status"]
            if os.path.exists(task_path):
                task_df = pd.read_csv(task_path)
                # Ensure all required columns exist
                for col in task_columns:
                    if col not in task_df.columns:
                        task_df[col] = ""
                task_df = task_df[task_columns]
            else:
                task_df = pd.DataFrame(columns=task_columns)
            # Display each task as a card with delete button
            if not task_df.empty:
                for i, row in task_df.iterrows():
                    cols = st.columns([10, 1.5])
                    with cols[0]:
                        st.markdown(f"""
                        <div style='background:#f0f7fa;border-radius:12px;box-shadow:0 2px 8px #e0e7ef;padding:1em 1.5em;margin-bottom:1em;position:relative;'>
                            <div style='font-size:1.1em;font-weight:600;color:#3b82f6;margin-bottom:0.2em;'>Task: {row['Task']}</div>
                            <div style='color:#64748b;margin-bottom:0.2em;'><b>Details:</b> {row['Details']}</div>
                            <div style='color:#64748b;margin-bottom:0.2em;'><b>Assigned To:</b> {row['AssignedTo']}</div>
                            <div style='color:#64748b;'><b>Status:</b> {row['Status']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with cols[1]:
                        confirm = st.checkbox("", key=f"confirm_delete_task_{i}", help="Confirm delete task")
                        if st.button("Delete", key=f"delete_task_{i}", help="Delete this task", use_container_width=True):
                            if confirm:
                                task_df = task_df.drop(i).reset_index(drop=True)
                                task_df.to_csv(task_path, index=False)
                                st.rerun()
            else:
                st.info("No tasks added yet.")

            # Add Task Form
            st.markdown("<div style='margin-top:2em;'></div>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:1.1em;font-weight:600;color:#6366f1;'>Add Task</span>", unsafe_allow_html=True)
            with st.form("add_task_form", clear_on_submit=True):
                task = st.text_input("Task Name")
                details = st.text_area("Details of Task")
                assigned_to = st.text_input("Person to Handle")
                status = st.selectbox("Status", ["Pending","Completed"])
                submitted = st.form_submit_button("Add Task")
                if submitted and task:
                    new_row = pd.DataFrame([[task, details, assigned_to, status]], columns=task_df.columns)
                    task_df = pd.concat([task_df, new_row], ignore_index=True)
                    task_df.to_csv(task_path, index=False)
                    st.success("Task added!")
                    st.rerun()


            # --- Installation Status ---
            inst_path = f"data/flat_{selected_flat}_installation.csv"
            if os.path.exists(inst_path):
                inst_df = pd.read_csv(inst_path)
                st.markdown("**Installation Status:**")
                st.dataframe(inst_df)
            else:
                st.info("No installation data for this flat.")
    else:
        st.warning("No flats found. Please add a flat first.")
elif role == "Customer":
    st.markdown("<span style='color:#2563eb;font-size:2.1em;font-weight:800;'>Customer Project Dashboard</span>", unsafe_allow_html=True)
    import re
    def safe_project_name(name):
        return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
    project_file = f"data/flats_{safe_project_name(selected_project)}.csv"
    if os.path.exists(project_file):
        df = pd.read_csv(project_file)
        # Project dashboard: progress for each flat
        st.subheader("Project Progress (All Flats)")
        status_counts = df['Status'].str.lower().value_counts()
        total_flats = len(df)
        completed = status_counts.get('completed', 0)
        pending = total_flats - completed
        st.markdown(f"**Total Flats:** {total_flats}")
        st.markdown(f"**Completed:** {completed}")
        st.markdown(f"**Pending:** {pending}")
        st.progress(completed / total_flats if total_flats else 0)
        # Per-flat progress table
        st.markdown("### Flat-wise Progress")
        st.dataframe(df[['FlatID', 'Status']])
        # If a flat is selected, show its details
        selected_flat = st.session_state.get("customer_selected_flat")
        if selected_flat and selected_flat != "No Flats":
            # Compare as stripped strings to avoid type/whitespace mismatch
            flat_df = df[df["FlatID"].astype(str).str.strip() == str(selected_flat).strip()]
            if not flat_df.empty:
                st.divider()
                st.subheader(f"Details for Flat {selected_flat}")
                # flat_row = flat_df.iloc[0]
                # st.markdown(f"**Owner:** {flat_row['Owner']}")
                # st.markdown(f"**Designer:** {flat_row['Designer']}")
                # st.markdown(f"**Engineer:** {flat_row['Engineer']}")
                # st.markdown(f"**Status:** {flat_row['Status']}")
                # --- Materials Used ---
                mat_path = f"data/flat_{selected_flat}_materials.csv"
                if os.path.exists(mat_path):
                    mat_df = pd.read_csv(mat_path)
                    st.markdown("**Materials Used:**")
                    st.dataframe(mat_df)
                else:
                    st.info("No materials data for this flat.")
                # --- Flat Task Progress ---
                task_path = f"data/flat_{selected_flat}_tasks.csv"
                if os.path.exists(task_path):
                    task_df = pd.read_csv(task_path)
                    completed_tasks = task_df[task_df['Status'].str.lower() == 'completed']
                    pending_tasks = task_df[task_df['Status'].str.lower() != 'completed']
                    st.markdown(f"**Tasks Completed:** {len(completed_tasks)} / {len(task_df)}")
                    st.progress(len(completed_tasks) / len(task_df) if len(task_df) else 0)
                    st.markdown("**Completed Tasks:**")
                    st.dataframe(completed_tasks[['Task', 'AssignedTo', 'Status']])
                    st.markdown("**Pending Tasks:**")
                    st.dataframe(pending_tasks[['Task', 'AssignedTo', 'Status']])
                else:
                    st.info("No tasks data for this flat.")
                # --- Moodboards ---
                st.markdown("**Moodboards:**")
                modules = ["Wardrobe", "Kitchen", "TV Unit", "Cupboard", "Bedroom", "Crockery", "Middle Box"]
                for module in modules:
                    gallery_path = f"data/moodboards/{selected_flat}_{module}"
                    if os.path.exists(gallery_path):
                        files = [f for f in os.listdir(gallery_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
                        if files:
                            st.markdown(f"*{module}*")
                            cols = st.columns(3)
                            for i, img in enumerate(files):
                                with cols[i % 3]:
                                    st.image(os.path.join(gallery_path, img), use_container_width=True)
                # --- Requirements ---
                # req_path = f"data/flat_{selected_flat}_requirements.csv"
                # if os.path.exists(req_path):
                #     req_df = pd.read_csv(req_path)
                #     st.markdown("**Requirements:**")
                #     st.dataframe(req_df)
                # else:
                #     st.info("No requirements data for this flat.")
                # # --- Installation Status ---
                # inst_path = f"data/flat_{selected_flat}_installation.csv"
                # if os.path.exists(inst_path):
                #     inst_df = pd.read_csv(inst_path)
                #     st.markdown("**Installation Status:**")
                #     st.dataframe(inst_df)
                # else:
                #     st.info("No installation data for this flat.")
            else:
                st.warning("Selected flat not found in project data. Please check your selection.")
    else:
        st.warning("No flats found for this project. Please ask the engineer to add a flat.")
## Remove Admin and Designer dashboards, only allow Customer and Engineer
