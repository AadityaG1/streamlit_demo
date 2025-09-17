import streamlit as st
import pandas as pd
import io
import time 
import importlib
from datetime import datetime

st.set_page_config(page_title="SAR Investigation Assistant", page_icon="🧠", layout="wide")

# --- Helper: try to import user model.py with a process(df) function ---
def load_user_model():
    try:
        mod = importlib.import_module("model")
        if hasattr(mod, "process"):
            return mod
    except Exception:
        pass
    return None

# --- Simple fallback processing if no model is provided ---
def fallback_process(df):
    # build a simple SAR-style narrative and some example flags
    rows, cols = df.shape
    first_col = df.columns[0] if cols > 0 else "N/A"
    sample_val = str(df[first_col].iloc[0]) if rows > 0 else "—"
    # narrative = (
        # f"On {datetime.utcnow().date()}, customer John Smith (Account Number ****1234) conducted unusual cash deposit activity involving multiple transactions totaling $250,000.\n\n"
        # f"WHO: John Smith, 45-year-old business owner, account holder since 2020.\n"
        # f"WHAT: 25 cash deposits ranging from $8,500 to $9,950, all below the $10,000 reporting threshold.\n\n"
        # f"WHEN: Concentrated over a 6-day period (January 10-15, 2024), representing a 300% increase from normal activity.\n\n"
        # f"WHERE: Deposits made across three different branch locations within a 50-mile radius of customer's primary address.\n\n"
        # f"WHY: Transactions appear designed to evade Currency Transaction Report (CTR) filing requirements. Customer unable to provide satisfactory explanation for source of funds.\n\n"
        # f"HOW: Detected via Large Cash Deposits AML rule trigger. Pattern analysis revealed systematic structuring behavior inconsistent with customer's historical transaction profile and stated business activities.\n\n"
        # f"Investigation confirmed SAR filing criteria based on structured transaction patterns and customer's evasive responses regarding fund sources.\n\n"
        # f"Recommendation: Proceed with manual review and consider filing a SAR if further investigation confirms suspicious intent."
    # )

    # narrative = ("""
    # This SAR is being filed because:  
    # 1) Lorem ipsom, a 24-year-old resident of Kenya, a high-risk jurisdiction, has been identified as the recipient of payments, mostly from elderly individuals located in the US, GB, and other countries, with no clear purpose for the activity;  
    # 2) The suspicious activity occurred between August 1, 2024, and October 31, 2024, involving credit amounts greater than $2,000 from 12 elderly counterparties with an average age of 54; and
    # 3) Nyandusi has been identified as the subject in this matter.  

    # PayPal operates an online payment system that allows individuals and businesses to send and receive money globally through an account created with an email address provided by the account holder. Funds can be loaded to a PayPal account with a bank account or credit/debit card. A PayPal account can be used to make purchases, pay bills, or transfer money directly to anyone with an email address, but to receive the funds the recipient must have a PayPal account associated with that email address.  

    # Between August 1, 2024, and October 31, 2024, Nyandusi received multiple payments from accounts based in the US, GB, and other countries. The volume and frequency of these transfers, combined with the significant age disparity between Nyandusi and the elderly senders, raise strong concerns consistent with Elder Financial Exploitation (EFE) typologies outlined in AML rule 2105. Notes associated with Nyandusi’s credit transactions included use of emojis and references to “friends and family,” which do not indicate a clear purpose for the transactions.  

    # The transfers suggest a coordinated pattern of potentially exploitative activity whereby funds are moved from elderly individuals’ accounts to a younger individual in a high-risk jurisdiction. This activity aligns with known red flags for elder exploitation, including age disparity, geographic risk, and multiple elderly source accounts.  

    # Given the typology and evidence, these transactions warrant enhanced scrutiny and ongoing monitoring. The associated accounts are flagged for potential law enforcement reporting and PayPal is prepared to provide additional documentation to support further investigation.
    # """)

    narrative = ("""
    This SAR is being filed because:  
    1) John Doe, a 25-year-old resident of a high-risk jurisdiction, has been identified as the recipient of payments, mostly from elderly individuals located in the US, GB, and other countries, with no clear purpose for the activity;  
    2) The suspicious activity occurred between January 1, 2023, and March 31, 2023, involving credit amounts greater than $2,000 from 12 elderly counterparties with an average age of 54; and  
    3) John Doe has been identified as the subject in this matter.  

    PayPal operates an online payment system that allows individuals and businesses to send and receive money globally through an account created with an email address provided by the account holder. Funds can be loaded to a PayPal account with a bank account or credit/debit card. A PayPal account can be used to make purchases, pay bills, or transfer money directly to anyone with an email address, but to receive the funds the recipient must have a PayPal account associated with that email address.  

    Between January 1, 2023, and March 31, 2023, John Doe received multiple payments from accounts based in the US, GB, and other countries. The volume and frequency of these transfers, combined with the significant age disparity between John Doe and the elderly senders, raise strong concerns consistent with Elder Financial Exploitation (EFE) typologies outlined in AML rule 2105. Notes associated with John Doe’s credit transactions included use of emojis and references to “friends and family,” which do not indicate a clear purpose for the transactions.  

    The transfers suggest a coordinated pattern of potentially exploitative activity whereby funds are moved from elderly individuals’ accounts to a younger individual in a high-risk jurisdiction. This activity aligns with known red flags for elder exploitation, including age disparity, geographic risk, and multiple elderly source accounts.  
    
    Given the typology and evidence, these transactions warrant enhanced scrutiny and ongoing monitoring. The associated accounts are flagged for potential law enforcement reporting and PayPal is prepared to provide additional documentation to support further investigation.
    """)

    
    # st.markdown(f"""
    # <div style="border:2px solid #4CAF50; border-radius:10px; padding:20px; background-color:#f9f9f9;">
    # {narrative}
    # </div>
    # """, unsafe_allow_html=True)


    flags = {
        "Large cash deposits below reporting thresholds": True,
        "Transactions with high-risk jurisdictions": False,
        "Use of multiple nominee accounts": False,
        "Rapid movement of funds between accounts": True,
        "Structuring or layeing activity": True
    }

    # create a small report dataframe as downloadable content (example)
    report_df = df.head(10).copy()
    report_df["_ai_flag_summary"] = "review_recommended"
    return narrative, flags, report_df

