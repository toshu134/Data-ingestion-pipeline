import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from llama_index.core import VectorStoreIndex, Document
from llama_index.llms.groq import Groq
import pandas as pd

def summarize_with_llamaindex(df):
    df_head = df.head(5).to_string()

    full_text = f"""Here is a preview of the dataset:

{df_head}

Summarize this data for a non-technical person.
"""
    doc = Document(text=full_text)
    llm = Groq(
        model="llama3-8b-8192",
        api_key="xxx"
    )
    index = VectorStoreIndex.from_documents([doc])
    query_engine = index.as_query_engine(llm=llm)
    response = query_engine.query("Summarize this data preview.")
    return str(response)

def send_email_summary(df_spark, version):
    df = df_spark.toPandas()
    html_preview = df.head().to_html(index=False)
    summary_text = summarize_with_llamaindex(df)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Delta Ingestion Summary - Version {version}"
    msg["From"] = "toshu129@@gmail.com"
    msg["To"] = "arnavsingh0325@gmail.com"
    html_body = f"""
    <html>
        <body>
            <h2>Delta Table Updated - Version {version}</h2>
            <h3>AI Summary:</h3>
            <p>{summary_text}</p>
            <h3>Top 5 Rows:</h3>
            {html_preview}
        </body>
    </html>
    """
    msg.attach(MIMEText(html_body, "html"))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("toshu129@gmail.com", "mmm")
            server.send_message(msg)
            print("Email sent with LlamaIndex summary.")
    except Exception as e:
        print(f"Failed to send email: {e}")
