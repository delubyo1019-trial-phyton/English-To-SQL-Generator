import os
import re
import time
from dotenv import load_dotenv
from groq import Groq
from schema import build_schema_context

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

client = Groq(api_key=api_key)

SCHEMA_CONTEXT = build_schema_context()

SYSTEM_PROMPT = f"""You are an expert Snowflake SQL assistant specializing in license-sharing detection for a software product.

You have access to the following database schema:

{SCHEMA_CONTEXT}

Your job:
1. Read the user's question carefully.
2. Write a clean, correct Snowflake SQL query using ONLY the tables and columns defined in the schema above.
3. Return the SQL query in a code block first.
4. Then explain in 2-3 sentences what the query does and why it answers the question.

Critical rules:
- ALWAYS use the exact table and column names from the schema — no invented names.
- ALWAYS filter USER_PERMISSIONED = 'Yes' unless the user specifically asks about inactive users.
- ALWAYS cast EVENT_DATA JSON extractions with :: e.g. EVENT_DATA:windows_credential::VARCHAR
- Use STAT_COLLECTED_DATE directly for date filtering.
- For license-sharing detection, the key pattern is: multiple distinct EVENT_DATA:windows_credential::VARCHAR values for the same LOGIN_ID within a time period.
- Use the standard join pattern: FROM FACT_WS_SESSIONS F LEFT JOIN DIM_USER U ON F.USER_D_KEY = U.USER_D_KEY LEFT JOIN DIM_CUSTOMER C ON F.CUSTOMER_D_KEY = C.CUSTOMER_D_KEY"""

REVIEW_PROMPT = """You are a Snowflake SQL reviewer. Review the SQL query below against the schema context provided and check for:
1. Correct table and column names (must match the schema exactly)
2. Correct Snowflake JSON syntax for EVENT_DATA (colon notation + :: casting)
3. Correct join keys
4. Whether USER_PERMISSIONED = 'Yes' filter is applied where needed
5. Whether the query actually answers the original question

If the query is correct, respond with: "✅ Query looks correct." followed by one sentence confirming why.
If there are issues, respond with: "⚠️ Issues found:" followed by specific corrections."""


def generate_sql(user_question: str) -> dict:
    """
    Chain 1: Generate SQL from the user's question using schema context.
    Chain 2: Self-review the generated SQL against the schema.
    Returns a dict with keys: question, sql, explanation, review, error
    """
    result = {
        "question": user_question,
        "sql": None,
        "explanation": None,
        "review": None,
        "error": None
    }

    try:
        # Chain 1 — Generate SQL (with retry for rate limits)
        max_retries = 3
        gen_response = None

        for attempt in range(max_retries):
            try:
                gen_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_question}
                    ],
                    temperature=0.1
                )
                break
            except Exception as e:
                if "429" in str(e) or "rate" in str(e).lower():
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    else:
                        raise
                else:
                    raise

        if gen_response is None:
            raise Exception("No response after retries")

        raw_output = gen_response.choices[0].message.content

        # Parse SQL and explanation from the response
        code_block_match = re.search(r"```(?:sql)?\n(.*?)```", raw_output, re.DOTALL)
        if code_block_match:
            sql_part = code_block_match.group(1).strip()
            explanation_part = raw_output[code_block_match.end():].strip()
        else:
            sql_part = raw_output.strip()
            explanation_part = ""

        result["sql"] = sql_part
        result["explanation"] = explanation_part

        # Chain 2 — Self-review
        review_contents = f"""Original question: {user_question}

Schema context:
{SCHEMA_CONTEXT}

Generated SQL to review:
```sql
{sql_part}
```

Review this SQL query."""

        review_response = None
        for attempt in range(max_retries):
            try:
                review_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": REVIEW_PROMPT},
                        {"role": "user", "content": review_contents}
                    ],
                    temperature=0.1
                )
                break
            except Exception as e:
                if "429" in str(e) or "rate" in str(e).lower():
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    else:
                        raise
                else:
                    raise

        if review_response is not None:
            result["review"] = review_response.choices[0].message.content

    except Exception as e:
        result["error"] = f"Error: {e}"

    return result