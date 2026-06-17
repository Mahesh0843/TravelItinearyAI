from langgraph.graph import StateGraph, END
from graph.state import TripData
from graph.nodes import (
    parse_inputs, get_places, get_coords, get_weather,
    order_activities, add_maps, write_plan, send_alert
)
from graph.edges import need_weather

def build_main_graph():
    builder = StateGraph(TripData)

    builder.add_node("parse_inputs", parse_inputs)
    builder.add_node("get_places", get_places)
    builder.add_node("get_coords", get_coords)
    builder.add_node("get_weather", get_weather)
    builder.add_node("order_activities", order_activities)
    builder.add_node("add_maps", add_maps)
    builder.add_node("write_plan", write_plan)
    builder.add_node("send_alert", send_alert)

    builder.set_entry_point("parse_inputs")
    builder.add_edge("parse_inputs", "get_places")
    builder.add_edge("get_places", "get_coords")

    builder.add_conditional_edges("get_coords", need_weather, {
        "get_weather": "get_weather",
        "skip": "order_activities"
    })
    builder.add_edge("get_weather", "order_activities")
    builder.add_edge("order_activities", "add_maps")
    builder.add_edge("add_maps", "write_plan")
    builder.add_edge("write_plan", "send_alert")
    builder.add_edge("send_alert", END)

    return builder.compile()

main_graph = build_main_graph()