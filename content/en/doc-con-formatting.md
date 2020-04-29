<!--
---
linkTitle: "Formatting Conventions"
weight: 2
---
-->
# Formatting Conventions for Tekton Documentation

Tekton documentation uses Markdown to format the content. See the[Markdown cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
to gain a basic understanding of Markdown conventions.

## User interface elements

- Use **bold** to indicate anything that's clickable, such as buttons or menu items.

    <table>
      <tr>
       <td>
    <strong>Do</strong>
       </td>
       <td><strong>Don't</strong>
       </td>
      </tr>
      <tr>
       <td>Start your build by clicking <strong>Build</strong>.
       </td>
       <td>Click on the build button to start your build.
       </td>
      </tr>
    </table>

- Use the exact label given to the UI element, screen, or page.

    <table>
      <tr>
       <td><strong>Do</strong>
       </td>
       <td><strong>Don't</strong>
       </td>
      </tr>
      <tr>
       <td>Choose your Smurfs by clicking <strong>Select Smurfs</strong>.
       </td>
       <td>Click select to choose your Smurfs.
       </td>
      </tr>
    </table>

- Use "quotes" to denote the name of a non-clickable elements, such as a menu or a page.

    <table>
      <tr>
       <td><strong>Do</strong>
       </td>
       <td><strong>Don't</strong>
     </td>
      </tr>
      <tr>
       <td>Click <strong>Next </strong>to advance to the "Set Up Billing" page.
       </td>
       <td>Click <strong>Next </strong>to open the billing setup page.
       </td>
      </tr>
    </table>

## Commands and code

- Format these as code and indicate what they are:

  - API objects
  - Commands
  - Names of files and directories

  For example:

    <table>
      <tr>
       <td><strong>Do</strong>
       </td>
       <td><strong>Don't</strong>
       </td>
      </tr>
      <tr>
       <td>Define a new <code>TaskRun</code> instance.
       </td>
       <td>Define a new taskrun.
       </td>
      </tr>
      <tr>
       <td>Run the <code>smurfcaptor</code> command.
       </td>
       <td>Run smurfcaptor.
       </td>
      </tr>
    </table>

- Use angle brackets for placeholders, such as variables, and tell the reader what the placeholders represent. For example:

     To force-catch a specific Smurf, run the following command:
  
          ```
          smurfcaptor -f <target-smurf>
          ```
      where `<target-smurf>` is the Smurf you want Smurfcaptor to catch.


      When the operation completes, Smurfcaptor displays the result.

- Use informative variable names and format them using camelCase. For example:

    <table>
      <tr>
       <td><strong>Do</strong>
       </td>
       <td><strong>Don't</strong>
       </td>
      </tr>
      <tr>
       <td><code>targetSmurf</code> 
       </td>
       <td><code>tarsmu</code>
       </td>
      </tr>
    </table>

- Remove trailing spaces. Some markdown objects, such as lists, require a specific number of spaces,
  and often, the absence of spaces in specific places, in order to render properly on the website.
  They can also cause unnecessary lint errors. 

## Links

- **Never use "here" or "this" as a link anchor.** Use either the exact title of the document being
   linked, or descriptive, in-context phrase and a brief description of the link target. This enables
   more meaningful results when searching the documentation set, and is more informative to the reader.
   For example:

    <table>
      <tr>
       <td><strong>Do</strong>
       </td>
       <td><strong>Don't</strong>
       </td>
      </tr>
      <tr>
       <td>For more information, see Installing Smurfcaptor.
       </td>
       <td>For more information, go here.
       </td>
      </tr>
      <tr>
       <td>See the Tekton website for tutorials that cover Smurfcaptor integration.
       </td>
       <td>Go to this site for tutorials.
       </td>
      </tr>
    </table>
