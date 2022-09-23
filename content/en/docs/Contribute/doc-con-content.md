<!--
---
title: "Content guidelines"
linkTitle: "Content guidelines"
weight: 1
description: >
  Content guidelines for Tekton documentation
---
-->

Follow these guidelines when planning and writing Tekton documentation. 

## Types of content

Each page in the Tekton documentation set must fall into one of the following categories:

+   **Tutorials** - These are introductory guides, focused on new users:
    - Task-oriented
    - Make sure it works: For Tekton, this means pick a runtime and stick with it
      throughout the entire tutorial, so you can have reproducible steps that a
      newcomer can copy-paste.
    - Do not explain anything in detail, focus on doing. This is a common
      pitfall, trying to explain things too early.
    - Do not provide more than one way of doing things. Pick the easiest path and
      go with it. This is another common pitfall, trying to show everything you
      can do in an introductory guide.
    - Show results immediately.

+   **How-to guides** - These are docs that explain how to complete a particular task:
    - Goal oriented.
    - Assumes some knowledge from the user, no need to start from scratch.
    - Focus on the goal at hand.
    - It’s fine to show several ways to achieve the goal, but there’s no need to
      be comprehensive. (That’s what reference docs are for). 
    - Provide a descriptive title.

+   **Reference Guides** - These provide the technical details for everything
    Tekton does. The most common example is the API reference docs:
    - Be accurate
    - Mirror the codebase when possible, so your reader knows what to expect.

+   **Explanations** - Conceptual information:
    - Descriptive content, explain how things work
    - Do not include steps here

You can find an in-depth discussion about this documentation framework in the
[Grand Unified Theory of Documentation](https://diataxis.fr/).

## Structure

We want our documentation to be easily digestible, so make sure your writing is clear and concise.
Follow these simple guidelines:

*   Break up long thoughts into multiple sentences.
*   Break up longer documents into logical sections.
*   Use paragraphs to separate thoughts and ideas.
*   Ensure paragraphs flow into one another - that is, they are logically connected.
*   Use headings and subheadings to indicate topics and sub-topics. Don't use
    more than 3 subheading levels.

## Style and tone

**Always use active voice.** It's much easier to parse and more user-friendly
(relatable) than passive. Passive voice sounds stuffy and officious. It takes
much more brain work to understand and causes the reader to zone out.

<table>
  <tr>
   <td><strong>Do</strong>
   </td>
   <td><strong>Don't</strong>
   </td>
  </tr>
  <tr>
   <td>The installer copies the files to the destination directory.
   </td>
   <td>The files being installed are copied to the destination directory by the installer.
   </td>
  </tr>
</table>

---

**Never use "should" or "might."** These words introduce uncertainty. We're
either sure how our software works or we're not.

<table>
  <tr>
   <td><strong>Do</strong>
   </td>
   <td><strong>Don't</strong>
   </td>
  </tr>
  <tr>
   <td>Click <strong>Build</strong> to start your build.
   </td>
   <td>When you click <strong>Build</strong>, your build should start.
   </td>
  </tr>
</table>

---

**Don't use future tense** unless no other way exists to convey the information.
Future tense creates an unwanted deferral of the result, while the result of
each step should be immediate. For example:

<table>
  <tr>
   <td><strong>Do</strong>
   </td>
   <td><strong>Don't</strong>
   </td>
  </tr>
  <tr>
   <td>Click <strong>Build</strong> to start your build.
   </td>
   <td>When you click <strong>Build</strong>, your build will start.
   </td>
  </tr>
</table>

---

**Avoid repetition.** Repetition is a "mental stumbling block" that gets in the
way of the reader's comprehension of the thought or topic. For example:

<table>
  <tr>
   <td><strong>Do</strong>
   </td>
   <td><strong>Don't</strong>
   </td>
  </tr>
  <tr>
   <td>Smurfcaptor supports single- and multi-Smurf capture events, including batch processing.
   </td>
   <td>Smurfcaptor supports single- and multi-Smurf capture events. Smurfcaptor also supports batch processing.
   </td>
  </tr>
</table>

---

**Never use "we."** The reader will wonder whether they're part of the "we" or
not. For example:

<table>
  <tr>
   <td><strong>Do</strong>
   </td>
   <td><strong>Don't</strong>
   </td>
  </tr>
  <tr>
   <td>Version 3.0 adds support for Smurf counting.
   </td>
   <td>In version 3.0 we added Smurf counting support.
   </td>
  </tr>
</table>

---

**Never use "might" or "may."** "May" is often confused with "might" but they
are not the same. "Might" introduces uncertainty just like "should," while "may"
implies the permission has been granted and not that an option or action is
available to the user. For example:

<table>
  <tr>
   <td><strong>Do</strong>
   </td>
   <td><strong> Don't</strong>
   </td>
  </tr>
  <tr>
   <td>The build starts when you click <strong>Build</strong>.
   </td>
   <td>The build might start when you click <strong>Build.</strong>
   </td>
  </tr>
  <tr>
   <td>You can choose either high or low Smurf sensitivity.
   </td>
   <td>You may choose high or low Smurf sensitivity.
   </td>
  </tr>
</table>

