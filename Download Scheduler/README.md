# AutoFetch — Browser-Based Download Scheduler

AutoFetch is a zero-dependency, high-performance client-side utility that automates and schedules file downloads directly in the browser. Built with a lightweight vanilla web stack, it features a real-time countdown engine, local persistence, an activity logging system, and an integrated Gemini-powered AI assistant that contextualizes itself with your active schedule list.

---

## Key Features

- 📅 **Flexible Recurrence Scheduling** — Schedule downloads by exact times with repeat options for daily intervals, business weekdays (Mon-Fri), weekends, or specific days of the week.
- ⏱️ **Real-Time Countdown Engine** — Active scheduler items display dynamic, ticking countdown badges showing the exact hours, minutes, and seconds until the next download attempt.
- 📋 **Comprehensive Activity Log** — Instant system feedback logging successful runs, manual triggers, scheduling modifications, and pause state toggles. Keep track of up to 50 events locally.
- 🤖 **Contextual AI Chatbot** — An on-screen assistant equipped with two operating modes:
  - **Live Google Gemini API Integration:** Seamless connection to `gemini-2.5-flash` using a secure, client-side API key stored locally in your browser. It is fully aware of your scheduled tasks, URLs, and timing.
  - **Intelligent Offline Fallback:** A smart local responder that handles core scheduler controls, offers user guides, and returns offline status lists when a remote key is not provided.
- 🔒 **Privacy-First & Secure** — All configuration schedules, activity logs, and Gemini API keys reside purely in the client's `localStorage`. No intermediate databases, no trackers, and no external tracking servers.
- 🎨 **Premium UI/UX Design** — A modern, fully responsive dashboard designed around a dark-theme system. Includes custom sliding toggle controls, fluid animations, dynamic scroll states, and responsive side panels.

---

## Technical Architecture & Lifecycle

AutoFetch operates entirely on client-side sandboxing, executing with zero backend dependencies. 

```
┌────────────────────────────────────────────────────────┐
│                      Web Browser                       │
│                                                        │
│   ┌──────────────────┐          ┌──────────────────┐   │
│   │   index.html     ├─────────►│    style.css     │   │
│   │ (DOM Structure)  │          │  (Responsive UX) │   │
│   └────────┬─────────┘          └──────────────────┘   │
│            │                                           │
│            ▼                                           │
│   ┌──────────────────┐          ┌──────────────────┐   │
│   │   scheduler.js   │◄─────────►   chatbot.js     │   │
│   │ (Task Engine &   │          │ (Gemini 2.5 API  │   │
│   │  Browser Alerts) │          │  Offline Engine) │   │
│   └────────┬─────────┘          └────────┬─────────┘   │
│            │                             │             │
│            ▼                             ▼             │
│   ┌──────────────────┐          ┌──────────────────┐   │
│   │   localStorage   │          │ Google Gemini API│   │
│   │  (Schedules,     │          │  (Secure Remote  │   │
│   │   Activity Logs) │          │   Integrations)  │   │
│   └──────────────────┘          └──────────────────┘   │
└────────────────────────────────────────────────────────┘
```

### 1. The Scheduling & Loop Mechanics
The core scheduler (`scheduler.js`) implements a precise, 1-second interval loop. On every tick, the engine:
1. Filters active tasks from `localStorage`.
2. Computes the target 24-hour timestamp based on the set user preferences.
3. Checks current calendar time and matches it against the item's custom recurrence rules (e.g., matching the current day indices `1` through `5` for weekdays).
4. Fires an automatic program-triggered simulated download when all matching criteria align at `ss === 0`.

### 2. Sandbox Safe Downloads
Because browser security policies prevent raw filesystem access from standard DOM pages, downloads are safely initiated using an simulated dynamic element lifecycle:
```javascript
const a = document.createElement('a');
a.href = task.url;
a.download = task.name;
document.body.appendChild(a);
a.click();
document.body.removeChild(a);
```
*Note: Depending on your browser settings, files will go directly to your designated downloads directory or prompt a "Save As" location dialog.*

### 3. Contextual Prompt Construction
When using the Gemini integration, the app generates a highly structured prompt context payload before making the API request. This injects the active state of your application directly into the AI's short-term context window:
```javascript
`You are AutoFetch Assistant — a highly capable...
 Application context:
 ${getScheduleContext()}
 
 User query: ${text}`
```

---

## File Structure

The project has been architected for quick loading, extreme reliability, and structural modularity:

```text
├── index.html       # Core page structure, layout view panels, and responsive widgets.
├── style.css        # The complete dark-mode design system, UI layout tokens, and transitions.
├── scheduler.js     # Scheduler loops, countdown math, task management, and logging.
└── chatbot.js       # Client chatbot logic, offline parser, and Google Gemini API bridge.
```

---

## Getting Started

### 1. Launching the App
AutoFetch requires no installation, npm packages, server setups, or build steps. Simply download the source and open the `index.html` file directly in any modern web browser:

```bash
# Clone the repository (or copy the files)
git clone https://github.com/your-username/autofetch.git

# Open index.html directly in Google Chrome, Brave, Safari, or Firefox
open index.html  # macOS
start index.html # Windows
xdg-open index.html # Linux
```

### 2. Setting Up the AI Assistant
By default, the assistant runs in **Offline Fallback Mode** to process basic setup instructions and display active queues. To activate the fully functional AI Assistant:
1. Click the **🔑 Key** button in the top header of the chat panel.
2. Enter a valid **Google Gemini API Key**. If you don't have one, click the link inside the panel to get one for free from Google AI Studio.
3. Click **Save**. The badge will change to a green **🔑 Key (Set)** indicator, and your connection is validated immediately.

---

## Production Configurations

For continuous scheduled tasks, make sure to adjust these browser behaviors:
- **Tab Sleeping/Suspension:** Modern browsers sleep inactive tabs to save memory. To ensure your schedules trigger reliably overnight, pin the AutoFetch tab or whitelist the page in your browser's performance settings (e.g., disable memory saver for the app's URL/origin).
- **Automatic Downloads Permission:** The browser might request permission to "Download multiple files" when a schedule runs for the first time. Select **Allow** to ensure future automated actions trigger silently.

---

## License

This project is open-source and licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it for personal and commercial workflows.
