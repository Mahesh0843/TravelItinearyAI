from langgraph.graph import StateGraph, END
from graph.state import TripData
from graph.nodes import get_weather, fix_plan, send_alert
from graph.edges import need_fix

def build_update_graph():
    builder = StateGraph(TripData)
    builder.add_node("get_weather", get_weather)
    builder.add_node("fix_plan", fix_plan)
    builder.add_node("send_alert", send_alert)

    builder.set_entry_point("get_weather")
    builder.add_conditional_edges("get_weather", need_fix, {
        "fix_plan": "fix_plan",
        "normal": "send_alert"
    })
    builder.add_edge("fix_plan", "send_alert")
    builder.add_edge("send_alert", END)

    return builder.compile()

update_graph = build_update_graph()