Guides to use Tekton with third-party services.

## Before you begin

To preview your documentation, check the guide on [how to run this site
locally][run-locally].

## Contributing documentation for the first time

Before you contribute, we strongly recommend that you join the [TektonCD
Slack][tekton-slack] and the [Tekton TW working group][tekton-tw-wg].


1. Create a new folder under `content/en/vendor/` with a descriptive 
   vendor name. Lower case, use dashes to separate words.

1. Write the documentation following the [content
   guidelines][content-guidelines] and [formatting
   conventions][format-conventions].

## Surface your documentation in existing guides

1. Create a new file under `content/en/vendor/<your-vendor>/` with a
   descriptive name.

1. Write the content as if it was part of the guide you want it to appear in.
   Keep in mind the style and tone of the parent document. Do not use first
   level headers.

1. In the relevant guide, use the `tabs` and [`readfile`][readfile] shortcodes
   to display your content alongside existing information. For example, to add
   platform-specific authentication steps to the "Authentication" section of an
   existing guide:

    ```html
    ## Authentication

    {{< tabs >}}

    {{< tab "Default" >}}
      Default authentication process:

      1. Step 1
      2. Step 2
    {{< /tab >}}

    {{< tab "My cloud provider" >}}
    {{< readfile file="/vendor/my-vendor/my-service-auth.md" >}}
    {{< /tab >}}

    {{< /tabs >}}
    ```
1.  If it's not already there, add the vendor disclaimer at the top of the
    document, below the front matter.

    ```html
    {{% pageinfo %}}
    {{% readfile "/vendor/disclaimer.md" %}}
    {{% /pageinfo %}}

    ```

## Publishing new guide

If you want to publish a standalone document instead of contributing to an
existing one:

1. Write your new document and save it under
   `content/en/vendor/<your-vendor>/`. Do not use a first level header for the
   title. You are going to set the title of the document in a subsequent step.

1. Determine the correct place show the document, that would usually be in one
   one of the following sections:

    - Installation
    - Getting Started
    - How-to Guides

   See the [content guidelines][content-guidelines] for more information.

1. In the folder corresponding to the section you selected, create a new
   file with a descriptive name. Add a [hugo front matter][hugo-frontmatter] in YAML
   format. For example, suppose you are adding a new installation guide, create
   the file `content/en/docs/Installation/my-vendor-install.md` with the
   following front matter:

    ```yaml
    ---
    title: Install Tekton on my cloud service
    linkTitle: Install Tekton on my cloud service
    weight: 3
    description: >
      Installation guide to run Tekton on my cloud service.
    ---
    ```

   Keep in mind that the `weight` parameter determines the order in the left
   navigation pane. Lower numbers appears earlier in the list, documents with
   the same weight are ordered alphabetically.

1.  Add the vendor disclaimer at the top of the document, below the front
    matter.

    ```html
    {{% pageinfo %}}
    {{% readfile "/vendor/disclaimer.md" %}}
    {{% /pageinfo %}}

    ```

1. Import your file with the `readfile` shortcode. The final markdown file looks
   like this:

   ```md
    ---
    title: Install Tekton on my cloud service
    linkTitle: Install Tekton on my cloud service
    weight: 3
    description: >
      Installation guide to run Tekton on my cloud service.
    ---

    {{% pageinfo %}}
    {{% readfile "/vendor/disclaimer.md" %}}
    {{% /pageinfo %}}

    {{% readfile "/vendor/my-vendor/installation.md" %}}

   ```

## Caveats

+  Because Docsy, the platform Tekton docs are built on, rebuilds files when
   their content changes, it will not pick up the changes in your included files
   unless you make a change on the parent file. You can make a small change,
   like increasing a dummy counter, while writing content to trigger rebuilding
   the parent file.

+  Documentation using this approach is meant to be read on the website. Reading
   the source files on GitHub will not be the best experience.

## Own your docs

If you are contributing documentation to show how Tekton works with a particular
platform, we encourage you to own your documentation.

+  Ensure freshness and accuracy.

+  Review reported user issues regarding your documentation.

+  Review Pull Requests to your docs.

[tekton-slack]: https://github.com/tektoncd/community/blob/main/working-groups.md#documentation
[tekton-tw-wg]: https://github.com/tektoncd/community/blob/main/working-groups.md#documentation
[tabs]: https://www.docsy.dev/docs/adding-content/shortcodes/#tabbed-panes
[readfile]: https://www.docsy.dev/docs/adding-content/shortcodes/#include-external-files
[content-guidelines]: /docs/contribute/doc-con-content/
[hugo-frontmatter]: https://gohugo.io/content-management/front-matter/
[run-locally]: /docs/contribute/run-locally/
[format-conventions]: /docs/contribute/doc-con-formatting/
