cd my-website/frontend
npm run build
cd ../../
cp -R my-website/frontend/build/* .
git add .
git commit -m "Update frontend build"
git push