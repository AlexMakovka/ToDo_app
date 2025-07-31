import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

FILE_PATH = "todo_data.csv"

LANGUAGES = {
    "ru": {
        "title": "📝 Todo-лист",
        "caption": "Управляй своими задачами с лёгкостью",
        "add_task": "➕ Добавить новую задачу",
        "choose_or_enter": "Выберите или введите задачу:",
        "or_enter_new": "Или введите новую задачу вручную:",
        "select_date": "Выберите дату задачи:",
        "select_time": "Выберите время задачи:",
        "add_button": "Добавить",
        "empty_warning": "Введите или выберите задачу.",
        "success_added": "Задача добавлена!",
        "filter_label": "Показать задачи:",
        "filter_all": "Все",
        "filter_not_done": "Только невыполненные",
        "filter_done": "Только выполненные",
        "task_list": "📋 Список задач",
        "no_tasks": "Нет задач для отображения.",
        "delete_button": "🗑️ Удалить",
        "done_stats": "📊 **Готово:** {done} из {total}",
        "theme_label": "Тема интерфейса",
        "theme_light": "Светлая",
        "theme_dark": "Тёмная",
        "sort_label": "Сортировать по:",
        "sort_created": "Дате создания",
        "sort_due": "Дате дедлайна",
        "sort_completed": "Выполненности",
        "search_placeholder": "🔍 Поиск задач...",
        "export_button": "📥 Скачать задачи Excel",
    },
    "uk": {
        "title": "📝 Todo-список",
        "caption": "Керуй своїми завданнями з легкістю",
        "add_task": "➕ Додати нове завдання",
        "choose_or_enter": "Оберіть або введіть завдання:",
        "or_enter_new": "Або введіть нове завдання вручну:",
        "select_date": "Оберіть дату завдання:",
        "select_time": "Оберіть час завдання:",
        "add_button": "Додати",
        "empty_warning": "Введіть або оберіть завдання.",
        "success_added": "Завдання додано!",
        "filter_label": "Показати завдання:",
        "filter_all": "Всі",
        "filter_not_done": "Тільки невиконані",
        "filter_done": "Тільки виконані",
        "task_list": "📋 Список завдань",
        "no_tasks": "Немає завдань для відображення.",
        "delete_button": "🗑️ Видалити",
        "done_stats": "📊 **Виконано:** {done} з {total}",
        "theme_label": "Тема інтерфейсу",
        "theme_light": "Світла",
        "theme_dark": "Темна",
        "sort_label": "Сортувати за:",
        "sort_created": "Датою створення",
        "sort_due": "Датою дедлайну",
        "sort_completed": "Виконанням",
        "search_placeholder": "🔍 Пошук завдань...",
        "export_button": "📥 Завантажити завдання Excel",
    },
    "de": {
        "title": "📝 Aufgabenliste",
        "caption": "Verwalte deine Aufgaben ganz einfach",
        "add_task": "➕ Neue Aufgabe hinzufügen",
        "choose_or_enter": "Wähle oder gib eine Aufgabe ein:",
        "or_enter_new": "Oder gib eine neue Aufgabe manuell ein:",
        "select_date": "Wähle das Aufgabendatum:",
        "select_time": "Wähle die Uhrzeit der Aufgabe:",
        "add_button": "Hinzufügen",
        "empty_warning": "Bitte gib eine Aufgabe ein oder wähle eine aus.",
        "success_added": "Aufgabe hinzugefügt!",
        "filter_label": "Aufgaben anzeigen:",
        "filter_all": "Alle",
        "filter_not_done": "Nur unerledigte",
        "filter_done": "Nur erledigte",
        "task_list": "📋 Aufgabenliste",
        "no_tasks": "Keine Aufgaben zum Anzeigen.",
        "delete_button": "🗑️ Löschen",
        "done_stats": "📊 **Erledigt:** {done} von {total}",
        "theme_label": "Theme",
        "theme_light": "Hell",
        "theme_dark": "Dunkel",
        "sort_label": "Sortieren nach:",
        "sort_created": "Erstellungsdatum",
        "sort_due": "Fälligkeitsdatum",
        "sort_completed": "Erledigt",
        "search_placeholder": "🔍 Aufgaben suchen...",
        "export_button": "📥 Aufgaben Excel herunterladen",
    },
    "en": {
        "title": "📝 Todo List",
        "caption": "Manage your tasks easily",
        "add_task": "➕ Add New Task",
        "choose_or_enter": "Choose or enter a task:",
        "or_enter_new": "Or enter a new task manually:",
        "select_date": "Select task date:",
        "select_time": "Select task time:",
        "add_button": "Add",
        "empty_warning": "Please enter or select a task.",
        "success_added": "Task added!",
        "filter_label": "Show tasks:",
        "filter_all": "All",
        "filter_not_done": "Only not done",
        "filter_done": "Only done",
        "task_list": "📋 Task List",
        "no_tasks": "No tasks to display.",
        "delete_button": "🗑️ Delete",
        "done_stats": "📊 **Done:** {done} of {total}",
        "theme_label": "Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "sort_label": "Sort by:",
        "sort_created": "Creation date",
        "sort_due": "Due date",
        "sort_completed": "Completion",
        "search_placeholder": "🔍 Search tasks...",
        "export_button": "📥 Download tasks Excel",
    }
}

def load_tasks():
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_csv(FILE_PATH)
            # Если нет колонок дедлайна, добавим их
            if "DueDate" not in df.columns:
                df["DueDate"] = ""
            if "DueTime" not in df.columns:
                df["DueTime"] = ""
            return df
        except (pd.errors.EmptyDataError, FileNotFoundError):
            return pd.DataFrame(columns=["Task", "Completed", "Created", "DueDate", "DueTime"])
    else:
        return pd.DataFrame(columns=["Task", "Completed", "Created", "DueDate", "DueTime"])

