# FOSSEE Workshop Booking

A workshop booking portal for coordinators to propose and track workshops run by IIT Bombay's FOSSEE group. Instructors accept proposals, coordinators track status. Built with Django 3, Bootstrap 4, and vanilla JS.

---

## Project Structure

```
workshop_booking-master/
├── .coveragerc
├── .gitignore
├── .sampleenv
├── .travis.yml
├── LICENSE
├── README.md
├── manage.py
├── requirements.txt
├── local_settings.py
│
├── cms/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── cms_base.html              ← UPDATED
│
├── docs/
│   ├── Getting_Started.md
│   └── ModelsTable_Diagram.jpg
│
├── statistics_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_views.py
│   └── templates/
│       └── statistics_app/
│           ├── paginator.html         ← UPDATED
│           ├── profile_stats.html     ← UPDATED
│           ├── team_stats.html        ← UPDATED
│           ├── workshop_public_stats.html  ← UPDATED
│           └── workshop_stats.html    ← UPDATED
│
├── teams/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── workshop_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                       ← UPDATED
│   ├── models.py
│   ├── reminder_script.py
│   ├── reminder_script.sh
│   ├── send_mails.py
│   ├── urls.py
│   ├── urls_password_reset.py
│   ├── views.py                       ← UPDATED
│   ├── logs/
│   │   └── emailconfig.yaml
│   ├── migrations/
│   │   └── (0001–0015 + __init__.py)
│   ├── static/
│   │   ├── cms/
│   │   │   ├── css/bootstrap.min.css
│   │   │   └── js/(bootstrap, jquery, popper)
│   │   └── workshop_app/
│   │       ├── css/
│   │       │   ├── base.css           ← UPDATED (full design system)
│   │       │   ├── bootstrap.min.css
│   │       │   ├── font-awesome.css
│   │       │   ├── jquery-ui.css
│   │       │   └── toastr.min.css
│   │       ├── fonts/  (unchanged)
│   │       ├── img/    (unchanged)
│   │       └── js/
│   │           ├── app.js             ← NEW FILE
│   │           ├── bootstrap.min.js
│   │           ├── datepicker.js
│   │           ├── jquery-3.4.1.min.js
│   │           ├── jquery-3.4.1.slim.min.js
│   │           ├── jquery-1.12.4.js
│   │           ├── jquery-ui.min.js
│   │           ├── jquery.formset.js
│   │           ├── jquery.js
│   │           ├── popper.min.js
│   │           └── toastr.min.js
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── custom_filters.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   └── test_views.py
│   └── templates/
│       ├── registration/
│       │   ├── password_change_done.html    ← UPDATED
│       │   ├── password_change_form.html    ← UPDATED
│       │   ├── password_reset_complete.html ← UPDATED
│       │   ├── password_reset_confirm.html  ← UPDATED
│       │   ├── password_reset_done.html     ← UPDATED
│       │   └── password_reset_form.html     ← UPDATED
│       └── workshop_app/
│           ├── activation.html         ← UPDATED
│           ├── add_workshop_type.html  ← UPDATED
│           ├── base.html               ← UPDATED
│           ├── edit_profile.html       ← UPDATED
│           ├── edit_workshop_type.html ← UPDATED
│           ├── login.html              ← UPDATED
│           ├── logout.html             ← UPDATED
│           ├── propose_workshop.html   ← UPDATED
│           ├── register.html           ← UPDATED
│           ├── view_profile.html       ← UPDATED
│           ├── workshop_details.html   ← UPDATED
│           ├── workshop_status_coordinator.html ← UPDATED
│           ├── workshop_status_instructor.html  ← UPDATED
│           ├── workshop_type_details.html       ← UPDATED
│           └── workshop_type_list.html          ← UPDATED
│
└── workshop_portal/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── views.py
    └── wsgi.py
```

---

## Setup Instructions

### Prerequisites

