# To Do

refactor: Replace unintended continuous text translation with a translate command in the right-click context menu

    Before this refactor, highlighted text is translated continuously, causing significant slowdown.

    After this refactor, the user can translate highlighted text with a command in the context menu.

feat: Remove langdetect

    Remove langdetect to make way for adding "Input Language" and "Output Language" OptionMenus next.

refactor: Replace "Translation" OptionMenu with "Input Language" and "Output Language" OptionMenus

    Support only Enlgish (en), Korean (ko), and Japanese (ja) for the time being.

fix: Fix issue in which the right-click context menu does not behave as expected.

    Before this fix, when the user clicks outside of an open context menu, a new menu appears.

    After this fix, clicking outside of an open context menu closes the menu.
 