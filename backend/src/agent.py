import logging
import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
from livekit import rtc
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation, assemblyai
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

# Load environment variables from .env.local first, then .env as fallback

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a friendly and enthusiastic barista at AgentX Coffee Shop. The user is interacting with you via voice.
            Your job is to take coffee orders and ensure all order details are complete.
            
            You need to collect the following information for each order:
            1. Drink type (e.g., latte, cappuccino, espresso, americano, mocha, cold brew)
            2. Size (small, medium, or large)
            3. Milk type (whole milk, skim milk, oat milk, almond milk, soy milk, or no milk)
            4. Extras (e.g., extra shot, whipped cream, caramel drizzle, vanilla syrup, sugar-free options)
            5. Customer name for the order
            
            Be conversational and friendly. Ask clarifying questions one at a time if information is missing.
            Once you have all the information, use the save_order tool to save the order.
            After saving, confirm the order details to the customer and thank them.
            
            Keep your responses natural and concise without complex formatting, emojis, or asterisks.""",
        )
        
        # Initialize order state
        self.order_state = {
            "drinkType": None,
            "size": None,
            "milk": None,
            "extras": [],
            "name": None
        }
        
        # Store room reference for sending data
        self.room = None
    
    def generate_drink_html(self):
        """Generate HTML visualization of the current drink order"""
        
        # Determine cup size - smaller to prevent overlap
        size_config = {
            "small": {"height": "80px", "width": "60px"},
            "medium": {"height": "95px", "width": "70px"},
            "large": {"height": "110px", "width": "80px"}
        }
        cup_size = size_config.get(self.order_state["size"], size_config["medium"])
        
        # Determine drink color based on type
        drink_colors = {
            "latte": "#D4A574",
            "cappuccino": "#A67C52",
            "espresso": "#4A2C2A",
            "americano": "#5D4037",
            "mocha": "#7B4B3A",
            "cold brew": "#6D4C41"
        }
        drink_color = drink_colors.get(self.order_state["drinkType"], "#A67C52")
        
        # Check for whipped cream
        has_whipped_cream = any("whipped cream" in extra.lower() for extra in self.order_state["extras"])
        
        # Build extras list
        extras_html = ""
        if self.order_state["extras"]:
            extras_items = "".join([f"<div style='margin: 2px 0; font-size: 12px;'>• {extra}</div>" for extra in self.order_state["extras"]])
            extras_html = f'<div style="margin: 0;">{extras_items}</div>'
        
        html = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; max-width: 260px; margin: 0 auto; color: white; box-shadow: 0 6px 20px rgba(0,0,0,0.3);">
            <div style="text-align: center; margin-bottom: 10px;">
                <h2 style="margin: 0; font-size: 17px; font-weight: 600; display: inline-flex; align-items: center; gap: 5px;">
                    <span style="font-size: 20px;">☕</span>
                    <span>AgentX Coffee</span>
                </h2>
            </div>
            
            <div style="background: white; border-radius: 10px; padding: 12px; color: #333; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <h3 style="margin: 0 0 10px 0; color: #667eea; text-align: center; font-size: 14px; font-weight: 600; border-bottom: 2px solid #e8eaf6; padding-bottom: 6px;">Your Order</h3>
                
                <!-- Drink Visualization -->
                <div style="display: flex; justify-content: center; align-items: center; margin: 10px 0; padding: 14px; background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px;">
                    <div style="position: relative; display: inline-block;">
                        <!-- Simple Modern Cup -->
                        <div style="position: relative; width: {cup_size['width']}; height: {cup_size['height']}; background: linear-gradient(to bottom, {drink_color} 0%, {drink_color} 85%, #3e2723 100%); border-radius: 0 0 15px 15px; box-shadow: 0 6px 12px rgba(0,0,0,0.2), inset -5px 0 10px rgba(0,0,0,0.1), inset 5px 0 10px rgba(255,255,255,0.1); border: 3px solid #3e2723; border-top: none;">
                            <!-- Cup Top/Rim -->
                            <div style="position: absolute; top: -8px; left: -3px; right: -3px; height: 12px; background: {drink_color}; border: 3px solid #3e2723; border-radius: 50%; box-shadow: inset 0 -2px 4px rgba(0,0,0,0.3);"></div>
                            
                            <!-- Whipped Cream -->
                            {f'''<div style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); width: calc(100% - 10px); height: 35px; background: radial-gradient(ellipse at center, #FFFEF7 0%, #FFF8E7 50%, #F5E6D3 100%); border-radius: 50% 50% 40% 40%; box-shadow: 0 2px 6px rgba(0,0,0,0.15); border: 2px solid #F0E5D8;"></div>
                            <div style="position: absolute; top: -30px; left: 50%; transform: translateX(-50%); width: 60%; height: 20px; background: radial-gradient(circle, #FFFFFF 0%, #FFFEF7 100%); border-radius: 50%; opacity: 0.9;"></div>''' if has_whipped_cream else ''}
                            
                            <!-- Cup Handle -->
                            <div style="position: absolute; right: -22px; top: 25%; width: 28px; height: 40%; border: 4px solid #3e2723; border-left: none; border-radius: 0 50% 50% 0; background: linear-gradient(to right, transparent 0%, {drink_color} 50%); opacity: 0.8;"></div>
                        </div>
                        
                        <!-- Size Badge -->
                        <div style="text-align: center; margin-top: 12px;">
                            <span style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 5px 14px; border-radius: 14px; font-weight: 700; font-size: 11px; letter-spacing: 1.2px; box-shadow: 0 2px 6px rg
                                  fill="url(#cupGradient)" 
                                  opacity="0.3"/>
                            
                            <!-- Cup Handle -->
                            <path d="M 150 80 Q 180 80 180 120 Q 180 160 150 160" 
                                  fill="none" 
                                  stroke="#2c1810" 
                                  stroke-width="8" 
                                  stroke-linecap="round"/>
                            <path d="M 150 85 Q 175 85 175 120 Q 175 155 150 155" 
                                  fill="none" 
                                  stroke="{drink_color}" 
                                  stroke-width="5" 
                                  stroke-linecap="round" 
                                  opacity="0.6"/>
                            
                            <!-- Whipped Cream -->
                            {f'''
                            <ellipse cx="90" cy="15" rx="55" ry="25" fill="#FFFAF0" stroke="#F5DEB3" stroke-width="2"/>
                            <ellipse cx="70" cy="10" rx="20" ry="15" fill="#FFFFFF" opacity="0.8"/>
                            <ellipse cx="110" cy="10" rx="20" ry="15" fill="#FFFFFF" opacity="0.8"/>
                            <ellipse cx="90" cy="5" rx="18" ry="12" fill="#FFFFFF" opacity="0.9"/>
                            ''' if has_whipped_cream else ''}
                            
                            <!-- Gradient Definition -->
                            <defs>
                                <linearGradient id="cupGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" style="stop-color:black;stop-opacity:0.3" />
                                    <stop offset="50%" style="stop-color:white;stop-opacity:0.1" />
                                    <stop offset="100%" style="stop-color:black;stop-opacity:0.2" />
                                </linearGradient>
                            </defs>
                        </svg>
                        
                        <!-- Size Label -->
                        <div style="text-align: center; margin-top: 10px;">
                            <span style="display: inline-block; background: #667eea; color: white; padding: 4px 12px; border-radius: 12px; font-weight: 700; font-size: 12px; letter-spacing: 1px;">
                                {self.order_state["size"].upper() if self.order_state["size"] else "SELECT SIZE"}
                            </span>
                        </div>
                    </div>
                </div>
                
                <!-- Order Details -->
                <div style="margin-top: 10px; background: #f8f9fa; border-radius: 8px; padding: 8px; font-size: 12px;">
                    <div style="display: grid; grid-template-columns: auto 1fr; gap: 5px 10px; align-items: start;">
                        <strong style="color: #667eea;">Drink:</strong>
                        <span>{self.order_state["drinkType"] or "Not selected"}</span>
                        
                        <strong style="color: #667eea;">Size:</strong>
                        <span>{self.order_state["size"] or "Not selected"}</span>
                        
                        <strong style="color: #667eea;">Milk:</strong>
                        <span>{self.order_state["milk"] or "Not selected"}</span>
                        
                        <strong style="color: #667eea;">Extras:</strong>
                        <div>{extras_html if self.order_state["extras"] else '<span style="color: #999; font-size: 11px;">None</span>'}</div>
                        
                        <strong style="color: #667eea;">Name:</strong>
                        <span>{self.order_state["name"] or "Not provided"}</span>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return html
    
    async def send_drink_visualization(self):
        """Send the drink visualization HTML to the frontend"""
        if self.room:
            try:
                html = self.generate_drink_html()
                # Send as data message
                await self.room.local_participant.publish_data(
                    html.encode('utf-8'),
                    topic="drink_visualization"
                )
                logger.info("Sent drink visualization to frontend")
            except Exception as e:
                logger.error(f"Failed to send visualization: {e}")
    
    def generate_receipt_html(self):
        """Generate HTML receipt for completed order"""
        extras_list = ", ".join(self.order_state["extras"]) if self.order_state["extras"] else "None"
        order_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        html = f"""
        <div style="font-family: 'Courier New', monospace; padding: 20px; background: white; border-radius: 12px; max-width: 350px; margin: 0 auto; color: #333; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border: 2px dashed #d4a574;">
            <div style="text-align: center; border-bottom: 2px dashed #d4a574; padding-bottom: 16px; margin-bottom: 16px;">
                <div style="font-size: 32px; margin-bottom: 8px;">☕</div>
                <h2 style="margin: 0; font-size: 22px; font-weight: bold; color: #8b4513;">AGENTX COFFEE SHOP</h2>
                <p style="margin: 4px 0 0 0; font-size: 12px; color: #666;">Order Receipt</p>
            </div>
            
            <div style="margin-bottom: 16px;">
                <p style="margin: 4px 0; font-size: 13px;"><strong>Order #:</strong> {datetime.now().strftime('%Y%m%d%H%M%S')}</p>
                <p style="margin: 4px 0; font-size: 13px;"><strong>Date:</strong> {order_time}</p>
                <p style="margin: 4px 0; font-size: 13px;"><strong>Customer:</strong> {self.order_state["name"]}</p>
            </div>
            
            <div style="border-top: 2px dashed #d4a574; border-bottom: 2px dashed #d4a574; padding: 12px 0; margin: 16px 0;">
                <p style="margin: 8px 0; font-size: 14px;"><strong>ITEM:</strong> {self.order_state["drinkType"].title()}</p>
                <p style="margin: 8px 0; font-size: 14px; padding-left: 20px;">Size: {self.order_state["size"].title()}</p>
                <p style="margin: 8px 0; font-size: 14px; padding-left: 20px;">Milk: {self.order_state["milk"]}</p>
                <p style="margin: 8px 0; font-size: 14px; padding-left: 20px;">Extras: {extras_list}</p>
            </div>
            
            <div style="text-align: center; margin-top: 16px; padding-top: 16px; border-top: 2px dashed #d4a574;">
                <p style="margin: 8px 0; font-size: 18px; font-weight: bold; color: #8b4513;">✓ ORDER CONFIRMED</p>
                <p style="margin: 8px 0; font-size: 13px; color: #666;">Your order will be ready shortly!</p>
            </div>
            
            <div style="text-align: center; margin-top: 16px; padding-top: 12px; border-top: 1px solid #e0e0e0;">
                <p style="margin: 4px 0; font-size: 11px; color: #999;">Thank you for choosing AgentX Coffee!</p>
                <p style="margin: 4px 0; font-size: 11px; color: #999;">Powered by AI Voice Technology ⚡</p>
            </div>
        </div>
        """
        return html
    
    async def send_receipt(self):
        """Send the receipt HTML to the frontend"""
        if self.room:
            try:
                html = self.generate_receipt_html()
                # Send as data message
                await self.room.local_participant.publish_data(
                    html.encode('utf-8'),
                    topic="order_receipt"
                )
                logger.info("Sent order receipt to frontend")
            except Exception as e:
                logger.error(f"Failed to send receipt: {e}")

    @function_tool
    async def save_order(self, context: RunContext):
        """Use this tool when all order information is collected (drinkType, size, milk, extras, and name).
        This will save the complete order to a JSON file.
        """
        
        # Check if all required fields are filled
        if not all([
            self.order_state["drinkType"],
            self.order_state["size"],
            self.order_state["milk"] is not None,
            self.order_state["name"]
        ]):
            return "Order is incomplete. Please collect all required information first."
        
        # Create orders directory if it doesn't exist
        orders_dir = Path("orders")
        orders_dir.mkdir(exist_ok=True)
        
        # Add timestamp to order
        order_with_timestamp = {
            **self.order_state,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        # Generate filename with timestamp
        filename = f"order_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.order_state['name'].replace(' ', '_')}.json"
        filepath = orders_dir / filename
        
        # Save to JSON file
        with open(filepath, 'w') as f:
            json.dump(order_with_timestamp, f, indent=2)
        
        logger.info(f"Order saved to {filepath}")
        logger.info(f"Order details: {json.dumps(order_with_timestamp, indent=2)}")
        
        # Generate and send receipt
        await self.send_receipt()
        
        # Reset order state for next customer
        self.order_state = {
            "drinkType": None,
            "size": None,
            "milk": None,
            "extras": [],
            "name": None
        }
        
        return f"Order saved successfully! Your order will be ready soon."
    
    @function_tool
    async def update_drink_type(self, context: RunContext, drink_type: str):
        """Update the drink type in the order.
        
        Args:
            drink_type: The type of drink (e.g., latte, cappuccino, espresso, americano, mocha, cold brew)
        """
        self.order_state["drinkType"] = drink_type
        logger.info(f"Updated drink type: {drink_type}")
        await self.send_drink_visualization()
        return f"Got it, {drink_type}."
    
    @function_tool
    async def update_size(self, context: RunContext, size: str):
        """Update the size in the order.
        
        Args:
            size: The size of the drink (small, medium, or large)
        """
        self.order_state["size"] = size.lower()
        logger.info(f"Updated size: {size}")
        await self.send_drink_visualization()
        return f"Perfect, {size} size."
    
    @function_tool
    async def update_milk(self, context: RunContext, milk_type: str):
        """Update the milk type in the order.
        
        Args:
            milk_type: The type of milk (whole milk, skim milk, oat milk, almond milk, soy milk, or no milk)
        """
        self.order_state["milk"] = milk_type
        logger.info(f"Updated milk: {milk_type}")
        await self.send_drink_visualization()
        return f"Noted, {milk_type}."
    
    @function_tool
    async def add_extra(self, context: RunContext, extra: str):
        """Add an extra item to the order.
        
        Args:
            extra: An extra item (e.g., extra shot, whipped cream, caramel drizzle, vanilla syrup)
        """
        if extra not in self.order_state["extras"]:
            self.order_state["extras"].append(extra)
        logger.info(f"Added extra: {extra}")
        await self.send_drink_visualization()
        return f"Added {extra}."
    
    @function_tool
    async def update_name(self, context: RunContext, customer_name: str):
        """Update the customer name for the order.
        
        Args:
            customer_name: The customer's name
        """
        self.order_state["name"] = customer_name
        logger.info(f"Updated name: {customer_name}")
        await self.send_drink_visualization()
        return f"Great, {customer_name}."
    
    @function_tool
    async def check_order_status(self, context: RunContext):
        """Check what information is still needed for the order.
        
        This function takes no parameters and returns the current order status.
        """
        missing = []
        if not self.order_state["drinkType"]:
            missing.append("drink type")
        if not self.order_state["size"]:
            missing.append("size")
        if self.order_state["milk"] is None:
            missing.append("milk preference")
        if not self.order_state["name"]:
            missing.append("name")
        
        if missing:
            return f"Still need: {', '.join(missing)}"
        else:
            return f"Order complete: {json.dumps(self.order_state, indent=2)}"


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=assemblyai.STT(),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
            model="gemini-flash-latest",
        ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
            voice="en-US-matthew",
            style="Conversation",
        ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=False,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Create assistant and set room reference
    assistant = Assistant()
    assistant.room = ctx.room
    
    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=assistant,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()

    # Send initial visualization to ensure UI is ready
    await assistant.send_drink_visualization()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
