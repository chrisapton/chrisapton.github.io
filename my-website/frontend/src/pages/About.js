import React, { useEffect, useState } from "react";

function dedupeDescription(description) {
  if (!description) return "";
  // Split into lines, remove duplicate lines (preserving order)
  const seen = new Set();
  return description
    .split('\n')
    .filter(line => {
      if (seen.has(line.trim())) return false;
      seen.add(line.trim());
      return true;
    })
    .join('\n');
}

const getCity = (location) => {
  if (!location) return "";
  return location.split(",")[0].trim();
};

const About = () => {
  // State for LinkedIn info
  const [linkedinInfo, setLinkedinInfo] = useState(null);

  useEffect(() => {
    fetch("https://chrisbackend.roundrobinstore.com/linkedin/about")
      .then((res) => res.json())
      .then((data) => setLinkedinInfo(data))
      .catch((err) => {
        console.error("Failed to fetch LinkedIn info:", err);
      });
  }, []);

  const [education, setEducation] = useState([]);

  useEffect(() => {
    fetch("https://chrisbackend.roundrobinstore.com/linkedin/education")
      .then((res) => res.json())
      .then((data) => setEducation(data))
      .catch((err) => {
        console.error("Failed to fetch education data:", err);
      });
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif'}}>
      <h1>About Me</h1>
      
      <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', marginBottom: '30px' }}>
        {/* Left Section - Text */}
        <div style={{ flex: '1', minWidth: '300px', marginRight: '20px' }}>
          <h2 style={{ fontSize: '1.5em', color: '#444' }}>Hi, I'm Christopher Apton!</h2>
          <p>
            I am passionate about uncovering insights and solving complex problems through the power of data. My journey in 
             <strong> Data Science</strong> has equipped me with a strong foundation in programming, statistical modeling, 
            and machine learning, along with hands-on experience in tools like <strong>Python, R, SQL, and Power BI</strong>. 
            I enjoy exploring new technologies and applying creative solutions to real-world challenges. 

            I thrive on continuous learning, whether it’s mastering the latest data visualization techniques or experimenting with 
            cutting-edge machine learning algorithms. My curiosity drives me to explore how data can shape impactful decisions 
            and innovate in fields ranging from healthcare to finance.
          </p>

          <p>
            Outside of work and academics, I enjoy rock climbing, which has taught me perseverance, 
            creative problem-solving, and a love for adventure. When I'm not scaling walls, I spend time 
            working on machine learning models, participating in hackathons, and exploring how data can 
            be used to solve real-world problems.
          </p>
        </div>

        {/* Right Section - Image */}
        <div style={{ flex: '0 0 200px', textAlign: 'center' }}>
          <img 
            src="/pic_of_me.JPG" 
            alt="Christopher Apton" 
            style={{ borderRadius: '50%', width: '200px', height: '200px', objectFit: 'cover', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' }} 
          />
        </div>
      </div>

        <div style={{
          marginTop: '40px',
          padding: '24px',
          background: '#f5f6fa',
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
          width: '83%',
          maxWidth: '1300px'
        }}>
          <h2 style={{ color: '#0072b1', marginBottom: '16px' }}>
            LinkedIn Information
          </h2>
          {linkedinInfo ? (
            <div style={{ lineHeight: '1.7', color: '#333' }}>
              <div><strong>Location:</strong> {linkedinInfo.location}</div>
              <div style={{ margin: '10px 0' }}>
                <strong>About:</strong>
                <div style={{ whiteSpace: 'pre-line', marginLeft: '12px' }}>
                  {linkedinInfo.about}
                </div>
              </div>
              <div><strong>Last Company:</strong> {linkedinInfo.company}</div>
              <div><strong>Job Title:</strong> {linkedinInfo.jobTitle}</div>
              <div>
                <strong>Resume:</strong>{" "}
                <a
                  href={linkedinInfo.resume}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View PDF
                </a>
              </div>
              <section style={{ marginTop: '32px', marginBottom: '30px' }}>
                <h2 style={{ fontSize: '1.5em', color: '#444' }}>Education</h2>
                <ul style={{ listStyleType: 'none', paddingLeft: '0' }}>
                  {education.length === 0 ? (
                    <li>Loading education...</li>
                  ) : (
                    education.map((edu, idx) => (
                      <li key={idx} style={{ marginBottom: '15px', display: "flex", alignItems: "center" }}>
                        {edu.company_image_url && (
                          <img
                            src={edu.company_image_url}
                            alt={edu.institution_name + " logo"}
                            style={{ width: 40, height: 40, objectFit: "cover", borderRadius: "8px", marginRight: 16 }}
                          />
                        )}
                        <div>
                          <strong>
                            <a href={edu.linkedin_url} target="_blank" rel="noopener noreferrer" style={{ color: "#004080" }}>
                              {edu.institution_name}
                            </a>
                          </strong>
                          {edu.from_date || edu.to_date ? (
                            <span style={{ marginLeft: 8, color: "#666", fontSize: "0.95em" }}>
                              ({edu.from_date || "?"} – {edu.to_date || "?"})
                            </span>
                          ) : null}
                          <br />
                          {edu.degree}
                          {edu.description && (
                            <>
                              <br />
                              <span style={{ whiteSpace: "pre-line", fontSize: "0.95em", color: "#444" }}>
                                {dedupeDescription(edu.description)}
                              </span>
                            </>
                          )}
                        </div>
                      </li>
                    ))
                  )}
                </ul>
              </section>

            </div>
          ) : (
            <div>Loading LinkedIn information...</div>
          )}
        </div>


{/* Education and Hobbies with Image */}
<div 
  style={{ 
    display: 'flex', 
    flexWrap: 'wrap', 
    alignItems: 'flex-start', 
    justifyContent: 'space-between', 
    gap: '20px',
  }}
>
  {/* Left Section - Education and Hobbies */}
  <div style={{ flex: '1', minWidth: '300px', maxWidth: '600px' }}>

    <section>
      <h2 style={{ marginTop: '32px', fontSize: '1.5em', color: '#444' }}>Hobbies</h2>
      <p>When I’m not working with data, I enjoy:</p>
      <ul>
        <li>Rock climbing at local gyms and outdoor climbing spots</li>
        <li>Exploring new cafes and restaurants in {getCity(edu.location)}</li>
        <li>Participating in hackathons to build innovative solutions</li>
      </ul>
    </section>

    <section style={{ marginBottom: '30px' }}>
        <h2 style={{ fontSize: '1.5em', color: '#444' }}>Contact</h2>
        <p>
          Feel free to connect with me via:
        </p>
        <ul>
          <li><strong>Email:</strong> <a href="mailto:chrisapton@gmail.com">chrisapton@gmail.com</a></li>
          <li><strong>GitHub:</strong> <a href="https://github.com/chrisapton" target="_blank" rel="noopener noreferrer">chrisapton</a></li>
          <li><strong>LinkedIn:</strong> <a href="https://linkedin.com/in/chrisapton" target="_blank" rel="noopener noreferrer">chrisapton</a></li>
        </ul>   
      </section>
  </div>

  {/* Right Section - Climbing Image */}
  <div 
    style={{ 
      flex: '0 0 300px', 
      width: '100%', 
      maxWidth: '300px', 
      textAlign: 'center',
      margin: '0 auto',
      marginTop: '32px'
    }}
  >
    <img 
      src="climbing_image.jpg" 
      alt="Climbing Image" 
      style={{ 
        width: '100%', 
        height: 'auto', 
        borderRadius: '10px', 
        objectFit: 'cover', 
        boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
      }} 
    />
  </div>
</div>
    </div>
  );
};

export default About;

