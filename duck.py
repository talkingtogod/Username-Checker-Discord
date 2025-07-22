import asyncio
import json
import logging
import random
import string
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import aiohttp
import aiofiles
from colorama import init, Fore, Style, Back
init(autoreset=True)

class Display:
    @staticmethod
    def print_banner():
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║  {Fore.YELLOW}██████╗ ██╗   ██╗ ██████╗██╗  ██╗                                                  {Fore.CYAN} ║
║  {Fore.YELLOW}██╔══██╗██║   ██║██╔════╝██║ ██╔╝                                                  {Fore.CYAN} ║
║  {Fore.YELLOW}██║  ██║██║   ██║██║     █████╔╝                                                   {Fore.CYAN} ║
║  {Fore.YELLOW}██║  ██║██║   ██║██║     ██╔═██╗                                                   {Fore.CYAN} ║
║  {Fore.YELLOW}██████╔╝╚██████╔╝╚██████╗██║  ██╗                                                  {Fore.CYAN} ║
║  {Fore.YELLOW}╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝                                                  {Fore.CYAN} ║
║                                                                                      ║
║  {Fore.WHITE}Discord Username Availability Checker v1.0                                         {Fore.CYAN} ║
║  {Fore.LIGHTBLACK_EX}Advanced async implementation with JSON configuration                              {Fore.CYAN} ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)

    @staticmethod
    def print_section_header(title: str):
        width = 60
        padding = (width - len(title) - 2) // 2
        print(f"\n{Fore.CYAN}{'═' * width}")
        print(f"{'═' * padding} {Fore.WHITE}{title}{Fore.CYAN} {'═' * padding}")
        print(f"{'═' * width}{Style.RESET_ALL}")

    @staticmethod
    def print_config_display(config):
        print(f"\n{Fore.CYAN}┌─────────────────── Current Configuration ───────────────────┐")
        print(f"│ {Fore.WHITE}Token Mode:{Fore.YELLOW} {'Multi-Token' if config.multi_token_mode else 'Single Token':<20}{Fore.CYAN} │")
        print(f"│ {Fore.WHITE}Request Delay:{Fore.YELLOW} {config.request_delay}s{'':<15}{Fore.CYAN} │")
        print(f"│ {Fore.WHITE}Character Sets:{'':<35}{Fore.CYAN} │")
        print(f"│   {Fore.GREEN if config.enable_letters else Fore.RED}Letters: {'Enabled' if config.enable_letters else 'Disabled':<25}{Fore.CYAN} │")
        print(f"│   {Fore.GREEN if config.enable_numbers else Fore.RED}Numbers: {'Enabled' if config.enable_numbers else 'Disabled':<25}{Fore.CYAN} │")
        print(f"│   {Fore.GREEN if config.enable_symbols else Fore.RED}Symbols: {'Enabled' if config.enable_symbols else 'Disabled':<25}{Fore.CYAN} │")
        print(f"│ {Fore.WHITE}Webhook:{Fore.YELLOW} {'Configured' if config.webhook_url else 'Not Set':<28}{Fore.CYAN} │")
        print(f"└──────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")

    @staticmethod
    def print_menu():
        menu = f"""
{Fore.CYAN}┌────────────────── Main Menu ──────────────────┐
│                                               │
│  {Fore.WHITE}[1]{Fore.YELLOW} Generate and check random usernames      {Fore.CYAN}│
│  {Fore.WHITE}[2]{Fore.YELLOW} Check usernames from file                {Fore.CYAN}│
│  {Fore.WHITE}[3]{Fore.YELLOW} Show current configuration               {Fore.CYAN}│
│  {Fore.WHITE}[4]{Fore.YELLOW} Reconfigure settings                     {Fore.CYAN}│
│  {Fore.WHITE}[5]{Fore.YELLOW} Exit application                         {Fore.CYAN}│
│                                               │
└───────────────────────────────────────────────┘{Style.RESET_ALL}
"""
        print(menu)
    @staticmethod
    def print_status(message: str, status_type: str = "info"):
        icons = {
            "success": f"{Fore.GREEN}[+]",
            "error": f"{Fore.RED}[!]",
            "warning": f"{Fore.YELLOW}[*]",
            "info": f"{Fore.CYAN}[i]",
            "checking": f"{Fore.BLUE}[?]"
        }
        icon = icons.get(status_type, icons["info"])
        print(f"{icon} {Fore.WHITE}{message}{Style.RESET_ALL}")

    @staticmethod
    def print_username_result(username: str, is_available: bool):
        if is_available:
            print(f"{Fore.GREEN}✓ {Fore.WHITE}'{username}' is {Fore.GREEN}AVAILABLE!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {Fore.WHITE}'{username}' is {Fore.RED}TAKEN{Style.RESET_ALL}")

    @staticmethod
    def print_results(stats: Dict):
        print(f"\n\n{Fore.CYAN}╔══════════════════════ RESULTS ══════════════════════╗")
        print(f"║                                                      ║")
        print(f"║  {Fore.WHITE}Available Usernames Found: {Fore.GREEN}{stats['total_available']:<15}{Fore.CYAN} ║")
        print(f"║  {Fore.WHITE}Total Checked: {Fore.YELLOW}{stats.get('total_checked', 0):<26}{Fore.CYAN} ║")
        print(f"║  {Fore.WHITE}Output File: {Fore.MAGENTA}{stats['output_file']:<28}{Fore.CYAN} ║")
        print(f"║                                                      ║")
        print(f"╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}")

