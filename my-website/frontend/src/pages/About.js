import React, { useEffect, useState } from "react";

function dedupeDescription(description) {
  if (!description) return "";
  const lines = description.split('\n');
  const seenLines = new Set();
  const seenPhraseSets = new Set(); // To dedupe lines with the same phrases even if no prefix
  const resultLines = [];

  // Helper to normalize phrase sets for comparison
  function phrasesKey(str) {
    return str
      .split(/,|\u00b7/)
      .map(s => s.trim())
      .filter(Boolean)
      .join('|'); // Order matters, if you want order-independent, use sort()
  }

  for (let line of lines) {
    const trimmedLine = line.trim();
    if (!trimmedLine) continue;

    // If line is already seen exactly, skip
    if (seenLines.has(trimmedLine)) continue;

    // Check for "prefix: ..." lines
    const match = trimmedLine.match(/^([^:]+:)(.*)$/);
    let phrasePart = "";
    let prefix = "";
    if (match) {
      prefix = match[1].trim();
      phrasePart = match[2].trim();
    } else {
      phrasePart = trimmedLine;
    }

    // If line is "Skills: ...." or just "...." with list of skills, dedupe based on phrases!
    if (phrasePart.includes('\u00b7') || phrasePart.includes(',')) {
      const key = phrasesKey(phrasePart);
      if (seenPhraseSets.has(key)) continue;
      seenPhraseSets.add(key);

      // Remove duplicate phrases within this line
      let phrases = phrasePart.split(/,|\u00b7/).map(p => p.trim()).filter(Boolean);
      const seenPhrases = new Set();
      phrases = phrases.filter(p => {
        if (seenPhrases.has(p)) return false;
        seenPhrases.add(p);
        return true;
      });
      const sep = phrasePart.includes('\u00b7') ? ' · ' : ', ';
      resultLines.push((prefix ? (prefix + " ") : "") + phrases.join(sep));
    } else {
      // If not a phrase list, just dedupe as a line
      resultLines.push(trimmedLine);
    }
    seenLines.add(trimmedLine);
  }

  return resultLines.join('\n');
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
        <li>Exploring new cafes and restaurants in {linkedinInfo ? getCity(linkedinInfo.location) : "my city"}</li>
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

