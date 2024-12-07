import os
import streamlit as st
from dotenv import load_dotenv
import openai
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import time
import json
from streamlit_lottie import st_lottie

load_dotenv()
OPENAI_API_KEY = 'Enter API'
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

if not OPENAI_API_KEY:
    st.error("Please set the OPENAI_API_KEY in your environment.")
    st.stop()

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

LESSON_PLAN_TEMPLATE = """
You are a teaching assistant AI. Given the following curriculum context:

{curriculum_context}

Create a fully personalized lesson plan for a {grade_level}-year-old student following the {country}'s curriculum, focusing on {subject}.

The tutor has requested the following:
- **Question/Focus Topic**: "{user_question}"
- **Duration of the lesson**: {lesson_duration} minutes
- **Focus Area**: {focus_area}

{special_needs_instructions}

**IMPORTANT:**
1. If the user's question or focus topic is **not related to the chosen subject ({subject})**, then simply respond:
   "**The question asked is not related to the subject selected.**"
   Do not produce a lesson plan in this case.
2. If it is related, then proceed as follows:
   - Begin by clearly stating the session details: "**This {lesson_duration}-minute, {focus_area} session will ...**"
   - For each section of the lesson (warm-up, theory, practice, etc.), mention the time allocated and highlight it in bold (e.g., "**Warm-up (5 minutes):** ...").
   - Highlight key learning objectives, essential concepts, resources, and differentiation strategies in **bold**.  
     For differentiation, bold words like "**support**" (for struggling students) and "**extension**" (for advanced learners).
   - Use **bold text** for all crucial instructions, titles, durations, resources, and any other critical information.

The lesson plan should include:
1. **Title and learning objectives** aligned with the curriculum.
2. A **warm-up activity**.
3. **Theory explanation**, age-appropriate and engaging.
4. **Practice questions** (mild, hot, spicy) with **model answers**.
5. **Gamification ideas**.
6. **Resources** (videos, worksheets, websites).
7. **Differentiation** (support for struggling students, extension for advanced).
8. A **tutor reflection prompt** at the end.

Also, ensure to provide approximate time allocations for each part so that the total fits into the chosen duration.
"""

FOLLOW_UP_TEMPLATE = """
You are a teaching assistant AI. Here is the conversation so far:

{conversation_context}

A new follow-up question is asked: "{follow_up_question}"

{special_needs_instructions}

**REMINDER:**
- The session is {lesson_duration} minutes and is {focus_area}.
- If the follow-up question is not related to the chosen subject, respond:
  "**The question asked is not related to the subject selected.**"
- Otherwise, continue using **bold text** to highlight key points, instructions, and resources in your follow-up answer.
"""

lesson_plan_prompt = PromptTemplate(
    input_variables=["curriculum_context", "grade_level", "country", "subject", "user_question", "special_needs_instructions", "lesson_duration", "focus_area"],
    template=LESSON_PLAN_TEMPLATE
)

follow_up_prompt = PromptTemplate(
    input_variables=["conversation_context", "follow_up_question", "special_needs_instructions", "lesson_duration", "focus_area"],
    template=FOLLOW_UP_TEMPLATE
)

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

def load_vector_store(country: str):
    persist_dir = f"chroma_dbs/chroma_{country}"
    if not os.path.exists(persist_dir):
        st.error(f"No vector store found for {country}. Please ensure it's created.")
        st.stop()

    db = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_dir
    )
    return db

with open("animation.json", "r") as f:
    lottie_animation = json.load(f)

def main():
    st.set_page_config(page_title="Curriculum-Aligned Lesson Plan Generator", layout="centered")

    st.title("Ed-Guide")

    if "conversation" not in st.session_state:
        st.session_state["conversation"] = ""

    with st.sidebar:
        st.header("Configuration")
        country = st.selectbox(
            "Select Curriculum Country:",
            options=["Australia", "India", "UK", "USA", "Europe"]
        )

        grade_level = st.number_input(
            "Student Age (Years):",
            min_value=5, max_value=18, value=14, step=1
        )

        subject = st.selectbox(
            "Subject:",
            options=["Mathematics", "Science", "English", "History", "Geography", "Computer Science"]
        )

        user_question = st.text_input("Enter your question or focus topic:", value="", help="Type a specific question or focus area for this lesson.")

        special_needs = st.selectbox("Special Needs:", options=["No", "Yes"], help="If yes, the lesson will be simplified for easier understanding.")

        lesson_duration = st.selectbox("Lesson Duration (minutes):", options=[30, 45, 60, 90, 120], index=2)
        focus_area = st.selectbox("Focus Area:", options=["Theory-heavy", "Practice-heavy", "Balanced"], index=2)

        top_k = st.slider("Number of curriculum context chunks to retrieve:", 1, 10, 4)

        generate_button = st.button("Generate Lesson Plan")

    special_needs_instructions = ""
    if special_needs == "Yes":
        special_needs_instructions = "Note: The student has special learning needs. Regardless of age, please simplify the concepts, use very accessible language, and provide additional **support** or scaffolding as necessary."

    if generate_button:
        loading_placeholder = st.empty()
        with loading_placeholder:
            st_lottie(lottie_animation, key="loading_lottie", height=300, width=300)

        db = load_vector_store(country)

        query = f"{grade_level}-year-old {subject} curriculum"
        docs = db.similarity_search(query, k=top_k)
        if not docs:
            loading_placeholder.empty()
            st.error("No relevant curriculum context found for your query.")
            return

        curriculum_context = "\n\n".join([d.page_content for d in docs])

        chain = LLMChain(llm=llm, prompt=lesson_plan_prompt)
        lesson_plan = chain.run(
            curriculum_context=curriculum_context,
            grade_level=str(grade_level),
            country=country,
            subject=subject,
            user_question=user_question,
            special_needs_instructions=special_needs_instructions,
            lesson_duration=str(lesson_duration),
            focus_area=focus_area
        )

        loading_placeholder.empty()

        st.session_state["conversation"] = f"Initial Lesson Plan:\n{lesson_plan}\n\n"

        st.subheader("Generated Lesson Plan")
        st.write(lesson_plan)
    else:
        if st.session_state["conversation"] == "":
            st.write("""
            ### Instructions:
            1. Set the country, age, and subject in the sidebar.
            2. (Optional) Enter a specific question or focus topic.
            3. Choose if the student has special needs (Yes/No).
            4. Choose a lesson duration and a focus area.
            5. Click 'Generate Lesson Plan'.
            6. After the plan is generated, you can ask multiple follow-up questions.
            """)

    if st.session_state["conversation"] != "":
        st.write("---")
        st.write("### Ask a Follow-Up Question")
        follow_up_question = st.text_input("Enter your follow-up question here:", key="follow_up_input")
        follow_up_button = st.button("Ask Follow-Up")

        if follow_up_button and follow_up_question.strip():
            follow_up_loading = st.empty()
            with follow_up_loading:
                st_lottie(lottie_animation, key="follow_up_lottie", height=300, width=300)

            time.sleep(2)

            follow_up_answer = LLMChain(llm=llm, prompt=follow_up_prompt).run(
                conversation_context=st.session_state["conversation"],
                follow_up_question=follow_up_question,
                special_needs_instructions=special_needs_instructions,
                lesson_duration=str(lesson_duration),
                focus_area=focus_area
            )

            follow_up_loading.empty()

            st.session_state["conversation"] += f"Follow-Up Q: {follow_up_question}\nAnswer: {follow_up_answer}\n\n"

            st.write("**Follow-Up Answer:**")
            st.write(follow_up_answer)

if __name__ == "__main__":
    main()
