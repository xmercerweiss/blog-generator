# blog-generator
 A Python script which converts a custom markdown document into a static HTML blog entry.

 This program is meant to be run locally on your web server in order to generate static
 HTML content based on a series of mardown documents containing the entry's formatting.
 It must be provided an HTML template for both your blog index page and each entry's 
 webpage. The given markdown document is only converted into the HTML content of the
 entry itself. (i.e. title, paragraphs, etc.)

 ## Metadata
 Below is a table of tokens which represent metadata within the defined markdown script.

 Each value may be set by beginning a new line with the token, followed by the assigned data.
 Each value may be used by simply placing its token in any portion of text.

| Token | Value |
| - | - |
| #! | The entry's title, "Untitled" by default |
| #? | The entry's date* |
| #$ | The entry's description, blank by default |
| #@ | The entry's author, "Anon" by default |

*NOTE: When left unset, the date of the entry will be defined as the date the program
is converting the markdown document into HTML, _not_ necessarily the date it was written.
All dates must be entered in YYYY-MM-dd format.

## Operations
Below is a table of tokens which represent operations/formatting within the defined 
markdown script.

Each operation must be used by beginning a new line with the token followed by a space,
then space-deliminated arguments. The output of an operation may be given as an argument
to another operation using the nesting operator. (See example page.)

| Token | Arguments | Operation |
| - | - | - |
| #1 through #6 | _text_ | Encloses the given text with HTML tags h1 through h6, respectively |
| #/ | _text_ | Italicizes the given text |
| #* | _text_ | Bolds the given text |
| #= | _link_, _text_ | Creates an anchor tag with an href of _link_ and contents of _text_ |
| #+ | __None__ | Opens a new p tag |
| #- | __None__ | Closes the last p tag | 
| #~ | __None__ | Replaced with an hr tag |
| #n | __None__ | Replaced with a br tag |
| ## | __None__ | Comments out the entire line |
| #& | _operator_, _args_ | The nesting operator. Used to pass the output of an operation as the argument of another operation |

## Example
Below is an example of the defined markdown script and resulting page contents.

```
#! An example page...
#$ This is an example of the blog-generator markdown script
#? 2025-02-04
#@ Xavier Mercerweiss

#1 #!
#3 #& #/ #$
#4 Published on #? by #@

#~

#+
This article is a test page for the blog-generator markdown script. It's
#/ pretty cool
isn't it?
#-
```

This document would be converted to the following HTML.

```html
<h1>An example page...</h1>
<h3><em>This is an example of the blog-generator markdown script</em></hr>
<h4>Published on Feb. 4th, 2025 by Xavier Mercerweiss</h4>

<hr>

<p>
   This article is a test page for the blog-generator markdown
   script. It's <em>pretty cool</em> isn't it?
</p>
```

And is, without CSS, rendered as the following image.

![image](media/rendered.png)

## Configuration
The script's CONF file must be set before entries may be generated. It's assumed that the script
is running directly on your web server, so all "local paths" are the relative paths to the content
on the server from the script. Below is a table of all needed configuration values.

| Key | Value |
| - | - |
| _entry_domain_format_ | The link through which domains will be referenced. e.g. for entries linked at `my.site/blog/1`, `my.site/blog/2`, this would be set to `my.site/blog`|