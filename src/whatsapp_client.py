"""WhatsApp client for sending messages via Twilio."""

from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_FROM,
    YOUR_WHATSAPP_NUMBER
)


class WhatsAppClient:
    """Client for sending WhatsApp messages via Twilio."""
    
    def __init__(self):
        """Initialize Twilio client."""
        self.account_sid = TWILIO_ACCOUNT_SID
        self.auth_token = TWILIO_AUTH_TOKEN
        self.from_number = TWILIO_WHATSAPP_FROM
        self.to_number = YOUR_WHATSAPP_NUMBER
        self.client = None
    
    def connect(self):
        """Establish connection to Twilio."""
        try:
            self.client = Client(self.account_sid, self.auth_token)
            print("✅ Connected to Twilio WhatsApp")
            return True
        except Exception as e:
            print(f"❌ Error connecting to Twilio: {e}")
            raise
    
    def send_message(self, message: str) -> bool:
        """
        Send a message via WhatsApp.
        
        Args:
            message: The message text to send
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            self.connect()
        
        try:
            # Send message
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            
            print(f"✅ Message sent successfully!")
            print(f"   Message SID: {message_obj.sid}")
            print(f"   Status: {message_obj.status}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def send_weekly_report(self, report: str) -> bool:
        """
        Send weekly report via WhatsApp.
        
        Args:
            report: The weekly report text
        
        Returns:
            True if successful, False otherwise
        """
        # Add header
        message = f"🎯 Your Weekly Insights\n\n{report}"
        
        # Check message length (WhatsApp has 1600 char limit via Twilio)
        if len(message) > 1600:
            print("⚠️ Message too long, truncating...")
            message = message[:1580] + "\n\n... (truncated)"
        
        return self.send_message(message)
    
    def test_connection(self) -> bool:
        """Test connection by sending a test message."""
        test_msg = "🤖 Alpha-X Test\n\nIf you received this, setup is working!"
        return self.send_message(test_msg)


if __name__ == "__main__":
    # Test the WhatsApp client
    try:
        client = WhatsAppClient()
        client.test_connection()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\nMake sure:")
        print("1. Your .env file has correct Twilio credentials")
        print("2. You've joined the Twilio Sandbox (for testing)")
        print("3. Your WhatsApp number is correctly formatted")

