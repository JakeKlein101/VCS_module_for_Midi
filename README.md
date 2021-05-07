<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="#">
    <img src="images/loading-logo.gif" alt="Git-bit logo" height="156" width="546">
  </a>

  <h3 align="center">Git-Bit VCS Module</h3>

  <p align="center">
    A version control platform for MIDI files.
    <br />
  </p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The VCS module</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
     <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#Commands">Commands</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About the Git-Bit VCS Module

The Git Bit VCS module (and the whole Git Bit project in general) was inspired by my struggles as a modern producer
with collaborating with other producers.

As a result, I decided that I want to create a platform like github, but for musicians.

### Built With

The VCS module portion utilizes the following python libraries:
* [Mido](https://mido.readthedocs.io/en/latest/)
* [Socket](https://docs.python.org/3/library/socket.html)


<!-- GETTING STARTED -->
## Getting Started

A good start to your journey into the Git Bit ecosystem is with creating an account on the [website.](https://github.com/JakeKlein101/Git-Bit_site_Django)



### Installation
Coming soon.


<!-- USAGE EXAMPLES -->
## Usage

### Commands

The main commands are as follows:
* Initiate a repository
  ```sh
  > gitbit init
  ```
* Commit changes
  ```sh
  > gitbit commit -o "Optional commit message."
  ```
  * Delete the repository
  ```sh
  > gitbit delete
  > "Are you sure you want to delete the repository? y/n: "
  ```

For information about the website portion, please refer to this [repository.](https://github.com/JakeKlein101/Git-Bit_site_Django)
