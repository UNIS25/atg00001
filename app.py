import streamlit as st
import pandas as pd

# Set up page configuration
st.set_page_config(page_title="United Nations Information Services Digitalization Project", layout="wide")

# UN branding
UN_LOGO = "https://logowik.com/content/uploads/images/un-united-nations3511.logowik.com.webp"

# Ensure session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Custom styling for UN Blue background, black content box, and white text
# Custom styling for UN Blue background and white text
st.markdown(
    """
    <style>
        /* Set full page background to UN Blue */
        body, .stApp {
            background-color: #009EDB !important;
            color: black !important;  /* Change text color to black */
        }

        /* Keep header white */
        .header {
            display: flex;
            align-items: center;
            justify-content: start;
            background-color: white !important;
            padding: 20px 50px;
            border-bottom: 5px solid #0072C6;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            color: black !important;
        }

        .header img {
            width: 240px;
            margin-right: 20px;
        }

        .header-content {
            display: flex;
            flex-direction: column;
            justify-content: center;
            color: black !important;
        }

        .header-text {
            font-size: 28px;
            font-weight: bold;
            text-align: left;
            color: black !important;
        }

        .tagline {
            font-size: 18px;
            font-weight: bold;
            color: black !important;  /* Ensure tagline is black */
            text-align: left;
        }

        .developer {
            font-size: 12px;
            color: black !important;
            margin-top: 5px;
        }

        /* Navigation bar remains blue */
        .nav-bar {
            display: flex;
            justify-content: start;
            background-color: #0072C6 !important;
            padding: 10px 20px;
        }

        .nav-button {
            font-size: 18px;
            padding: 12px 30px;
            border: 2px solid white;
            background: none;
            color: white !important;
            cursor: pointer;
            transition: background 0.3s, color 0.3s;
            margin: 0 5px;
        }
        .nav-button:hover {
            background-color: white !important;
            color: #0072C6 !important;
        }

        /* Make content sections UN Blue */
        .container {
            text-align: center;
            padding: 50px;
            background-color: #009EDB !important;
            color: black !important;  /* Change content text color to black */
            border-radius: 10px;
            width: 80%;
            margin: auto;
        }

        /* Make section headings and text black */
        h2, h3, h4, h5, h6, p {
            color: black !important;
        }

        a {
            color: #0072C6 !important; /* UN Blue links */
        }

    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
st.markdown(
    f"""
    <div class="header">
        <img src="{UN_LOGO}" alt="UN Logo">
        <div class="header-content">
            <div class="header-text">United Nations Information Services Digitalization Project</div>
            <div class="tagline">Transforming traditional documentation into a digital future</div>
            <div class="developer">Developed by ATG</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Add the black box wrapper for navigation
st.markdown('<div class="black-box">', unsafe_allow_html=True)

# Navigation Bar inside black box
selected_page = st.radio("", ["Home", "Weekly Report", "Contact"], horizontal=True)

# Close the black box
st.markdown('</div>', unsafe_allow_html=True)

# Set page session
st.session_state.page = selected_page

# Home Page
if st.session_state.page == "Home":
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("<h2>Welcome to the Digital Future</h2><p>Explore the power of digital transformation in streamlining UN documentation.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Weekly Report Page
elif st.session_state.page == "Weekly Report":
    st.markdown("<div class='container'><h2>Weekly Report</h2><p>Upload your files and analyze engagement data.</p></div>", unsafe_allow_html=True)

    import pandas as pd

    # Function to read uploaded files
    def read_file(uploaded_file, platform=None):
        if uploaded_file.name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xls", ".xlsx")):
            if platform == "LinkedIn":
                return pd.read_excel(uploaded_file, sheet_name="All posts", skiprows=1)
            return pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Upload .csv, .xls, or .xlsx files.")
            return None

    # Function to dynamically detect column names
    def map_columns(df, column_map):
        new_mapping = {}
        for key, value in column_map.items():
            possible_columns = key.split("|")
            for col in possible_columns:
                if col in df.columns:
                    new_mapping[col] = value
                    break
        return new_mapping

    # Platform processing function
    def process_platform(df, platform, cols_map, engagement_cols, start_date, end_date):
        cols_map = map_columns(df, cols_map)
        df_selected = df[list(cols_map.keys())].rename(columns=cols_map)
        df_selected['Date'] = pd.to_datetime(df_selected['Date'], errors='coerce')

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        df_selected = df_selected[(df_selected['Date'] >= start_date) & (df_selected['Date'] <= end_date)]
        df_selected['Engagements'] = df_selected[engagement_cols].sum(axis=1)
        df_selected = df_selected.sort_values(by='Engagements', ascending=False).head(3)
        df_selected.insert(0, 'Platform', platform)
        df_selected.insert(1, 'Rank', [1, 2, 3])
        df_selected['Date'] = df_selected['Date'].dt.strftime('%m/%d/%Y')
        return df_selected[["Platform", "Rank", "Date", "Post text", "Link", "Impressions", "Engagements", "Reactions", "Comments", "Shares"]]

    # Streamlit app
    st.title('📊 Social Media Engagement Report')

    # Date range selection
    st.sidebar.header("Select Date Range")
    start_date = st.sidebar.date_input("Start date")
    end_date = st.sidebar.date_input("End date")

    processing_functions = {
        "X English": lambda df: process_platform(df, "X English", {
            "Date": "Date", "Post text": "Post text", "Link": "Link", "Impressions": "Impressions",
            "Engagements": "Engagements", "Likes": "Reactions", "Replies": "Comments", "Reposts": "Shares"
        }, ["Engagements"], start_date, end_date),

        "X French": lambda df: process_platform(df, "X French", {
            "Date": "Date", "Texte du post": "Post text", "Lien": "Link", "Impressions": "Impressions",
            "Engagements": "Engagements", "J'aime": "Reactions", "Réponses": "Comments", "Reposts": "Shares"
        }, ["Engagements"], start_date, end_date),

        "Facebook": lambda df: process_platform(df, "Facebook", {
            "Publish time|Heure de publication": "Date", "Title|Titre": "Post text", "Permalink|Permalien": "Link", 
            "Reach|Couverture": "Impressions", "Reactions|Réactions": "Reactions", "Comments|Commentaires": "Comments", 
            "Shares|Partages": "Shares"
        }, ["Reactions", "Comments", "Shares"], start_date, end_date),

        "Instagram": lambda df: process_platform(df, "Instagram", {
            "Publish time|Heure de publication": "Date", "Description": "Post text", "Permalink|Permalien": "Link", 
            "Reach|Couverture": "Impressions", "Likes|Mentions J’aime": "Reactions", "Shares|Partages": "Shares", 
            "Follows|Followers en plus": "Follows", "Comments|Commentaires": "Comments", "Saves|Enregistrements": "Saves"
        }, ["Reactions", "Shares", "Follows", "Comments", "Saves"], start_date, end_date),

        "LinkedIn": lambda df: process_platform(df, "LinkedIn", {
            "Created date": "Date", "Post title": "Post text", "Post link": "Link", "Impressions": "Impressions",
            "Clicks": "Clicks", "Likes": "Reactions", "Comments": "Comments", "Reposts": "Shares", "Follows": "Follows"
        }, ["Clicks", "Reactions", "Comments", "Shares", "Follows"], start_date, end_date)
    }

    platform_dfs = {}

    for platform in processing_functions:
        uploaded_file = st.file_uploader(f'Upload file for {platform}', type=['csv', 'xls', 'xlsx'], key=platform)
        if uploaded_file:
            df = read_file(uploaded_file, platform=platform)
            if df is not None:
                platform_df = processing_functions[platform](df)
                platform_dfs[platform] = platform_df
                st.write(f"Top 3 Posts for {platform}")
                st.dataframe(platform_df)
                st.markdown('---')

    # ✅ FIXED INDENTATION ISSUE HERE
    if platform_dfs:
        combined_df = pd.concat(platform_dfs.values(), ignore_index=True)
        st.write("### Combined Top Posts Report")
        st.dataframe(combined_df)

        combined_df.to_excel("final_social_report.xlsx", index=False)
        with open("final_social_report.xlsx", "rb") as f:
            st.download_button("Download Excel Report", f, "Social_Media_Report.xlsx")

        # Extract the links from the final report
        post_links = combined_df["Link"].dropna().unique()

        # Display the "Open Tabs" button
        if st.button("Open Tabs"):
            st.markdown("### Click below to open each post:")
            for link in post_links:
                st.markdown(f"- [Open Post]({link})", unsafe_allow_html=True)

    else:
        st.info("Please upload files for each platform to generate the report.")

if st.session_state.page == "Contact":
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("<h2>Contact Us</h2><p>For inquiries, reach out to:</p><p><strong>Email:</strong> <a href='mailto:adrian.vasuveluppillai@un.org'>adrian.vasuveluppillai@un.org</a></p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<!-- Dialogflow Messenger -->
<script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
<df-messenger
  intent="WELCOME"
  chat-title="ATGtest01"
  agent-id="0001190c-56d5-4596-8075-b0322e6c9322"
  language-code="en">
</df-messenger>

<style>
  df-messenger {
    z-index: 999;
    position: fixed;
    bottom: 16px;
    right: 16px;
  }
</style>
""", unsafe_allow_html=True)

