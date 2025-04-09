import streamlit as st
import random
import string
import re
import pyperclip

# Glassmorphism styling 
st.markdown("""
    <style>
    html, body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2, #6fa3ef);
        color: #ffffff;
        padding: 0;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
    }

    .glass-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        width: 90%;
        max-width: 500px;
        margin-bottom: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #000;
    }

    .title {
        font-size: 42px;
        text-align: center;
        font-weight: 700;
        color: #fff;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        color: #fff;
        margin-bottom: 30px;
        font-size: 18px;
    }

    .score-box {
        font-size: 20px;
        text-align: center;
        padding: 12px;
        border-radius: 12px;
        margin-top: 20px;
        font-weight: bold;
        width: 100%;
        transition: background-color 0.3s;
    }

    .strong { background-color: #27ae60; color: white; }
    .moderate { background-color: #f39c12; color: white; }
    .weak { background-color: #c0392b; color: white; }

    .checklist {
        font-size: 17px;
        line-height: 2;
        padding-left: 15px;
        color: #fff;
    }

    .note-box {
        background: rgba(255,255,255,0.08);
        padding: 15px;
        border-left: 5px solid #f39c12;
        border-radius: 12px;
        margin-top: 25px;
    }

    .st-emotion-cache-1wrcr25{
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2, #6fa3ef);       
        }
    .button {
        background-color: #6c5ce7;
        color: white;
        padding: 10px 20px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .button:hover {
        background-color: #4834d4;
    }

    .footer {
        text-align: center;
        color: #fff;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and input
st.markdown('<div class="title">🔒 Password Strength Meter</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze your password or generate a strong one instantly</div>', unsafe_allow_html=True)

# Password generator
def generate_strong_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

if "password" not in st.session_state:
    st.session_state.password = ""

st.markdown('<div class="glass-box">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])

with col2:
    if st.button("💡 Suggest Strong Password", key="generate", use_container_width=True):
        st.session_state.password = generate_strong_password()

with col3:
    if st.button("📋 Copy Password", key="copy", use_container_width=True):
        pyperclip.copy(st.session_state.password)
        st.success("Password copied to clipboard!")

with col1:
    st.session_state.password = st.text_input(
        "🔑 Enter your password:",
        value=st.session_state.password,
        type="password",
        help="Enter a password to analyze its strength"
    )

password = st.session_state.password
st.markdown('</div>', unsafe_allow_html=True)

# Common password blacklist
blacklist = {
    "123456", "password", "12345678", "qwerty",
    "abc123", "password123", "111111", "123123", "letmein"
}

# Password strength logic
def check_password_strength(password):
    score = 0
    feedback = []

    if password.lower() in blacklist:
        feedback.append("❌ This password is too common. Try something more unique.")
        return 0, feedback

    weights = {
        "length": 2,
        "upper_lower": 1,
        "digits": 1,
        "special": 2
    }

    if len(password) >= 8:
        score += weights["length"]
        feedback.append("✅ Length: 8 or more characters")
    else:
        feedback.append("❌ Length: Less than 8 characters")

    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += weights["upper_lower"]
        feedback.append("✅ Upper & lowercase letters included")
    else:
        feedback.append("❌ Missing mix of upper/lowercase")

    if re.search(r'\d', password):
        score += weights["digits"]
        feedback.append("✅ Contains a number (0-9)")
    else:
        feedback.append("❌ Add at least one number")

    if re.search(r'[!@#$%^&*()]', password):
        score += weights["special"]
        feedback.append("✅ Special character included (!@#$%^&*())")
    else:
        feedback.append("❌ Add a special character (!@#$%^&*())")

    return score, feedback

# Show results
if password:
    score, feedback = check_password_strength(password)
    max_score = 6

    if score >= 5:
        strength = "Strong"
        strength_class = "strong"
    elif score >= 3:
        strength = "Moderate"
        strength_class = "moderate"
    else:
        strength = "Weak"
        strength_class = "weak"

    st.markdown(
        f'<div class="score-box {strength_class}"><i class="fa-solid fa-shield-halved"></i> '
        f'Password Strength: <strong>{strength}</strong> (Score: {score}/{max_score})</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("### 💡 Password Tips", unsafe_allow_html=True)
    st.markdown('<div class="checklist">', unsafe_allow_html=True)

    for tip in feedback:
        st.write(tip)

    st.markdown('</div>', unsafe_allow_html=True)

    if score >= 5:
        st.success("🎉 Excellent! Your password is strong and secure.")
        st.balloons()
    elif score <= 2:
        st.warning("⚠️ Consider strengthening your password with more characters, digits, and symbols.")
else:
    st.info("Start by typing your password above to analyze it.")

st.markdown('<div class="note-box"><i class="fa-solid fa-circle-info"></i> <strong>Tip:</strong> Use passphrases made of multiple unrelated words and include symbols to improve memorability and security.</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="footer">💻 Crafted with love by Awais Khan using Streamlit</div>', unsafe_allow_html=True)