- Python 3.7+
- pip
- virtualenv (recommended)

### Installation

```bash
# 1. Clone / extract the project
git clone https://github.com/FOSSEE/workshop_booking.git
cd workshop_booking-master

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate          # Linux/macOS
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure local settings
# Copy .sampleenv to .env and fill in DB and email credentials
# Edit local_settings.py with your email server details

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start development server
python manage.py runserver
```

### Admin Setup

```
localhost:8000/admin
```

1. Create a Group named **instructor** and grant all permissions.
2. Set user profile `position` to `instructor` in Profile admin.
3. Add instructor users to the **instructor** group.
4. Create a CMS Page with title matching `HOME_PAGE_TITLE` in `settings.py` for a custom home page.

### Environment Variables (.env / local_settings.py)

| Variable | Description |
|---|---|
| `EMAIL_HOST` | SMTP server hostname |
| `EMAIL_PORT` | SMTP port (usually 587) |
| `EMAIL_HOST_USER` | Sender email address |
| `EMAIL_HOST_PASSWORD` | Sender email password |
| `EMAIL_USE_TLS` | `True` for TLS |
| `SENDER_EMAIL` | From address in emails |
| `DB_ENGINE` | Database engine (default: `sqlite3`) |
| `DB_NAME` | Database name or path |

---

## UI/UX Improvements Made

### Design System (`base.css`)

- **CSS custom properties**: Full token system for color, spacing, radius, shadow — every component derives from these variables, making global theme changes a single-line edit.
- **Sticky footer**: Replaced `position: fixed` (which overlapped content) with a CSS flexbox sticky footer using `flex: 1` on `.base-content`.
- **Typography scale**: Three clear levels — page heading (22px/700), section title (11px/700 uppercase), body (15px/400).
- **Card system**: Unified `.card`, `.card-header`, `.card-body` overrides that match the design language.
- **Badge redesign**: Coloured pill badges using background + text from the same color family (no raw Bootstrap defaults).
- **Table improvements**: `th` with uppercase tracking, `td` with proper vertical alignment, hover states.
- **Workshop card grid**: CSS Grid responsive layout — 1 column on mobile, 2 at 576px, 3 at 900px.
- **Mobile status cards** (`.status-card`): Card-list layout for workshop tables on narrow screens — replaces overflowing tables.
- **Empty state component** (`.empty-state`): Centered icon, heading, description, and CTA — replaces deprecated Bootstrap jumbotron.
- **Comment cards**: Structured author/date/body layout with consistent spacing.
- **Form controls**: 1.5px border, 10px padding, focus ring with box-shadow, `is-invalid` state.
- **Mobile nav touch targets**: 44×44px minimum per WCAG 2.1 SC 2.5.5, full-width padded links in collapsed state.

### JavaScript (`app.js`)

- **Double-submit prevention**: Global `submit` event listener disables the button and shows a spinner. Resets after 10s as a failsafe.
- **Active nav highlighting**: Compares `window.location.pathname` against each nav link `href` and adds `.active-page` class.
- **Auto-dismiss alerts**: Fades out and removes `role="alert"` elements after 5 seconds.
- **Accept modal wiring**: Sets the `href` on the confirm link using `data-base-url` + `data-workshop-id` attributes.
- **Native date constraints**: Sets `min`/`max` on `#id_date` from JavaScript — no jQuery UI datepicker needed.
- **T&C fetch**: Replaces jQuery AJAX with native `fetch()` API, shows spinner while loading, handles errors gracefully.

### Templates

