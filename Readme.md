# AZURE - AWS - LOCAL - STREAMLIT

This project facilitates the conversion of files stored in various storage solutions including local storage, Azure Blob Storage, and AWS S3 buckets. It is designed to retrieve data based on user-provided credentials, convert this data into chunks, and subsequently create a chroma vector store. The application is built with a user-friendly interface implemented using Streamlit, making it accessible and easy to use.

### Key Features:
- **Data Conversion**: Converts data into manageable chunks and creates a chroma vector store.
- **Multiple Storage Options**: Supports local storage, Azure Blob Storage, and AWS S3 buckets.
- **Streamlit Interface**: Features a Streamlit-based GUI for ease of use and accessibility.

## Storage Configuration

### Azure Blob Storage
- **Input Required**:
  - Azure Blob connection string
  - Container name

### AWS S3 Bucket
- **Input Required**:
  - AWS Access Key
  - AWS Secret Key
  - Bucket name
  - Object name

### Local Storage
- **Assumption**:
  - The local folder is located at the root of the project.

## Installation and Setup

To replicate and run this project, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shyamsundar009/azure-aws-local-streamlit
   cd azure-aws-local-streamlit
   ```

2. **Install Required Libraries**
    
    Follow the steps to create a virtual environment and install the required libraries.
   ```bash
    python -m venv myenv
    
    myenv\Scripts\activate
    
    pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
    Insert OpenAI Key

    Insert your OpenAI API key in the appropriate configuration file or environment variable. Use the .env_template file and paste the key and rename it as .env

    ```bash
    OPENAI_API_KEY="sk-#####################"
    ```
4. **Run the Streamlit Application**
   ```bash
   streamlit run homepage.py
   ```

5. **Access the Application**
   - Open your web browser and navigate to `http://localhost:8501` to view the application.



Enjoy converting your files with ease and efficiency!