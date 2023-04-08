# To Do (Next)

feat: Add image to text transcription.

    Add simple image to text transcription using an open source optical character recognition tool (OCR).

    Does not have to be perfect! More To Dos to follow after the first successful transcription.

feat: Add an A.I. chat bot. 

    Add a simple A.I. chat bot using an open source large language model (LLM).  

    Does not have to be perfect! More To Dos to follow after the first successful  

# Planned Features/Refactors Etc. (Less Detail than To Do, will become To Do list next)

Add support for as many text, image, audio, and video files as possible both from file on local machine and from link to a source on the web.

Add loading message and animation, including a screen for when the program is first loading up.

Optimize GUI. (layout, how things move when the user zooms in and out, etc). Finalize a layout for first release.

Tweak A.I. chat bot as much as possible. Can it pretend to be a bird?

Finalize style and user hints. 

Make read me.

Make updateable and executable.

Make landing page.

Complete this by Friday, April 14th.

# Completed

fix/feat: Fix issue in which the right-click context menu does not behave as expected. Also, add Cut, Copy, and Paste features.

    Before this fix, when the user clicks outside of an open context menu, a new menu appears.

    After this fix, clicking outside of an open context menu closes the menu.

    Also, basic Cut, Copy, and Paste functionality have been added.

refactor: Replace "Translation" OptionMenu with "Input Language" and "Output Language" OptionMenus

    Support only Enlgish (en), Korean (ko), and Japanese (ja) for the time being.

feat: Remove langdetect

    Remove langdetect to make way for adding "Input Language" and "Output Language" OptionMenus next.

    lang_code = "en" for the time being.

refactor: Replace unintended continuous text translation with a translate command in the right-click context menu

    Before this refactor, highlighted text is translated continuously, causing significant slowdown.

    After this refactor, the user can translate highlighted text with a command in the context menu.