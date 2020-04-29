<!--
---
linkTitle: "Content Guidelines"
weight: 2
---
-->
## Content Guidelines for Tekton Documentation

Follow these guidelines when planning and writing Tekton documentation. 

## Types of content

Each page in the Tekton documentation set must fall into one of the following categories:

- **Concept** - explains a Tekton concept, such as what a `Task` is or how a `TaskRun` executes a `Task`.
  It can be either high-level: "Understanding the flow of data in a `Pipeline`" or low-level:
  "Understanding the `SmurfCapture` method in the Smurfcaptor API".
- **Task** - contains procedures that explain how to do something in Tekton - for example, how to
  create a `Task`.
- **Tutorial** - guides you through a specific journey in order to familiarize you with multiple concepts
  and tasks in one go. For example, a tutorial could explain how to set up a `Pipeline` that pulls source
  code from GitHub and stores the outputs in the cloud. Tutorials are self-contained and goal-focused.
- **Reference** - a collection of concepts that serves as an authoritative source of in-depth knowledge
  about a specific area. A great example would be the Tekton API reference.

## Structure

We want our documentation to be easily digestible, so make sure your writing is clear and concise.
Follow these simple guidelines:

*   Break up long thoughts into multiple sentences.
*   Break up longer documents into logical sections.
*   Use paragraphs to separate thoughts and ideas.
*   Ensure paragraphs flow into one another - that is, they are logically connected.
*   Use headings and subheadings to indicate topics and sub-topics.

## Style and tone

- **Always use active voice.** It's much easier to parse and more user-friendly (relatable) than passive. Passive voice
  sounds stuffy and officious. It takes much more brain work to understand and causes the reader to zone out.

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

- **Never use "should" or "might."** These words introduce uncertainty. We're either sure how our software works or we're not.

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

- **Don't use future tense** unless no other way exists to convey the information. Future tense creates an unwanted deferral of the result, while the result of each step should be immediate. For example:

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

- **Avoid repetition.** Repetition is a "mental stumbling block" that gets in the way of the reader's comprehension of the thought or topic. For example:

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

- **Never use "we."** The reader will wonder whether they're part of the "we" or not. For example:

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

- **Never use "might" or "may."** "May" is often confused with "might" but they are not the same. "Might" introduces uncertainty
  just like "should," while "may" implies the permission has been granted and not that an option or action is available to the user. For example:

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

## Calling out important things

To call out something of particular importance, use the three severity levels of callouts: note, caution, and warning.
<table>
  <tr>
   <td><strong>Callout Type</strong>
   </td>
   <td><strong>Example</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Note</strong> calls the reader's attention to something important.
   </td>
   <td><strong>Note:</strong> It is best to capture Smurfs in batches, as processing a large number of Smurfs at once can result in long wait times.
   </td>
  </tr>
  <tr>
   <td><strong>Caution</strong> indicates something that may cost the reader additional time and work if not followed. 
   </td>
   <td><strong>Caution:</strong> Papa Smurf is a highly skilled mage. To maximize your Smurf yields, avoid capturing him along with other Smurfs.
   </td>
  </tr>
  <tr>
   <td><strong>Warning</strong> warns the reader of a potential catastrophic failure.
   </td>
   <td><strong>Warning: </strong>Looking directly into the Basilisk's eyes turns you instantly to stone.
   </td>
  </tr>
</table>

## Things to avoid

Avoid the following:

- **Copy-pasting large portions of existing documentation.** If you need to reuse a large piece of content,
    link it instead. Duplication inevitably leads to the two copies going out of sync and confusing readers.
- **Vendor-specific links.** We don't want to imply any kind of endorsement.
- **Links to external projects.** Do not link to projects outside of the Tekton repository.
  Those projects might move or go away, leaving the link broken.
