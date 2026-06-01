# ==========================================================
# AI VIDEO PROMPT GENERATOR PRO
#
# Features:
# - Gemini Prompt Generation
# - Multiple Video Styles
# - Prompt Review
# - Prompt History
# - Download Prompt
# - Statistics Dashboard
# - Professional UI
# ==========================================================

import streamlit as st
import google.generativeai as genai

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Video Prompt Generator Pro",
    page_icon="🎬",
    layout="wide"
)

# ==========================================================
# GEMINI CONFIGURATION
# ==========================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "video_prompt" not in st.session_state:
    st.session_state.video_prompt = ""

if "prompt_review" not in st.session_state:
    st.session_state.prompt_review = ""

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🎬 Video Prompt Pro")

    st.markdown("---")

    st.subheader("⚙ Generation Settings")

    duration = st.selectbox(
        "Video Duration",
        [
            "5 Seconds",
            "10 Seconds",
            "15 Seconds",
            "30 Seconds"
        ]
    )

    quality = st.selectbox(
        "Video Quality",
        [
            "Standard",
            "HD",
            "Ultra HD",
            "4K"
        ]
    )

    video_style = st.selectbox(
        "Video Style",
        [
            "Cinematic",
            "Realistic",
            "Anime",
            "Cyberpunk",
            "Documentary",
            "Advertisement"
        ]
    )

    st.markdown("---")

    st.subheader("📊 Statistics")

    st.metric(
        "Prompts Generated",
        len(st.session_state.prompt_history)
    )

    if st.button(
        "🗑 Clear History",
        use_container_width=True
    ):

        st.session_state.prompt_history = []

        st.success(
            "History Cleared"
        )

# ==========================================================
# MAIN TITLE
# ==========================================================

st.title("🎬 AI Video Prompt Generator Pro")

st.caption(
    "Generate Professional AI Video Prompts Using Gemini"
)

st.markdown("---")

# ==========================================================
# USER INPUT
# ==========================================================

st.header("📝 Video Idea")

prompt = st.text_area(
    "Describe your video idea",
    height=150,
    placeholder="""
Example:

A futuristic AI classroom where students learn
using holographic displays and intelligent
virtual assistants.
"""
)

# ==========================================================
# BUTTONS
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    generate_button = st.button(
        "🎥 Generate Prompt",
        use_container_width=True
    )

with col2:

    review_button = st.button(
        "⭐ Review Prompt",
        use_container_width=True
    )

# ==========================================================
# GENERATE PROMPT
# ==========================================================

if generate_button:

    if not prompt.strip():

        st.warning(
            "Please enter a video idea."
        )

    else:

        # ==================================================
        # STYLE INSTRUCTIONS
        # ==================================================

        if video_style == "Cinematic":

            style_instruction = """
Use:
- cinematic lighting
- dramatic atmosphere
- Hollywood visuals
- dynamic camera movement
- movie quality
"""

        elif video_style == "Realistic":

            style_instruction = """
Use:
- photorealistic visuals
- realistic motion
- natural lighting
- real-world detail
"""

        elif video_style == "Anime":

            style_instruction = """
Use:
- anime style visuals
- vibrant colors
- smooth animation
- expressive characters
"""

        elif video_style == "Cyberpunk":

            style_instruction = """
Use:
- neon lighting
- futuristic cityscapes
- cyberpunk atmosphere
- high-tech environments
"""

        elif video_style == "Documentary":

            style_instruction = """
Use:
- educational storytelling
- realistic camera work
- informative visuals
- documentary tone
"""

        else:

            style_instruction = """
Use:
- commercial quality visuals
- marketing language
- product showcase style
- engaging presentation
"""

        with st.spinner(
            "Generating Professional Video Prompt..."
        ):

            try:

                video_prompt_request = f"""
You are an expert AI video prompt engineer.

User Idea:
{prompt}

Duration:
{duration}

Quality:
{quality}

Video Style:
{video_style}

Style Instructions:
{style_instruction}

Create a professional text-to-video prompt.

Include:

1. Environment
2. Subject Description
3. Lighting
4. Camera Movement
5. Visual Style
6. Motion Details
7. Rendering Quality

Return ONLY the final optimized prompt.
"""

                response = model.generate_content(
                    video_prompt_request,
                    generation_config={
                        "temperature": 0.7
                    }
                )

                st.session_state.video_prompt = (
                    response.text
                )

                st.session_state.prompt_history.append(
                    {
                        "style": video_style,
                        "prompt": response.text
                    }
                )

                st.success(
                    "Prompt Generated Successfully!"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

# ==========================================================
# REVIEW PROMPT
# ==========================================================

if review_button:

    if not st.session_state.video_prompt:

        st.warning(
            "Generate a prompt first."
        )

    else:

        with st.spinner(
            "Reviewing Prompt..."
        ):

            try:

                review_request = f"""
Review this AI video prompt.

Provide:

1. Quality Score (0-100)
2. Strengths
3. Weaknesses
4. Suggestions
5. Professional Rating

Prompt:

{st.session_state.video_prompt}
"""

                review_response = model.generate_content(
                    review_request
                )

                st.session_state.prompt_review = (
                    review_response.text
                )

            except Exception as e:

                st.error(
                    f"Review Error: {e}"
                )

# ==========================================================
# DISPLAY GENERATED PROMPT
# ==========================================================

if st.session_state.video_prompt:

    st.markdown("---")

    st.subheader(
        "🎬 Generated Video Prompt"
    )

    st.code(
        st.session_state.video_prompt,
        language="text"
    )

    st.download_button(
        label="📥 Download Prompt",
        data=st.session_state.video_prompt,
        file_name="video_prompt.txt",
        mime="text/plain",
        use_container_width=True
    )

# ==========================================================
# DISPLAY REVIEW
# ==========================================================

if st.session_state.prompt_review:

    st.markdown("---")

    with st.expander(
        "⭐ Prompt Review Report"
    ):

        st.markdown(
            st.session_state.prompt_review
        )

# ==========================================================
# PROMPT HISTORY
# ==========================================================

if st.session_state.prompt_history:

    st.markdown("---")

    st.subheader(
        "📜 Prompt History"
    )

    for item in reversed(
        st.session_state.prompt_history
    ):

        with st.expander(
            f"🎨 {item['style']}"
        ):

            st.write(
                item["prompt"]
            )