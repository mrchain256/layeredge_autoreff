import asyncio
import aiohttp
import logging
from urllib.parse import urlparse
import os
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

user_agent = UserAgent(os=['windows', 'macos', 'linux'], browsers='chrome')
random_user_agent = user_agent.random

class LayerEdgeRegistration:
    def __init__(self, proxy_file='proxy.txt', wallet_file='wallet_addresses.txt'):
        self.proxy_file = proxy_file
        self.wallet_file = wallet_file
        self.proxies = []
        self.wallet_addresses = []

    async def load_resources(self):
        # Load proxies
        with open(self.proxy_file, 'r') as f:
            self.proxies = [line.strip() for line in f]
        
        # Load wallet addresses
        with open(self.wallet_file, 'r') as f:
            self.wallet_addresses = [line.strip() for line in f]
    
    def parse_proxy_url(self, proxy_url):
        try:
            parsed = urlparse(proxy_url)
            username = parsed.username or ''
            password = parsed.password or ''
            proxy_str = f"http://{username}:{password}@{parsed.hostname}:{parsed.port}"
            return proxy_str
        except Exception as e:
            logger.error(f"Invalid proxy URL: {proxy_url}. Error: {e}")
            return None

    """async def validate_invite(self, session, proxy):
        invite_url = 'https://dashboard.layeredge.io/api/validate-invite'
        headers = {
            ':authority': 'dashboard.layeredge.io',
            ':method': 'POST',
            ':path': '/api/validate-invite',
            ':scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://dashboard.layeredge.io',
            'user-agent': random_user_agent
        }
        payload = {'code': '6uGxSrsu'}

        async with session.post(invite_url, json=payload, headers=headers, proxy=proxy) as response:
            if response.status == 200:
                result = await response.json()
                return result.get('success', False)
            return False """

    async def register_wallet(self, session, wallet_address, proxy_url):
        try:
            register_url = 'https://dashboard.layeredge.io/api/proxy/register-wallet/6uGxSrsu'
            headers = {
                ':authority': 'dashboard.layeredge.io',
                ':method': 'POST',
                ':path': f'/api/proxy/register-wallet/6uGxSrsu',
                ':scheme': 'https',
                'accept': 'application/json',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'content-type': 'application/json',
                'origin': 'https://dashboard.layeredge.io',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            }
            payload = {'walletAddress': wallet_address}

            async with session.post(register_url, json=payload, headers=headers, proxy=proxy_url) as response:
                if response.status == 200:
                    logger.info(f"Successfully registered wallet: {wallet_address}")
                    return True
                else:
                    logger.warning(f"Wallet registration failed for {wallet_address}. Status: {response.status}")
        except Exception as e:
            logger.error(f"Registration failed: {e}")
        
        return False

    async def run(self):
        await self.load_resources()
        
        for proxy_url in self.proxies:
            parsed_proxy = self.parse_proxy_url(proxy_url)
            print(f"Connected with proxy: {parsed_proxy}")
            
            if not parsed_proxy:
                logger.error(f"Skipping invalid proxy: {proxy_url}")
                continue

            async with aiohttp.ClientSession() as session:
                # Validate invite
                # invite_valid = await self.validate_invite(session, proxy_connector)
                
                """if not invite_valid:
                    logger.warning(f"Invite validation failed for proxy: {proxy_url}")
                    continue """

                # Process wallets
                for wallet_address in self.wallet_addresses:
                    await self.register_wallet(session, wallet_address, parsed_proxy)

async def main():
    registration = LayerEdgeRegistration()
    await registration.run()

if __name__ == "__main__":
    asyncio.run(main())