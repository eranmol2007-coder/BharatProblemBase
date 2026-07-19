let geminiApiKey = localStorage.getItem("gemini_api_key") || "";

function getScheduleContext() 
{
  if (!tasks || tasks.length === 0) return "The user has no download schedules set up yet.";
  return "Current schedules:\n" + tasks.map(t =>
    `- "${t.name}" | URL: ${t.url} | Time: ${t.displayTime || t.time} | Days: ${daysLabel(t.days)} | Status: ${t.active ? 'Active' : 'Paused'}`
  ).join("\n");
}

// ── API Key Panel & Management ─────────────────────
function toggleKeySettings() {
  const panel = document.getElementById("api-key-panel");
  if (panel.style.display === "none") {
    panel.style.display = "block";
    document.getElementById("api-key-input").focus();
  } else {
    panel.style.display = "none";
  }
}

function saveApiKey() {
  const input = document.getElementById("api-key-input");
  const key = input.value.trim();
  const btn = document.getElementById("api-key-btn");
  
  if (key) {
    localStorage.setItem("gemini_api_key", key);
    geminiApiKey = key;
    btn.innerHTML = `<span style="display:inline-flex; align-items:center; gap:3px; color: var(--green);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:10px; height:10px;"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3M15.5 7.5L14 9M18.5 4.5L17 6"/></svg> Key (Set)</span>`;
    appendBotBubble("<strong>System:</strong> Gemini API Key saved successfully! I am now connected to the live Google Gemini API. 🚀", true);
  } else {
    localStorage.removeItem("gemini_api_key");
    geminiApiKey = "";
    btn.innerHTML = `<span style="display:inline-flex; align-items:center; gap:3px;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:10px; height:10px;"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3M15.5 7.5L14 9M18.5 4.5L17 6"/></svg> Key</span>`;
    appendBotBubble("<strong>System:</strong> API Key removed. Reverting to local offline assistant mode.", true);
  }
  document.getElementById("api-key-panel").style.display = "none";
}

function initApiKey() {
  const input = document.getElementById("api-key-input");
  const btn = document.getElementById("api-key-btn");
  if (geminiApiKey) {
    input.value = geminiApiKey;
    btn.innerHTML = `<span style="display:inline-flex; align-items:center; gap:3px; color: var(--green);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:10px; height:10px;"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3M15.5 7.5L14 9M18.5 4.5L17 6"/></svg> Key (Set)</span>`;
  }
}

// ── Drawer Toggle ──────────────────────────────────
function toggleCopilot() {
  const panel = document.getElementById("chat-panel");
  const floatingBtn = document.getElementById("floating-chat-trigger");
  const navItem = document.getElementById("nav-copilot-toggle");
  
  const isCollapsed = panel.classList.toggle("collapsed");
  localStorage.setItem("copilot_collapsed", isCollapsed ? "true" : "false");
  
  if (isCollapsed) {
    floatingBtn.classList.add("visible");
    if (navItem) navItem.classList.remove("active");
  } else {
    floatingBtn.classList.remove("visible");
    if (navItem) navItem.classList.add("active");
  }
}

function initCopilotCollapse() {
  const collapsed = localStorage.getItem("copilot_collapsed");
  const panel = document.getElementById("chat-panel");
  const floatingBtn = document.getElementById("floating-chat-trigger");
  const navItem = document.getElementById("nav-copilot-toggle");
  
  if (collapsed === "true" || collapsed === null) {
    panel.classList.add("collapsed");
    floatingBtn.classList.add("visible");
    if (navItem) navItem.classList.remove("active");
  } else {
    panel.classList.remove("collapsed");
    floatingBtn.classList.remove("visible");
    if (navItem) navItem.classList.add("active");
  }
}

// ── Send Message ────────────────────────────────────
async function sendMessage() 
{
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;

  input.value = '';
  hideSuggestions();
  appendUserBubble(text);
  const typingEl = appendTyping();

  document.getElementById('send-btn').disabled = true;

  if (geminiApiKey) {
    try {
      const url = new URL("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent");
      url.searchParams.set("key", geminiApiKey);

      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: `You are AutoFetch Assistant — a highly capable, intelligent AI companion built into a file download scheduler web app.
                     You help users manage scheduled downloads, explain how the app works, and act as a general-purpose AI assistant answering any questions.
                     Keep answers concise, helpful, and formatted beautifully using markdown (bolding, lists, code snippets). Keep the tone friendly and professional.
                     
                     Application context (reference this if the user asks about schedules or downloads):
                     ${getScheduleContext()}
                     
                     User query: ${text}`
            }]
          }]
        })
      });

      const data = await response.json();
      typingEl.remove();

      if (response.ok && data?.candidates?.[0]?.content?.parts?.[0]?.text) {
        let reply = data.candidates[0].content.parts[0].text;
        reply = parseMarkdown(reply);
        appendBotBubble(reply, true);
      } else {
        const errMsg = data?.error?.message || "Invalid API key or model response. Please check your API key settings.";
        appendBotBubble(`<strong>Error:</strong> ${escChat(errMsg)}`, true);
      }
    } catch (err) {
      typingEl.remove();
      appendBotBubble("<strong>Connection Error:</strong> Unable to connect to Gemini API. Please verify your internet connection or check if your API Key is valid.", true);
    }
  } else {
    // Simulated smart offline fallback response
    setTimeout(() => {
      typingEl.remove();
      const reply = getAIResponse(text);
      appendBotBubble(reply, true);
    }, 600 + Math.random() * 400);
  }

  document.getElementById('send-btn').disabled = false;
}

