import requests
import streamlit as st
from xml.etree import ElementTree
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils.constant import (SMTP_SERVER_ADDRESS, PORT, SENDER_PASSWORD, SENDER_ADDRESS)
import datetime

from utils.helper import send_email

# List of arXiv categories and their full names
categories = {
    "cs.AI": "Artificial Intelligence",
    "cs.AR": "Hardware Architecture",
    "cs.CC": "Computational Complexity",
    "cs.CE": "Computational Engineering, Finance, and Science",
    "cs.CG": "Computational Geometry",
    "cs.CL": "Computation and Language (Natural Language Processing)",
    "cs.CR": "Cryptography and Security",
    "cs.CV": "Computer Vision and Pattern Recognition",
    "cs.CY": "Computers and Society",
    "cs.DB": "Databases",
    "cs.DC": "Distributed, Parallel, and Cluster Computing",
    "cs.DL": "Digital Libraries",
    "cs.DM": "Discrete Mathematics",
    "cs.DS": "Data Structures and Algorithms",
    "cs.ET": "Emerging Technologies",
    "cs.FL": "Formal Languages and Automata Theory",
    "cs.GL": "General Literature",
    "cs.GR": "Graphics",
    "cs.GT": "Computer Science and Game Theory",
    "cs.HC": "Human-Computer Interaction",
    "cs.IR": "Information Retrieval",
    "cs.IT": "Information Theory",
    "cs.LG": "Machine Learning",
    "cs.LO": "Logic in Computer Science",
    "cs.MA": "Multiagent Systems",
    "cs.MM": "Multimedia",
    "cs.MS": "Mathematical Software",
    "cs.NA": "Numerical Analysis",
    "cs.NE": "Neural and Evolutionary Computing",
    "cs.NI": "Networking and Internet Architecture",
    "cs.OH": "Other Computer Science",
    "cs.OS": "Operating Systems",
    "cs.PF": "Performance",
    "cs.PL": "Programming Languages",
    "cs.RO": "Robotics",
    "cs.SC": "Symbolic Computation",
    "cs.SD": "Sound",
    "cs.SE": "Software Engineering",
    "cs.SI": "Social and Information Networks",
    "cs.SY": "Systems and Control",
    # Economics
    "econ.EM": "Econometrics",
    "econ.GN": "General Economics",
    "econ.TH": "Theoretical Economics",
    # Electrical Engineering and Systems Science
    "eess.AS": "Audio and Speech Processing",
    "eess.IV": "Image and Video Processing",
    "eess.SP": "Signal Processing",
    "eess.SY": "Systems and Control",
    # Mathematics
    "math.AC": "Commutative Algebra",
    "math.AG": "Algebraic Geometry",
    "math.AP": "Analysis of PDEs",
    "math.AT": "Algebraic Topology",
    "math.CA": "Classical Analysis and ODEs",
    "math.CO": "Combinatorics",
    "math.CT": "Category Theory",
    "math.CV": "Complex Variables",
    "math.DG": "Differential Geometry",
    "math.DS": "Dynamical Systems",
    "math.FA": "Functional Analysis",
    "math.GM": "General Mathematics",
    "math.GN": "General Topology",
    "math.GR": "Group Theory",
    "math.GT": "Geometric Topology",
    "math.HO": "History and Overview",
    "math.IT": "Information Theory",
    "math.KT": "K-Theory and Homology",
    "math.LO": "Logic",
    "math.MG": "Metric Geometry",
    "math.MP": "Mathematical Physics",
    "math.NA": "Numerical Analysis",
    "math.NT": "Number Theory",
    "math.OA": "Operator Algebras",
    "math.OC": "Optimization and Control",
    "math.PR": "Probability",
    "math.QA": "Quantum Algebra",
    "math.RA": "Rings and Algebras",
    "math.RT": "Representation Theory",
    "math.SG": "Symplectic Geometry",
    "math.SP": "Spectral Theory",
    "math.ST": "Statistics Theory",
    # Physics
    "astro-ph.CO": "Cosmology and Nongalactic Astrophysics",
    "astro-ph.EP": "Earth and Planetary Astrophysics",
    "astro-ph.GA": "Astrophysics of Galaxies",
    "astro-ph.HE": "High Energy Astrophysical Phenomena",
    "astro-ph.IM": "Instrumentation and Methods for Astrophysics",
    "astro-ph.SR": "Solar and Stellar Astrophysics",
    "cond-mat.dis-nn": "Disordered Systems and Neural Networks",
    "cond-mat.mes-hall": "Mesoscale and Nanoscale Physics",
    "cond-mat.mtrl-sci": "Materials Science",
    "cond-mat.other": "Other Condensed Matter",
    "cond-mat.quant-gas": "Quantum Gases",
    "cond-mat.soft": "Soft Condensed Matter",
    "cond-mat.stat-mech": "Statistical Mechanics",
    "cond-mat.str-el": "Strongly Correlated Electrons",
    "cond-mat.supr-con": "Superconductivity",
    "gr-qc": "General Relativity and Quantum Cosmology",
    "hep-ex": "High Energy Physics - Experiment",
    "hep-lat": "High Energy Physics - Lattice",
    "hep-ph": "High Energy Physics - Phenomenology",
    "hep-th": "High Energy Physics - Theory",
    "math-ph": "Mathematical Physics",
    "nlin.AO": "Adaptation and Self-Organizing Systems",
    "nlin.CD": "Chaotic Dynamics",
    "nlin.CG": "Cellular Automata and Lattice Gases",
    "nlin.PS": "Pattern Formation and Solitons",
    "nlin.SI": "Exactly Solvable and Integrable Systems",
    "nucl-ex": "Nuclear Experiment",
    "nucl-th": "Nuclear Theory",
    "physics.acc-ph": "Accelerator Physics",
    "physics.ao-ph": "Atmospheric and Oceanic Physics",
    "physics.app-ph": "Applied Physics",
    "physics.atm-clus": "Atomic and Molecular Clusters",
    "physics.atom-ph": "Atomic Physics",
    "physics.bio-ph": "Biological Physics",
    "physics.chem-ph": "Chemical Physics",
    "physics.class-ph": "Classical Physics",
    "physics.comp-ph": "Computational Physics",
    "physics.data-an": "Data Analysis, Statistics and Probability",
    "physics.ed-ph": "Physics Education",
    "physics.flu-dyn": "Fluid Dynamics",
    "physics.gen-ph": "General Physics",
    "physics.geo-ph": "Geophysics",
    "physics.hist-ph": "History and Philosophy of Physics",
    "physics.ins-det": "Instrumentation and Detectors",
    "physics.med-ph": "Medical Physics",
    "physics.optics": "Optics",
    "physics.plasm-ph": "Plasma Physics",
    "physics.pop-ph": "Popular Physics",
    "physics.soc-ph": "Physics and Society",
    "physics.space-ph": "Space Physics",
    "quant-ph": "Quantum Physics",
    # Quantitative Biology
    "q-bio.BM": "Biomolecules",
    "q-bio.CB": "Cell Behavior",
    "q-bio.GN": "Genomics",
    "q-bio.MN": "Molecular Networks",
    "q-bio.NC": "Neurons and Cognition",
    "q-bio.OT": "Other Quantitative Biology",
    "q-bio.PE": "Populations and Evolution",
    "q-bio.QM": "Quantitative Methods",
    "q-bio.SC": "Subcellular Processes",
    "q-bio.TO": "Tissues and Organs",
    # Quantitative Finance
    "q-fin.CP": "Computational Finance",
    "q-fin.EC": "Economics",
    "q-fin.GN": "General Finance",
    "q-fin.MF": "Mathematical Finance",
    "q-fin.PM": "Portfolio Management",
    "q-fin.PR": "Pricing of Securities",
    "q-fin.RM": "Risk Management",
    "q-fin.ST": "Statistical Finance",
    "q-fin.TR": "Trading and Market Microstructure",
    # Statistics
    "stat.AP": "Applications",
    "stat.CO": "Computation",
    "stat.ME": "Methodology",
    "stat.ML": "Machine Learning",
    "stat.OT": "Other Statistics",
    "stat.TH": "Statistics Theory",
}

