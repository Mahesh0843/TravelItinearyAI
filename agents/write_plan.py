from services.call_llm import ask_gemini

def write_plan(city, start, end, travelers, start_loc, likes, places, plan, forecast=None, budget="medium"):
    # Build a simple text version from the plan (fallback)
    days_text = ""
    if plan:
        for day in plan:
            days_text += f"\n**Day {day['day']}**\n"
            for act in day["activities"]:
                days_text += f"- {act['time']} {act['name']}\n"
            if forecast and day['day']-1 < len(forecast):
                fc = forecast[day['day']-1]
                days_text += f"\n*Weather: {fc['condition']}, {fc['temp']}°C*\n"
    else:
        days_text = "No activities planned."
    
    # Budget guidance
    budget_note = ""
    if "low" in budget.lower():
        budget_note = "Focus on free or low-cost attractions, suggest walking/public transit, and include budget-friendly dining."
    elif "medium" in budget.lower():
        budget_note = "Mix of free and paid attractions. Suggest reasonable dining options."
    elif "high" in budget.lower():
        budget_note = "Include premium experiences, fine dining, and optional private tours."
    
    prompt = f"""
    Create a friendly day-by-day itinerary for {city} from {start} to {end}.
    Travelers: {travelers}
    Starting location: {start_loc}
    Interests: {', '.join(likes)}
    Budget level: {budget}
    {budget_note}
    
    Use this activity plan:
    {days_text}
    
    Add short tips, mention weather if relevant, and keep it engaging.
    """
    
    llm_output = ask_gemini(prompt)
    if llm_output:
        return llm_output
    else:
        fallback = f"# Itinerary for {city}\n\n{days_text}\n\n*Note: AI generation failed – showing basic plan.*"
        return fallback