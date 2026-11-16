# daily_earnings.py
def calculate_daily_earnings(user_id):
    # Fetch user activity for the day
    activity = get_user_activity(user_id)
    views = activity.get("views", 0)
    clicks = activity.get("clicks", 0)
    
    # Engine Five's rules (example)
    earnings_per_view = 0.01  # £0.01 per view
    earnings_per_click = 0.05  # £0.05 per click
    
    total_earnings = (views * earnings_per_view) + (clicks * earnings_per_click)
    
    # Cap at £15 for human verification
    max_earnings = 15
    return min(total_earnings, max_earnings)
