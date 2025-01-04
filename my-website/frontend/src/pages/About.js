import React from 'react';

const About = () => {
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

      {/* Education and Hobbies with Image */}
      <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'flex-start', justifyContent: 'space-between', gap: '20px' }}>
        {/* Left Section - Education and Hobbies */}
        <div style={{ flex: '1', minWidth: '300px', maxWidth: '600px' }}>
          <section style={{ marginBottom: '30px' }}>
            <h2 style={{ fontSize: '1.5em', color: '#444' }}>Education</h2>
            <ul style={{ listStyleType: 'none', paddingLeft: '0' }}>
              <li style={{ marginBottom: '15px' }}>
                <strong>University of Southern California (USC)</strong>, Los Angeles, CA
                <br />
                MS, Applied Data Science (Expected May 2025), GPA: 3.8
              </li>
              <li>
                <strong>University of California, Los Angeles (UCLA)</strong>, Los Angeles, CA
                <br />
                BS, Data Theory (Mathematics, Statistics, & Data Science) with a minor in Bioinformatics, GPA: 3.7
              </li>
            </ul>
          </section>

          <section>
            <h2 style={{ fontSize: '1.5em', color: '#444' }}>Hobbies</h2>
            <p>When I’m not working with data, I enjoy:</p>
            <ul>
              <li>Rock climbing at local gyms and outdoor climbing spots</li>
              <li>Exploring new cafes and restaurants in Los Angeles</li>
              <li>Participating in hackathons to build innovative solutions</li>
            </ul>
          </section>
        </div>

        {/* Right Section - Climbing Image */}
        <div style={{ flex: '0 0 300px', marginLeft: '-300px', position: 'relative', textAlign: 'center' }}>
          <img 
            src="climbing_image.jpg" 
            alt="Climbing Image" 
            style={{ 
              width: '100%', 
              height: 'auto', 
              maxWidth: '300px', 
              borderRadius: '10px', 
              objectFit: 'cover', 
              transform: 'translateX(-300px)',
              boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)'
            }} 
          />
        </div>
      </div>

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

        <p>
          You can also download my resume <a href="/resume.pdf" target="_blank" rel="noopener noreferrer" 
          style={{ color: '#007bff', textDecoration: 'none', fontWeight: 'bold' }}> here</a>.
        </p>
    
      </section>
    </div>
  );
};

export default About;

