# Christopher Apton – Personal Website

Welcome to the source code for my personal portfolio website, built to showcase my data science work, technical projects, and professional experience. The site features a modern frontend with a custom backend, designed for interactivity, modularity, and easy updates which is hosted on a raspberry pi.
**Live Site:** [chrisapton.github.io](https://chrisapton.github.io/)

---

## Features

* **Homepage/About:** Introduction and personal summary with a profile image.
* **Projects:** Dynamic project cards populated from GitHub, including repository descriptions, skills, and date ranges.
* **Experience:** Timeline of relevant professional roles and internships, with descriptions and achievements.
* **Responsive Design:** Works across desktop and mobile, leveraging [Tailwind CSS](https://tailwindcss.com/) for clean styling.
* **Resume Download:** PDF resume is available for download.
* **Backend Integration:**

  * **Custom Python backend** handles dynamic content such as GitHub repo info, LinkedIn data scraping, and project list updates.
  * Scheduled or on-demand updates for project data and resume download via backend scripts.
* **Deployment:** Frontend hosted with GitHub Pages and automated deployment scripts. Backend hosted on a raspberry pi.

---

## Tech Stack

**Frontend:**

* React.js (see `frontend/`)
* Tailwind CSS
* HTML5 & JavaScript

**Backend:**

* Python (see `pi_backend/`)
* Flask API (for serving data, e.g. GitHub/LinkedIn info)
* Jupyter Notebook (analysis/testing utilities)
* Web scraping utilities (LinkedIn/project data)

---

## Repository Structure

```
.
├── my-website/
│   ├── frontend/
│   │   ├── build/              # Production build files
│   │   ├── public/             # Static files (favicon, assets)
│   │   ├── src/                # React source code
│   │   ├── package.json        # Frontend dependencies
│   │   └── tailwind.config.js  # Tailwind CSS config
│   ├── pi_backend/
│   │   ├── app.py              # Flask backend/API
│   │   ├── linkedin_scraper/   # Scraper modules
│   │   ├── github_repo_updater.py  # GitHub integration
│   │   └── requirements.txt    # Backend Python requirements
│   ├── Resume.pdf              # Downloadable resume
│   ├── index.html, 404.html    # Static entry points
│   ├── deploy.sh               # Deploy script for GitHub Pages
│   └── static/                 # Static website assets
└── ...
```

---

## How to Run Locally

**Frontend:**

1. Navigate to `my-website/frontend/`.
2. Install dependencies:

   ```bash
   npm install
   ```
3. Start the development server:

   ```bash
   npm start
   ```

   The site will be available at `http://localhost:3000`.

**Backend:**

1. Navigate to `my-website/pi_backend/`.
2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:

   ```bash
   python app.py
   ```

   The backend will be available at `http://localhost:5000`.
   
---

## Deployment

* **Static Site:** The main site is deployed using [GitHub Pages](https://pages.github.com/) and can be updated using the `deploy.sh` script.
* **Backend:** The backend is used for local or private automation tasks (e.g., scraping/updating project data).

---

## License

MIT License. See [LICENSE](./LICENSE) for details.

---

## Contact

* [Personal Website](https://chrisapton.github.io/)
* Email: [chrisapton@gmail.com](mailto:chrisapton@gmail.com)
