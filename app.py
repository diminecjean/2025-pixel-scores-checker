import streamlit as st
import json
import pandas as pd

# Constants
SCORE_CRITERIA = [
    ("content_clarity", "Content Clarity (10%)"),
    ("impact_benefit", "Impact & Benefit (10%)"),
    ("innovation_creativity", "Innovation Creativity (5%)"),
    ("innovativeness", "Innovativeness (10%)"),
    ("practicality", "Practicality (5%)"),
    ("presentation", "Presentation (5%)"),
    ("problem_statement", "Problem Statement (10%)"),
    ("solution", "Solution (35%)"),
    ("entrepreneurship", "Entrepreneurship (10%)")
]

@st.cache_data
def load_data():
    """Load JSON data from responses.json"""
    with open('responses.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_score_value(record, field, default=0):
    """Safely get score value from record"""
    return record.get(field, default) or default

def calculate_total_score(record):
    """Calculate total score for a record"""
    return sum(get_score_value(record, field) for field, _ in SCORE_CRITERIA)

def get_metadata_info(record):
    """Extract metadata information from record"""
    return {
        'project_name': record['project_name'][0],
        'project_year': record.get('project_year', [''])[0],
        'major': record.get('project_major', [''])[0],
        'sdg': record.get('sdg', [''])[0],
        'judge': f"{record.get('judge_salutation', [''])[0]} {record.get('judge_name', [''])[0]}",
        'evaluation_id': record.get('evaluation_id')
    }

def render_metadata(metadata):
    """Render metadata section"""
    st.markdown(f"**Project Year:** {metadata['project_year']}")
    st.markdown(f"**Major:** {metadata['major']}")
    st.markdown(f"**SDG:** {metadata['sdg']}")
    st.markdown(f"**Judge:** {metadata['judge']}")
    st.markdown(f"**Evaluation ID:** {metadata['evaluation_id']}")

def create_score_dataframe(record, include_total=True):
    """Create a dataframe with scores for a single record"""
    criteria_names = [name for _, name in SCORE_CRITERIA]
    scores = [get_score_value(record, field) for field, _ in SCORE_CRITERIA]
    
    if include_total:
        criteria_names.append("Total Score (100%)")
        total = calculate_total_score(record)
        scores.append(total if total else 'N/A')
    
    return pd.DataFrame({
        "Criteria": criteria_names,
        "Score": scores
    })

def render_record(record):
    """Render a single evaluation record"""
    metadata = get_metadata_info(record)
    st.subheader(metadata['project_name'])
    
    # Metadata information
    render_metadata(metadata)
    
    # Comments
    st.markdown("### 📝 Comments")
    st.markdown(record['comments'])

    # Evaluation Scores
    st.markdown("### 📊 Evaluation Scores")
    score_df = create_score_dataframe(record)
    st.table(score_df)
    
    st.markdown("---")

def combine_scores_table(records):
    """Combine scores from multiple records into a single table"""
    criteria_names = [name for _, name in SCORE_CRITERIA] + ["Total Score (100%)"]
    
    # Create the base dataframe with criteria
    combined_data = {"Criteria": criteria_names}
    
    # Add scores for each judge
    for idx, record in enumerate(records, 1):
        judge_name = f"Judge {idx}"
        scores = [get_score_value(record, field) for field, _ in SCORE_CRITERIA]
        scores.append(calculate_total_score(record))
        combined_data[judge_name] = scores
    
    # Calculate average scores if multiple judges
    score_columns = [col for col in combined_data.keys() if col != "Criteria"]
    if len(score_columns) > 1:
        combined_data["Average"] = []
        for row_idx in range(len(criteria_names)):
            scores = [combined_data[col][row_idx] for col in score_columns]
            avg_score = sum(scores) / len(scores)
            combined_data["Average"].append(round(avg_score, 2))
    
    return pd.DataFrame(combined_data)

def search_projects(data, search_term):
    """Search for projects by name"""
    search_term_lower = search_term.lower()
    return [
        record for record in data
        if any(search_term_lower in name.lower() for name in record.get("project_name", []))
    ]

def render_search_results(results):
    """Render search results"""
    # Display combined scores if exactly 3 results (complete project evaluation)
    if len(results) == 3:
        st.write("### 📊 Combined Evaluation Scores")
        combined_df = combine_scores_table(results)
        st.table(combined_df)
    
    st.write(f"### Found {len(results)} matching record(s)")
    
    # Display individual records in expandable sections
    for idx, record in enumerate(results, 1):
        metadata = get_metadata_info(record)
        with st.expander(f"{idx}. {metadata['project_name']}"):
            render_record(record)

# Streamlit app UI
st.title("Want to know how your FYP Pixel judges score your project?")
data = load_data()
search_term = st.text_input("Search by Project Name", "")

if search_term:
    search_term_lower = search_term.lower()
    # Filter matching projects
    results = search_projects(data, search_term_lower)
    render_search_results(results)
else:
    st.info("Enter a project name to begin searching.")
