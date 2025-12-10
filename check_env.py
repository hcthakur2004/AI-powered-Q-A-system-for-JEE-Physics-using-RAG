from dotenv import load_dotenv
import os

load_dotenv()

print("=" * 60)
print("Environment Variables Check")
print("=" * 60)

groq_key = os.getenv('GROQ_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')

print(f"GROQ_API_KEY: {'✅ SET (' + groq_key[:20] + '...)' if groq_key else '❌ NOT SET'}")
print(f"GEMINI_API_KEY: {'✅ SET (' + gemini_key[:20] + '...)' if gemini_key else '❌ NOT SET'}")
print("=" * 60)

if groq_key:
    print("✅ Groq will be used (PRIMARY)")
elif gemini_key:
    print("⚠️ Only Gemini available (may have quota issues)")
else:
    print("❌ No API keys found!")

print("\nYour .env file should look like this:")
print("GROQ_API_KEY=gsk_your_actual_key_here")
print("GEMINI_API_KEY=your_gemini_key_here")
