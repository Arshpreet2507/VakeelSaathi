/* ══════════════════════════════════════════
   VAKEEL SAATHI — PREMIUM FRONTEND LOGIC
   ══════════════════════════════════════════ */

let currentLanguage = "en";
let latestCaseData = null;
let particleAnimId = null;

/* ───────── Translations ───────── */
const translations = {
  en: {
    heroBadge: "Legal clarity for the first 24 hours",
    heroTitle: 'Understand the situation.<br /><span>Know what happens next.</span>',
    heroSubtext: "A simple legal emergency assistant that helps families understand rights, next steps, and police procedure in plain language.",
    point1: "✅ Immediate guidance",
    point2: "✅ Simple language",
    point3: "✅ Situation-based help",
    checkerTitle: "Emergency Situation Checker",
    checkerSubtitle: "Answer 2 questions to get legal guidance instantly.",
    crimeLabel: "Select Offence",
    situationLabel: "Select Situation",
    mainBtn: "Get Legal Guidance",
    dashboardTitle: "Case Guidance Dashboard",
    dashboardSubtitle: "Your situation-specific legal summary appears below.",
    quick1: "Call Lawyer",
    quick2: "Bail Process",
    quick3: "Know Rights",
    quick4: "Emergency Help",
    quickSub1: "Get legal representation",
    quickSub2: "Understand bail steps",
    quickSub3: "Your fundamental rights",
    quickSub4: "Immediate assistance",
    aiTitle: "AI Case Explanation",
    aiBtn: "Explain This Case Simply",
    aiPlaceholder: "Click the button to get a simple case explanation.",
    riskTitle: "Legal Risk Meter",
    riskLow: "LOW",
    riskMedium: "MEDIUM",
    riskHigh: "HIGH"
  },
  hi: {
    heroBadge: "गिरफ्तारी के बाद पहले 24 घंटों के लिए कानूनी स्पष्टता",
    heroTitle: 'स्थिति को समझें।<br /><span>जानें आगे क्या होगा।</span>',
    heroSubtext: "एक सरल कानूनी सहायक जो परिवारों को उनके अधिकार, अगले कदम और पुलिस प्रक्रिया साधारण भाषा में समझाता है।",
    point1: "✅ तुरंत मार्गदर्शन",
    point2: "✅ सरल भाषा",
    point3: "✅ स्थिति आधारित सहायता",
    checkerTitle: "आपातकालीन स्थिति जाँच",
    checkerSubtitle: "तुरंत कानूनी मार्गदर्शन पाने के लिए 2 सवालों के उत्तर दें।",
    crimeLabel: "अपराध चुनें",
    situationLabel: "स्थिति चुनें",
    mainBtn: "कानूनी मार्गदर्शन प्राप्त करें",
    dashboardTitle: "केस मार्गदर्शन डैशबोर्ड",
    dashboardSubtitle: "आपकी स्थिति के अनुसार कानूनी सारांश नीचे दिखाया गया है।",
    quick1: "वकील से संपर्क",
    quick2: "जमानत प्रक्रिया",
    quick3: "अधिकार जानें",
    quick4: "आपात सहायता",
    quickSub1: "कानूनी प्रतिनिधित्व प्राप्त करें",
    quickSub2: "जमानत की प्रक्रिया समझें",
    quickSub3: "आपके मूल अधिकार",
    quickSub4: "तुरंत सहायता",
    aiTitle: "AI केस व्याख्या",
    aiBtn: "इस केस को सरल भाषा में समझाएँ",
    aiPlaceholder: "सरल केस व्याख्या प्राप्त करने के लिए बटन दबाएँ।",
    riskTitle: "कानूनी जोखिम मीटर",
    riskLow: "कम",
    riskMedium: "मध्यम",
    riskHigh: "उच्च"
  }
};

