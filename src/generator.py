import google.generativeai as genai
import os
import re
import time
from langsmith import traceable

class ContentGenerator:
    def __init__(self):
        # Gemini Setup
        self.api_keys = [
            os.getenv("GOOGLE_API_KEY"),
            os.getenv("GOOGLE_API_KEY_2"),
            os.getenv("GOOGLE_API_KEY_3")
        ]
        self.api_keys = [k for k in self.api_keys if k]
        
        self.gemini_models = [
            'gemini-2.5-flash-lite', 
            'gemini-flash-lite-latest'
        ]
        
        self.current_key_idx = 0
        self.provider = 'gemini' # 'gemini' or 'groq'
        
        # Groq Setup
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_keys and not self.groq_api_key:
             print("[Generator Warning] No API keys found for Gemini or Groq.")

    def _configure_gemini_current(self):
        """Configures Gemini with the current active key."""
        if self.current_key_idx < len(self.api_keys):
            try:
                genai.configure(api_key=self.api_keys[self.current_key_idx])
            except Exception as e:
                print(f"Error configuring Key #{self.current_key_idx+1}: {e}")

    def generate_email(self, company_profile, lead_data):
        """
        Generates email content, maintaining state of which key/provider is active.
        """
        lead_name = lead_data.get('Name') or lead_data.get('First Name') or 'there'
        lead_company = lead_data.get('Company') or lead_data.get('Company Name') or 'your company'
        key_stats = "25% conversion increase, 30% lower CAC, 3x ROI"
        
        prompt = f"""
        You are Salman, Marketing Lead at D360 Solutions.
        Write a personalized outreach email body to {lead_name} at {lead_company}.
        
        Context:
        - Their Challenge: "{lead_data.get('Biggest challenge?', 'growth')}"
        - Our Solution Proof: {key_stats}
        - Company Profile: "{company_profile[:2000]}"  # Truncate to avoid huge context if needed

        
        Framework (Hormozi x SMYKM):
        1. **The Hook (Show Me You Know Me)**: Start by acknowledging their specific challenge in the context of their industry. Prove you understand their pain. INFERS the industry from context. If unknown, use "your sector". NEVER use brackets like [Industry] or placeholders.
        2. **The Offer (Hormozi Style)**: State the transformation clearly. "We help companies like yours [Achieve X] using [Mechanism]." Stick to the 'Grand Slam Offer' concept (High Value, Low Effort for them).
        3. **The Proof**: Cite our stats ({key_stats}) as hard evidence of the result.
        4. **The Ask (Low Friction)**: "Would you be opposed to a 10-minute strategy walk-through? No pressure, just value."
        
        Tone: Confident, Direct, High-Value.
        Formatting: Use **Bold** for key stats and the hook's pain point. Use bullet points if listing multiple items. Keep paragraphs short (2-3 lines max) for readability.
        Length: 5-7 sentences. Ensure it feels substantial but punchy.
        
        Output Format:
        Return ONLY the email body. Do not include a greeting (Hi Name), the subject line, or sign-off.
        """
        
        sign_off = "\n\nBest regards,\nSalman\nMarketing Lead\nD360 Solutions"

        while True:
            # --- GEMINI PATH ---
            if self.provider == 'gemini':
                if self.current_key_idx >= len(self.api_keys):
                    # All Gemini keys exhausted -> Switch to Groq
                    print("All Gemini keys exhausted. Switching to Groq...", flush=True)
                    self.provider = 'groq'
                    continue
                
                # Configure current key
                self._configure_gemini_current()
                
                # Try models on this current key
                for model_name in self.gemini_models:
                    try:
                        @traceable(run_type="llm", name="generate_email_gemini")
                        def call_gemini(m_name, p_text):
                            model = genai.GenerativeModel(m_name)
                            return model.generate_content(p_text)

                        response = call_gemini(model_name, prompt)
                        text = response.text.strip()
                        return self._process_text(text, lead_name, lead_company, lead_data, sign_off)
                    
                    except Exception as e:
                        err_str = str(e)
                        if "429" in err_str or "quota" in err_str.lower() or "403" in err_str or "leaked" in err_str.lower() or "expired" in err_str.lower():
                            print(f"Quota/Error on {model_name} (Gemini Key #{self.current_key_idx+1}). Switching Key...", flush=True)
                            self.current_key_idx += 1 # Move to next key PERMANENTLY
                            break # Break model loop to reload with new key (next iteration of while True)
                        elif "not found" in err_str.lower():
                             continue # Try next model
                        else:
                             # Unknown error, maybe skip model or switch key? 
                             # Let's switch key to be safe
                             print(f"Error on {model_name} (Key #{self.current_key_idx+1}): {err_str}")
                             self.current_key_idx += 1
                             break
            
            # --- GROQ PATH ---
            elif self.provider == 'groq':
                if not self.groq_api_key:
                    print("Groq API Key not found. Sleeping...", flush=True)
                    self._sleep_and_reset()
                    continue

                try:
                    from groq import Groq
                    client = Groq(api_key=self.groq_api_key)
                    
                    @traceable(run_type="llm", name="generate_email_groq")
                    def call_groq(p_text):
                        return client.chat.completions.create(
                            messages=[{"role": "user", "content": p_text}],
                            model="llama-3.3-70b-versatile",
                        )
                    
                    completion = call_groq(prompt)
                    text = completion.choices[0].message.content.strip()
                    return self._process_text(text, lead_name, lead_company, lead_data, sign_off)
                
                except Exception as e:
                    print(f"[Groq Error] {e}. Groq failed/exhausted.", flush=True)
                    self._sleep_and_reset()
                    # After sleep, we resume at top of loop. 
                    
    def _sleep_and_reset(self):
        print("All providers exhausted. Waiting 12 hours before retry...", flush=True)
        time.sleep(43200)
        print("Resuming retries. Resetting keys...", flush=True)
        self.current_key_idx = 0
        self.provider = 'gemini'

    def _process_text(self, text, lead_name, lead_company, lead_data, sign_off):
        # 1. Remove Subject
        if "Subject:" in text:
            text = text.split("Subject:", 1)[-1].strip()
            if "\n" in text: 
                parts = text.split("\n", 1)
                if len(parts) > 1: text = parts[1].strip()
        
        # 2. Remove Greeting
        greeting_patterns = [f"Hi {lead_name}", f"Dear {lead_name}", f"Hello {lead_name}", "Hi there", "Hello there"]
        lower_text = text.lower()
        for gp in greeting_patterns:
            if lower_text.startswith(gp.lower()):
                if "\n" in text:
                    text = text.split("\n", 1)[1].strip()
                else:
                    text = text[len(gp):].strip().strip(",").strip()
                break
        
        # 3. Check for brackets
        if re.search(r"\[.*?\]", text):
             raise ValueError(f"Content contains brackets: {re.search(r'\[.*?\]', text).group(0)}")
        
        # 4. Error check
        if not text or "Error" in text[:20] or "429" in text[:20]:
             raise ValueError(f"Content looks like error: {text[:50]}")
        
        # Manual formatting
        raw_val = lead_data.get('Biggest challenge?')
        if not raw_val or str(raw_val).lower() == 'nan':
            challenge_raw = 'Growth'
        else:
            challenge_raw = str(raw_val)
        
        challenge_clean = challenge_raw.replace('"', '').replace("'", "").strip()[:30]
        if len(challenge_raw) > 30: challenge_clean += "..."
        subject = f"Subject: Solving {challenge_clean} for {lead_company}"
        
        return f"{subject}\n\nHi {lead_name.split()[0]},\n\n{text}{sign_off}"
