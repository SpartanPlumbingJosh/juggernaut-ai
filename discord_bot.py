#!/usr/bin/env python3
"""
DISCORD BOT FOR JUGGERNAUT AI
Provides mobile access to the existing Juggernaut AI system
Integrates with flux_hf_api.py for image generation
"""

import os
import sys
import asyncio
import logging
import json
from datetime import datetime
import discord
from discord.ext import commands
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JuggernautDiscordBot:
    def __init__(self):
        # Bot configuration
        self.bot_token = os.getenv('DISCORD_BOT_TOKEN', '')
        self.authorized_users = self.parse_user_list(os.getenv('DISCORD_AUTHORIZED_USERS', ''))
        self.admin_users = self.parse_user_list(os.getenv('DISCORD_ADMIN_USERS', ''))
        
        # Bot setup
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        # Setup bot events and commands
        self.setup_events()
        self.setup_commands()
        
        logger.info("Discord bot initialized")
    
    def parse_user_list(self, user_string):
        """Parse comma-separated user IDs"""
        if not user_string:
            return []
        try:
            return [int(uid.strip()) for uid in user_string.split(',') if uid.strip()]
        except ValueError:
            return []
    
    def setup_events(self):
        """Setup bot events"""
        
        @self.bot.event
        async def on_ready():
            logger.info(f"✅ {self.bot.user} is now online!")
            logger.info(f"Bot ID: {self.bot.user.id}")
            logger.info(f"Servers: {len(self.bot.guilds)}")
            
            # Set bot status
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name="for Juggernaut AI commands"
            )
            await self.bot.change_presence(activity=activity)
        
        @self.bot.event
        async def on_message(message):
            # Ignore bot's own messages
            if message.author == self.bot.user:
                return
            
            # Check authorization
            if not self.is_authorized(message.author.id):
                await message.reply("❌ You are not authorized to use this bot.")
                return
            
            # Process natural language commands
            if not message.content.startswith('!'):
                await self.handle_natural_language(message)
                return
            
            # Process bot commands
            await self.bot.process_commands(message)
        
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                await ctx.reply("❌ Command not found. Use `!help` for available commands.")
            else:
                logger.error(f"Command error: {error}")
                await ctx.reply(f"❌ Error: {str(error)}")
    
    def setup_commands(self):
        """Setup bot commands"""
        
        @self.bot.command(name='help')
        async def help_command(ctx):
            """Show help information"""
            embed = discord.Embed(
                title="🚀 Juggernaut AI Bot Commands",
                description="Your AI assistant with image generation capabilities",
                color=0xff4444
            )
            
            embed.add_field(
                name="🎨 Image Generation",
                value="`!image [prompt]` - Generate an image\n`!flux [prompt]` - Generate with FLUX.1",
                inline=False
            )
            
            embed.add_field(
                name="💬 Natural Language",
                value="Just type normally! No commands needed.\nExample: 'Generate an image of a sunset'",
                inline=False
            )
            
            embed.add_field(
                name="📊 System",
                value="`!status` - Bot status\n`!images` - List recent images",
                inline=False
            )
            
            embed.set_footer(text="Powered by Juggernaut AI")
            await ctx.reply(embed=embed)
        
        @self.bot.command(name='image', aliases=['img', 'generate'])
        async def generate_image(ctx, *, prompt):
            """Generate an image with FLUX.1"""
            await self.handle_image_generation(ctx, prompt)
        
        @self.bot.command(name='flux')
        async def flux_image(ctx, *, prompt):
            """Generate an image with FLUX.1"""
            await self.handle_image_generation(ctx, prompt)
        
        @self.bot.command(name='status')
        async def status(ctx):
            """Show bot status"""
            embed = discord.Embed(
                title="🤖 Bot Status",
                color=0x00ff00
            )
            
            embed.add_field(name="Status", value="✅ Online", inline=True)
            embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
            embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
            
            # Check FLUX status
            try:
                if os.path.exists("generated_images"):
                    images = os.listdir("generated_images")
                    embed.add_field(name="FLUX Status", value="✅ Ready", inline=True)
                    embed.add_field(name="Images Generated", value=len(images), inline=True)
                else:
                    embed.add_field(name="FLUX Status", value="⚠️ No images folder", inline=True)
            except Exception as e:
                embed.add_field(name="FLUX Status", value="❌ Error", inline=True)
            
            embed.set_footer(text=f"Uptime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            await ctx.reply(embed=embed)
        
        @self.bot.command(name='images')
        async def list_images(ctx):
            """List recent generated images"""
            try:
                if not os.path.exists("generated_images"):
                    await ctx.reply("📁 No images generated yet.")
                    return
                
                images = [f for f in os.listdir("generated_images") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                
                if not images:
                    await ctx.reply("📁 No images generated yet.")
                    return
                
                # Sort by modification time, newest first
                images.sort(key=lambda x: os.path.getmtime(os.path.join("generated_images", x)), reverse=True)
                
                embed = discord.Embed(
                    title="🎨 Recent Generated Images",
                    description=f"Showing last {min(10, len(images))} images",
                    color=0xff4444
                )
                
                for i, img in enumerate(images[:10]):
                    file_path = os.path.join("generated_images", img)
                    stat = os.stat(file_path)
                    embed.add_field(
                        name=f"{i+1}. {img}",
                        value=f"Size: {stat.st_size} bytes\nCreated: {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M')}",
                        inline=True
                    )
                
                await ctx.reply(embed=embed)
                
            except Exception as e:
                logger.error(f"Error listing images: {e}")
                await ctx.reply("❌ Error listing images.")
    
    async def handle_natural_language(self, message):
        """Handle natural language messages"""
        content = message.content.lower()
        
        # Check for image generation requests
        image_keywords = [
            'generate image', 'create image', 'make image', 'draw', 
            'generate picture', 'create picture', 'make picture',
            'image of', 'picture of', 'flux'
        ]
        
        if any(keyword in content for keyword in image_keywords):
            # Extract prompt
            prompt = self.extract_image_prompt(message.content)
            if prompt:
                await self.handle_image_generation(message, prompt)
            else:
                await message.reply("🎨 I'd love to generate an image! Please tell me what you want me to create.\nExample: 'Generate an image of a red sports car'")
        else:
            # General AI response
            await message.reply("🤖 I'm your Juggernaut AI assistant! I can generate images with FLUX.1.\n\nTry saying: 'Generate an image of a beautiful sunset' or use `!help` for commands.")
    
    def extract_image_prompt(self, message):
        """Extract image prompt from message"""
        message_lower = message.lower()
        
        # Look for patterns
        patterns = [
            'generate image of', 'create image of', 'make image of',
            'generate image:', 'create image:', 'make image:',
            'draw:', 'image of', 'picture of'
        ]
        
        for pattern in patterns:
            if pattern in message_lower:
                index = message_lower.find(pattern)
                prompt = message[index + len(pattern):].strip()
                if prompt:
                    return prompt
        
        # Look for simple patterns
        if 'generate' in message_lower and ('image' in message_lower or 'picture' in message_lower):
            # Remove command words and return the rest
            words_to_remove = ['generate', 'create', 'make', 'image', 'picture', 'of', 'a', 'an']
            words = message.split()
            filtered_words = [word for word in words if word.lower() not in words_to_remove]
            if filtered_words:
                return ' '.join(filtered_words)
        
        return None
    
    async def handle_image_generation(self, ctx, prompt):
        """Handle image generation requests"""
        try:
            # Send initial response
            if hasattr(ctx, 'reply'):
                initial_msg = await ctx.reply(f"🎨 Generating image: '{prompt}'\n⏳ Please wait...")
            else:
                initial_msg = await ctx.send(f"🎨 Generating image: '{prompt}'\n⏳ Please wait...")
            
            # Generate image using flux_hf_api.py
            try:
                result = subprocess.run([
                    'python', 'flux_hf_api.py', prompt
                ], capture_output=True, text=True, timeout=180)
                
                if result.returncode == 0:
                    # Parse output to find generated file
                    output_lines = result.stdout.strip().split('\n')
                    generated_file = None
                    
                    for line in output_lines:
                        if 'Image saved successfully:' in line:
                            generated_file = line.split('Image saved successfully: ')[-1].strip()
                            break
                    
                    if generated_file and os.path.exists(generated_file):
                        # Send success message with file
                        embed = discord.Embed(
                            title="✅ Image Generated Successfully!",
                            description=f"**Prompt:** {prompt}",
                            color=0x00ff00
                        )
                        
                        embed.set_footer(text=f"Generated with FLUX.1 • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        
                        # Send the image file
                        filename = os.path.basename(generated_file)
                        discord_file = discord.File(generated_file, filename=filename)
                        embed.set_image(url=f"attachment://{filename}")
                        
                        await initial_msg.edit(content="", embed=embed, attachments=[discord_file])
                    else:
                        await initial_msg.edit(content=f"✅ Image generated but file not found for upload.\nOutput: {result.stdout}")
                
                else:
                    # Send error message
                    error_output = result.stderr or result.stdout or "Unknown error"
                    embed = discord.Embed(
                        title="❌ Image Generation Failed",
                        description=f"**Prompt:** {prompt}\n**Error:** {error_output}",
                        color=0xff0000
                    )
                    
                    await initial_msg.edit(content="", embed=embed)
            
            except subprocess.TimeoutExpired:
                await initial_msg.edit(content="❌ Image generation timed out. Please try again.")
            except Exception as e:
                await initial_msg.edit(content=f"❌ Error running image generation: {str(e)}")
        
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            error_msg = f"❌ Error generating image: {str(e)}"
            
            if 'initial_msg' in locals():
                await initial_msg.edit(content=error_msg)
            else:
                if hasattr(ctx, 'reply'):
                    await ctx.reply(error_msg)
                else:
                    await ctx.send(error_msg)
    
    def is_authorized(self, user_id):
        """Check if user is authorized"""
        # If no authorized users set, allow everyone (for initial setup)
        if not self.authorized_users:
            return True
        
        return user_id in self.authorized_users or user_id in self.admin_users
    
    def run(self):
        """Run the bot"""
        if not self.bot_token:
            logger.error("❌ Bot token not set! Please set DISCORD_BOT_TOKEN environment variable.")
            print("\n🔧 SETUP INSTRUCTIONS:")
            print("1. Go to https://discord.com/developers/applications")
            print("2. Create a new application and bot")
            print("3. Copy the bot token")
            print("4. Set environment variable: set DISCORD_BOT_TOKEN=your_token_here")
            print("5. Run this script again")
            return
        
        try:
            logger.info("🚀 Starting Juggernaut AI Discord Bot...")
            self.bot.run(self.bot_token)
        except Exception as e:
            logger.error(f"❌ Error running bot: {e}")

def main():
    """Main function for running the bot"""
    print("🤖 JUGGERNAUT AI DISCORD BOT")
    print("=" * 40)
    print("Mobile access to your Juggernaut AI system")
    print("Integrates with flux_hf_api.py for image generation")
    print()
    
    bot = JuggernautDiscordBot()
    bot.run()

if __name__ == "__main__":
    main()

