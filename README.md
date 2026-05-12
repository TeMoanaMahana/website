# Te Moana Mahana Website

Welcome to the GitHub repository for the Te Moana Mahana: Ocean change forecasting for climate resilience in Aotearoa website. This website, in accordance with our doctrine of free and open data/resources, is completely free for you to clone and edit. It has been built within the [Hugo](https://github.com/gohugoio/hugo) framework using an extensively modified version of the [Hugoplate](https://github.com/zeon-studio/hugoplate) theme, developed by Zeon Studio.

Hugo is designed for simplicity and thus modification of this website is relatively straightforward.

## Prerequisites

Before getting started, make sure you have the following installed on your machine:

- **Git** — required to clone the repository. Download it from [git-scm.com](https://git-scm.com/downloads) and follow the install instructions for your operating system.
- A **terminal** (macOS/Linux) or **PowerShell** (Windows)

## Folders and Purposes

Below is a list of all folders and the uses and purposes of them. Use this to familiarise yourself with the way in which this website works and how to make your desired changes.

<details>

<summary>Assets</summary>

Assets contains two folders, **css/** and **images/**, both of which are commonly used if you want to change this website.

- **css/** contains all the custom css components that are used in the website. These are standard elements, such as buttons and cards, that are used throughout the entire website. All of the css code for these is located within **css/components/** and are imported into the Hugo framework via **css/custom.css**.

- **images/** contains all of the images that are used within the site. These images are called directly within the .html or .md files that are used to build the website.

</details>

<details>

<summary>Config</summary>

Config contains several general parameters (all of which are stored in .toml files) for the website, for example you can change the logo image here, or update the navigation bar found at the top of the webpage with new webpages you have developed. If you explore these files, it should be all quite self explanatory as to what does what.

</details>

<details>

<summary>Content</summary>

This is the bread and butter of the Hugo framework. Within this folder (**content/english/**) is the entirety of the 'content' of the website. Each webpage is divided into their own directory, with all of the content written in a markdown (.md) format with a .yaml header. The main content for that webpage is ***always*** stored within a file called **_index.md**, with adjacent comments within each file.

- For example, within **content/english/blog/** are several .md files. The main **_index.md** is present, which defines the webpage, with each blog post getting its own .md file, the name of which is reflected in the url for that blog post.

- Another example is that of the **authors/** directory, which again contains the **_index.md** file and then a separate markdown file for each team member. Within the yaml at the top of these markdown files, you will find that several parameters are defined, such as the title of the page, the last name (used for ordering), their role, the portrait image used for that team member, and their social links that are highlighted on their page.

Within the main **content/english/** page, you will find a **_index.md** file. This file contains all of the yaml for the home page of the website.

</details>

<details>

<summary>Data</summary>

Data contains just two .json files.

- **social.json** contains the link at the bottom of the page to 'socials'. This may include a link to a 'mailto:' account, or other links to various social medias.

- **theme.json** contains the colours and fonts that are used throughout the website. **WARNING** while this file seems simple, I have had some major issues with it in the past. I would say just leave this as is. Adjust at your own risk and have a backup!

</details>

<details>

<summary>Layouts</summary>

Layouts contain all of the custom .html that was used to create this website that is separate from that provided in the Hugoplate template. All of these files were based on an existing Hugoplate template.

As you will notice, there are several subdirectories in here.

- **_partials/** includes several elements that are used within other .html files, such as widgets, headers, and the landing page map.

- **authors/, blog/, publications/** all contain various .html files that are used to define how their respective pages are laid out.

- **shortcodes/** contains additional .html files for the glider map that is found within the glider page.

In addition to these directories, there are several .html files within **layouts/**

- **404.en.html** defines how the 404 page looks.

- **about.html** defines how the about page is formatted.

- **home.html** defines how the home page is formatted.

- **single.html** defines how the general 'single' page is formatted. This page is used in the "Learn About the Ocean" page and is used as a generic option for if you want a page that contains simple markdown and yaml. It can be reused for new pages in the future.

</details>

<details>

<summary>Scripts</summary>

This directory holds several scripts that are used in the function of the website. Most came with the Hugoplate template, with the two python scripts, **glider_data_processing.py** and **glider_plotting.py**, along with the associated **requirements.txt** files were added to allow for recurrent running and updating of the glider data.

</details>

<details>

<summary>Static</summary>

This directory is used to hold glider data and various non-changing assets. These files are similar to those found in the assets folder, but the files are copied as is when the website is published. Those within the assets folder may be transformed and adjusted when the website is being built.

</details>

<details>

<summary>Themes</summary>

This folder should not be adjusted. It contains the original .html files for the Hugoplate theme and will be overwritten if the theme is being updated. All adjustments to the layouts of the page should be performed in the other folders, specifically in the **assets** and **layouts/** folders.

</details>

The only other file that may need to be adjusted is that of the **hugo.toml** file within the root directory. This file contains various options on how the website will work when it is published. Most notably, is that of the **baseURL** variable at the top of the file, which if not set to the correct URL on publishing the website, will break all links that are within the website.

## Building the Website on Your Machine

This website was built using a macOS machine, and thus instructions for UNIX (macOS/Linux) machines are at the top with instructions for Windows machines below.

***NOTE***
This step does require the use of the terminal. The terminal is an essential part of your computer and don't be scared!! Simply copy and paste the commands and if you get an error, consult documentation online or ask a suitable AI chatbot for help. The terminal is a great way to run programmes!!

### First Steps

1. Clone this repository by running the following command in your terminal:

```
git clone https://github.com/TeMoanaMahana/website.git
```

2. Navigate into the cloned repository:

```
cd website
```

### UNIX

The instructions below involve the use of homebrew, a popular package manager for macOS and Linux systems. It should be noted that there are many other ways to install the required dependencies of Hugo, Node.js, and Go. Please use your preferred versions or visit the install instructions on the respective websites below if you want to use a different method.

- [Hugo](https://gohugo.io/installation/)
- [Node.js](https://nodejs.org/en/download)
- [Go](https://go.dev/doc/install)

1. If on a machine that can use homebrew, install it via the instructions at [this link](https://brew.sh), or by copying and pasting the command below into your terminal:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Next, install Hugo, Node.js, and Go by running the below command:

```
brew install hugo node go
```

3. Run the below command to install dependencies:

```
npm install
```

4. Run the development command and start developing:

```
npm run dev
```

This will create a locally hosted site with the url "http://localhost:1313" on your machine. You can access this url on any regular browser and start developing! When a file is changed within the repository, the website should automatically reload and your changes should be reflected.

***NOTE***
Some changes require the site to be rebuilt, in which case, cancel the ```npm run dev``` command with ctrl-c, and re-run ```npm run dev```

### Windows

The instructions below involve the use of chocolatey, a popular package manager for Windows systems. It should be noted that there are many other ways to install the required dependencies of Hugo, Node.js, and Go. Please use your preferred versions or visit the install instructions on the respective websites below if you want to use a different method.

- [Hugo](https://gohugo.io/installation/)
- [Node.js](https://nodejs.org/en/download)
- [Go](https://go.dev/doc/install)

1. Follow the instructions for installing chocolatey via [this link](https://chocolatey.org/install) or via the steps below:

2. Open powershell.exe and run ```Get-ExecutionPolicy```. If the return is ```Restricted```, then run ```Set-ExecutionPolicy AllSigned``` or ```Set-ExecutionPolicy Bypass -Scope Process```.

3. Next, run the command below:

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

4. Next, install Hugo, Node.js, and Go by running the below command:

```
choco install hugo nodejs go
```

5. Run the below command to install dependencies:

```
npm install
```

6. Run the development command and start developing:

```
npm run dev
```

This will create a locally hosted site with the url "http://localhost:1313" on your machine. You can access this url on any regular browser and start developing! When a file is changed within the repository, the website should automatically reload and your changes should be reflected.

***NOTE***
Some changes require the site to be rebuilt, in which case, cancel the ```npm run dev``` command with ctrl-c, and re-run ```npm run dev```

## Pushing Updates

Once you have made your changes, you'll need to push them back to GitHub. The three commands you'll use most often are:

```
git add .
```
Stages all of your changes, marking them as ready to be committed.

```
git commit -m "a short description of your changes"
```
Saves a snapshot of your staged changes with a message describing what you did.

```
git push
```
Uploads your committed changes to GitHub.

For a more complete reference, including details on the initial setup and connection to your remote repository, see the [official Git documentation](https://git-scm.com/docs). If you'd prefer a visual interface to avoid memorising commands, [lazygit](https://github.com/jesseduffield/lazygit) is a great CLI tool that makes this much easier. It can be installed on UNIX machines via Homebrew (`brew install lazygit`) or on Windows via chocolatey (`choco install lazygit`).

## Hosting

This website is hosted directly on GitHub Pages for free. More information can be found on the [official Hugo documentation website for hosting with GitHub Pages](https://gohugo.io/host-and-deploy/host-on-github-pages/).