def save_tasks(df):
    df.to_csv(FILE_PATH, index=False)

def add_task(task_text, due_date, due_time, df):
    new_row = {
        "Task": task_text,
        "Completed": False,
        "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "DueDate": due_date.strftime("%Y-%m-%d") if due_date else "",
        "DueTime": due_time.strftime("%H:%M") if due_time else "",
    }
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

def delete_task(df, index):
    return df.drop(index).reset_index(drop=True)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Tasks")
    output.seek(0)  # Вернуть указатель потока в начало
    return output.getvalue()



def main():
    st.set_page_config(page_title="Todo List", page_icon="✅")

    lang = st.sidebar.selectbox("🌐 Язык / Language", options=list(LANGUAGES.keys()))
    t = LANGUAGES[lang]

    # Темы
    theme = st.sidebar.selectbox(t["theme_label"], [t["theme_light"], t["theme_dark"]])
    if theme == t["theme_dark"]:
        st.markdown(
            """
            <style>
            .main {
                background-color: #0e1117;
                color: white;
            }
            div.stButton > button {
                background-color: #333;
                color: white;
            }
            </style>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .main {
                background-color: white;
                color: black;
            }
            div.stButton > button {
                background-color: #eee;
                color: black;
            }
            </style>
            """, unsafe_allow_html=True
        )

    st.title(t["title"])
    st.caption(t["caption"])

    tasks_df = load_tasks()

    # Фильтр по выполненным
    filter_option = st.radio(t["filter_label"], [t["filter_all"], t["filter_not_done"], t["filter_done"]])

    # Сортировка
    sort_option = st.selectbox(
        t["sort_label"],
        [t["sort_created"], t["sort_due"], t["sort_completed"]]
    )

    # Поиск
    search_text = st.text_input(t["search_placeholder"])

    # Ввод задачи
    with st.form("task_form"):
        task_input = st.text_input(t["or_enter_new"])
        due_date = st.date_input(t["select_date"], value=None)
        due_time = st.time_input(t["select_time"], value=None)
        submitted = st.form_submit_button(t["add_button"])

    if submitted:
        task_text = task_input.strip()
        if task_text == "":
            st.warning(t["empty_warning"])
        else:
            tasks_df = add_task(task_text, due_date, due_time, tasks_df)
            save_tasks(tasks_df)
            st.success(t["success_added"])

    # Применяем фильтр
    if filter_option == t["filter_not_done"]:
        filtered_df = tasks_df[tasks_df["Completed"] == False]
    elif filter_option == t["filter_done"]:
        filtered_df = tasks_df[tasks_df["Completed"] == True]
    else:
        filtered_df = tasks_df.copy()

    # Применяем поиск
    if search_text:
        filtered_df = filtered_df[filtered_df["Task"].str.contains(search_text, case=False, na=False)]

    # Применяем сортировку
    if sort_option == t["sort_created"]:
        filtered_df["Created_dt"] = pd.to_datetime(filtered_df["Created"], errors='coerce')
        filtered_df = filtered_df.sort_values("Created_dt", ascending=True)
    elif sort_option == t["sort_due"]:
        def due_datetime(row_inner):
            try:
                return datetime.strptime(f"{row_inner['DueDate']} {row_inner['DueTime']}", "%Y-%m-%d %H:%M")
            except Exception:
                return datetime.max
        filtered_df["Due_dt"] = filtered_df.apply(due_datetime, axis=1)
        filtered_df = filtered_df.sort_values("Due_dt", ascending=True)
    elif sort_option == t["sort_completed"]:
        filtered_df = filtered_df.sort_values("Completed")

    filtered_df = filtered_df.reset_index(drop=True)

    st.subheader(t["task_list"])

    if filtered_df.empty:
        st.info(t["no_tasks"])
    else:
        for i, row in filtered_df.iterrows():
            cols = st.columns([0.05, 0.65, 0.2, 0.1])
            checkbox = cols[0].checkbox("Done", value=row["Completed"], key=f"cb_{i}", label_visibility="collapsed")
            if checkbox != row["Completed"]:
                idx = tasks_df[(tasks_df["Task"] == row["Task"]) & (tasks_df["Created"] == row["Created"])].index
                if len(idx) == 1:
                    tasks_df.at[idx[0], "Completed"] = checkbox
                    save_tasks(tasks_df)

            task_display = f"~~{row['Task']}~~" if checkbox else row['Task']
            due_text = ""
            if row["DueDate"]:
                due_text = f"📅 {row['DueDate']}"
            if row["DueTime"]:
                due_text += f" ⏰ {row['DueTime']}"

            cols[1].markdown(f"{task_display}  \n{due_text}")

            if cols[2].button(t["delete_button"], key=f"del_{i}"):
                idx = tasks_df[(tasks_df["Task"] == row["Task"]) & (tasks_df["Created"] == row["Created"])].index
                if len(idx) == 1:
                    tasks_df = delete_task(tasks_df, idx[0])
                    save_tasks(tasks_df)
                    st.rerun()

    st.markdown("---")
    total = len(tasks_df)
    done = tasks_df["Completed"].sum()
    st.markdown(t["done_stats"].format(done=done, total=total))

    st.download_button(
        label=t["export_button"],
        data=to_excel(tasks_df),
        file_name="tasks.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if __name__ == "__main__":
    main()
