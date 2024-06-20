import random
import time
from datetime import datetime, timedelta

from functions.log_functions import (
    log_search_product,
    log_view_product,
    log_add_to_cart,
    log_remove_from_cart,
    log_compare_products,
    log_apply_coupon,
    log_purchase,
    log_cancel_order,
    log_order_tracking,
    log_view_cart,
    log_checkout,
    log_save_for_later,
    log_view_wishlist,
    log_add_to_wishlist,
    log_remove_from_wishlist,
    log_write_review,
    log_view_order_history,
    log_contact_support,
)

user_sessions = {}
user_last_action = {}
user_states = {}

def get_next_action(user_id):
    if user_id not in user_states:
        user_states[user_id] = 0
    actions = [
        log_search_product,
        log_view_product,
        log_add_to_cart,
        log_remove_from_cart,
        log_compare_products,
        log_apply_coupon,
        log_purchase,
        log_cancel_order,
        log_order_tracking,
        log_view_cart,
        log_checkout,
        log_save_for_later,
        log_view_wishlist,
        log_add_to_wishlist,
        log_remove_from_wishlist,
        log_write_review,
        log_view_order_history,
        log_contact_support
    ]
    next_action = actions[user_states[user_id]]
    user_states[user_id] += 1
    if user_states[user_id] >= len(actions):
        user_states[user_id] = 0
    return next_action

def generate_logs(per_second, duration):
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        for _ in range(per_second):
            user_id = random.randint(1, 100)  # Simulate different users
            action = get_next_action(user_id)
            log_entry = action(user_id, user_sessions, user_last_action)
            if log_entry:
                print(log_entry)
        time.sleep(1)

if __name__ == "__main__":
    logs_per_second = int(input("Enter the number of logs per second: "))
    duration_seconds = int(input("Enter the duration in seconds: "))
    generate_logs(logs_per_second, duration_seconds)