// ── Markdown Parser ──────────────────────────────────
function parseMarkdown(text) {
  let html = String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // Bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');

  // Italic
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  html = html.replace(/_(.*?)_/g, '<em>$1</em>');

  // Inline code
  html = html.replace(/`(.*?)`/g, '<code style="background: var(--bg-input); padding: 2px 6px; border-radius: 4px; font-family: var(--mono); font-size: 0.9em; border: 1px solid var(--border);">$1</code>');

  // Multi-line code blocks
  html = html.replace(/```([\s\S]*?)```/g, '<pre style="background: var(--bg-input); padding: 12px; border-radius: var(--radius); font-family: var(--mono); font-size: 0.85em; border: 1px solid var(--border); overflow-x: auto; margin: 8px 0; white-space: pre-wrap; word-break: break-all;"><code>$1</code></pre>');

  // Line breaks
  html = html.replace(/\n/g, '<br>');

  return html;
}

// ── Local AI Smart Fallback Responder ─────────────────
function getAIResponse(text) 
{
  const query = text.toLowerCase().trim();

  const escapeHTML = (str) => {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  };

  // 1. Add schedule
  if (
    query.includes("add") || 
    query.includes("create") || 
    query.includes("new schedule") || 
    query.includes("how to use") || 
    query.includes("schedule a download") ||
    query.includes("how do i add")
  ) {
    return `To schedule a new download, follow these simple steps:<br><br>
1. <strong>Display name</strong>: Enter a friendly name for your download (e.g., <em>Daily Backup</em>).<br>
2. <strong>File URL</strong>: Paste the direct download link of the file.<br>
3. <strong>Download time</strong>: Select the hour, minute, and AM/PM when you want the download to trigger.<br>
4. <strong>Repeat on</strong>: Choose how often you want it to repeat (e.g., Every day, Weekdays, or weekends).<br>
5. Click <strong>Add Schedule</strong>.<br><br>
Once scheduled, as long as this browser tab remains open, the app will automatically download the file at the set time!`;
  }

  // 2. Supported files
  if (
    query.includes("file type") || 
    query.includes("extension") || 
    query.includes("support") || 
    query.includes("pdf") || 
    query.includes("xlsx") || 
    query.includes("csv") || 
    query.includes("zip") || 
    query.includes("what file")
  ) {
    return `AutoFetch supports <strong>any file type</strong>! Since it initiates the download directly through your browser, you can schedule:<br><br>
• <strong>Spreadsheets & Docs</strong>: PDF, XLSX, CSV, DOCX, TXT<br>
• <strong>Compressed Archives</strong>: ZIP, RAR, 7Z, TAR.GZ<br>
• <strong>Media Files</strong>: PNG, JPG, MP4, MP3, WAV<br>
• <strong>Executables</strong>: EXE, DMG, MSI<br><br>
Just ensure the URL you provide is a direct link that prompts a download immediately when visited.`;
  }

  // 3. How to test
  if (
    query.includes("test") || 
    query.includes("how do i test") || 
    query.includes("try it") || 
    query.includes("manual") || 
    query.includes("work")
  ) {
    return `To test a scheduled download immediately without waiting for the scheduled time:<br><br>
Find your scheduled download in the <strong>"Scheduled downloads"</strong> list, and click the <strong>Download now</strong> button (the tray-arrow icon) on the right side of the card.<br><br>
This will trigger the browser to start downloading the file immediately, allowing you to confirm that the URL works!`;
  }

  // 4. Show active schedules
  if (
    query.includes("show my active") || 
    query.includes("show schedule") || 
    query.includes("list schedule") || 
    query.includes("current schedule") || 
    query.includes("active schedule") || 
    query.includes("my schedule") || 
    query.includes("status")
  ) {
    if (!tasks || tasks.length === 0) {
      return `You currently have <strong>no scheduled downloads</strong> set up. Feel free to add one using the scheduler form on the left!`;
    }

    const scheduleList = tasks.map(t => {
      const statusIcon = t.active ? "🟢 Active" : "🟡 Paused";
      const countdownStr = t.active ? ` (Next run: ⏱ ${getCountdown(t.time)})` : '';
      return `• <strong>${escapeHTML(t.name)}</strong><br>
&nbsp;&nbsp;⏰ Time: ${t.displayTime || formatTime(t.time)} · ${daysLabel(t.days)}<br>
&nbsp;&nbsp;⚡ Status: ${statusIcon}${countdownStr}<br>
&nbsp;&nbsp;🔗 Link: <a href="${escapeHTML(t.url)}" target="_blank" style="color: var(--accent); text-decoration: none; word-break: break-all;">${escapeHTML(t.url)}</a>`;
    }).join("<br><br>");

    return `Here are your current download schedules:<br><br>${scheduleList}`;
  }

  // 5. Delete, Pause, Resume, Controls
  if (
    query.includes("delete") || 
    query.includes("remove") || 
    query.includes("pause") || 
    query.includes("stop") || 
    query.includes("resume") || 
    query.includes("start") || 
    query.includes("turn off") || 
    query.includes("turn on") || 
    query.includes("toggle")
  ) {
    return `You can easily manage any scheduled download using the action buttons on the right side of its card:<br><br>
• <strong>Pause/Resume</strong>: Use the green/yellow toggle switch to enable or disable the schedule.<br>
• <strong>Download Now</strong>: Click the tray-arrow icon to run the download manually right now.<br>
• <strong>Delete</strong>: Click the trash icon to permanently remove the schedule.`;
  }

  // 6. Log / history
  if (
    query.includes("log") || 
    query.includes("history") || 
    query.includes("activity") || 
    query.includes("track")
  ) {
    return `Every download event is logged automatically! You can view the list of downloads by clicking <strong>Activity Log</strong> in the left sidebar.<br><br>
The badge on the sidebar will show you how many new events have occurred. To clear the log, simply open the Activity Log panel and click the **Clear log** button in the top right.`;
  }

  // 7. Greeting
  if (
    query.includes("hello") || 
    query.includes("hi") || 
    query.includes("hey") || 
    query.includes("greetings") || 
    query.includes("morning") || 
    query.includes("afternoon") || 
    query.includes("yo")
  ) {
    return `Hello! 👋 I'm your AutoFetch AI Assistant. I can help you with anything related to scheduling and managing your file downloads.<br><br>
How can I assist you today?`;
  }

  // 8. General AI / chatbot response fallback
  return `I'm here to help you manage your downloads with AutoFetch! 
Otherwise, feel free to ask me about AutoFetch:<br>
• <em>"How do I add a new schedule?"</em><br>
• <em>"Show my active schedules"</em><br>
• <em>"How do I test my downloads?"</em><br>
• <em>"What file types are supported?"</em>`;
}

