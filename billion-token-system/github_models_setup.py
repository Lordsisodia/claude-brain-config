#!/usr/bin/env python3
"""
GitHub Models Integration for Billion Token System
Adds GitHub Models API support with 40+ models
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()
console = Console()

class GitHubModelsClient:
    """GitHub Models API client"""
    
    def __init__(self):
        self.base_url = "https://models.inference.ai.azure.com"
        self.available_models = {
            # OpenAI Models
            "gpt-4o": {"tier": "high", "rpm": 10, "rpd": 50, "tokens_in": 8000, "tokens_out": 4000},
            "gpt-4o-mini": {"tier": "low", "rpm": 15, "rpd": 150, "tokens_in": 8000, "tokens_out": 4000},
            
            # Meta Llama Models  
            "llama-3.2-90b": {"tier": "high", "rpm": 10, "rpd": 50, "tokens_in": 4000, "tokens_out": 4000},
            "llama-3.2-11b": {"tier": "low", "rpm": 15, "rpd": 150, "tokens_in": 4000, "tokens_out": 4000},
            "llama-3.3-70b": {"tier": "high", "rpm": 10, "rpd": 50, "tokens_in": 4000, "tokens_out": 4000},
            
            # Microsoft Phi Models
            "phi-3-medium": {"tier": "low", "rpm": 15, "rpd": 150, "tokens_in": 4000, "tokens_out": 4000},
            "phi-3-mini": {"tier": "low", "rpm": 15, "rpd": 150, "tokens_in": 4000, "tokens_out": 4000},
            
            # Mistral Models
            "mistral-large": {"tier": "high", "rpm": 10, "rpd": 50, "tokens_in": 4000, "tokens_out": 4000},
            "mistral-small": {"tier": "low", "rpm": 15, "rpd": 150, "tokens_in": 4000, "tokens_out": 4000},
            
            # AI21 Labs
            "jamba-1.5-large": {"tier": "high", "rpm": 10, "rpd": 50, "tokens_in": 4000, "tokens_out": 4000},
            "jamba-1.5-mini": {"tier": "low", "rpm": 15, "rpd": 150, "tokens_in": 4000, "tokens_out": 4000}
        }
    
    def calculate_daily_capacity(self, github_tokens: int) -> dict:
        """Calculate daily token capacity based on models available"""
        capacity = {}
        total_capacity = 0
        
        for model, limits in self.available_models.items():
            # Conservative estimate: use 80% of daily requests
            daily_requests = int(limits["rpd"] * 0.8)
            avg_tokens_per_request = (limits["tokens_in"] + limits["tokens_out"]) // 2
            daily_tokens = daily_requests * avg_tokens_per_request
            
            capacity[model] = {
                "daily_requests": daily_requests,
                "tokens_per_request": avg_tokens_per_request,
                "daily_tokens": daily_tokens,
                "tier": limits["tier"]
            }
            total_capacity += daily_tokens
        
        return {
            "total_daily_tokens": total_capacity * github_tokens,
            "per_account": total_capacity,
            "models": capacity
        }
    
    async def test_github_models_access(self, github_token: str) -> dict:
        """Test GitHub Models API access"""
        if not github_token or 'XXX' in github_token:
            return {"success": False, "error": "No valid GitHub token"}
        
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json"
        }
        
        # Test with a simple model
        data = {
            "model": "gpt-4o-mini", 
            "messages": [{"role": "user", "content": "Hello from GitHub Models"}],
            "max_tokens": 50
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/chat/completions"
                async with session.post(url, headers=headers, json=data, timeout=15) as response:
                    if response.status == 200:
                        return {"success": True, "status": "✅ Working"}
                    else:
                        text = await response.text()
                        return {"success": False, "error": f"HTTP {response.status}: {text[:100]}"}
        except Exception as e:
            return {"success": False, "error": f"Connection failed: {str(e)[:50]}"}

async def main():
    """Test GitHub Models integration"""
    
    console.print("[bold cyan]🔬 GITHUB MODELS INTEGRATION TEST[/bold cyan]\n")
    
    client = GitHubModelsClient()
    
    # Show available models
    table = Table(title="Available GitHub Models", show_header=True, header_style="bold magenta")
    table.add_column("Model", style="cyan", width=20)
    table.add_column("Tier", justify="center", width=8)
    table.add_column("RPM", justify="center", width=6)
    table.add_column("RPD", justify="center", width=6)
    table.add_column("Daily Tokens", justify="right", style="yellow")
    
    for model, limits in client.available_models.items():
        daily_requests = int(limits["rpd"] * 0.8)  # Conservative 80%
        avg_tokens = (limits["tokens_in"] + limits["tokens_out"]) // 2
        daily_tokens = daily_requests * avg_tokens
        
        tier_color = "green" if limits["tier"] == "low" else "red"
        table.add_row(
            model,
            f"[{tier_color}]{limits['tier'].upper()}[/{tier_color}]",
            str(limits["rpm"]),
            str(limits["rpd"]),
            f"{daily_tokens:,}"
        )
    
    console.print(table)
    
    # Calculate capacity
    capacity = client.calculate_daily_capacity(1)  # Per account
    console.print(f"\n[yellow]Total Daily Capacity per GitHub Account: {capacity['per_account']:,} tokens[/yellow]")
    
    # Test access if token available
    github_tokens = []
    for i in range(1, 11):
        token = os.getenv(f'GITHUB_TOKEN_{i}')
        if token and 'XXX' not in token:
            github_tokens.append((i, token))
    
    if github_tokens:
        console.print(f"\n[green]Found {len(github_tokens)} GitHub tokens to test[/green]")
        
        for i, token in github_tokens:
            console.print(f"\nTesting GitHub token {i}...")
            result = await client.test_github_models_access(token)
            
            if result["success"]:
                console.print(f"✅ GitHub Models token {i}: {result['status']}")
            else:
                console.print(f"❌ GitHub Models token {i}: {result['error']}")
    else:
        console.print("\n[yellow]No GitHub tokens found in .env file[/yellow]")
        console.print("To add GitHub Models:")
        console.print("1. Go to: https://github.com/settings/tokens")
        console.print("2. Generate new token (classic)")
        console.print("3. Select scope: 'read:packages' or 'models:read'")
        console.print("4. Add to .env as: GITHUB_TOKEN_1=ghp_xxxx")
    
    # Show scaling potential
    console.print(f"\n[bold]SCALING POTENTIAL:[/bold]")
    console.print(f"• 1 GitHub account = {capacity['per_account']:,} tokens/day")
    console.print(f"• 10 GitHub accounts = {capacity['per_account'] * 10:,} tokens/day") 
    console.print(f"• 100 GitHub accounts = {capacity['per_account'] * 100:,} tokens/day")

if __name__ == "__main__":
    asyncio.run(main())