# Progress log

Session-by-session notes. Add a new dated section at the top when you work on the project.

---

## 2026-02-09

### Path events: Join, leave & discussion

- **Join / Leave**
  - Non-staff users can **join** and **leave** published path events (Define Your Path).
  - New model: `PathEventRegistration` (event, user, joined_at; unique per event+user).
  - Views: `path_event_join` and `path_event_leave` (POST only, `@login_required`). Join respects `max_participants`; full events show “This event is full.”
  - URLs: `define-your-path/event/<pk>/join/` and `.../leave/`.
  - Event detail page shows “Join event” / “Leave event” buttons and participant count (e.g. “You’re joined (3 / 10 participants)”). Anonymous users see “Log in to join this event or join the discussion.”

- **Event comments (discussion)**
  - New model: `PathEventComment` (event, author, content, created_at).
  - New form: `PathEventCommentForm` (content).
  - `path_event_detail` loads comments, shows a comment form for logged-in users, and handles POST to add a comment (redirect back to event detail).
  - Event detail template: “Discussion (N)” section with comment list and form; “Log in to join the discussion” when not logged in.

- **Migration**
  - `0009_patheventregistration_patheventcomment.py` — creates `PathEventRegistration` and `PathEventComment` tables. Run: `python manage.py migrate`.

### Diary comments (backend)

- **Models & forms**
  - `DiaryComment` (page FK, author FK, content, created_at) and `DiaryCommentForm` already in place.
  - `diary_page_detail` view updated to load comments, show comment form for logged-in users, and handle POST to save a comment.

- **Still to do**
  - Migration for `DiaryComment` (if not already applied).
  - In `diary_page_detail.html`: add comments list, comment form, and “Login to comment” for anonymous users.

---

## How to add to this file

1. Add a new `## YYYY-MM-DD` section at the top (below the “Progress log” title and the first `---`).
2. Use `###` for feature areas and bullets for specific changes.
3. Keep it short: what was built, key files or migrations, and any “still to do” for that area.