env = Environment(
            loader=FileSystemLoader('./templates'),  # Set the path to your templates directory
            autoescape=select_autoescape(['html', 'xml'])
        )

def fetch_arxiv_papers(category, max_results=10):
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = f'cat:{category}'
    params = {
        'search_query': search_query,
        'max_results': max_results,
        'sortBy': 'lastUpdatedDate',
        'sortOrder': 'descending',
    }
 
    response = requests.get(base_url, params=params)
    return response.text

def extract_paper_information(xml_string):
    root = ElementTree.fromstring(xml_string)
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
        url = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
        papers.append({
            'title': title,
            'summary': summary,
            'url': url
        })
    return papers




def main():
    st.title('arXiv Paper Extractor')

    category = st.selectbox(
        "Select a research topic",
        list(categories.keys()),
        format_func=lambda x: categories[x]
    )

    if st.button('Fetch Papers'):
        with st.spinner('Fetching papers...'):
            xml_result = fetch_arxiv_papers(category)
            papers = extract_paper_information(xml_result)
            st.session_state.papers = papers  # Store papers in session_state
            st.success(f'Fetched top 10 papers on {categories[category]}!')
            st.subheader(f'Top 10 most recent papers on {categories[category]}')
            for i, paper in enumerate(papers, start=1):
                with st.expander(f"{i}. {paper['title']}"):
                    st.markdown(paper['summary'])

    # Once papers are fetched, show the input box and button to send email
    if 'papers' in st.session_state:
        with st.form(key='send_email_form'):
            recipient_email = st.text_input("Recipient Email", key='recipient_email_input')
            submit_button = st.form_submit_button(label='Send Email')
            if submit_button and recipient_email:
                st.success('Sending email...')
                # Render the email template
                template = env.get_template('email_template.html')
                email_message = template.render(subject = "Here is Your "+categories[category]+" Research Papers Summary !",
papers=st.session_state.papers, current_year=datetime.datetime.now().year)
                subject = "We Have Prepared The Research Papers Summary !"
                # Send the email
                try:
                    send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD,
                receiver=recipient_email, smtp_server=SMTP_SERVER_ADDRESS, smtp_port=PORT,
                email_message=email_message, subject=subject, attachment=False, is_html=True)
                    st.success('Email sent successfully!')
                except Exception as e:
                    st.error(f'An error occurred: {e}')

# Helper to clear the session state when needed
def clear_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Add a button to clear the fetched papers if necessary
st.button("Clear Papers", on_click=clear_state)

main()