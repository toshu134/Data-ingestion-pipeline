# 🚀 Delta Lake ETL Pipeline with AI Email Summary

This project demonstrates a fully automated **ETL pipeline** using **PySpark**, **Delta Lake**, and **LlamaIndex** to generate fake data every few minutes, store it in Delta format, and email a smart summary of the data using a large language model (LLM).

---

## 🔍 Key Features

- 🔁 Fake data generation using `Faker`
- ⚡ Ingestion into Delta Lake with Spark
- 🧠 AI-powered summary using `LlamaIndex` + `Groq`
- 📩 Email delivery with Gmail SMTP
- ⏱️ Runs every 5 minutes in a loop
- 🔄 Tracks Delta version before and after write

---

## 🗂️ Project Structure

```bash
celebal-project/
├── data_generation.py     # Generates fake name, address, email using Faker
├── Ingestion_csv          # (Auto-generated) stores the being generated into a csv file 
├── email_utils.py         # Uses LlamaIndex + Groq LLM to generate summary and send email
├── main_pipeline.py       # Master pipeline: generates, ingests, reads, summarizes and emails
├── spark.py               # Handles Spark session init, Delta write/read/versioning
├── data/                  # (Auto-generated) Delta table directory with version history
├── requirements.txt       # List of Python packages
└── README.md              # Project overview and instructions
```

---
## 💾 Data Storage Details

- **CSV (Optional):**  
  While currently not written, the fake data can easily be saved as a `.csv` using:
  ```python
  df.to_csv(f"batch_{timestamp}.csv", index=False)
  ```
  Useful for keeping a local log of batches.

- **Delta Table:**  
  Spark writes all records to a Delta table stored in the `data/` directory in **transactional parquet format**, maintaining **version history** using `DeltaTable.history()`.
---

---
## ⚙️ How It Works

1. `data_generation.py` creates 1000 fake records every cycle.
2. `spark.py` writes this data into a Delta Lake table and tracks its version history.
3. `main_pipeline.py` runs the full loop: generate → ingest → read → summarize → email.
4. `email_utils.py` uses **LlamaIndex** to summarize the ingested data and sends the summary + preview via email.

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies

Make sure you have Python 3.8+ and Java 8 or 11 installed (`java -version` to check).

Then, run:

```bash
pip install -r requirements.txt
```

---

## 🧪 Running the Pipeline

To start the looped pipeline:

```bash
python main_pipeline.py
```

It will:
- Generate fake user data
- Append it to a Delta table
- Track version before & after write
- Summarize new data via Groq LLM
- Email the summary every 5 minutes

---

## 🔐 Credentials To Replace

In `email_utils.py`:
- Replace `"your_groq_api_key"` with your **Groq API key**
- Replace Gmail credentials (`server.login(...)`) with your Gmail app password. Enable 2FA and generate an app password:  
  [How to Get App Password →](https://support.google.com/accounts/answer/185833)

---
![image](https://github.com/user-attachments/assets/4a894589-4143-40db-9cac-deef973fc144)

![image](https://github.com/user-attachments/assets/18ac42e9-45b4-402f-8d2f-a5d8d61bdf13)


## 👤 Author

**Arnav Kumar Singh**  
B.Tech CSE | Data & AI Enthusiast  
📧 arnavsingh0325@gmail.com  
🌐 [LinkedIn](https://www.linkedin.com/in/arnav-kumar-singh)

---

## 🛡 License

MIT License – Free to use for learning and demonstration.
