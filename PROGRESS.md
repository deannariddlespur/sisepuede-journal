# Progress log

Session-by-session notes. Add a new dated section at the top when you work on the project.

---

## 2026-02-09

**Summary:** Path events (join/leave + comments), diary comments, non-staff “define yourself” (journal entries), home hero + “Define Yourself” CTA, clickable event cards, broken-image fallback sitewide, staff “New Entry” on Diary & Path, About page (staff-only edit), Railway media docs. Migrations: 0009, 0010, 0011.

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

### Diary comments

- **Models & forms**
  - `DiaryComment` (page FK, author FK, content, created_at) and `DiaryCommentForm` in place.
  - `diary_page_detail` view loads comments, comment form for logged-in users, POST to save comment.
- **Migration:** `0010_diarycomment.py` for `DiaryComment` table.
- **Template:** `diary_page_detail.html` — “Comments (N)” section with form for logged-in users, list of comments, “Log in to join the discussion” for guests. Non-staff can comment on public diary pages.

### Define yourself (non-staff journal entries)

- **Any logged-in user** can create, edit, and delete **their own** journal entries (not just staff).
- Views: `entry_create` is `@login_required`; `entry_edit` and `entry_delete` allow author or staff. `entry_toggle_publish` stays staff-only.
- Home and entries list: show published entries plus the current user’s own entries (including drafts). Entry detail viewable if published or user is author or staff.
- **UI:** “New Entry” in nav and “Create Your First Entry” / “Write your entry” on home and entries list for **all authenticated users**. Edit/delete dropdown on entry cards and detail for entry author or staff. (`base.html`, `home.html`, `entries_list.html`, `entry_detail.html`.)

### Home hero & CTA

- Hero: “Me Defino” with fly-in animation. Removed “I define myself” line.
- Replaced white header bar with a single **“Define Yourself”** button (serif, matches hero style, fly-in). Links to new entry when logged in, login when not. Correct capitals: “Define Yourself.”

### Path event cards

- **Whole event card** on Define Your Path (Upcoming Paths and Recent Paths) is clickable → event detail. Keyboard: Enter/Space on focused card. Staff edit/delete dropdown still works (stops propagation).

### Images

- Diary page images: if image fails to load (missing file, wrong URL), the image block is hidden via `onerror` so no broken [?] icon. Applied in `diary_page_detail.html`, `diary_list.html`, `diary_page_form.html`.

### Other

- **AGENT_BEHAVIOR.md** — local behavior file (do not commit). Instructs: when user asks to push to GitHub, run add/commit/push. File listed in `.gitignore`.

### Later session (same day)

- **Hero:** “I define myself” back under “Me Defino”; match size/style (2.5rem, uppercase, letter-spacing); fly-in with 0.4s delay.
- **Broken images:** `onerror` hide on all image usages — home, entries list, entry detail, entry form, path calendar, path event detail, landing, diary (already had). No broken [?] icon when file missing.
- **Staff add entries anywhere:** “+ New Entry” for staff on DeAnna’s Diary header (with “+ New Page”) and on Define Your Path hero (with “Create New Event”). Nav “New Entry” already on every page.
- **About page:** Public `/about/` page. Model `AboutPage` (single row: content, updated_at). Only staff can edit (form on page when staff, or via admin). Nav “About” for everyone. Migration: `0011_aboutpage.py`.
- **Media on Railway:** `RAILWAY_MEDIA.md` and `RAILWAY_VOLUME_MOUNT_PATH` in settings so uploads can persist on a volume.

---

## How to add to this file

1. Add a new `## YYYY-MM-DD` section at the top (below the “Progress log” title and the first `---`).
2. Use `###` for feature areas and bullets for specific changes.
3. Keep it short: what was built, key files or migrations, and any “still to do” for that area.
