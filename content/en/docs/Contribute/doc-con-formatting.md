<!--
---
title: "Formatting conventions"
linkTitle: "Formatting conventions"
weight: 2
description: >
  Formatting conventions for Tekton documentation
---
-->

Tekton documentation uses Markdown to format the content. See the
[CommonMark tutorial](https://commonmark.org/help/) to learn the basics.

Tekton markdown formatting conventions:

-   **Lists**
    - Capitalize the first word for each item.
    - Don't put a period at the end of each item in lists containing only nouns
      or single-word items.
    - Use sentence punctuation in any other case.

-   **Code Format**
    - Use code formatting when referencing API objects, commands, files and
      directories.
    - Use angle brackets for placeholders such as variables. For example:

      ```
      kubectl apply -f <pipeline-file>
      ```

-   **Markdown files**
    - Hard-wrap the file lines so they are not longer than 80 characters.
    - Use [reference-style links][ref-links] if the URL in the link is too
      long. There's no specific URL length, use your best judgement to keep
      markdown files readable.
   
[ref-links]: https://www.markdownguide.org/basic-syntax/#reference-style-links