@dataclass
class Configuration:
    discord_token: str = ""
    request_delay: float = 0.5
    enable_letters: bool = True
    enable_numbers: bool = True
    enable_symbols: bool = False
    webhook_url: str = ""
    multi_token_mode: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


class ConfigManager:

    def __init__(self, config_path: Path = Path("config.json")):
        self.config_path = config_path
        self.config = Configuration()

    async def load_or_create_config(self) -> Configuration:
        if self.config_path.exists():
            await self._load_existing_config()
        else:
            await self._create_new_config()

        return self.config

    async def _load_existing_config(self) -> None:
        try:
            async with aiofiles.open(self.config_path, 'r') as file:
                data = json.loads(await file.read())
                self.config = Configuration(**data)
                Display.print_status("Configuration loaded successfully", "success")
        except Exception as error:
            Display.print_status(f"Failed to load config: {error}", "error")
            await self._create_new_config()

    async def _create_new_config(self) -> None:
        Display.print_section_header("CONFIGURATION SETUP")

        print(f"{Fore.YELLOW}Setting up your Discord Username Checker configuration...")
        print(f"{Fore.LIGHTBLACK_EX}Please provide the following information:\n")

        print(f"{Fore.CYAN}┌─── Discord Token ───┐")
        self.config.discord_token = input(f"│ {Fore.WHITE}Enter token: {Fore.YELLOW}").strip()
        print(f"{Fore.CYAN}└─────────────────────┘")

        print(f"\n{Fore.CYAN}┌─── Request Settings ───┐")
        delay_input = input(f"│ {Fore.WHITE}Delay between requests (seconds) [{Fore.GREEN}0.5{Fore.WHITE}]: {Fore.YELLOW}").strip()
        self.config.request_delay = float(delay_input) if delay_input else 0.5
        print(f"{Fore.CYAN}└─────────────────────────┘")

        print(f"\n{Fore.CYAN}┌─── Character Sets ───┐")
        self.config.enable_letters = self._get_boolean_input(f"│ {Fore.WHITE}Include letters (a-z)? {Fore.GREEN}[Y/n]: ")
        self.config.enable_numbers = self._get_boolean_input(f"│ {Fore.WHITE}Include numbers (0-9)? {Fore.GREEN}[Y/n]: ")
        self.config.enable_symbols = self._get_boolean_input(f"│ {Fore.WHITE}Include symbols (._)? {Fore.RED}[y/N]: ", default=False)
        print(f"{Fore.CYAN}└───────────────────────┘")

        print(f"\n{Fore.CYAN}┌─── Webhook (Optional) ───┐")
        webhook = input(f"│ {Fore.WHITE}Webhook URL: {Fore.YELLOW}").strip()
        self.config.webhook_url = webhook if webhook else ""
        print(f"{Fore.CYAN}└──────────────────────────┘")

        print(f"\n{Fore.CYAN}┌─── Token Mode ───┐")
        self.config.multi_token_mode = self._get_boolean_input(f"│ {Fore.WHITE}Multi-token mode? {Fore.RED}[y/N]: ", default=False)
        print(f"{Fore.CYAN}└───────────────────┘")

        await self._save_config()
        Display.print_status("Configuration created successfully", "success")

    def _get_boolean_input(self, prompt: str, default: bool = True) -> bool:
        while True:
            response = input(prompt).strip().lower()
            if not response:
                return default
            if response in ['y', 'yes', 'true', '1']:
                return True
            elif response in ['n', 'no', 'false', '0']:
                return False
            Display.print_status("Please enter y/n", "warning")

    async def _save_config(self) -> None:
        async with aiofiles.open(self.config_path, 'w') as file:
            await file.write(json.dumps(self.config.to_dict(), indent=2))
        Display.print_status("Configuration saved", "success")