function sendSuggestion(btn) 
{
  document.getElementById('chat-input').value = btn.textContent;
  sendMessage();
}

function hideSuggestions() 
{
  const s = document.getElementById('chat-suggestions');
  if (s) s.style.display = 'none';
}

function appendUserBubble(text) 
{
  const box = document.getElementById('chat-messages');
  const el = document.createElement('div');
  el.className = 'chat-bubble user';
  el.innerHTML = `
    <div class="bubble-avatar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
      </svg>
    </div>
    <div class="bubble-content">${escChat(text)}</div>
  `;
  box.appendChild(el);
  box.scrollTop = box.scrollHeight;
}

function appendBotBubble(text, isHTML = false) 
{
  const box = document.getElementById('chat-messages');
  const el = document.createElement('div');
  el.className = 'chat-bubble bot';
  el.innerHTML = `
    <div class="bubble-avatar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9.813 15.904L9 21L8.188 15.904L3 15L8.188 14.096L9 9L9.813 14.096L15 15L9.813 15.904Z"/>
      </svg>
    </div>
    <div class="bubble-content">${isHTML ? text : escChat(text)}</div>
  `;
  box.appendChild(el);
  box.scrollTop = box.scrollHeight;
}

function appendTyping() 
{
  const box = document.getElementById('chat-messages');
  const el = document.createElement('div');
  el.className = 'chat-bubble bot';
  el.innerHTML = `
    <div class="bubble-avatar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9.813 15.904L9 21L8.188 15.904L3 15L8.188 14.096L9 9L9.813 14.096L15 15L9.813 15.904Z"/>
      </svg>
    </div>
    <div class="bubble-content">
      <div class="typing-dots">
        <span></span><span></span><span></span>
      </div>
    </div>
  `;
  box.appendChild(el);
  box.scrollTop = box.scrollHeight;
  return el;
}

function clearChat() 
{
  const box = document.getElementById('chat-messages');
  box.innerHTML = `
    <div class="chat-bubble bot">
      <div class="bubble-avatar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9.813 15.904L9 21L8.188 15.904L3 15L8.188 14.096L9 9L9.813 14.096L15 15L9.813 15.904Z"/>
        </svg>
      </div>
      <div class="bubble-content">Chat cleared! How can I help you today?</div>
    </div>
  `;
  document.getElementById('chat-suggestions').style.display = 'flex';
}

function escChat(s) 
{
  return String(s)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/\n/g,'<br>');
}

// Initialize on page load
initApiKey();
initCopilotCollapse();