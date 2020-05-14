<!--
---
linkTitle: "Writing Primer"
weight: 2
---
-->
# Writing High Quality Documentation for Tekton

“I hate writing!” is a line heard all too often. Documenting a feature can be an intimidating task. 

The most common questions that come up when writing a document are:

- “Where do I start?” 
- “What do I say?” 
- “How do I know when I’m done?”
- “Who can I ask for help?”
- “Where can I find writing resources?”

These and many other questions can form mental barriers that discourage from contributing to
documentation. When we remove or lower these  barriers, writing can become an enjoyable,
satisfying activity.

## I hate writing!

That’s fine. Professional writers do, too. We’re just better at hiding it! The first thing to
remember is that writing is an iterative process. Professional writers never produce the perfect
document on their first try. 

Instead, we start with an SFD (Shoddy First Draft), and then edit, edit, edit. The goal is not to
write a perfect document, but to write one that is good enough to convey the information in an
approachable way. This removes the pressure of writing a polished piece and instead lets us focus
on conveying the correct information in the right order and proportion. 

Write an SFD and brainstorm it with others - it really works!

## Where do I start?

Begin by asking yourself, “Who is my audience?” Engineers? Less technical readers, such as
management? Aliens? Once you know your audience, you’ll know how much detail to include, the
tone to use, and who your reviewers will be.

Next, put yourself in your audience’s shoes and ask, “What do I, as this type of reader, need
to know to use this thing I’m writing about?” Things that are obvious to you may not be obvious
to an outsider. What tasks will the reader need to accomplish? What will they need to know to
accomplish each task?

Write down headings representing each of those major points or areas. For example, “Installation,”
“Configuration,” “Operation modes,” or “Command-line options.” These major things become the outline
of your document. 

## What do I say?

Look at your outline. What does the reader need to know about each of those topics or areas of
interest? For example, if you're writing a procedure, you may also want to include prerequisites - that
is, steps the reader must complete before starting the procedure. What are the possible scenarios when
starting the procedure? What are the possible outcomes? Do the steps differ depending on the starting
scenario and the desired outcome?

Write down some ideas or sub-topics for each key area. These become the mini table of contents for
each section. Once you have those, your document outline is complete! 

Flesh out one section at a time, keeping the level of detail appropriate to your audience. For example,
if you’re writing a command-line reference, chances are the reader will be an advanced user who needs
to understand the intricacies of each option, including allowed values, the default value, the behavior
resulting from each value, and any exceptions and caveats. 

On the other hand, if you’re documenting a specific feature, start by describing what it does, so that
the reader has context, and describe how to use the feature afterwards. Put the “what” before the “how”
and start simple, then introduce more detail as you go.

## Active or passive voice?

**Always use active voice.** Active voice is much easier to parse and more relatable for the reader than
passive voice. Passive voice sounds stuffy and officious; it reads like a boring legal document or that
college textbook that made you fall asleep. It takes much more brain work to understand and causes the
reader to zone out.

Consider the following:

"The files being installed are copied to the destination directory by the installer. The destination
directory is created by the installer before the files are copied."

And now read the same information in active voice:

"The installer creates the destination directory, then copies the files to it."

Night and day, don't you think?

## How do I know when I’m done?

This is the hardest part. When do you stop writing? 

Go over each section and ask yourself again, “would I know how to use this thing based solely on what’s
written?” If so, send your document out for review. Tekton engineers and contributors will confirm the
document’s technical accuracy, while a technical writer will polish the style, tone, and structure of
the document.

## How can I learn more?

Take a look at the [Google Developer Style Guide](https://developers.google.com/style/). It covers
style, tone, grammar, and punctuation. Also, ask @sergetron for reading recommendations!