/* ───────── Language Toggle ───────── */
function setLanguage(lang) {
  currentLanguage = lang;
  document.getElementById("lang-en").classList.toggle("active", lang === "en");
  document.getElementById("lang-hi").classList.toggle("active", lang === "hi");

  const t = translations[lang];
  const setText = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.innerHTML = val;
  };

  setText("hero-badge", t.heroBadge);
  setText("hero-title", t.heroTitle);
  setText("hero-subtext", t.heroSubtext);
  setText("point1", t.point1);
  setText("point2", t.point2);
  setText("point3", t.point3);
  setText("checker-title", t.checkerTitle);
  setText("checker-subtitle", t.checkerSubtitle);
  setText("crime-label", t.crimeLabel);
  setText("situation-label", t.situationLabel);
  setText("main-btn", t.mainBtn);
  setText("dashboard-title", t.dashboardTitle);
  setText("dashboard-subtitle", t.dashboardSubtitle);
  setText("quick1", t.quick1);
  setText("quick2", t.quick2);
  setText("quick3", t.quick3);
  setText("quick4", t.quick4);
  setText("ai-title", t.aiTitle);
  setText("ai-btn", t.aiBtn);
  setText("ai-placeholder", t.aiPlaceholder);

  const subs = document.querySelectorAll(".quick-sub");
  if (subs.length >= 4) {
    subs[0].textContent = t.quickSub1;
    subs[1].textContent = t.quickSub2;
    subs[2].textContent = t.quickSub3;
    subs[3].textContent = t.quickSub4;
  }

  if (latestCaseData) renderCase(latestCaseData);
}

/* ───────── Risk Assessment ───────── */
function getRiskLevel(law) {
  if (!law.bailable && law.cognizable) return { level: "high", percent: 90 };
  if (law.bailable && law.cognizable) return { level: "medium", percent: 60 };
  return { level: "low", percent: 30 };
}

function getRiskLabel(level) {
  const t = translations[currentLanguage];
  if (level === "high") return t.riskHigh;
  if (level === "medium") return t.riskMedium;
  return t.riskLow;
}

function getRiskColor(level) {
  if (level === "high") return "#ef4444";
  if (level === "medium") return "#f59e0b";
  return "#3ddc97";
}

/* ───────── SVG Gauge Builder ───────── */
function buildGaugeHTML(risk, lawName, lawSection) {
  const t = translations[currentLanguage];
  const arcLength = 251.2;
  const fillAmount = arcLength * (risk.percent / 100);
  const color = getRiskColor(risk.level);
  const needleAngle = -90 + (risk.percent / 100) * 180;

  return `
    <h3>${t.riskTitle}</h3>
    <p class="risk-subtitle">${lawName} — ${lawSection}</p>
    <div class="risk-gauge-wrap">
      <div class="gauge-glow ${risk.level}"></div>
      <canvas id="riskParticles" width="260" height="160"></canvas>
      <svg class="risk-gauge-svg" viewBox="0 0 260 160">
        <path class="gauge-track"
              d="M 30 140 A 100 100 0 0 1 230 140" />
        <path class="gauge-fill"
              d="M 30 140 A 100 100 0 0 1 230 140"
              stroke="${color}"
              stroke-dasharray="${arcLength}"
              stroke-dashoffset="${arcLength - fillAmount}"
              id="gaugeFill" />
        <g class="gauge-needle" style="transform:rotate(${needleAngle}deg)">
          <line x1="130" y1="140" x2="130" y2="55" />
          <circle cx="130" cy="140" r="6" />
        </g>
      </svg>
      <div class="risk-value-label ${risk.level}">${getRiskLabel(risk.level)}</div>
    </div>
    <p class="risk-percent">${risk.percent}% Risk Score</p>
  `;
}

