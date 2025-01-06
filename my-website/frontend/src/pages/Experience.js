import React from 'react';

const Experience = () => {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Experience</h1>
      
      {/* Work Experience Section */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>Work Experience</h2>
        <ul style={styles.list}>
          <li style={styles.listItem}>
            <strong>Voya Financial</strong>, New York, NY | <em>Data Science Intern</em>  
            <br />
            <span style={styles.date}>May 2024 - Aug 2024</span>
            <ul style={styles.innerList}>
              <li>
                Created a Data Quality Checker app using Python, SQL, and Snowflake, which ran on a daily basis to provide developers 24/7 business validations on financial data and identify outliers for review.
              </li>
              <li>
                Developed 44 data-driven tests, including one leveraging linear regression to establish a 99% prediction interval for identifying outliers.
              </li>
              <li>
                Conducted in-depth data analysis on portfolio data using Power BI and Python, investigating anomalies.
              </li>
              <li>
                Completed three different certification courses on data modeling for Snowflake data analysis and Datavault 2.0.
              </li>
            </ul>
          </li>
          <li style={styles.listItem}>
            <strong>Public Editor</strong>, Berkeley, CA | <em>Software Developer</em>  
            <br />
            <span style={styles.date}>Mar 2020 - May 2021</span>
            <ul style={styles.innerList}>
              <li>
                Managed the Article Funnel system using Python, Java, SQL, JavaScript, and Angular.
              </li>
              <li>
                Enhanced user experience by transitioning from client-side to server-side pagination, significantly reducing user load as article volume increased.
              </li>
            </ul>
          </li>
        </ul>
      </section>



      {/* Research Experience Section */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>Research Experience</h2>
        <ul style={styles.list}>
          <li style={styles.listItem}>
            <strong>Herman Ostrow School of Dentistry of USC</strong>, Los Angeles, CA | <em>Data Science Research Assistant</em>
            <br />
            <span style={styles.date}>Mar 2024 - Sep 2024</span>
            <ul style={styles.innerList}>
              <li>
                Designed code that manipulates data from patient 3D scans to be compatible with a pre-trained LLM model that segments teeth.
              </li>
              <li>
                Presented data biweekly to a research group specializing in AI and Orthodontics.
              </li>
            </ul>
          </li>
          <li style={styles.listItem}>
            <strong>USC Sol Price School of Public Policy</strong>, Los Angeles, CA | <em>Graduate Researcher</em>
            <br />
            <span style={styles.date}>Jan 2024 - Sep 2024</span>
            <ul style={styles.innerList}>
              <li>
                Leveraged LLMs to classify AI's effects on various government job roles at the local, state, and federal levels.
              </li>
              <li>
                Scraped and cleaned federal job data from PDF files for analysis using pre-trained models.
              </li>
            </ul>
          </li>
          <li style={styles.listItem}>
            <strong>University of California, Los Angeles (UCLA)</strong>, Los Angeles, CA | <em>Directed Research</em>
            <br />
            <span style={styles.date}>Jan 2022 - Jun 2023</span>
            <ul style={styles.innerList}>
              <li>
                Performed independent research on time series techniques, bootstrapping, and using LSTMs with time series under the guidance of Professor Michael Tsiang.
              </li>
              <li>
                Presented findings at UCLA’s undergraduate research event.
              </li>
            </ul>
          </li>
        </ul>
      </section>


      {/* Certifications Section */}
      <section style={styles.section}>
  <h2 style={styles.sectionTitle}>Certifications</h2>
  <ul style={styles.list}>
    <li style={styles.listItem}>
      <strong>Hands-On Essentials: Data Warehousing Workshop</strong>  
      <br />
      <span style={styles.date}>Issued Jun 2024</span> | <em>Snowflake</em>
      <br />
      <span>Credential ID: 6d673959-9159-42c5-a74f-dd3be309ea12</span>
      <br />
      <strong>Skills:</strong> Snowflake · Snowflake Cloud
    </li>

    <li style={styles.listItem}>
      <strong>Introduction to Data Modeling in Snowflake</strong>  
      <br />
      <span style={styles.date}>Issued Jun 2024</span> | <em>DataCamp</em>
      <br />
      <span>Credential ID: 663c40fda372669f8e0f6bb405096176c8ec8902</span>
      <br />
      <strong>Skills:</strong> Snowflake · Data Modeling
    </li>

    <li style={styles.listItem}>
      <strong>Modeling Data Warehouse with Data Vault 2.0</strong>  
      <br />
      <span style={styles.date}>Issued Jun 2024</span> | <em>Udemy</em>
      <br />
      <span>Credential ID: UC-9f47488d-1e83-405d-805a-7f669ab3476e</span>
      <br />
      <strong>Skills:</strong> Data Vault
    </li>

    <li style={styles.listItem}>
      <strong>Improving Deep Neural Networks: Hyperparameter Tuning, Regularization and Optimization</strong>  
      <br />
      <span style={styles.date}>Issued Dec 2023</span> | <em>Coursera</em>
      <br />
      <span>Credential ID: UKKP7ZGYMEAG</span>
      <br />
      <strong>Skills:</strong> Neural Networks
    </li>

    <li style={styles.listItem}>
      <strong>Neural Networks and Deep Learning</strong>  
      <br />
      <span style={styles.date}>Issued Dec 2023</span> | <em>Coursera</em>
      <br />
      <span>Credential ID: HJ6FDYZENHYC</span>
      <br />
      <strong>Skills:</strong> Deep Learning
    </li>

    <li style={styles.listItem}>
      <strong>Structuring Machine Learning Projects</strong>  
      <br />
      <span style={styles.date}>Issued Dec 2023</span> | <em>Coursera</em>
      <br />
      <span>Credential ID: JBL7RY43EW7N</span>
      <br />
      <strong>Skills:</strong> Machine Learning
    </li>

    <li style={styles.listItem}>
      <strong>Machine Learning Scientist with Python</strong>  
      <br />
      <span style={styles.date}>Issued Oct 2023</span> | <em>DataCamp</em>
      <br />
      <span>Credential ID: 7fb970bc9bf9fac807de002388dafeef1217b894</span>
      <br />
      <strong>Skills:</strong> Machine Learning
    </li>

    <li style={styles.listItem}>
      <strong>Data Scientist Professional with Python</strong>  
      <br />
      <span style={styles.date}>Issued Sep 2023</span> | <em>DataCamp</em>
      <br />
      <span>Credential ID: 915f8400ffb6d255a00cb26487818742c6bc9b2b</span>
      <br />
      <strong>Skills:</strong> Data Science
    </li>

    <li style={styles.listItem}>
      <strong>Data Scientist with Python</strong>  
      <br />
      <span style={styles.date}>Issued Jan 2023</span> | <em>DataCamp</em>
      <br />
      <span>Credential ID: 96794e622b015afeea347f160d6a33bdf49e838f</span>
      <br />
      <strong>Skills:</strong> Data Science
    </li>
  </ul>
</section>

    </div>
  );
};

// CSS-in-JS Styles
const styles = {
  section: {
    marginBottom: '30px',
    borderBottom: '1px solid #ccc',
    paddingBottom: '20px',
  },
  sectionTitle: {
    fontSize: '1.5em',
    color: '#444',
    marginBottom: '10px',
  },
  list: {
    listStyleType: 'none',
    paddingLeft: '0',
  },
  listItem: {
    marginBottom: '15px',
    fontSize: '1rem',
    lineHeight: '1.5',
  },
  date: {
    color: '#888',
    fontSize: '0.9rem',
  },
  link: {
    color: '#007bff',
    textDecoration: 'none',
  },
  innerList: {
    listStyleType: 'disc', // Bullet points for inner list
    marginTop: '10px',
    marginLeft: '20px', // Indent for nested lists
    paddingLeft: '20px',
    lineHeight: '1.6', // Add spacing between lines
  },
};

export default Experience;
