import streamlit as st

_CSS = """
<style>
    .about-header { color: #004080; font-size: 2rem; font-weight: bold; margin-bottom: 20px; text-align: center; }
    .about-section { background-color: #f8f9fa; border-radius: 15px; padding: 25px; margin-bottom: 25px;
                     box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .profile-img { border-radius: 50%; width: 150px; height: 150px; object-fit: cover;
                   border: 4px solid #004080; display: block; }
    .section-title { color: #004080; font-size: 1.5rem; font-weight: bold; margin-bottom: 15px;
                     border-bottom: 2px solid #004080; padding-bottom: 8px; }
    .contact-info { background-color: #e9f7fe; padding: 15px; border-radius: 10px; margin-top: 10px; }
    .profile-container { display: flex; align-items: center; gap: 30px; margin-bottom: 20px; }
    .profile-text { flex: 1; }
    .github-btn { background-color: #333; color: white; padding: 8px 15px; border-radius: 5px;
                  text-decoration: none; display: inline-block; margin-top: 10px; font-weight: bold; }
    .github-btn:hover { background-color: #555; }
    @media (max-width: 768px) {
        .profile-container { flex-direction: column; text-align: center; }
        .profile-img { margin: 0 auto; }
    }
</style>
"""


def _section(html):
    st.markdown(f'<div class="about-section">{html}</div>', unsafe_allow_html=True)


def render(data):
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown('<h1 class="about-header">ℹ️ About</h1>', unsafe_allow_html=True)

    _section('''
    <div class="profile-container">
        <img src="https://media.licdn.com/dms/image/v2/D5603AQGH9FTKrbtsBQ/profile-displayphoto-shrink_200_200/B56ZavaEF2GgAc-/0/1746699569459?e=1752105600&v=beta&t=Ka2PPXH6ii9rMbIQ3WPfNO2meHi3T-Qb03xAfME1fZs" class="profile-img" alt="Ankita Chavan">
        <div class="profile-text">
            <h2 class="section-title">👩‍🔬 About the Author</h2>
            <p style="font-size: 1.1rem;"><strong>Ankita Chavan</strong></p>
            <p>Currently pursuing a Master's degree in Bioinformatics from DES (Deccan Education Society) Pune University, Pune.</p>
            <p>Passionate about computational drug discovery, cheminformatics, and developing bioinformatics tools to solve biological problems.</p>
            <p>This web application is part of my academic project under the guidance of Dr. Kushagra Kashyap.</p>
        </div>
    </div>''')

    _section("""
    <h2 class="section-title">🌐 About This Web Server</h2>
    <p>This web server provides advanced cheminformatics tools for:</p>
    <ul>
        <li>Molecular similarity searching using fingerprint techniques</li>
        <li>Compound database screening</li>
        <li>Molecular property calculation and visualization</li>
        <li>Drug discovery research support</li>
    </ul>
    <p>The application is built using:</p>
    <ul>
        <li>Python with RDKit for cheminformatics</li>
        <li>Streamlit for web interface</li>
        <li>Pandas for data handling</li>
    </ul>""")

    _section('''
    <div class="profile-container">
        <img src="https://media.licdn.com/dms/image/v2/D5603AQF9gsU7YBjWVg/profile-displayphoto-shrink_400_400/B56ZZI.WrdH0Ag-/0/1744981029051?e=1752105600&v=beta&t=F4QBDSEgjUvnBS00xPkKqPTLI0jQaMpYefaOzARY1Yg" class="profile-img" alt="Dr. Kushagra Kashyap">
        <div class="profile-text">
            <h2 class="section-title">👨‍🏫 About the Mentor</h2>
            <p style="font-size: 1.1rem;"><strong>Dr. Kushagra Kashyap</strong></p>
            <p>Assistant Professor at DES (Deccan Education Society) Pune University.</p>
            <p>Specializes in Bioinformatics and Cheminformatics, with research interests in computational drug discovery and molecular modeling.</p>
            <p>Provides guidance on bridging the gap between biological sciences and computational technologies.</p>
        </div>
    </div>''')

    _section("""
    <h2 class="section-title">🙏 Acknowledgement</h2>
    <p>I am deeply grateful to DES (Deccan Education Society) Pune University for providing the academic foundation and resources that made this project possible.</p>
    <p>My sincere thanks to Dr. Kushagra Kashyap for his expert guidance, mentorship, and invaluable insights in cheminformatics and computational drug discovery, which were instrumental in shaping this work.</p>
    <p>I also extend my appreciation to the Streamlit team for developing such an intuitive and powerful framework, which enabled the seamless creation of this interactive web application.</p>
    <p>Special thanks to the RDKit community for their open-source cheminformatics toolkit that forms the backbone of this application's molecular analysis capabilities.</p>
    <p>This work was supported by the Bioinformatics department at DES Pune University, whose infrastructure and academic environment fostered this research.</p>""")

    _section("""
    <h2 class="section-title">📬 Contact & Feedback</h2>
    <p>For any questions, suggestions, or feedback about this web application:</p>
    <div class="contact-info">
        <p><strong>📧 Email:</strong> 3522411012@despu.edu.in</p>
        <p><strong>🔗 LinkedIn:</strong> <a href="https://www.linkedin.com/in/ankita-chavan-408709226" target="_blank">Ankita Chavan's Profile</a></p>
        <p><strong>💻 Source Code:</strong>
            <a href="https://github.com/AnkitaSchavan/DrugD/edit/main/p1.py" target="_blank" class="github-btn">View on GitHub</a>
        </p>
    </div>
    <p style="margin-top: 15px; font-style: italic;">Your feedback helps improve this tool for the research community!</p>""")
