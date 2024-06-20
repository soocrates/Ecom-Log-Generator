import random

def generate_random_public_ip():
    while True:
        ip_parts = [random.randint(1, 223) for _ in range(4)]
        ip_parts[0] = random.choice([i for i in range(1, 224) if i != 127])  # Avoid reserved first octets
        ip = '.'.join(map(str, ip_parts))
        if not is_reserved_ip(ip):
            return ip

def is_reserved_ip(ip):
    parts = list(map(int, ip.split('.')))
    if parts[0] == 10:
        return True
    elif parts[0] == 172 and 16 <= parts[1] <= 31:
        return True
    elif parts[0] == 192 and parts[1] == 168:
        return True
    elif parts[0] == 127:
        return True
    elif parts[0] == 169 and parts[1] == 254:
        return True
    elif 224 <= parts[0] <= 239:
        return True
    elif parts == [255, 255, 255, 255]:
        return True
    elif parts[0] >= 240:
        return True
    else:
        return False
