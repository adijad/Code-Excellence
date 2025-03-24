import requests
import json
import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
import time
from typing import List


def generate_response(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    history = []

    # Append new prompt to history
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model": "CodeExcellence",
        "prompt": final_prompt,
        "stream": False
    }

    # Make the request to the API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response = response.text
        data = json.loads(response)
        actual_response = data['response']
        return actual_response
    else:
        st.error(f"Error: {response.text}")


def show_typing_animation():
    with st.spinner("CodeExcellence is thinking... Generating your response... 💭"):
        time.sleep(1.5)


def main():
    st.set_page_config(page_title="CodeExcellence - Your Coding Assistant", page_icon="🤖", layout="wide")

    st.markdown(
        """
        <style>
        body {background-color: #1e1e2f; color: #ffffff;}
        .stButton>button {
            background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px; border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {background-color: #3e8e41;}
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #282c34; color: white; border: 1px solid #4CAF50;
            border-radius: 8px; padding: 10px;
        }
        .stSlider>div>div>div>div {
            background-color: #4CAF50;
        }
        .message-bubble {
            background-color: #3a3b3c; color: white; padding: 10px; border-radius: 10px; margin-bottom: 10px;
            animation: fadeIn 0.5s;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("✨ CodeExcellence: Your Interactive Coding Assistant")
    st.write("Helping you solve coding problems and providing detailed explanations.")

    st.markdown('---')

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown("### Problem Details")
        problem_statement = st.text_area("Describe your coding problem:", height=150, help="Provide a detailed description of your coding problem.")
        examples = st.text_area("Example Test Cases:", height=150, help="Provide sample test cases to test your solution.")
        constraints = st.text_area("Constraints:", height=100, help="Specify constraints for your coding problem.")

    with col2:
        st.markdown("### Settings")
        function_signature = st.text_input("Function Signature:", help="Specify the function signature if applicable.")
        approach = st.radio("Approach:", ("Brute Force", "Optimized"), help="Select the approach you want to generate.")
        language = st.selectbox("Programming Language:", ("Python", "Python3", "Java", "C++", "JavaScript"), help="Select your preferred programming language.")
        temperature = st.slider("Temperature (Creativity Level):", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="Control the randomness of the response. Lower values make the response more accurate.")

        st.write("""
            **Temperature Guide:**
            - Low (0.0 - 0.4): Accurate and structured responses.
            - Medium (0.5 - 0.7): Balanced creativity and precision.
            - High (0.8 - 1.0): Highly creative, less structured.
            """)

    st.markdown('---')

    if st.button("Generate Solution"):
        if problem_statement.strip() or function_signature.strip() or examples.strip() or constraints.strip():
            show_typing_animation()  # Show typing animation

            system_prompt = f'''
                FROM codellama
                ## Set the Temperature
                PARAMETER temperature {temperature}

                ## set the system prompt
                SYSTEM """
                You are CodeExcellence, a highly advanced code teaching assistant created by Aditya.
                Your purpose is to assist users with coding tasks, especially LeetCode problems, by providing:
                - Accurate code solutions.
                - Step-by-step explanations.
                - Debugging and optimization suggestions.
                - Comparison between brute-force and optimized approaches when applicable.
                - Handling multiple programming languages (Python, Python3, Java, C++, JavaScript, etc.)

                When solving problems, always follow this structure:
                1. Brute Force Solution:
                   - Provide the code solution.
                   - Explain the approach.
                   - Show example usage with test cases.

                2. Optimized Solution:
                   - Provide the code solution.
                   - Explain the optimized approach.
                   - Compare with the brute force approach.
                   - Show example usage with test cases.
                """
                '''

            prompt = system_prompt
            prompt += f"\n\nProblem: {problem_statement}" if problem_statement.strip() else ""
            prompt += f"\n\nFunction Signature: {function_signature}" if function_signature.strip() else ""
            prompt += f"\n\nExamples: {examples}" if examples.strip() else ""
            prompt += f"\n\nConstraints: {constraints}" if constraints.strip() else ""
            prompt += f"\n\nApproach: {approach}"
            prompt += f"\n\nProgramming Language: {language}"

            response = generate_response(prompt)

            if response:
                st.markdown(f'<div class="message-bubble">{response}</div>', unsafe_allow_html=True)

                if st.button("Run the Code and Check if it Works"):
                    st.info("Please provide feedback: Did the code run successfully? If not, specify the error or the issue.")
                    additional_input = st.text_area("Provide Additional Information or Error Details:")

                    if st.button("Reattempt Generation with Feedback") and additional_input.strip():
                        prompt += f"\n\nAdditional Feedback: {additional_input}"
                        response = generate_response(prompt)
                        st.markdown(f'<div class="message-bubble">{response}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please provide at least one field before generating a solution.")


if __name__ == "__main__":
    main()