| Template | Key changes |
|---|---|
| `base.html` | `lang="en"`, scripts end of body, preconnect for fonts, footer inside `<body>`, accessible navbar |
| `login.html` | Centered card, proper label association, forgot-password inline, prominent register CTA |
| `register.html` | Sectioned into 3 groups, all fields with `<label>` + help text + per-field errors |
| `propose_workshop.html` | Native `type="date"` (kills jQuery UI), visible labels, T&C Bootstrap modal |
| `workshop_type_list.html` | Card grid replaces table, empty state, fixed pagination bug (`workshoptype` → `workshop_type`) |
| `workshop_status_*.html` | Mobile card + desktop table dual layout, `<tbody>` outside loop, Bootstrap modal replaces `confirm()` |
| `workshop_details.html` | Semantic comment cards, accessible form labels |
| `view_profile.html` | Removed nested `<form>` tags and stray `{% csrf_token %}`, `<label>` misuse replaced with `<dl>` |
| `edit_profile.html` | `{% url %}` tag replaces hardcoded `URL_ROOT`, `<center>` removed |
| `activation.html` | Empty-state layout replaces jumbotron, clear status messages |
| All password pages | Consistent card layout, proper field loops, no JS-retrofit of CSS classes |
| `workshop_public_stats.html` | Bootstrap modal replaces jQuery UI dialog for charts, mobile card list |
| `cms_base.html` | `lang="en"`, scripts end of body, sticky footer |

### `forms.py`

- `WorkshopForm.date` widget changed from `class="datepicker"` (jQuery UI) to `type="date"` (native OS picker).
- All form fields get `form-control` / `custom-select` class at widget level via `_add_form_control()` helper.
- Placeholder text and `autocomplete` attributes added for mobile autofill.
- Error messages made more user-friendly.

### `views.py`

- `propose_workshop` passes `min_date` / `max_date` ISO strings to template context.
- `messages.success/error/info/warning` used consistently throughout.
- `add_workshop_type` bug fixed (was passing class instead of instance to template on GET).
- `_workshop_date_context()` helper extracted to keep date logic DRY.

---

## Design Principles

### Mobile-First

Every layout decision starts from 375px (iPhone SE). Tables are hidden below `md` breakpoint and replaced with stacked card lists. The navbar collapses to a full-width drawer with 44px touch targets. Forms stack vertically. The CSS Grid for workshop cards starts at `1fr` and expands.

### Visual Hierarchy

Three typographic levels are enforced: `.page-heading` (22px bold), `.section-title` (11px uppercase tracking), body (15px). Color carries semantic meaning — green = accepted, amber = pending, red = error — never decorative.

### Accessibility

- `<html lang="en">` declared (WCAG 3.1.1 Level A).
- All form inputs have associated `<label>` elements with matching `for`/`id`.
- `role="alert"` on all error messages so screen readers announce them on submit.
- `aria-label` on all icon-only buttons.
- `aria-modal="true"` and `aria-labelledby` on all modals.
- `<footer>` moved inside `<body>` (was outside — invalid HTML).
- `<tbody>` moved outside `{% for %}` loops (was creating multiple tbody per table — invalid HTML).
- Nested `<form>` tags removed from `view_profile.html`.
- `<label>` misuse as data display containers replaced with `<dl>/<dt>/<dd>`.

### Performance

- All JS moved to end of `<body>` — no render-blocking scripts.
- Chart.js and jQuery UI only loaded on pages that need them (via `{% block extra-dependencies %}`).
- `rel="preconnect"` hints for Google Fonts.
- `fetch()` replaces jQuery AJAX for T&C loading (no extra library weight).
- Duplicate jQuery files noted (4 versions in `/static/js/`) — only `jquery-3.4.1.min.js` is loaded in `base.html`; the others remain in `/static` but are not referenced.

---

## Trade-offs

