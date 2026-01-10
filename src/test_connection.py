"""Test script to verify all connections and setup."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from sheets_client import SheetsClient
from whatsapp_client import WhatsAppClient


def test_configuration():
    """Test configuration setup."""
    print("=" * 60)
    print("1️⃣ Testing Configuration")
    print("=" * 60)
    
    try:
        config.validate_config()
        print("✅ Configuration is valid!")
        print(f"   - Google Sheet ID: {config.GOOGLE_SHEET_ID[:20]}...")
        print(f"   - Credentials Path: {config.GOOGLE_CREDENTIALS_PATH}")
        print(f"   - WhatsApp Number: {config.YOUR_WHATSAPP_NUMBER}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_google_sheets():
    """Test Google Sheets connection."""
    print("\n" + "=" * 60)
    print("2️⃣ Testing Google Sheets Connection")
    print("=" * 60)
    
    try:
        client = SheetsClient()
        client.connect()
        
        # Try to fetch data
        df = client.get_all_data()
        print(f"✅ Successfully connected to Google Sheets!")
        print(f"   - Total records: {len(df)}")
        print(f"   - Columns: {list(df.columns)[:5]}...")
        
        if len(df) > 0:
            print(f"   - Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        return True
    except Exception as e:
        print(f"❌ Google Sheets error: {e}")
        print("\nTroubleshooting:")
        print("   - Make sure google_sheets_credentials.json is in credentials/")
        print("   - Share your Google Sheet with the service account email")
        print("   - Enable Google Sheets API in Google Cloud Console")
        return False


def test_whatsapp():
    """Test WhatsApp connection."""
    print("\n" + "=" * 60)
    print("3️⃣ Testing WhatsApp Connection")
    print("=" * 60)
    
    response = input("⚠️ This will send a test message to your WhatsApp. Continue? (y/n): ")
    
    if response.lower() != 'y':
        print("⏭️ Skipping WhatsApp test")
        return None
    
    try:
        client = WhatsAppClient()
        success = client.test_connection()
        
        if success:
            print("✅ Test message sent successfully!")
            print("   Check your WhatsApp for the test message")
            return True
        else:
            print("❌ Failed to send test message")
            return False
    except Exception as e:
        print(f"❌ WhatsApp error: {e}")
        print("\nTroubleshooting:")
        print("   - Check your Twilio credentials in .env")
        print("   - For testing: Join Twilio Sandbox by sending 'join <code>' to the sandbox number")
        print("   - Make sure your WhatsApp number format is correct: whatsapp:+countrycode_number")
        return False


def test_end_to_end():
    """Test end-to-end flow."""
    print("\n" + "=" * 60)
    print("4️⃣ Testing End-to-End Flow")
    print("=" * 60)
    
    response = input("⚠️ This will generate and send a weekly report. Continue? (y/n): ")
    
    if response.lower() != 'y':
        print("⏭️ Skipping end-to-end test")
        return None
    
    try:
        # Import main function
        from main import main
        
        # Run with dry_run=False to actually send
        print("\nGenerating weekly report...")
        main(weeks_ago=0, dry_run=False)
        
        print("✅ End-to-end test completed!")
        return True
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Alpha-X - Connection Test Suite                        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    results = {
        "Configuration": test_configuration(),
        "Google Sheets": test_google_sheets(),
        "WhatsApp": test_whatsapp(),
        "End-to-End": test_end_to_end()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⏭️ SKIPPED"
        
        print(f"{test_name:20s} {status}")
    
    print("=" * 60)
    
    # Overall result
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0 and passed > 0:
        print("\n🎉 All tests passed! Your setup is ready!")
    elif failed > 0:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
    
    print()


if __name__ == "__main__":
    main()

