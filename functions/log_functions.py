import random
from datetime import datetime, timedelta

from functions.random_ip import generate_random_public_ip
from functions.user_agents import user_agents, platform_probabilities

def generate_user_agent(user_id, user_sessions):
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'ip': generate_random_public_ip(),
            'user_agent': random.choices(user_agents, platform_probabilities, k=1)[0]
        }
    return user_sessions[user_id]['user_agent']

def generate_status_code():
    return random.choice([200, 201, 204, 301, 302, 400, 401, 403, 404, 500, 502, 503])

def get_user_ip(user_id, user_sessions):
    if user_id not in user_sessions:
        user_sessions[user_id] = {'ip': generate_random_public_ip(), 'user_agent': random.choices(user_agents, platform_probabilities, k=1)[0]}
    return user_sessions[user_id]['ip']

def generate_weighted_time():
    current_hour = datetime.now().hour
    weights = {
        0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.3, 7: 0.3, 8: 0.5, 9: 1.0,
        10: 1.0, 11: 1.0, 12: 1.0, 13: 1.0, 14: 1.0, 15: 1.0, 16: 1.0, 17: 1.0, 18: 1.5,
        19: 1.5, 20: 1.5, 21: 1.5, 22: 0.5, 23: 0.2
    }

    hours = list(weights.keys())
    probabilities = [weights[hour] for hour in hours]
    normalized_probabilities = [float(i)/sum(probabilities) for i in probabilities]
    chosen_hour = random.choices(hours, normalized_probabilities)[0]
    
    return datetime.now().replace(hour=chosen_hour, minute=random.randint(0, 59), second=random.randint(0, 59), microsecond=0)

def generate_timestamp():
    timestamp = generate_weighted_time()
    return timestamp.strftime("[%d/%b/%Y:%H:%M:%S %z]")

def parse_platform(user_agent):
    if "Windows NT" in user_agent:
        return "Windows"
    elif "Macintosh" in user_agent or "Mac OS X" in user_agent:
        return "Mac"
    elif "Android" in user_agent:
        return "Android"
    elif "iPhone" in user_agent or "iPad" in user_agent:
        return "iOS"
    elif "Linux" in user_agent and "Android" not in user_agent:
        return "Linux"
    else:
        return "Other"

def log_action(user_id, action, user_sessions, user_last_action):
    if user_id not in user_last_action:
        user_last_action[user_id] = datetime.now()

    if (datetime.now() - user_last_action[user_id]).total_seconds() > 300:  # 5 minutes
        del user_sessions[user_id]
        del user_last_action[user_id]
        return None

    ip_address = get_user_ip(user_id, user_sessions)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent(user_id, user_sessions)
    platform = parse_platform(user_agent)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "{action} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'

    user_last_action[user_id] = datetime.now()
    return log_entry

def log_search_product(user_id, user_sessions, user_last_action):
    search_term = random.choice(["laptop", "smartphone", "headphones", "shoes", "watch"])
    return log_action(user_id, f'GET /search?q={search_term}', user_sessions, user_last_action)

def log_view_product(user_id, user_sessions, user_last_action):
    product_id = random.randint(1000, 9999)
    return log_action(user_id, f'GET /product/{product_id}', user_sessions, user_last_action)

def log_add_to_cart(user_id, user_sessions, user_last_action):
    product_id = random.randint(1000, 9999)
    return log_action(user_id, f'POST /cart/add/{product_id}', user_sessions, user_last_action)

def log_remove_from_cart(user_id, user_sessions, user_last_action):
    product_id = random.randint(1000, 9999)
    return log_action(user_id, f'POST /cart/remove/{product_id}', user_sessions, user_last_action)

def log_compare_products(user_id, user_sessions, user_last_action):
    product_ids = random.sample(range(1000, 9999), 2)
    return log_action(user_id, f'GET /compare?products={product_ids[0]},{product_ids[1]}', user_sessions, user_last_action)

def log_apply_coupon(user_id, user_sessions, user_last_action):
    coupon_code = random.choice(["DISCOUNT10", "SAVE20", "FREESHIP"])
    return log_action(user_id, f'POST /cart/apply-coupon coupon={coupon_code}', user_sessions, user_last_action)

def log_purchase(user_id, user_sessions, user_last_action):
    order_id = random.randint(1000, 9999)
    if (datetime.now() - user_last_action.get(user_id, datetime.now())).total_seconds() > 300:
        return log_action(user_id, f'POST /purchase order_id={order_id} (Cancelled due to long payment process)', user_sessions, user_last_action)
    return log_action(user_id, f'POST /purchase order_id={order_id}', user_sessions, user_last_action)

def log_cancel_order(user_id, user_sessions, user_last_action):
    order_id = random.randint(1000, 9999)
    return log_action(user_id, f'POST /order/cancel order_id={order_id}', user_sessions, user_last_action)

def log_order_tracking(user_id, user_sessions, user_last_action):
    order_id = random.randint(1000, 9999)
    return log_action(user_id, f'GET /order/track/{order_id}', user_sessions, user_last_action)

def log_view_cart(user_id, user_sessions, user_last_action):
    return log_action(user_id, 'GET /cart/view', user_sessions, user_last_action)

def log_checkout(user_id, user_sessions, user_last_action):
    return log_action(user_id, 'POST /checkout', user_sessions, user_last_action)

def log_save_for_later(user_id, user_sessions, user_last_action):
    product_id = random.randint(1000, 9999)
    return log_action(user_id, f'POST /cart/save-for-later/{product_id}', user_sessions, user_last_action)

def log_view_wishlist(user_id, user_sessions, user_last_action):
    return log_action(user_id, 'GET /wishlist/view', user_sessions, user_last_action)

def log_add_to_wishlist(user_id, user_sessions, user_last_action):
    product_id = random.randint(1000, 9999)
    return log_action(user_id, f'POST /wishlist/add/{product_id}', user_sessions, user_last_action)

def log_remove_from_wishlist(user_id, user_sessions, user_last_action):
    product_id = random.randint(1000, 9999)
    return log_action(user_id, f'POST /wishlist/remove/{product_id}', user_sessions, user_last_action)

def log_write_review(user_id, user_sessions, user_last_action):
    product_id = random.randint(1000, 9999)
    return log_action(user_id, f'POST /product/{product_id}/review', user_sessions, user_last_action)

def log_view_order_history(user_id, user_sessions, user_last_action):
    return log_action(user_id, 'GET /order/history', user_sessions, user_last_action)

def log_contact_support(user_id, user_sessions, user_last_action):
    return log_action(user_id, 'POST /support/contact', user_sessions, user_last_action)
