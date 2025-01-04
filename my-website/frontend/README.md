# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

## Updating website:

cd my-website/frontend
npm run build
cd ..
cd ..
cp -R my-website/frontend/build/* .

push GitHub changes

<<<<<<< HEAD
Note: if github pages tries to run the backend instead of the frontend, run
touch .nojekyll
in the main directory

=======
>>>>>>> bce3e7489740b31f13281a91f10fe2a755b6ef1d
## Updating backend:
cd backend
git add .
git commit -m "Add /run-python-code route"
git push heroku master