| Decision | Reason | Trade-off |
|---|---|---|
| Kept Bootstrap 4 (not 5) | Avoid rebuild; stay within "improve not rebuild" constraint | Carry deprecated `mr-auto`, `jumbotron` references in old code; Bootstrap 5 utility API unavailable |
| Native `type="date"` vs jQuery UI datepicker | Universal mobile support, zero JS dependency | Cannot prevent weekends at the browser level (weekend exclusion is server-side validated) |
| Dual view (mobile cards + desktop table) | Clean mobile UX without removing table for desktop users | Slight HTML duplication; both rendered and CSS `d-none/d-md-block` controls visibility |
| Django templates (not React) | The project is a Django app with server-side rendering; converting to React would require rebuilding the entire backend API layer | No client-side routing, no component reuse across pages |
| `fetch()` for T&C (no error retry) | Keeps JS minimal | On network failure user must click again; no exponential back-off |

---

## Challenges and Solutions

**Challenge 1: Footer overlapping content**
`position: fixed` on the footer caused buttons and submit controls at the bottom of forms to be permanently obscured on mobile. Solution: replaced with CSS flexbox sticky footer — `body { display: flex; flex-direction: column; min-height: 100vh }` + `flex: 1` on `.base-content` + `margin-top: auto` on footer.

**Challenge 2: jQuery UI datepicker on mobile**
The jQuery UI calendar opens at a fixed pixel size, ignores viewport, and requires precise finger taps for month navigation. Solution: switched `WorkshopForm.date` widget to `type="date"` which delegates to the native OS date picker. Min/max constraints previously set by the datepicker are now set via JavaScript on page load in `app.js`.

**Challenge 3: `confirm()` dialog blocked on mobile**
Many mobile browsers in secure contexts block or silently dismiss `window.confirm()`. The instructor accept button used `onclick="return confirm(...)"`. Solution: replaced with a proper Bootstrap modal with a confirm button whose `href` is dynamically set via `data-workshop-id` attribute and the `show.bs.modal` event.

**Challenge 4: Multiple `<tbody>` tags from Django `{% for %}` loops**
Every table had `<tbody>` inside the `{% for %}` loop, creating N tbody elements. Bootstrap's `table-striped` doesn't work correctly with multiple tbodies, and some browsers produce inconsistent row rendering. Solution: moved `<tbody>` outside all `{% for %}` loops across all 4 affected templates.

**Challenge 5: Pagination typo breaking navigation**
`workshop_type_list.html` used `workshoptype.has_previous` (no underscore) while the view context variable is `workshop_type`. The "Previous" page link never appeared. Solution: corrected to `workshop_type.has_previous`.

**Challenge 6: Nested `<form>` tags in `view_profile.html`**
The template had two nested `<form action="" method="post">` tags with two `{% csrf_token %}` tags. This is invalid HTML — browsers parse it inconsistently and Safari drops the inner form's POST data. Solution: removed the outer form wrapper entirely.

---

## Screenshots to Include in README

Capture at 375px (iPhone SE) and 1280px (desktop) for each:

| # | Screen | What it shows |
|---|---|---|
| 1 | Login page (mobile, before/after) | Centered card, prominent CTAs, proper input styling |
| 2 | Registration form (mobile, before/after) | `form.as_table` raw → sectioned form with labels |
| 3 | Workshop types list (desktop, before/after) | Plain table → card grid with hover |
| 4 | Workshop status (mobile, before/after) | 6-column overflow table → stacked cards |
| 5 | Propose workshop form (mobile, before/after) | jQuery UI datepicker → native date input |
| 6 | Empty state (before/after) | Bootstrap jumbotron → empty-state with CTA |

Use Chrome DevTools Device Toolbar (Ctrl+Shift+M), set to "iPhone SE" (375×667) for mobile captures.

## After
# 1. Login 
# Desktop
<img width="1152" height="788" alt="image" src="https://github.com/user-attachments/assets/4f108651-a775-4644-8b6d-fa39133a6e16" />
# Mobile
<img width="739" height="1026" alt="image" src="https://github.com/user-attachments/assets/b8fbaac4-2ec3-45a6-a539-c23d83797155" />
# 2. Registration desktop
# 3. Workshop types desktop
# 4. Workshop status desktop
# 5. Propose workshop desktop
# 6. Empty state desktop
# 7. 


