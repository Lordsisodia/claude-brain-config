#!/usr/bin/env python3
"""Quick Billion Token System"""
import os, asyncio, aiohttp
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BillionTokenSystem:
    def __init__(self):
        self.keys = {}
        self.stats = {"gemini": 0, "groq": 0}
        self.load_keys()
    
    def load_keys(self):
        # Load Gemini keys
        for i in range(1, 11):
            key = os.getenv(f'GEMINI_API_KEY_{i}')
            if key and 'XXX' not in key:
                self.keys[f'gemini_{i}'] = key
                print(f"✅ Loaded Gemini key {i}")
        
        # Load Groq keys  
        for i in range(1, 11):
            key = os.getenv(f'GROQ_API_KEY_{i}')
            if key and 'XXX' not in key:
                self.keys[f'groq_{i}'] = key
                print(f"✅ Loaded Groq key {i}")
    
    async def call_gemini(self, key, prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 500}
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, timeout=10) as response:
                if response.status == 200:
                    self.stats["gemini"] += 500
                    return True
                return False
    
    async def call_groq(self, key, prompt):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {key}"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data, timeout=10) as response:
                if response.status == 200:
                    self.stats["groq"] += 500
                    return True
                return False
    
    async def run_test(self):
        print("\n📊 SYSTEM CAPACITY:")
        gemini_keys = sum(1 for k in self.keys if k.startswith('gemini'))
        groq_keys = sum(1 for k in self.keys if k.startswith('groq'))
        
        daily_capacity = (gemini_keys * 6_000_000) + (groq_keys * 1_000_000)
        print(f"Gemini Keys: {gemini_keys} × 6M = {gemini_keys * 6_000_000:,} tokens/day")
        print(f"Groq Keys: {groq_keys} × 1M = {groq_keys * 1_000_000:,} tokens/day")
        print(f"TOTAL CAPACITY: {daily_capacity:,} tokens/day")
        
        if daily_capacity >= 1_000_000_000:
            print("🎯 YOU HAVE REACHED 1 BILLION TOKENS/DAY!")
        else:
            needed = (1_000_000_000 - daily_capacity) // 8_000_000
            print(f"Need {needed} more team members for 1B tokens/day")
        
        # Test a request
        print("\n🧪 Testing API connections...")
        for key_name, key in list(self.keys.items())[:2]:
            if 'gemini' in key_name:
                success = await self.call_gemini(key, "Say hello")
                print(f"Gemini: {'✅ Working' if success else '❌ Failed'}")
            elif 'groq' in key_name:
                success = await self.call_groq(key, "Say hello")
                print(f"Groq: {'✅ Working' if success else '❌ Failed'}")

async def main():
    print("="*50)
    print("BILLION TOKEN SYSTEM")
    print("="*50)
    
    system = BillionTokenSystem()
    
    if not system.keys:
        print("\n❌ No API keys found!")
        print("Please edit .env file and add your keys:")
        print("• Gemini: https://aistudio.google.com/apikey")
        print("• Groq: https://console.groq.com/keys")
        return
    
    await system.run_test()

if __name__ == "__main__":
    asyncio.run(main())