class DiscordAPI:

    BASE_URL = "https://discord.com/api/v9"
    POMELO_ENDPOINT = f"{BASE_URL}/users/@me/pomelo-attempt"
    USER_ENDPOINT = f"{BASE_URL}/users/@me"

    def __init__(self, config: Configuration):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.current_token_index = 0
        self.tokens = self._load_tokens() if config.multi_token_mode else [config.discord_token]

    def _load_tokens(self) -> List[str]:
        try:
            with open("tokens.txt", 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            Display.print_status("tokens.txt not found, using single token mode", "warning")
            return [self.config.discord_token]

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Origin": "https://discord.com",
            "Authorization": self.tokens[self.current_token_index]
        }

    async def check_username_availability(self, username: str) -> Tuple[bool, Optional[str]]:
        payload = {"username": username}

        try:
            async with self.session.post(
                self.POMELO_ENDPOINT,
                headers=self._get_headers(),
                json=payload
            ) as response:

                if response.status == 429:
                    return await self._handle_rate_limit_and_retry(response, username)

                try:
                    data = await response.json()
                except:
                    return False, "Failed to parse response"

                if data.get("taken") is not None:
                    return not data["taken"], None
                else:
                    error_msg = data.get("message", "Unknown error")
                    return False, error_msg

        except Exception as error:
            return False, str(error)

    async def _handle_rate_limit_and_retry(self, response: aiohttp.ClientResponse, username: str) -> Tuple[bool, Optional[str]]:
        if self.config.multi_token_mode and len(self.tokens) > 1:
            old_index = self.current_token_index
            self.current_token_index = (self.current_token_index + 1) % len(self.tokens)

            if self.current_token_index != old_index:
                Display.print_status(f"Switched to token {self.current_token_index + 1}/{len(self.tokens)}", "warning")
                return await self.check_username_availability(username)

        try:
            data = await response.json()
            retry_after = data.get("retry_after", 5)
        except:
            retry_after = 5

        Display.print_status(f"Rate limited, waiting {retry_after} seconds", "warning")
        await asyncio.sleep(retry_after)
        return await self.check_username_availability(username)

    async def get_current_user(self) -> Optional[Dict]:
        try:
            async with self.session.get(
                self.USER_ENDPOINT,
                headers=self._get_headers()
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except Exception as error:
            Display.print_status(f"Failed to get user info: {error}", "error")
            return None

class UsernameGenerator:

    def __init__(self, config: Configuration):
        self.config = config
        self.character_pool = self._build_character_pool()

    def _build_character_pool(self) -> str:
        pool = ""

        if self.config.enable_letters:
            pool += string.ascii_lowercase

        if self.config.enable_numbers:
            pool += string.digits

        if self.config.enable_symbols:
            pool += "_."

        return pool or string.ascii_lowercase 

    def generate(self, length: int) -> str:
        if not 2 <= length <= 32:
            raise ValueError("Username length must be between 2 and 32 characters")

        return ''.join(random.choices(self.character_pool, k=length))

    def generate_batch(self, count: int, length: int) -> List[str]:
        return [self.generate(length) for _ in range(count)]

class ResultManager:

    def __init__(self, output_file: Path = Path("available_usernames.txt")):
        self.output_file = output_file
        self.available_usernames: List[str] = []
        self.total_checked = 0

    async def save_username(self, username: str) -> None:
        self.available_usernames.append(username)
        async with aiofiles.open(self.output_file, 'a') as file:
            await file.write(f"{username}\n")

    def increment_checked(self):
        self.total_checked += 1

    def get_stats(self) -> Dict[str, int]:
        return {
            "total_available": len(self.available_usernames),
            "total_checked": self.total_checked,
            "output_file": str(self.output_file)
        }

class WebhookNotifier:

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url)

    async def notify_available_username(self, username: str) -> None:
        if not self.enabled:
            return

        payload = {
            "username": "DUCK - Username Checker",
            "embeds": [{
                "title": f"Username Available: {username}",
                "color": 0x00ff00,
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {"text": "DUCK v2.0"}
            }]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 204:
                        Display.print_status(f"Webhook sent for {username}", "success")
        except Exception as error:
            Display.print_status(f"Webhook failed: {error}", "error")

class UsernameChecker:

    def __init__(self):
        self.config_manager = ConfigManager()
        self.config: Optional[Configuration] = None
        self.discord_api: Optional[DiscordAPI] = None
        self.generator: Optional[UsernameGenerator] = None
        self.result_manager = ResultManager()
        self.webhook_notifier: Optional[WebhookNotifier] = None

        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    async def initialize(self) -> None:
        Display.print_banner()

        self.config = await self.config_manager.load_or_create_config()
        self.generator = UsernameGenerator(self.config)
        self.webhook_notifier = WebhookNotifier(self.config.webhook_url)

        async with DiscordAPI(self.config) as api:
            user_info = await api.get_current_user()
            if not user_info:
                Display.print_status("Invalid Discord token!", "error")
                sys.exit(1)

            username = user_info.get('username', 'Unknown')
            discriminator = user_info.get('discriminator', '0000')
            Display.print_status(f"Connected as: {username}#{discriminator}", "success")

            self.discord_api = api

    async def run(self) -> None:
        await self.initialize()

        while True:
            Display.print_menu()
            choice = input(f"\n{Fore.WHITE}Select option {Fore.CYAN}[1-5]: {Fore.YELLOW}").strip()

            if choice == "1":
                await self._handle_generate_mode()
            elif choice == "2":
                await self._handle_file_mode()
            elif choice == "3":
                Display.print_config_display(self.config)
            elif choice == "4":
                await self._reconfigure()
            elif choice == "5":
                Display.print_section_header("GOODBYE")
                sys.exit(0)
            else:
                Display.print_status("Invalid choice! Please select 1-5", "error")

    async def _reconfigure(self) -> None:
        await self.config_manager._create_new_config()
        self.config = self.config_manager.config
        self.generator = UsernameGenerator(self.config)
        self.webhook_notifier = WebhookNotifier(self.config.webhook_url)

    async def _handle_generate_mode(self) -> None:
        Display.print_section_header("GENERATE MODE")

        try:
            length = int(input(f"{Fore.WHITE}Username length {Fore.CYAN}[2-32]: {Fore.YELLOW}"))
            if not 2 <= length <= 32:
                Display.print_status("Length must be between 2 and 32!", "error")
                return

            count = int(input(f"{Fore.WHITE}Number to generate: {Fore.YELLOW}"))
            if count <= 0:
                Display.print_status("Count must be positive!", "error")
                return

            usernames = self.generator.generate_batch(count, length)
            await self._check_usernames(usernames)

        except ValueError:
            Display.print_status("Please enter valid numbers!", "error")

    async def _handle_file_mode(self) -> None:
        Display.print_section_header("FILE MODE")

        file_path = Path("usernames.txt")

        if not file_path.exists():
            Display.print_status(f"File {file_path} not found!", "error")
            return

        try:
            async with aiofiles.open(file_path, 'r') as file:
                usernames = [line.strip() for line in await file.readlines() if line.strip()]

            Display.print_status(f"Loaded {len(usernames)} usernames from file", "info")
            await self._check_usernames(usernames)

        except Exception as error:
            Display.print_status(f"Error reading file: {error}", "error")

    async def _check_usernames(self, usernames: List[str]) -> None:
        Display.print_section_header("CHECKING USERNAMES")

        async with DiscordAPI(self.config) as api:
            for username in usernames:
                is_available, error = await api.check_username_availability(username)
                self.result_manager.increment_checked()

                if error:
                    Display.print_status(f"Error checking '{username}': {error}", "error")
                elif is_available:
                    Display.print_username_result(username, True)
                    await self.result_manager.save_username(username)
                    await self.webhook_notifier.notify_available_username(username)
                else:
                    Display.print_username_result(username, False)

                await asyncio.sleep(self.config.request_delay)

            stats = self.result_manager.get_stats()
            Display.print_results(stats)

async def main():
    checker = UsernameChecker()
    await checker.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Application interrupted by user{Style.RESET_ALL}")
    except Exception as error:
        print(f"{Fore.RED}Unexpected error: {error}{Style.RESET_ALL}")
        sys.exit(1)




      

# by @midlegg on discord
# by @midlegg on discord
# by @talkingtogod on github, make it better, remove the loader bar, if taken then red x if not taken green also put this in the ascii art 
