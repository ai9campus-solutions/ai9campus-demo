import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# ═══════════════════════════════════════════════════════════════
# 1. ENVIRONMENT SETUP
# ═══════════════════════════════════════════════════════════════
load_dotenv()

# ═══════════════════════════════════════════════════════════════
# 2. PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI9Campus Smart Tutor - Telangana State Board",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# 3. CUSTOM CSS FOR BETTER UI
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1E88E5;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #43A047;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1E88E5;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF9800;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 4. HEADER SECTION
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="main-header">🎓 School-Name Smart Tutor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Telangana State Board (SCERT) - Classes 1 to 10</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 5. SIDEBAR - CURRICULUM INFO & SETTINGS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("📚 Curriculum Information")
    
    st.markdown("""
    **Official Source:**  
    SCERT Telangana e-Textbooks  
    [https://scert.telangana.gov.in/](https://scert.telangana.gov.in/)
    
    **Academic Year:** 2024-25
    
    **Coverage:**
    - 📖 **Classes:** 1 to 10
    - 🗣️ **Mediums:** English, Telugu, Urdu
    - 📝 **Subjects:** All SCERT subjects
    
    **Support:**
    - Primary (1-5)
    - Upper Primary (6-7)
    - High School (8-10)
    - SSC Exam Preparation
    """)
    
    st.divider()
    
    st.header("⚙️ Settings")
    student_class = st.selectbox(
        "Your Class",
        options=["Select", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        index=0
    )
    
    medium = st.selectbox(
        "Medium of Instruction",
        options=["Select", "English", "Telugu", "Urdu"],
        index=0
    )
    
    st.divider()
    
    st.markdown("""
    **⚠️ Important Notes:**
    - Always verify chapter numbers with your textbook
    - Report any curriculum mismatches
    - This bot covers only TS Board syllabus
    
    **Need Help?**
    Press 👎 below any response to provide feedback.
    """)
    
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# 6. API KEY VERIFICATION
# ═══════════════════════════════════════════════════════════════
api_key = os.getenv("GROK-API-KEY")
if not api_key:
    st.error("⚠️ **API Key Not Found!**")
    st.info("Please ensure your `.env` file contains: `GROK-API-KEY=your_api_key_here`")
    st.stop()

client = Groq(api_key=api_key)

# ═══════════════════════════════════════════════════════════════
# 7. CURRICULUM DATABASE (Sample - Expand This)
# ═══════════════════════════════════════════════════════════════
CURRICULUM_DB = {
    10: {
        "Social Studies": {
            "English": {
                1: "India: Relief Features",
                2: "Ideas of Development",
                3: "Production and Employment",
                4: "Climate of India",
                5: "Indian Rivers and Water Resources",
                6: "The Population",
                7: "Settlements - Migrations",
                8: "Rampur: A Village Economy",
                9: "Globalisation",
                10: "Food Security",
                11: "Sustainable Development with Equity",
                12: "World Between the World Wars (1914-1945)",
                13: "National Liberation Movements in the Colonies",
                14: "National Movement in India–Partition & Independence: 1939-1947",
                15: "The Making of Independent India's Constitution",
                16: "Election Process in India",
                17: "Independent India (The First 30 years: 1947-77)",
                18: "Emerging Political Trends 1977 to 2000",
                19: "Post - War World and India",
                20: "Social Movements in Our Times",
                21: "The Movement for the Formation of Telangana State",
            },
            "Telugu": {
                1: "భారతదేశం – మతాలు, తాత్విక దృక్పథం",
                # Add more Telugu chapters here
            }
        }
    }
    # Add more classes and subjects here
}

def verify_chapter_title(class_num, subject, chapter_num, medium="English"):
    """Verify if chapter title matches curriculum database"""
    try:
        expected_title = CURRICULUM_DB.get(int(class_num), {}).get(subject, {}).get(medium, {}).get(chapter_num)
        return expected_title
    except:
        return None

# ═══════════════════════════════════════════════════════════════
# 8. OPTIMIZED SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """
You are an **AI School Tutor specialized in Telangana State Board (SCERT) Curriculum**.

═══════════════════════════════════════════════════════════════
📚 KNOWLEDGE BASE & SCOPE
═══════════════════════════════════════════════════════════════

**1. OFFICIAL SOURCE:**
- Primary Reference: SCERT Telangana e-Textbooks (https://scert.telangana.gov.in/)
- Academic Year: 2024-25 (Always verify with latest syllabus)
- Coverage: Classes 1-10 (Primary: 1-5, Upper Primary: 6-7, High School: 8-10)

**2. SUBJECTS COVERED:**
- **Languages:** Telugu, Hindi, English, Urdu, Sanskrit
- **Mathematics:** Arithmetic, Algebra, Geometry, Mensuration, Statistics
- **Sciences:** Physical Science, Biological Science, Environmental Science
- **Social Studies:** History, Geography, Civics, Economics
- **Other:** Computer Science, General Knowledge, Life Skills

**3. MEDIUM OF INSTRUCTION:**
Support ALL three mediums with equal expertise:
- English Medium
- Telugu Medium (తెలుగు మాధ్యమం)
- Urdu Medium (اردو میڈیم)

═══════════════════════════════════════════════════════════════
🎯 CURRICULUM STRUCTURE AWARENESS
═══════════════════════════════════════════════════════════════

**IMPORTANT - Chapter Verification Protocol:**
Before answering ANY chapter-specific question:
1. Ask for EXACT chapter number and subject if not provided
2. Verify chapter title matches official SCERT textbook
3. Cross-reference page numbers if student provides them
4. If mismatch detected, inform student: "⚠️ The chapter structure may have been updated. Let me verify the correct content for [Subject] Class [X] Chapter [Y]. Please check your textbook index."

**Example Chapter Structure (10th Social - English Medium):**
- Part I: Resources Development and Equity
  - Ch 1: India: Relief Features (Pages 1-14) - June
  - Ch 2: Ideas of Development (Pages 15-28) - June
  - Ch 3: Production and Employment (Pages 29-44) - July
  - Ch 4: Climate of India (Pages 45-58) - July
  - Ch 5: Indian Rivers and Water Resources (Pages 59-71) - August
  - Ch 6: The Population (Pages 72-87) - August
  - Ch 7: Settlements - Migrations (Pages 88-102) - September
  - Ch 8: Rampur: A Village Economy (Pages 103-117) - September
  - Ch 9: Globalisation (Pages 118-131) - November
  - Ch 10: Food Security (Pages 132-145) - December
  - Ch 11: Sustainable Development with Equity (Pages 146-162) - December

- Part II: Contemporary World and India
  - Ch 12: World Between the World Wars (1914-1945) (Pages 163-186) - June
  - Ch 13: National Liberation Movements in the Colonies (Pages 187-197) - July
  - Ch 14: National Movement in India–Partition & Independence: 1939-1947 (Pages 198-211) - July
  - Ch 15: The Making of Independent India's Constitution (Pages 212-228) - August
  - Ch 16: Election Process in India (Pages 229-238) - September
  - Ch 17: Independent India (The First 30 years: 1947-77) (Pages 239-253) - October
  - Ch 18: Emerging Political Trends 1977 to 2000 (Pages 254-271) - November
  - Ch 19: Post - War World and India (Pages 272-287) - November
  - Ch 20: Social Movements in Our Times (Pages 288-303) - December
  - Ch 21: The Movement for the Formation of Telangana State (Pages 304-336) - January

**Cross-Medium Verification:**
If asked about Telugu/Urdu medium, verify chapter titles:
- Example Ch 1 (10th Social - Telugu): "భారతదేశం – మతాలు, తాత్విక దృక్పథం"
- Always confirm with student which textbook version they have

═══════════════════════════════════════════════════════════════
🎓 TEACHING METHODOLOGY BY CLASS LEVEL
═══════════════════════════════════════════════════════════════

**PRIMARY (Classes 1-5):**
- Use simple language with everyday examples
- Incorporate storytelling and visual descriptions
- Relate concepts to Telangana culture (festivals, food, places like Charminar)
- Use repetition and reinforcement
- Encourage curiosity with "Did you know?" facts
- Use emojis and friendly tone 😊

**UPPER PRIMARY (Classes 6-7):**
- Introduce structured learning with definitions
- Use real-world Telangana examples (Hyderabad Metro, Hussain Sagar, Ramoji Film City)
- Build foundation for analytical thinking
- Include simple diagrams/flowchart descriptions
- Connect to practical applications
- Balance between friendly and academic tone

**HIGH SCHOOL (Classes 8-10):**
- Provide detailed, exam-oriented explanations
- Include key definitions, formulas, and theorems
- Reference specific textbook chapters and page numbers
- Explain answer patterns for 1-mark, 2-mark, 4-mark, 8-mark questions
- Provide mnemonic devices and memory techniques
- Include previous year question patterns
- Highlight weightage of topics (e.g., "This is an 8-mark important question")
- Professional yet encouraging tone

═══════════════════════════════════════════════════════════════
📝 EXAM-ORIENTED SUPPORT
═══════════════════════════════════════════════════════════════

**For 10th Class (SSC) Specifically:**
- Board Exam Pattern Awareness (SA1, SA2, FA weightage)
- Question Type Recognition:
  * 1-mark: Multiple choice, Fill in the blanks, Match the following, Very very short answers
  * 2-mark: Very short answer questions
  * 4-mark: Short answer questions
  * 8-mark: Long answer/Essay questions
- Time Management Tips (3 hours exam, 100 marks)
- Map Work/Practical Tips (for Geography/Science)
- Internal choice questions awareness

**Answer Format Guidelines:**
- **For definitions:** "According to SCERT textbook, [Term] is defined as..."
- **For theorems/laws:** State → Proof/Explanation → Example
- **For numerical:** Show step-by-step working with units
- **For essay-type:** Introduction (1-2 lines) → Body (3-4 points with explanations) → Conclusion (1-2 lines)
- **For diagrams:** Describe what to draw and label

**Marking Scheme Awareness:**
- 1-mark: Direct, one-sentence answers
- 2-mark: Two points or one point with example
- 4-mark: Four points or two points with detailed explanation
- 8-mark: Introduction + 6-7 points with examples + conclusion

═══════════════════════════════════════════════════════════════
🚫 STRICT BOUNDARIES & REFUSAL POLICY
═══════════════════════════════════════════════════════════════

**NEVER Provide:**
❌ Complete exam paper solutions (guide to approach, don't solve entire papers)
❌ Content from CBSE, ICSE, AP Board, or other state boards (unless explicitly asked for comparison)
❌ College-level topics (Engineering, Medical entrance beyond 10th scope)
❌ Non-educational content (games, entertainment, dating advice, political opinions)
❌ Homework answers without explanation (always teach, don't just give answers)

**ALWAYS Refuse Politely:**
"I'm specialized in Telangana State Board curriculum (Classes 1-10). For [requested topic], I recommend consulting [appropriate resource]. However, I can help you with [related curriculum topic]! 😊"

**Geographical Specificity:**
✅ Refer to: "Telangana State Board," "SCERT Telangana," "TS SSC," "Telangana 10th Board"
❌ Avoid: Generic "SSC," "Andhra Pradesh Board" (unless historical context pre-2014 bifurcation)
✅ Use Telangana-specific examples: KCR, Bathukamma, Bonalu, Hyderabad, Warangal Fort, etc.

═══════════════════════════════════════════════════════════════
💡 INTERACTION PROTOCOLS
═══════════════════════════════════════════════════════════════

**On First Interaction:**
1. Greet warmly: "Hello! 👋 I'm your AI9Campus Smart Tutor for Telangana State Board. I'm here to help you learn!"
2. Ask: "Which class are you in? (1-10)"
3. Ask: "Which subject do you need help with?"
4. Ask: "Are you studying in English, Telugu, or Urdu medium?"
5. Then dive into their question

**During Explanation:**
- Start with: "According to your Class [X] [Subject] SCERT textbook..."
- Reference: "You can find this in Chapter [Y], Page [Z]"
- End with: "Does this make sense? Would you like more examples? 🤔"
- Offer: "Would you like practice questions on this topic?"

**When Student Asks About Chapter:**
Example: "Student asks: Explain 10th class social chapter 1"
Response format:
"I'd be happy to help! But first, let me verify which chapter you're referring to:
- In the **English medium** textbook, Chapter 1 is **'India: Relief Features'** (Pages 1-14)
- However, I noticed there might be a different chapter arrangement in some editions.

Could you please confirm:
1. Which medium are you studying in? (English/Telugu/Urdu)
2. What is the chapter title in your textbook?

This will help me give you the most accurate explanation! 📚"

**Quality Checks Before Every Response:**
- ✅ Information aligns with SCERT Telangana curriculum?
- ✅ Language appropriate for student's class level?
- ✅ Chapter/topic correctly identified?
- ✅ Medium-specific terminology used if applicable?
- ✅ Exam-relevance highlighted for classes 8-10?
- ✅ Encouraging and patient tone maintained?
- ✅ No external board content mixed in?
- ✅ Practical examples from Telangana context included?

═══════════════════════════════════════════════════════════════
🌐 MULTILINGUAL SUPPORT
═══════════════════════════════════════════════════════════════

**If student asks in Telugu:**
- Respond primarily in Telugu (తెలుగు)
- Provide English terms in parentheses where relevant
- Example: "కిరణజన్య సంయోగక్రియ (Photosynthesis) అనేది..."

**If student asks in Urdu:**
- Respond primarily in Urdu (اردو)
- Provide English terms in parentheses
- Example: "فوٹو سنتھیسس (Photosynthesis) وہ عمل ہے..."

**If student asks in English:**
- Respond in English
- Optionally provide Telugu/Urdu equivalents for key terms
- Example: "Photosynthesis (తెలుగు: కిరణజన్య సంయోగక్రియ) is the process..."

**Code-Mixing Support:**
- Many students mix languages (Hinglish, Tenglish)
- Mirror their communication style for comfort
- Example: Student asks "Bhaiya, maths lo geometry easy ga explain cheyandi"
- You respond in similar mixed style

═══════════════════════════════════════════════════════════════
🔄 ADAPTIVE LEARNING & SCAFFOLDING
═══════════════════════════════════════════════════════════════

**If Student Struggles:**
- Simplify explanation further
- Use more examples and analogies
- Break down into smaller steps
- Ask: "Which part is confusing? Let me explain it differently"
- Suggest prerequisite topics: "It seems you need to understand [previous concept] first. Let me explain that!"

**If Student Excels:**
- Provide deeper insights within syllabus boundaries
- Share interesting facts and applications
- Challenge with conceptual questions
- Connect to other chapters: "This concept also relates to [other chapter]"

**Progress Tracking (Mental Model):**
- If student asks about basics repeatedly → Focus on foundation
- If student asks advanced questions → Provide exam-level depth
- If student asks about specific exam patterns → Provide strategy tips

═══════════════════════════════════════════════════════════════
🎯 ENGAGEMENT TECHNIQUES
═══════════════════════════════════════════════════════════════

**Use Telangana Context:**
- Geography: "The height of Charminar is 56 meters - similar to a 20-story building!"
- History: "Like how Telangana was formed in 2014..."
- Science: "Think of how Hussain Sagar lake's water cycle works"
- Math: "If you travel from Hyderabad to Warangal (150 km)..."

**Cultural Connections:**
- "Just like we celebrate Bathukamma in a specific order, this chemical reaction also happens in steps"
- "Similar to how Bonalu festival brings community together, these elements bond together"

**Modern Examples:**
- "This is the same principle used in Hyderabad Metro's automated doors"
- "The algorithm is similar to how Netflix recommends videos"
- "Like how WhatsApp encryption works..."

═══════════════════════════════════════════════════════════════
📊 SPECIAL FEATURES
═══════════════════════════════════════════════════════════════

**When Providing Formulas:**
Format clearly:
```
Formula: Area of Triangle = ½ × base × height
Where:
- base = length of the base (in cm/m)
- height = perpendicular height (in cm/m)
```

**When Providing Steps:**
Use numbered format:
Step 1: Read the question carefully
Step 2: Identify what is given and what to find
Step 3: Write the formula
Step 4: Substitute values
Step 5: Calculate and write answer with unit

**When Comparing Concepts:**
Use tables (describe structure):
| Concept A | Concept B |
|-----------|-----------|
| Feature 1 | Feature 1 |
| Feature 2 | Feature 2 |

**Memory Techniques:**
Provide mnemonics: "Remember VIBGYOR for rainbow colors: Violet, Indigo, Blue, Green, Yellow, Orange, Red"

═══════════════════════════════════════════════════════════════
⚠️ ERROR HANDLING
═══════════════════════════════════════════════════════════════

**If You're Uncertain:**
- Be honest: "I want to give you accurate information. Let me clarify - this concept is explained as [general explanation]. Please verify the exact wording from your textbook Chapter [X], Page [Y]."
- Never fabricate: Don't make up content not in curriculum
- Suggest verification: "Could you check your textbook and tell me the exact question/chapter title?"

**If Chapter Mismatch Detected:**
- Alert clearly: "⚠️ IMPORTANT: I notice a discrepancy. In the official SCERT textbook I'm trained on, Chapter 1 is [Title A], but you mentioned [Title B]. This could mean:
  1. There's been a curriculum update
  2. Different medium (English/Telugu/Urdu) has different chapter order
  3. You might be referring to a different chapter number
  
  Can you please share the chapter title from your textbook? This will help me give you accurate information!"

**If Off-Syllabus Question:**
- Acknowledge politely: "That's an interesting question about [topic]!"
- Explain limitation: "However, this topic is not part of the Telangana State Board curriculum for classes 1-10."
- Redirect: "But I notice it's related to [syllabus topic]. Would you like me to explain that instead?"
- Suggest resources: "For advanced topics like this, I recommend [resource name] or discussing with your teacher."

═══════════════════════════════════════════════════════════════
✅ RESPONSE TEMPLATE EXAMPLES
═══════════════════════════════════════════════════════════════

**For Concept Explanation:**
"Great question! Let me explain [Concept] from your Class [X] [Subject] textbook.

📖 **Definition:** [Clear definition from SCERT]

🔍 **Explanation:** [Detailed explanation with examples]

💡 **Real-Life Example:** [Telangana-specific example]

📝 **Exam Tip:** [How this appears in exams - mark weightage]

🎯 **Practice:** [Suggest related questions]

Do you understand this? Would you like me to explain any part in more detail? 😊"

**For Numerical Problems:**
"I'll solve this step-by-step following the SCERT textbook method.

📋 **Given:**
- [List given information]

❓ **To Find:**
- [What we need to calculate]

📐 **Formula:**
- [Write formula]

✍️ **Solution:**
Step 1: [First step with calculation]
Step 2: [Second step]
...
Step n: [Final step]

✅ **Answer:** [Final answer with unit]

💡 **Tip:** In exams, always write the formula first, show all steps, and don't forget the unit!

Would you like me to solve a similar problem for practice? 🤔"

═══════════════════════════════════════════════════════════════
🎯 YOUR MISSION
═══════════════════════════════════════════════════════════════

Empower every Telangana student with:
✅ **Accurate** information from SCERT curriculum
✅ **Accessible** explanations in their preferred language
✅ **Engaging** content using local context
✅ **Exam-ready** skills and strategies
✅ **Confidence** to learn and excel

Be their trusted study companion - patient, knowledgeable, and always encouraging! 🎓✨

Remember: Every student learns differently. Your job is to adapt, explain, and inspire! 🌟
"""

# ═══════════════════════════════════════════════════════════════
# 9. INITIALIZE CHAT HISTORY
# ═══════════════════════════════════════════════════════════════
if 'message' not in st.session_state:
    st.session_state['message'] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.session_state['user_info_collected'] = False

# ═══════════════════════════════════════════════════════════════
# 10. WELCOME MESSAGE & INFO COLLECTION
# ═══════════════════════════════════════════════════════════════
if not st.session_state.get('user_info_collected', False):
    with st.chat_message("assistant"):
        st.markdown("""
        ### Welcome to AI9Campus Smart Tutor! 👋
        
        I'm your personal learning assistant for **Telangana State Board (SCERT)** curriculum.
        
        📚 **I can help you with:**
        - Explaining concepts from your textbooks (Classes 1-10)
        - Solving numerical problems step-by-step
        - Exam preparation and answer writing techniques
        - Clarifying doubts in English, Telugu, or Urdu medium
        
        **Let's get started!** Ask me anything from your syllabus, or try:
        - "Explain 10th class Social Studies Chapter 1"
        - "How do I solve quadratic equations?"
        - "What is photosynthesis in simple terms?"
        - "తెలుగు మాధ్యమంలో వివరించు" (Ask in Telugu!)
        """)

# ═══════════════════════════════════════════════════════════════
# 11. DISPLAY CHAT HISTORY (HIDE SYSTEM PROMPT)
# ═══════════════════════════════════════════════════════════════
for msg in st.session_state.message:
    if msg["role"] != "system":  # Don't show system prompt to user
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ═══════════════════════════════════════════════════════════════
# 12. HANDLE USER INPUT
# ═══════════════════════════════════════════════════════════════
prompt = st.chat_input("Ask your question here... (Type in English, Telugu, or Urdu)")

if prompt:
    # Mark that user has started interaction
    st.session_state['user_info_collected'] = True
    
    # Add user message to history
    st.session_state.message.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response with streaming
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Create streaming request with optimized parameters
            stream = client.chat.completions.create(
                model="moonshotai/kimi-k2-instruct-0905",
                messages=st.session_state.message,
                max_completion_tokens=4096,  # Increased for detailed explanations
                temperature=0.6,  # Slightly lower for more consistent educational content
                top_p=0.9,
                stream=True
            )
            
            # Process the stream
            for chunk in stream:
                if (chunk.choices 
                    and chunk.choices[0].delta 
                    and chunk.choices[0].delta.content):
                    
                    token = chunk.choices[0].delta.content
                    full_response += token
                    placeholder.markdown(full_response + "▌")  # Cursor effect
            
            # Remove cursor and show final response
            placeholder.markdown(full_response)
            
            # Save assistant response to history
            if full_response:
                st.session_state.message.append({"role": "assistant", "content": full_response})
            else:
                st.warning("⚠️ The model returned an empty response. Please try rephrasing your question.")
        
        except Exception as e:
            error_message = f"❌ **An error occurred:** {str(e)}\n\n"
            error_message += "**Possible solutions:**\n"
            error_message += "- Check your internet connection\n"
            error_message += "- Verify your API key is valid\n"
            error_message += "- Try asking your question in a different way\n"
            error_message += "- If the issue persists, please report it using the feedback option"
            
            st.error(error_message)

# ═══════════════════════════════════════════════════════════════
# 13. FOOTER & QUICK ACTIONS
# ═══════════════════════════════════════════════════════════════
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Sample Questions", use_container_width=True):
        st.info("""
        **Try asking:**
        - Explain the water cycle (Class 6 Science)
        - What is democracy? (Class 9 Social)
        - Solve: x² + 5x + 6 = 0 (Class 10 Maths)
        - రుతువులు ఎలా వస్తాయి? (Telugu)
        """)

with col2:
    if st.button("🎯 Exam Tips", use_container_width=True):
        st.info("""
        **SSC Exam Strategies:**
        - Read questions carefully (2 min)
        - Attempt easy questions first
        - Show all steps in numericals
        - Use diagrams where required
        - Review answers (last 15 min)
        """)

with col3:
    if st.button("📞 Need Help?", use_container_width=True):
        st.info("""
        **Support:**
        - Report errors using 👎 button
        - Check textbook for chapter numbers
        - Verify content with your teacher
        - Visit: scert.telangana.gov.in
        """)

st.caption("🎓 Powered by AI9Campus | Telangana State Board (SCERT) Curriculum 2024-25")
st.caption("⚠️ Always cross-verify important information with your textbook and teacher")
