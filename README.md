# RSS-backup

repo used to backup a given RSS feed source,
would download the feed and all url links to a local folder, then change the links in the feed to point to the local files.

further more this is suggested to work with GitHub Pages and GitHub Actions to automatically update the feed and the files.

branch `master` contains the code to run everything, with GitHub Action configs and python code.

branch `gh-pages` contains the generated files, and the feed.xml file, which is 'cotinuously' updated by the GitHub Action.

Notice that this might violate GitHub's EULA, so use at your own risk.