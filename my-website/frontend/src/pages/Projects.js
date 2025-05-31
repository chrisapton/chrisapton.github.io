import React, { useEffect, useState } from "react";

const Projects = () => {
  const [projects, setProjects] = useState([]);

  // Fetch projects from the backend
  useEffect(() => {
    fetch("https://chrisbackend.roundrobinstore.com/repos")
      .then((response) => response.json())
      .then((data) => setProjects(data))
      .catch((error) => console.error("Error fetching projects:", error));
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Projects</h1>
      <p>Here are some of my projects:</p>
      <div>
        {projects.map((project, index) => (
          <div key={index} style={styles.projectCard}>
            <div style={styles.header}>
              <div style={styles.title}>
                {project.title}
                <a
                  href={project.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={styles.githubLink}
                >
                  <img
                    src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
                    alt="GitHub"
                    style={styles.githubLogo}
                  />
                </a>
              </div>
              <div style={styles.date}>
                {project.startDate
                  ? new Date(project.startDate).toLocaleDateString("en-US", { timeZone: "UTC" })
                  : "No Start Date"} -{" "}
                {project.ongoing
                  ? "Ongoing"
                  : project.endDate
                  ? new Date(project.endDate).toLocaleDateString("en-US", { timeZone: "UTC" })
                  : "No End Date"}
              </div>
            </div>
            <p style={styles.description}>{project.description}</p>

            {/* Render the demo dynamically based on demoType */}
            {project.demoType === "link" && (
              <a
                href={project.demoContent}
                target="_blank"
                rel="noopener noreferrer"
                style={styles.demoLink}
              >
                Link to Project
              </a>
            )}
            {project.demoType === "image" && (
              <img
                src={project.demoContent}
                alt={`${project.title} Demo`}
                style={styles.demoImage}
              />
            )}
            {project.demoType === "code" && (
              <pre style={styles.codeSnippet}>
                {project.demoContent}
              </pre>
            )}
            {project.demoType === "script" && (
              <p style={styles.script}>
                Run: <code>{project.demoContent}</code>
              </p>
            )}
            {!project.demoType && (
              <p style={styles.noDemo}></p>
            )}
            {/* Skills Section */}
            <div>
              <strong>Skills:</strong>{" "}
              {project.skills.map((skill, i) => (
                <span key={i} style={styles.skill}>
                  {skill}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  projectCard: {
    border: "1px solid #ccc",
    borderRadius: "8px",
    padding: "16px",
    margin: "16px 0",
    backgroundColor: "#f9f9f9",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "8px",
  },
  title: {
    fontWeight: "bold",
    fontSize: "1.2rem",
    display: "flex",
    alignItems: "center",
  },
  githubLink: {
    marginLeft: "8px",
  },
  githubLogo: {
    width: "20px",
    height: "20px",
  },
  date: {
    fontSize: "1rem",
    color: "#555",
    whiteSpace: "nowrap",
  },
  description: {
    margin: "0",
    fontSize: "1rem",
    color: "#333",
  },
  demoLink: {
    display: "block",
    marginTop: "10px",
    textDecoration: "none",
    color: "#007bff",
  },
  demoImage: {
    display: "block",
    marginTop: "10px",
    maxWidth: "100%",
    height: "auto",
    borderRadius: "8px",
  },
  codeSnippet: {
    backgroundColor: "#f4f4f4",
    padding: "10px",
    borderRadius: "5px",
    marginTop: "10px",
    fontFamily: "monospace",
  },
  script: {
    marginTop: "10px",
    fontFamily: "monospace",
  },
  skill: {
    display: "inline-block",
    marginRight: "8px",
    padding: "4px 8px",
    backgroundColor: "#007bff",
    color: "#fff",
    borderRadius: "4px",
    fontSize: "0.85rem",
  },
};

export default Projects;
