# TalentScout Hiring Assistant

## Project Overview

The TalentScout Hiring Assistant is an intelligent chatbot designed to streamline the initial candidate screening process for a fictional recruitment agency specializing in technology placements. This chatbot gathers essential candidate information and assesses their technical proficiency by posing relevant questions based on their declared tech stack. It uses a Streamlit interface and the Gemini 2.0 Flash language model to create an interactive and efficient recruitment tool.

## Installation Instructions

1.  **Clone the Repository:**

    ```
    git clone  https://github.com/VINAYAK-N-MAGAJIKONDI/Hiring-Assistant.git
    cd talentscout
    ```
2.  **Create a Virtual Environment:**

    ```
    python -m venv venv
    source venv/bin/activate   # On Linux/macOS
    venv\Scripts\activate      # On Windows
    ```
3.  **Install Dependencies:**

    ```
    pip install -r requirements.txt
    ```
4.  **Set Up Environment Variables:**

    *   Create a `.env` file in the project root directory.
    *   Add your Gemini API key:

        ```
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY
        ```
    *   Optionally, set other configuration variables:

        ```
        DEBUG=False
        DEFAULT_LANGUAGE=en
        ```
5.  **Run the Application:**

    ```
    streamlit run app.py
    ```

## Usage Guide

1.  **Initial Setup:**
    *   The Application opens up in your browser
2.  **Start a Conversation:**
    *   The chatbot will initiate the conversation with a greeting. If it doesn't, you can type "Hello."
3.  **Provide Information:**
    *   Respond to the chatbot's questions about your:
        *   Full Name
        *   Email Address
        *   Phone Number
        *   Years of Experience
        *   Desired Position(s)
        *   Current Location
4.  **Declare Your Tech Stack:**
    *   Specify the programming languages, frameworks, databases, and tools you are proficient in.
5.  **Answer Technical Questions:**
    *   Answer the technical questions tailored to your declared tech stack.
6.  **View Conversation Analytics:**
    *   Check the sidebar for:
        *   Sentiment Analysis: See the sentiment trend of the conversation.
        *   Technical Assessment: View your scores on the technical assessment.
7.  **Manage Sessions:**
    *   Use the sidebar to:
        *   Reset Conversation: Start a new interview.
        *   Save Session: Store the current conversation for future review.
        *   Load Session: Resume a previously saved conversation.
8.  **End the Conversation:**
    *   Type "quit", "exit", "bye", or "end" to gracefully end the interview.

## Technical Details

*   **Programming Language:** Python
*   **Libraries:**
    *   `streamlit`: For creating the user interface.
    *   `google-genai`: For interacting with the Gemini 2.0 Flash language model.
    *   `python-dotenv`: For loading environment variables from the `.env` file.
    *   `textblob`: For performing sentiment analysis.
    *   `matplotlib` & `plotly`: For creating data visualizations.
    *   `langdetect`: For detecting the language of user input.
    *   `pycountry`: For language name retrieval.
*   **Model Details:**
    *   Gemini 2.0 Flash: A cost-effective and low-latency language model from Google.
*   **Architecture:**
    *   **Modular Design**: Separates concerns into distinct modules for better maintainability and scalability.
    *   **State Management**: Uses Streamlit's session state to maintain conversation context.
    *   **Prompt Engineering**: Employs tailored prompts to guide the LLM through different stages of the interview.
    *   **Streaming**: Leverages Gemini's streaming capability for a more responsive user experience.

## Prompt Design

The prompts were designed to effectively guide the Gemini model through the following stages:

*   **Greeting**: Introduces the chatbot and sets expectations.
*   **Information Gathering**: Systematically collects candidate details.
*   **Tech Stack Declaration**: Prompts the candidate to specify their technical skills.
*   **Technical Question Generation**: Generates tailored questions based on the declared tech stack, taking into account the candidate's experience level.
*   **Conclusion**: Gracefully ends the conversation and provides next steps.

The prompts are crafted to be clear, concise, and context-aware. They include:

*   A base prompt that defines the chatbot's role and guidelines.
*   Instructions specific to the current stage of the conversation.
*   Dynamic information about the candidate, such as their declared tech stack.
*   Sentiment analysis and language detection to adapt the tone and language of the response.

## Challenges & Solutions

*   **Challenge:** Accurately extracting and categorizing technical skills from free-form text.
    *   **Solution:** Implemented regular expressions and a comprehensive list of keywords to identify a wide range of technologies.
*   **Challenge:** Generating relevant and challenging technical questions.
    *   **Solution:** Designed prompts that instruct the LLM to create questions tailored to the candidate's declared tech stack and experience level.
*   **Challenge:** Handling sensitive candidate information securely.
    *   **Solution:** All data is stored in Streamlit's session state, which is ephemeral. No persistent storage of personal data is used.
*   **Challenge:** Maintaining conversation flow and context.
    *   **Solution:** Leveraged Streamlit's session state and included conversation history in each prompt to provide context to the language model.
*   **Challenge:** Ensuring the chatbot's responses are engaging and appropriate.
    *   **Solution:** Incorporated sentiment analysis to adjust the chatbot's tone and language to match the candidate's emotional state. Multilingual support ensures candidates can interact in their preferred language.

