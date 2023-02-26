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

## Markdown formatting conventions:

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
    - Use [reference-style links][ref-links] if the URL is too long. There's no
      specific URL length, use your best judgment to keep markdown files
      readable.

## Embed code samples

You can import code from external files. To do this, use the [`readfile`
shortcode][readfile-shortcode] with the `code` and `lang` options. For example,
the following code embeds the file `samples/task.yaml`:

```html
{{</* readfile file="samples/task.yaml" code="true" lang="yaml" */>}}
```

This is rendered as:

{{< readfile file="samples/task.yaml" code="true" lang="yaml" >}}

You can also embed code samples in tabs using the `tabpane` shortcode. For
example, the following code embeds `samples/pipeline1.yaml` and
`samples/pipeline2.yaml` in different tabs:

```html
{{</* tabs */>}}
{{</* tab "v1beta1" */>}}
{{</* readfile file="samples/pipeline1.yaml" code="true" lang="yaml" */>}}
{{</* /tab */>}}

{{</* tab "v1" */>}}
{{</* readfile file="samples/pipeline2.yaml" code="true" lang="yaml" */>}}
{{</* /tab */>}}
{{</* /tabs */>}}
```

Rendered as:

{{< tabs >}}
{{< tab "v1beta1" >}}
{{< readfile file="samples/pipeline1.yaml" code="true" lang="yaml" >}}
{{< /tab >}}

{{< tab "v1" >}}
{{< readfile file="samples/pipeline2.yaml" code="true" lang="yaml" >}}
{{< /tab >}}
{{< /tabs >}}

{{% alert title="Warning" color="warning" %}}
The `path` parameter don't support relative paths to parent directories. For
example, `path="../sample.yaml"` does not work.
{{% /alert %}}

[ref-links]: https://www.markdownguide.org/basic-syntax/#reference-style-links
[readfile-shortcode]: https://www.docsy.dev/docs/adding-content/shortcodes/#include-code-files

