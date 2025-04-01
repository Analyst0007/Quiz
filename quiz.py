# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 09:36:33 2025

@author: Hemal
"""
import streamlit as st
import requests
import random

# Function to fetch questions from the Open Trivia Database API
def fetch_questions(amount=10, category=9, difficulty="medium", type="multiple"):
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type={type}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error("Failed to fetch questions from the API.")
        return []

# Initialize session state variables
if "questions" not in st.session_state:
    st.session_state.questions = fetch_questions()
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "correct" not in st.session_state:
    st.session_state.correct = False

# Function to display the current question and capture the user's response
def display_question():
    question_data = st.session_state.questions[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1}/{len(st.session_state.questions)}")
    st.write(question_data["question"])
    options = question_data["incorrect_answers"] + [question_data["correct_answer"]]
    random.shuffle(options)
    selected_option = None
    for option in options:
        if st.checkbox(option, key=option):
            selected_option = option
    return selected_option, question_data["correct_answer"]

# Function to check if the user's answer is correct and update the score
def check_answer(selected_option, correct_answer):
    if selected_option == correct_answer:
        st.session_state.score += 1
        st.session_state.correct = True
        st.success("Correct!")
    else:
        st.session_state.correct = False
        st.error(f"Wrong! The correct answer was: {correct_answer}")

# Main app logic
def main():
    st.title("Interactive Quiz App")
    if st.session_state.current_question < len(st.session_state.questions):
        selected_option, correct_answer = display_question()
        if st.button("Submit"):
            if selected_option is not None:
                st.session_state.submitted = True
                check_answer(selected_option, correct_answer)
            else:
                st.warning("Please select an answer before submitting.")

        if st.session_state.submitted:
            if st.session_state.correct:
                if st.button("Next"):
                    st.session_state.current_question += 1
                    st.session_state.submitted = False
                    st.session_state.correct = False
                    st.rerun()
            else:
                st.write("Please try again.")
    else:
        st.subheader("Quiz Finished!")
        st.write(f"Your final score is {st.session_state.score}/{len(st.session_state.questions)}.")
        if st.button("Restart Quiz"):
            st.session_state.questions = fetch_questions()
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.submitted = False
            st.session_state.correct = False
            st.rerun()

if __name__ == "__main__":
    main()
