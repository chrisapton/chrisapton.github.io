import React, { useEffect, useState } from 'react';

// Utility to split backend bullet string into array
function parseBullets(desc) {
  if (!desc) return [];
  return desc
    .split('\u2022')
    .map(s => s.trim())
    .filter(Boolean);
}

const styles = {
  section: {
    marginBottom: '30px',
    borderBottom: '1px solid #ccc',
    paddingBottom: '20px',
  },
  sectionTitle: {
    fontSize: '2.6em',
    color: '#222',
    marginBottom: '10px',
    marginTop: '0px'
  },
  certSectionTitle: {
    fontSize: '1.7em',
    color: '#222',
    marginBottom: '12px',
    marginTop: '32px',
  },
  list: {
    listStyleType: 'none',
    paddingLeft: '0',
  },
  listItem: {
    marginBottom: '24px',
    fontSize: '1rem',
    lineHeight: '1.5',
  },
  date: {
    color: '#888',
    fontSize: '0.98rem',
  },
  link: {
    color: '#0072b1',
    textDecoration: 'none',
    fontWeight: 500,
  },
  innerList: {
    listStyleType: 'disc',
    marginTop: '10px',
    marginLeft: '20px',
    paddingLeft: '20px',
    lineHeight: '1.6',
  },
  logo: {
    width: 32,
    height: 32,
    objectFit: "contain",
    verticalAlign: "middle",
    marginRight: 12,
    borderRadius: 6,
    background: "#fff",
    border: "1px solid #eee"
  },
  certLogo: {
    width: 28,
    height: 28,
    objectFit: "contain",
    verticalAlign: "middle",
    marginRight: 10,
    borderRadius: 6,
    background: "#fff",
    border: "1px solid #eee"
  },
  certCompany: {
    fontWeight: 500,
    color: "#555",
    marginLeft: 4,
    marginRight: 8
  },
  certSkills: {
    fontSize: "0.97em",
    color: "#555",
    marginTop: 3,
    display: "block"
  },
  certId: {
    fontSize: "0.92em",
    color: "#888",
    display: "block"
  }
};

const Experience = () => {
  const [experiences, setExperiences] = useState([]);
  const [certifications, setCertifications] = useState([]);
  const [loadingExp, setLoadingExp] = useState(true);
  const [loadingCert, setLoadingCert] = useState(true);

  // Fetch experiences
  useEffect(() => {
    fetch("https://chrisbackend.roundrobinstore.com/linkedin/experience")
      .then(res => res.json())
      .then(data => {
        setExperiences(data);
        setLoadingExp(false);
      })
      .catch(err => {
        console.error("Failed to fetch experiences:", err);
        setLoadingExp(false);
      });
  }, []);

  // Fetch certifications
  useEffect(() => {
    fetch("https://chrisbackend.roundrobinstore.com/linkedin/certifications")
      .then(res => res.json())
      .then(data => {
        setCertifications(data);
        setLoadingCert(false);
      })
      .catch(err => {
        console.error("Failed to fetch certifications:", err);
        setLoadingCert(false);
      });
  }, []);

  return (
    <div style={{padding: "20px", fontFamily: 'Arial, sans-serif', background: "#ecf3fa" }}>
      <h1 style={styles.sectionTitle}>Experience</h1>
      <section style={{ ...styles.section, borderBottom: 'none', paddingBottom: 0 }}>
        <ul style={styles.list}>
          {loadingExp ? (
            <li>Loading experiences...</li>
          ) : (
            experiences.map((exp, idx) => (
              <li key={idx} style={styles.listItem}>
                {/* Company logo and name */}
                <div style={{ display: 'flex', alignItems: 'center', flexWrap: "wrap" }}>
                  {exp.logo_url && (
                    <img src={exp.logo_url} alt={exp.company} style={styles.logo} />
                  )}
                  <div>
                    <strong>
                      {exp.company_url ? (
                        <a
                          href={exp.company_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={styles.link}
                        >
                          {exp.company}
                        </a>
                      ) : (
                        exp.company
                      )}
                    </strong>
                    {exp.location ? `, ${exp.location}` : ""}
                    {" | "}
                    <em>{exp.title}</em>
                  </div>
                </div>
                {/* Dates */}
                <div style={styles.date}>
                  {exp.dates}
                </div>
                {/* Description as bullet points */}
                <ul style={styles.innerList}>
                  {parseBullets(exp.description).map((point, i) => (
                    <li key={i}>{point}</li>
                  ))}
                </ul>
              </li>
            ))
          )}
        </ul>
      </section>

      {/* Certifications Section */}
      <section style={{ ...styles.section, borderBottom: 'none', paddingBottom: 0 }}>
        <h2 style={styles.certSectionTitle}>Certifications</h2>
        <ul style={styles.list}>
          {loadingCert ? (
            <li>Loading certifications...</li>
          ) : (
            certifications.map((cert, idx) => (
              <li key={idx} style={styles.listItem}>
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: 2 }}>
                  {cert.company_image_url && (
                    <img src={cert.company_image_url} alt={cert.company} style={styles.certLogo} />
                  )}
                  <span style={styles.certCompany}>{cert.company}</span>
                  <span style={{ fontWeight: 600 }}>{cert.name}</span>
                </div>
                <div style={styles.date}>
                  {cert.date_issued}
                  {cert.credential_url && (
                    <>
                      {" | "}
                      <a
                        href={cert.credential_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={styles.link}
                      >
                        View Credential
                      </a>
                    </>
                  )}
                </div>
                {cert.credential_id && (
                  <span style={styles.certId}>Credential ID: {cert.credential_id}</span>
                )}
                {cert.skills && cert.skills.length > 0 && (
                  <span style={styles.certSkills}>
                    <strong>Skills:</strong> {cert.skills.join(", ").replace(/·/g, "·")}
                  </span>
                )}
              </li>
            ))
          )}
        </ul>
      </section>
    </div>
  );
};

export default Experience;