/* ───────── Particle Effect ───────── */
function startParticles(level) {
  if (particleAnimId) cancelAnimationFrame(particleAnimId);

  const canvas = document.getElementById("riskParticles");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const W = canvas.width;
  const H = canvas.height;
  const color = getRiskColor(level);
  const particles = [];

  for (let i = 0; i < 25; i++) {
    particles.push({
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 2 + 0.5,
      dx: (Math.random() - 0.5) * 0.6,
      dy: (Math.random() - 0.5) * 0.6,
      alpha: Math.random() * 0.5 + 0.2
    });
  }

  function animate() {
    ctx.clearRect(0, 0, W, H);
    for (const p of particles) {
      p.x += p.dx;
      p.y += p.dy;
      if (p.x < 0 || p.x > W) p.dx *= -1;
      if (p.y < 0 || p.y > H) p.dy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.globalAlpha = p.alpha;
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    particleAnimId = requestAnimationFrame(animate);
  }

  animate();
}

/* ───────── Render Case Dashboard ───────── */
function renderCase(data) {
  const resultDiv = document.getElementById("result");
  const resultHeader = document.getElementById("resultHeader");
  const aiSection = document.getElementById("aiSection");
  const chatSection = document.getElementById("chatSection");
  const t = translations[currentLanguage];

  resultHeader.classList.remove("hidden");
  aiSection.classList.remove("hidden");
  if (chatSection) chatSection.classList.remove("hidden");

  const risk = getRiskLevel(data.law);

  resultDiv.innerHTML = `
    <div class="card risk-meter-card">
      ${buildGaugeHTML(risk, data.law.offence_name, data.law.section)}
    </div>

    <div class="card large">
      <h3>Case Overview</h3>
      <p><strong>Offence:</strong> ${data.law.offence_name}</p>
      <p><strong>Section:</strong> ${data.law.section}</p>
      <p><strong>Explanation:</strong> ${data.law.plain_explanation}</p>
      <div class="badge-row">
        <span class="badge ${data.law.bailable ? "green" : "red"}">
          ${data.law.bailable ? "Bailable" : "Non-Bailable"}
        </span>
        <span class="badge ${data.law.cognizable ? "blue" : "green"}">
          ${data.law.cognizable ? "Cognizable" : "Non-Cognizable"}
        </span>
        <span class="badge blue">
          Arrest Possible: ${data.law.arrest_possible}
        </span>
      </div>
    </div>

    <div class="card medium">
      <h3>Immediate Situation</h3>
      <p><strong>${data.checklist ? data.checklist.title : "Situation Guidance"}</strong></p>
      <ul class="list">
        ${
          data.checklist?.immediate_steps
            ? data.checklist.immediate_steps.map(step => `<li>${step}</li>`).join("")
            : "<li>No checklist available.</li>"
        }
      </ul>
    </div>

    <div class="card medium">
      <h3>Next 2 Hours</h3>
      <ul class="list">
        ${data.law.next_2_hours.map(item => `<li>${item}</li>`).join("")}
      </ul>
    </div>

    <div class="card medium">
      <h3>Your Rights</h3>
      <ul class="list">
        ${data.rights.map(item => `<li><strong>${item.title}:</strong> ${item.plain_text}</li>`).join("")}
      </ul>
    </div>

    <div class="card medium">
      <h3>What Police Can Do</h3>
      <ul class="list">
        ${data.law.police_can_do.map(item => `<li>${item}</li>`).join("")}
      </ul>
    </div>

    <div class="card medium">
      <h3>What Police Cannot Do</h3>
      <ul class="list">
        ${data.law.police_cannot_do.map(item => `<li>${item}</li>`).join("")}
      </ul>
    </div>

    <div class="card medium">
      <h3>Documents Needed</h3>
      <ul class="list">
        ${data.law.documents_needed.map(item => `<li>${item}</li>`).join("")}
      </ul>
    </div>

    <div class="card medium">
      <h3>What Happens Next</h3>
      <ul class="list">
        ${data.law.what_happens_next.map(item => `<li>${item}</li>`).join("")}
      </ul>
    </div>

    <div class="card full">
      <h3>Maximum Punishment</h3>
      <p>${data.law.max_punishment}</p>
    </div>
  `;

  requestAnimationFrame(() => startParticles(risk.level));
}

/* ───────── Get Guidance (Dropdown Flow) ───────── */
async function getGuidance() {
  const crime = document.getElementById("crime").value;
  const situation = document.getElementById("situation").value;
  const resultDiv = document.getElementById("result");
  const aiBox = document.getElementById("aiBox");

  resultDiv.innerHTML = `<div class="loading">Loading legal guidance...</div>`;
  if (aiBox) aiBox.innerHTML = `<p>${translations[currentLanguage].aiPlaceholder}</p>`;

  try {
    const response = await fetch("http://127.0.0.1:8000/get-guidance", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ crime, situation })
    });

    const data = await response.json();
    latestCaseData = data;

    if (!data.law) {
      resultDiv.innerHTML = `<div class="error">No legal guidance found for this case.</div>`;
      return;
    }

    renderCase(data);

    setTimeout(() => {
      document.getElementById("resultHeader").scrollIntoView({ behavior: "smooth", block: "start" });
    }, 300);
  } catch (error) {
    resultDiv.innerHTML = `
      <div class="error">
        Could not fetch data from backend. Make sure FastAPI is running and CORS is enabled.
      </div>
    `;
    console.error(error);
  }
}

