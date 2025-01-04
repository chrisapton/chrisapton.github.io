import React, { useState } from 'react';

const Projects = () => {
  const [projects] = useState([
    {
      title: 'Portfolio Website',
      description: 'A personal portfolio website to showcase my work.',
      github: 'https://github.com/username/portfolio',
      startDate: '2023-01-01',
      endDate: '2023-12-15',
      ongoing: false,
    },
    {
      title: 'Task Manager App',
      description: 'A task management tool with drag-and-drop functionality.',
      github: 'https://github.com/username/task-manager',
      startDate: '2023-06-01',
      endDate: '2023-10-05',
      ongoing: false,
    },
    {
      title: 'Blog Platform',
      description: 'An ongoing project for a personal blog platform.',
      github: 'https://github.com/username/blog-platform',
      startDate: '2023-08-01',
      ongoing: true, // This project is ongoing
    },
  ]);

  // Sort projects: Ongoing projects at the top, then by end date (newest first)
  const sortedProjects = [...projects].sort((a, b) => {
    if (a.ongoing && !b.ongoing) return -1; // Ongoing projects come first
    if (!a.ongoing && b.ongoing) return 1;
    return new Date(b.endDate || '9999-12-31') - new Date(a.endDate || '9999-12-31'); // Sort by end date
  });

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif'}}>
      <h1>Projects</h1>
      <p>Here are my projects:</p>
      <div>
        {sortedProjects.map((project, index) => (
          <div key={index} style={styles.projectCard}>
            {/* Header section with title, GitHub link, and date range */}
            <div style={styles.header}>
              {/* Title and GitHub link */}
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
              {/* Date range */}
              <div style={styles.date}>
                {new Date(project.startDate).toLocaleDateString()} -{' '}
                {project.ongoing
                  ? 'Ongoing'
                  : new Date(project.endDate).toLocaleDateString()}
              </div>
            </div>
            {/* Description */}
            <p style={styles.description}>{project.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  projectCard: {
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '16px',
    margin: '16px 0',
    backgroundColor: '#f9f9f9',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between', // Push title and date to opposite sides
    alignItems: 'center',
    marginBottom: '8px',
  },
  title: {
    fontWeight: 'bold',
    fontSize: '1.2rem',
    display: 'flex',
    alignItems: 'center',
  },
  githubLink: {
    marginLeft: '8px',
  },
  githubLogo: {
    width: '20px',
    height: '20px',
  },
  date: {
    fontSize: '1rem',
    color: '#555',
    whiteSpace: 'nowrap', // Prevents wrapping for the date
  },
  description: {
    margin: '0',
    fontSize: '1rem',
    color: '#333',
  },
};

export default Projects;
