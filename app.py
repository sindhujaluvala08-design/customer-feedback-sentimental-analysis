import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Customer Feedback Dashboard",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(to right, #fffaf5, #fef6e9);
}

/* Headers */
h1, h2, h3 {
    color: #7c2d12;
    font-family: 'Segoe UI';
    font-weight: 700;
}

/* KPI Cards */
.kpi-card {
    background: rgba(255,255,255,0.9);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    border-bottom: 5px solid #fb923c;
    transition: 0.3s;
}

.kpi-card:hover {
    transform: translateY(-5px);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #fdba74, #fb923c);
}

/* Sidebar Labels */
section[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background-color: #ea580c;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #c2410c;
    color: white;
}

/* Download Button */
.stDownloadButton>button {
    background-color: #f97316;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

/* Insight Boxes */
.insight-box {
    background: white;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #7c2d12;
    padding: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():

    col1, col2, col3 = st.columns([1,1.5,1])

    with col2:

        st.markdown("<h1 style='text-align:center;'> Secure Login</h1>", unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("Invalid Credentials")

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():

    df = pd.read_csv("customer_feedback_satisfaction.csv")

    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title(" Filters")

country_filter = st.sidebar.multiselect(
    "Country",
    df["Country"].unique(),
    default=df["Country"].unique()
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

loyalty_filter = st.sidebar.multiselect(
    "Loyalty Level",
    df["LoyaltyLevel"].unique(),
    default=df["LoyaltyLevel"].unique()
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["Country"].isin(country_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["LoyaltyLevel"].isin(loyalty_filter))
]

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>
 Customer Feedback Satisfaction Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; color:#7c2d12; font-size:18px;'>
Customer Insights & Satisfaction Analysis
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- KPI SECTION ----------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>Total Customers</h4>
    <h2>{filtered_df["CustomerID"].nunique()}</h2>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>Avg Satisfaction</h4>
    <h2>{filtered_df["SatisfactionScore"].mean():.1f}</h2>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>Avg Income</h4>
    <h2>₹ {filtered_df["Income"].mean():,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>Purchase Frequency</h4>
    <h2>{filtered_df["PurchaseFrequency"].mean():.1f}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- CHARTS ----------------
c1, c2 = st.columns(2)

with c1:

    country_sat = filtered_df.groupby("Country")[
        "SatisfactionScore"
    ].mean().reset_index()

    fig1 = px.bar(
        country_sat,
        x="Country",
        y="SatisfactionScore",
        color="Country",
        text_auto=True,
        title=" Country-wise Satisfaction",
        color_discrete_sequence=[
            "#fdba74",
            "#fb923c",
            "#f97316",
            "#ea580c"
        ]
    )

    fig1.update_layout(template="plotly_white", height=420)

    st.plotly_chart(fig1, use_container_width=True)

with c2:

    feedback = filtered_df["FeedbackScore"].value_counts().reset_index()
    feedback.columns = ["Feedback", "Count"]

    fig2 = px.pie(
        feedback,
        values="Count",
        names="Feedback",
        hole=0.5,
        title="💬 Feedback Distribution",
        color_discrete_sequence=[
            "#ffedd5",
            "#fdba74",
            "#fb923c",
            "#ea580c"
        ]
    )

    fig2.update_layout(template="plotly_white", height=420)

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- SECOND ROW ----------------
c3, c4 = st.columns(2)

with c3:

    quality_df = filtered_df.groupby("LoyaltyLevel")[
        ["ProductQuality", "ServiceQuality"]
    ].mean().reset_index()

    fig3 = px.bar(
        quality_df,
        x="LoyaltyLevel",
        y=["ProductQuality", "ServiceQuality"],
        barmode="group",
        title=" Product vs Service Quality",
        color_discrete_sequence=["#f97316", "#fb923c"]
    )

    fig3.update_layout(template="plotly_white", height=420)

    st.plotly_chart(fig3, use_container_width=True)

with c4:

    purchase_df = filtered_df.groupby("LoyaltyLevel")[
        "PurchaseFrequency"
    ].mean().reset_index()

    fig4 = px.bar(
        purchase_df,
        x="LoyaltyLevel",
        y="PurchaseFrequency",
        color="LoyaltyLevel",
        text_auto=True,
        title="Loyalty vs Purchase Frequency",
        color_discrete_sequence=[
            "#ffedd5",
            "#fdba74",
            "#fb923c",
            "#ea580c"
        ]
    )

    fig4.update_layout(template="plotly_white", height=420)

    st.plotly_chart(fig4, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.markdown("---")

st.subheader(" Key Insights")

st.markdown(f"""
<div class='insight-box'>
 Highest Satisfaction Country:
<b>{country_sat.sort_values(by='SatisfactionScore', ascending=False).iloc[0]['Country']}</b>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='insight-box'>
 Most Common Loyalty Level:
<b>{filtered_df['LoyaltyLevel'].mode()[0]}</b>
</div>
""", unsafe_allow_html=True)

# ---------------- DOWNLOAD BUTTON ----------------
st.markdown("---")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label=" Download Dataset",
    data=csv,
    file_name="customer_feedback.csv",
    mime="text/csv",
    use_container_width=True
)

# ---------------- FOOTER ----------------
st.markdown("""
<div class='footer'>
 Developed using Streamlit, Pandas & Plotly
</div>
""", unsafe_allow_html=True)