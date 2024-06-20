import random
from datetime import datetime, timedelta
import pytz
import time

# Store user sessions to ensure consistent IP addresses for the same user
user_sessions = {}

# Define a list of User-Agent strings with different platforms
user_agents = [
    # Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",

    # Macintosh
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",

    # Linux
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",

    # Android
    "Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ2A.210405.005; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",

    # iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1",

    # Windows Phone
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36 Edge/15.15254",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 650) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36 Edge/15.15254",

    # Others
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
]


def generate_random_public_ip():
    while True:
        ip_parts = [random.randint(1, 223) for _ in range(4)]
        ip_parts[0] = random.choice([i for i in range(1, 224) if i != 127])  # Avoid reserved first octets
        ip = '.'.join(map(str, ip_parts))
        if not is_reserved_ip(ip):
            return ip

def is_reserved_ip(ip):
    parts = list(map(int, ip.split('.')))
    # Class A Private
    if parts[0] == 10:
        return True
    # Class B Private
    elif parts[0] == 172 and 16 <= parts[1] <= 31:
        return True
    # Class C Private
    elif parts[0] == 192 and parts[1] == 168:
        return True
    # Loopback
    elif parts[0] == 127:
        return True
    # Link-Local
    elif parts[0] == 169 and parts[1] == 254:
        return True
    # Multicast
    elif 224 <= parts[0] <= 239:
        return True
    # Broadcast
    elif parts == [255, 255, 255, 255]:
        return True
    # Reserved by IANA for future use
    elif parts[0] >= 240:
        return True
    # Public
    else:
        return False

def generate_user_agent():
    return random.choice(user_agents)

def generate_status_code():
    return random.choice([200, 201, 204, 301, 302, 400, 401, 403, 404, 500, 502, 503])

def get_user_ip(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = generate_random_public_ip()
    return user_sessions[user_id]

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

def log_search_product(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    search_term = random.choice(["laptop", "smartphone", "headphones", "shoes", "watch"])
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "GET /search?q={search_term} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_view_product(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    product_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "GET /product/{product_id} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_add_to_cart(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    product_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /cart/add/{product_id} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_remove_from_cart(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    product_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /cart/remove/{product_id} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_compare_products(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    product_ids = random.sample(range(1000, 9999), 2)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "GET /compare?products={product_ids[0]},{product_ids[1]} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_apply_coupon(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    coupon_code = random.choice(["DISCOUNT10", "SAVE20", "FREESHIP"])
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /cart/apply-coupon HTTP/1.1" {status_code} - "coupon={coupon_code}" "{user_agent}" "{platform}"'
    return log_entry

def log_purchase(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    order_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /purchase HTTP/1.1" {status_code} - "order_id={order_id}" "{user_agent}" "{platform}"'
    return log_entry

def log_cancel_order(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    order_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /order/cancel HTTP/1.1" {status_code} - "order_id={order_id}" "{user_agent}" "{platform}"'
    return log_entry

def log_order_tracking(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    order_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "GET /order/track/{order_id} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_view_cart(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "GET /cart/view HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_checkout(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /checkout HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_save_for_later(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    product_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /cart/save-for-later/{product_id} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_view_wishlist(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "GET /wishlist/view HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_add_to_wishlist(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    product_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /wishlist/add/{product_id} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_remove_from_wishlist(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    product_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /wishlist/remove/{product_id} HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_write_review(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    product_id = random.randint(1000, 9999)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /product/{product_id}/review HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_view_order_history(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "GET /order/history HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def log_contact_support(user_id):
    ip_address = get_user_ip(user_id)
    timestamp = generate_timestamp()
    user_agent = generate_user_agent()
    platform = parse_platform(user_agent)
    status_code = generate_status_code()
    log_entry = f'{ip_address} - - {timestamp} "POST /support/contact HTTP/1.1" {status_code} - "-" "{user_agent}" "{platform}"'
    return log_entry

def generate_logs(per_second, duration):
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
    
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        for _ in range(per_second):
            user_id = random.randint(1, 100)  # Simulate different users
            log_entry = random.choice(actions)(user_id)
            print(log_entry)
        time.sleep(1)

if __name__ == "__main__":
    logs_per_second = int(input("Enter the number of logs per second: "))
    duration_seconds = int(input("Enter the duration in seconds: "))
    generate_logs(logs_per_second, duration_seconds)
