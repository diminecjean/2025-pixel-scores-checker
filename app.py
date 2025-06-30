import streamlit as st
import json
import pandas as pd

# Load your JSON data
@st.cache_data
def load_data():
    with open('responses.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

def render_record(record):
    st.subheader(record['project_name'][0])

    # Metadata information
    st.markdown(f"**Project Year:** {record.get('project_year', [''])[0]}")
    st.markdown(f"**Major:** {record.get('project_major', [''])[0]}")
    st.markdown(f"**SDG:** {record.get('sdg', [''])[0]}")
    
    # Judge information
    st.markdown(f"**Judge:** {record.get('judge_salutation', [''])[0]} {record.get('judge_name', [''])[0]}")
    st.markdown(f"**Evaluation ID:** {record.get('evaluation_id')}")

    st.markdown("### 📝 Comments")
    st.markdown(record['comments'])



    st.markdown("### 📊 Evaluation Scores")
    total_score = record.get('content_clarity') + record.get('impact_benefit') + record.get('innovation_creativity') + record.get('innovativeness') + record.get('practicality') + record.get('presentation') + record.get('problem_statement') + record.get('solution') + record.get('entrepreneurship')
    # Display scores in a table
    score_data = {
        "Criteria": [
            "Content Clarity (10%)",
            "Impact & Benefit (10%)", 
            "Innovation Creativity (5%)", 
            "Innovativeness (10%)", 
            "Practicality (5%)", 
            "Presentation (5%)", 
            "Problem Statement (10%)", 
            "Solution (35%)", 
            "Entrepreneurship (10%)",
            "Total Score (100%)"
        ],
        "Score": [
            f"{record.get('content_clarity')}",
            f"{record.get('impact_benefit')}",
            f"{record.get('innovation_creativity')}",
            f"{record.get('innovativeness')}",
            f"{record.get('practicality')}",
            f"{record.get('presentation')}",
            f"{record.get('problem_statement')}",
            f"{record.get('solution')}",
            f"{record.get('entrepreneurship')}",
            f"{total_score if total_score else 'N/A'}"
        ]
    }
    
    # Create and display the table
    score_df = pd.DataFrame(score_data)
    st.table(score_df)

    st.markdown("---")


# Streamlit app UI
st.title("Want to know how your FYP Pixel judges score your project?")
search_term = st.text_input("Search by Project Name", "")

if search_term:
    search_term_lower = search_term.lower()
    # Filter matching projects
    results = [
        record for record in data
        if any(search_term_lower in name.lower() for name in record.get("project_name", []))
    ]

    st.write(f"### Found {len(results)} matching record(s)")

    for idx, record in enumerate(results, 1):
        with st.expander(f"{idx}. {record['project_name'][0]}"):
            render_record(record)
else:
    st.info("Enter a project name to begin searching.")
