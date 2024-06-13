# RAG-Powered Chatbot for PDF Document Queries

## Overview

This repository contains a Retrieval-Augmented Generation (RAG) powered chatbot designed to answer questions based on the Churchill motor insurance policy booklet. The chatbot utilizes natural language processing techniques for document retrieval and generation. The front end is developed using Streamlit to provide an interactive user interface.

## Project Structure

### Files Included

- **`README.md`**: This file, providing an overview of the project and instructions for setup.
- **`requirements.txt`**: Lists the Python dependencies required to run the project.
- **`app.py`**: Main file for the Streamlit application, handling user interactions and displaying responses.
- **`main.py`**: Contains the implementation of the chatbot model using Ollama for text embedding and retrieval.
- **`run.py`**: Contains the Query function to return the response.
- **`testdata.csv`**: Dataset file containing query-response pairs used for training and evaluation.

### Setup Instructions

1. **Environment Setup**:
   - Clone this repository to your local machine.
   - Navigate to the project directory.

2. **Install Dependencies**:
   - Ensure Python 3.x is installed.
   - Install required Python packages using pip:

     ```
     pip install -r requirements.txt
     ```

3. **Running Ollama Server**:
   - Before running the chatbot, start the Ollama server for text embedding and retrieval:
     - Download and install Ollama from [Ollama Website](https://ollama.com).
     - Start the Ollama server using the command:

       ```
       ollama serv
       ```

     - Note: Ensure the Ollama server is running and accessible before proceeding.

4. **Running the Chatbot**:
5. - Execute the main.py to register the PDF and to create chunks.
     ```
     python3 main.py
     ```
   - Execute the Streamlit application to start the chatbot interface:
     ```
     streamlit run app.py
     ```
   - This command launches the Streamlit server locally.
   - Access the chatbot interface in your web browser at `http://localhost:8501`.

### Usage

- Input your query related to the Churchill motor insurance policy booklet.
- The chatbot will retrieve relevant information and display the response.
- Evaluate the accuracy of responses based on expected answers provided in `data.csv`.

### Contributors

- Anirudh Malhotra


### Additional Notes
- Additional PDFs can be added to the data folder and run simultanously by running the main.py file.
