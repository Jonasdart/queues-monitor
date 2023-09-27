from resources.database import get_all_messages
from typing import Optional
from resources.config import load_configs
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from resources.queue_controller import reprocess_message_by_id, load_queues_definitions

st.set_page_config(layout="wide")

streaming_activate = st.toggle("Streaming")

if streaming_activate:
    st_autorefresh(interval=10000)
    st.cache_data.clear()
    st.cache_resource.clear()

global_configs = load_configs()

pages = {}


def queues_data_view(
    messages: list,
    field: str,
    sub_field: str,
    scape: Optional[str] = "",
    configs: Optional[dict] = {},
):
    from resources.queue_controller import group_by_parameter, group_by_timestamp
    import streamlit as st
    from streamlit_timeline import st_timeline
    import pyperclip

    grouped_data = st.cache_resource(group_by_parameter)(messages, field)

    expanded = global_configs["defaults"]["expanded"]
    for item in grouped_data:
        if item:
            items = st.cache_resource(group_by_parameter)(
                grouped_data[item], sub_field, scape
            )
            title = item
            if configs.get("lastMessageOnTitle"):
                title = f"{item} 📌 {list(items.keys())[-1]}"

            with st.expander(title, expanded=expanded):
                timeline = st_timeline(
                    st.cache_resource(group_by_timestamp)(
                        items, sub_key=scape, configs=configs
                    ),
                    groups=[],
                    options={},
                    height="500px",
                )
                st.subheader("Selected Message")

                try:
                    selected_message = timeline["id"]
                    timeline = None
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


queues = {}
for queue in load_queues_definitions():
    for field in global_configs["fields"]:
        try:
            queues[queue.alias].append(
                {
                    "queue_id": queue.id,
                    "field_name": field,
                    "configs": global_configs["fields"][field].get("configs", {}),
                }
            )
        except (TypeError, KeyError):
            queues[queue.alias] = [
                {
                    "queue_id": queue.id,
                    "field_name": field,
                    "configs": global_configs["fields"][field].get("configs", {}),
                }
            ]

for queue in queues:
    for field in queues[queue]:
        messages = get_all_messages(field["queue_id"])
        field_definition = list(global_configs["fields"][field["field_name"]].items())
        sub_field, scape = field_definition[0]

        page_name = f"{queue} -> {field['field_name']} -> {sub_field}"

        pages[page_name] = {
            "page": queues_data_view,
            "field": field["field_name"],
            "subField": sub_field,
            "scape": scape,
            "configs": field["configs"],
            "messages": messages,
        }


page_name = st.sidebar.selectbox("Group queue data by", pages.keys())
pages[page_name]["page"](
    pages[page_name]["messages"],
    pages[page_name]["field"],
    pages[page_name]["subField"],
    pages[page_name]["scape"],
    pages[page_name]["configs"],
)
