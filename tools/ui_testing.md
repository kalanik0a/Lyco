# UI Testing Notes (Qt5)

Automated DAST-style UI testing for Qt5 is possible with:
- `pytest-qt` (signals/slots, Qt event loop integration)
- `pyautogui` or OS-native tools for end-to-end GUI driving

This repo currently **does not** include UI-driving tests because:
- The GUI requires a display server (not stable in CI).
- Cross-platform GUI automation is brittle.

If you want to add UI tests:
- Add `pytest-qt` to `requirements-dev.txt`.
- Create smoke tests for opening/closing the GUI.
- Gate them behind `RUN_GUI_TESTS=1`.