/* ───────── AI Situation Analyzer ───────── */
async function analyzeSituation() {
  const query = document.getElementById("caseQuery").value.trim();
  const resultBox = document.getElementById("aiCaseResult");
  const aiBox = document.getElementById("aiBox");

  if (!query) {
    resultBox.innerHTML = "Please describe the situation first.";
    return;
  }

  resultBox.innerHTML = "Analyzing situation...";
  if (aiBox) aiBox.innerHTML = `<p>${translations[currentLanguage].aiPlaceholder}</p>`;

  try {
    const response = await fetch("http://127.0.0.1:8000/ai-case-guidance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query })
    });

    const data = await response.json();

    if (!data.law) {
      resultBox.innerHTML = "Could not identify the case clearly. Try describing it differently.";
      return;
    }

    latestCaseData = data;

    resultBox.innerHTML = `
      <strong>Detected Crime:</strong> ${data.parsed_case.crime || "Not identified"}<br>
      <strong>Detected Situation:</strong> ${data.parsed_case.situation || "Not identified"}<br>
      <strong>Confidence:</strong> ${data.parsed_case.confidence}<br>
      <strong>AI Note:</strong> ${data.parsed_case.explanation}
    `;

    renderCase(data);

    setTimeout(() => {
      document.getElementById("resultHeader").scrollIntoView({ behavior: "smooth", block: "start" });
    }, 300);
  } catch (error) {
    resultBox.innerHTML = "Could not analyze the case. Make sure backend is running.";
    console.error(error);
  }
}

/* ───────── AI Explanation with Typing Effect ───────── */
async function getAIExplanation() {
  const aiBox = document.getElementById("aiBox");

  if (!latestCaseData) {
    aiBox.innerHTML = `<p>Please get legal guidance first.</p>`;
    return;
  }

  aiBox.innerHTML = `<p class="ai-typing">Generating explanation</p>`;

  try {
    const response = await fetch("http://127.0.0.1:8000/explain-case", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        law: latestCaseData.law,
        checklist: latestCaseData.checklist,
        language: currentLanguage
      })
    });

    const data = await response.json();
    typeOutExplanation(aiBox, data.explanation);
  } catch (error) {
    aiBox.innerHTML = `<p style="color:#ffb1b1;">Could not generate explanation.</p>`;
    console.error(error);
  }
}

function typeOutExplanation(container, html) {
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = html;
  const fullText = tempDiv.innerHTML;

  container.innerHTML = `<p class="ai-typing"></p>`;
  const target = container.querySelector("p");

  let i = 0;
  const speed = 8;

  function typeChar() {
    if (i < fullText.length) {
      if (fullText[i] === "<") {
        const closeIndex = fullText.indexOf(">", i);
        if (closeIndex !== -1) {
          target.innerHTML += fullText.substring(i, closeIndex + 1);
          i = closeIndex + 1;
        } else {
          target.innerHTML += fullText[i];
          i++;
        }
      } else {
        target.innerHTML += fullText[i];
        i++;
      }
      requestAnimationFrame(() => setTimeout(typeChar, speed));
    } else {
      target.classList.remove("ai-typing");
    }
  }

  typeChar();
}

/* ───────── Chatbot ───────── */
async function sendChatMessage() {
  const input = document.getElementById("chatInput");
  const chatBox = document.getElementById("chatBox");
  const message = input.value.trim();

  if (!message || !latestCaseData) return;

  chatBox.innerHTML += `<div class="chat-msg user">${message}</div>`;
  input.value = "";

  chatBox.innerHTML += `<div class="chat-msg bot" id="typingMsg">Thinking...</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch("http://127.0.0.1:8000/chatbot-guidance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query: message,
        crime: latestCaseData.law.offence_key,
        situation: latestCaseData.checklist ? latestCaseData.checklist.situation_key : null
      })
    });

    const data = await response.json();

    const typingMsg = document.getElementById("typingMsg");
    if (typingMsg) typingMsg.remove();

    chatBox.innerHTML += `<div class="chat-msg bot">${data.reply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
    const typingMsg = document.getElementById("typingMsg");
    if (typingMsg) typingMsg.remove();

    chatBox.innerHTML += `<div class="chat-msg bot">Could not fetch chatbot response.</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
    console.error(error);
  }
}

/* ───────── Quick Card Scroll ───────── */
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}