<!--
---
title: "Create a blog post"
linkTitle: "Create a blog post"
weight: 6
description: >
  Contributions to the Tekton blog are welcome!
---
-->

If you have an interesting, fun, or practical idea that you want to share with the
world, you can write a blog post about it!

Blog posts don't have to follow strict writing rules or styles. They are a good
place for you to have fun talking about Tekton.

This is how:

## Set up a local version of the website

1.  [Fork][] the [documentation repository][docs-repo].

1.  Clone the repository to your computer:

    ```bash
    git clone https://github.com/<your-git-username>/website.git
  
    ```

1.  [Install Docker Compose][docker-compose], if it's not already installed on
    your computer. 

1.  Change directory to the repository root and run the website server:

    ```bash
    cd website
    docker-compose up
    ```
    And wait for the confirmation message to pop up:

    ```
    ┌─────────────────────────────────────────────────┐
    │                                                 │
    │   ◈ Server now ready on http://localhost:8888   │
    │                                                 │
    └─────────────────────────────────────────────────┘
    ```

    Keep the server running while you write your post. Press *Ctrl + C* to stop
    it.

1.  Open your browser and go to `http://localhost:8888`.

## Draft your blog post

1.  Create a folder under `content/en/blog/<year>/` with a descriptive name.
    Lower case, use dashes to separate words.

1.  Inside the newly created folder, create a file and add a [front matter][]
	  with the following format:

    ```yaml
    ---
    title: Title
    likTitle: Title
    date: <date, for example 2022-10-26>
    author: "Author name"
    description: >
      A heading sentence about your post
    ---
    ```

1.	Save the file as `index.md`. As soon as you save it a new blog entry is now
    visible on your browser.

1.	Below the front matter, write to your heart's content. Every time you save,
    the server automatically builds the page and shows the changes.

If you need some inspiration, you can find examples on the [website
repository][blogs-folder].

## Open a PR for review

1.  After you complete your blog post, open a Pull Request and wait for it to
    be reviewed.


1.  Your blog post is now public and we are all excited to read it.
    Congratulations!

[docs-repo]: https://github.com/tektoncd/website
[fork]: https://docs.github.com/en/get-started/quickstart/fork-a-repo
[docker-compose]: https://docs.docker.com/get-docker/
[front matter]: https://gohugo.io/content-management/front-matter/
[blogs-folder]: https://github.com/tektoncd/website/tree/main/content/en/blog