# --- UI ---
st.title("SAR Investigation Assistant")


# --- Custom CSS for bigger uploader ---
st.markdown("""
    <style>
    .stFileUploader {
        border: 3px dashed #4CAF50;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        background-color: #f9f9f9;
    }
    .stFileUploader > div:first-child {
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- File Uploader (big square box) ---
uploaded = st.file_uploader("📥 Drop your Excel/CSV file here to start investigation", type=["csv", "xlsx", "xls"])






# uploaded = st.file_uploader("Upload CSV or Excel file to start investigation", type=["csv", "xlsx", "xls"])

if not uploaded:
    st.info("Please upload a CSV / Excel file to begin the investigation.")
    st.stop()

# Read file
try:
    if uploaded.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)
except Exception as e:
    st.error(f"Could not read file: {e}")
    st.stop()



# --- Show investigation started with timer ---
status_box = st.empty()
for i in range(3, 0, -1):  # countdown 3 → 1
    status_box.info(f"⏳ Investigation started... generating report (about {i} sec left)")
    time.sleep(1)

status_box.empty()  # remove the "investigation started" box




# Run model if available else fallback
user_model = load_user_model()
if user_model:
    try:
        # Expect model.process to return (narrative:str, flags:dict, report_df:pd.DataFrame) or just a dataframe
        result = user_model.process(df)
        if isinstance(result, tuple) and len(result) >= 3:
            narrative, flags, report_df = result[0], result[1], result[2]
        elif isinstance(result, pd.DataFrame):
            narrative = "Model returned a dataframe result. See downloadable report."
            flags = {}
            report_df = result
        else:
            # unknown shape, fallback
            narrative, flags, report_df = fallback_process(df)
    except Exception as e:
        st.error(f"Error running model.process: {e}")
        narrative, flags, report_df = fallback_process(df)
else:
    narrative, flags, report_df = fallback_process(df)

# --- Downloadable report button (visible after processing) ---
# csv_bytes = report_df.to_csv(index=False).encode("utf-8")
# st.download_button(
#     label="Download Investigation Report (CSV)",
#     data=csv_bytes,
#     file_name="investigation_report.csv",
#     mime="text/csv",
# )

# --- Downloadable report button (visible after processing) ---

csv_bytes = report_df.to_csv(index=False).encode("utf-8")

# st.download_button(

#     label="Download Investigation Report (CSV)",

#     data=csv_bytes,

#     file_name="investigation_report.csv",

#     mime="text/csv",

# )
 

st.markdown(
    """
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <a href="data:file/csv;base64,{csv}" download="investigation_report.csv">
            <button style="
                background-color: #10b981;   /* change to #3b82f6 for blue */
                color: white;
                font-weight: bold;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;">
                ⬇ Download Investigation Report (CSV)
            </button>
        </a>
    </div>
    """.format(csv=csv_bytes.decode("latin1")),
    unsafe_allow_html=True,
)


st.markdown("---")

# --- Two-column UI: Narrative (left) and AML Red Flags (right) ---
left, right = st.columns([3, 2])

with left:
    st.subheader("SAR Narrative")

    st.write(narrative)


with right:
    st.subheader("AML Red Flags")
    if not flags:
        st.write("No automated flags produced.")
    else:
        for k, v in flags.items():
            if v:
                st.markdown(f"- ✅ {k}")
            else:
                st.markdown(f"- ❌ {k}")


st.markdown("---")
st.caption("This is an automated investigation summary. Always verify findings manually before filing any formal report.")
