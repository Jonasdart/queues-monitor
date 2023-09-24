from resources.database import get_all_messages
from typing import Optional
from resources.config import load_configs
from dotenv import load_dotenv
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from resources.queue_controller import reprocess_message_by_id, load_queues_definitions

st.set_page_config(layout="wide")
st_autorefresh(interval=10000)

load_dotenv()
configs = load_configs()

pages = {}


def queues_data_view(
    messages: list, field: str, sub_field: str, scape: Optional[str] = ""
):
    from resources.queue_controller import group_by_parameter, group_by_timestamp
    import streamlit as st
    from streamlit_timeline import st_timeline
    import pyperclip

    grouped_data = group_by_parameter(messages, field)

    expanded = True
    for item in grouped_data:
        if item:
            with st.expander(item, expanded=expanded):
                items = group_by_parameter(grouped_data[item], sub_field, scape)
                timeline = st_timeline(
                    group_by_timestamp(items),
                    groups=[],
                    options={},
                    height="500px",
                )
                st.subheader("Selected Message")

                try:
                    selected_message = timeline["id"]
                    pyperclip.copy(selected_message)
                    st.toast("Copied!", icon="✅")
                except TypeError:
                    selected_message = "🖱️ Click on timeline items to select them"

                st.code(selected_message)

                st.subheader("All Messages")
                st.json(items, expanded=False)

            if expanded:
                expanded = False

    reprocess = st.chat_input("Message to reprocess")
    if reprocess:
        reprocess_message_by_id(reprocess)


fields = {}
for queue in load_queues_definitions():
    for field in configs["fields"]:
        try:
            fields[queue.alias].append({"queue_id": queue.id, "field_name": field})
        except (TypeError, KeyError):
            fields[queue.alias] = [{"queue_id": queue.id, "field_name": field}]

for _field in fields:
    for field in fields[_field]:
        messages = get_all_messages(field["queue_id"])
        sub_field, scape = list(configs["fields"][field["field_name"]].items())[0]

        page_name = f"{_field} -> {field['field_name']} -> {sub_field}"
        pages[page_name] = {
            "page": queues_data_view,
            "field": field["field_name"],
            "subField": sub_field,
            "scape": scape,
            "messages": messages,
        }


page_name = st.sidebar.selectbox("Group queue data by", pages.keys())
pages[page_name]["page"](
    pages[page_name]["messages"],
    pages[page_name]["field"],
    pages[page_name]["subField"],
    pages[page_name]["scape"],
)
