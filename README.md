# Life@USTC RSS

[![Create feeds](https://github.com/Life-USTC/LU_RSS/actions/workflows/run.yaml/badge.svg)](https://github.com/Life-USTC/LU_RSS/actions/workflows/run.yaml)

## Introduction

Backup a given RSS feed source, download the feed's XML file and all url links' content to a local folder,
then change the links in the feed to point to the local files. (or URLs)

_This is suggested to work with GitHub Pages and GitHub Actions to automatically update the feed and the files._

## Notice

- With little modifications you could backup anything you want with this method, just currently we're backing up RSS urls from WeRSS (which isn't supposed to be shared).
- **This might violate GitHub's EULA or ToS, so use at your own risk.**
- Other modifications might be added to satisify the app's need
  - The simple backup version would be stored in `archived` branch in the future.
- This repo is open-sourced, but not licensed.
  - You may use this for learning purposes only.
  - We open source this for public review purposes (so that we don't easily get hacked and publish harmful messages to users)

## Branches

- `master` contains the code, and runs by GitHub Action

- `gh-pages` contains the generated files(Backups and XMLs), and is hosted on GitHub Pages.

## Deploy

To customize your own one, fork the repo and edit `config.yaml`, configure GitHub Pages' domain name.

**We recommend you configure a CDN like us to lower GitHub's load.**
