/* Veragensia push-to-talk: a large walkie-talkie button for the public demo.
 * Hold to talk (webkitSpeechRecognition in the phone browser), release to act.
 * The recognized text goes to the in-container voice gateway
 * (/voice-gateway/command -> nginx -> gateway -> S4 operation invoke, audited).
 * Designed for one-thumb use on a phone: big circle, bottom-right, high
 * contrast, vibration + color feedback, no keyboard or precision needed. */
(function () {
  "use strict";
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  var STATE = { idle: "TALK", listening: "\u2026 LISTENING" };

  var button = document.createElement("button");
  button.id = "veragensia-talk";
  button.setAttribute("aria-label", "Hold to talk");
  button.textContent = STATE.idle;
  Object.assign(button.style, {
    position: "fixed", right: "18px", bottom: "96px", width: "132px", height: "132px",
    borderRadius: "50%", border: "4px solid #0e0b18", cursor: "pointer",
    background: "radial-gradient(circle at 35% 30%, #8b7ec8, #4a3f78 70%)",
    color: "#f2edff", fontSize: "22px", fontWeight: "700", zIndex: "2147483647",
    boxShadow: "0 6px 24px rgba(0,0,0,.6)", touchAction: "none",
    userSelect: "none", webkitUserSelect: "none", webkitTapHighlightColor: "transparent",
    fontfamily: "system-ui, sans-serif", fontFamily: "system-ui, sans-serif",
  });

  var status = document.createElement("div");
  status.id = "veragensia-talk-status";
  Object.assign(status.style, {
    position: "fixed", right: "18px", bottom: "238px", maxWidth: "60vw",
    padding: "10px 14px", borderRadius: "12px", background: "rgba(14,11,24,.92)",
    color: "#e6e0f8", fontSize: "16px", fontWeight: "600", zIndex: "2147483647",
    display: "none", fontFamily: "system-ui, sans-serif", lineHeight: "1.3",
  });

  function showStatus(text, ok) {
    status.textContent = text;
    status.style.display = "block";
    status.style.border = "2px solid " + (ok ? "#7ee2b8" : "#e08b8b");
    clearTimeout(status._t);
    status._t = setTimeout(function () { status.style.display = "none"; }, 4000);
  }
  function setButton(state, listening) {
    button.textContent = state;
    button.style.background = listening
      ? "radial-gradient(circle at 35% 30%, #d2b45a, #8a6d1f 70%)"
      : "radial-gradient(circle at 35% 30%, #8b7ec8, #4a3f78 70%)";
  }
  function buzz(pattern) {
    if (navigator.vibrate) { try { navigator.vibrate(pattern); } catch (e) {} }
  }

  var recognition = null;
  var held = false;
  var listeningStartedAt = 0;

  function startListening(event) {
    event.preventDefault();
    if (!SR) { showStatus("Voice not supported in this browser", false); buzz(80); return; }
    held = true;
    recognition = new SR();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.continuous = false;
    recognition.onresult = function (event) {
      var result = event.results[0][0];
      var text = result.transcript;
      var confidence = typeof result.confidence === "number" ? result.confidence : null;
      submit(text, confidence, listeningStartedAt ? Date.now() - listeningStartedAt : null);
    };
    recognition.onerror = function (event) {
      if (!held) return;
      setButton(STATE.idle, false);
      showStatus(event.error === "not-allowed"
        ? "Microphone blocked — allow mic access" : "Heard nothing — hold and speak", false);
      buzz(80);
    };
    recognition.onend = function () {
      if (held) { setButton(STATE.idle, false); held = false; }
    };
    setButton(STATE.listening, true);
    buzz(40);
    listeningStartedAt = Date.now();
    try {
      recognition.start();
    } catch (e) {
      listeningStartedAt = 0;
      setButton(STATE.idle, false);
      held = false;
      showStatus("Voice could not start — try again", false);
    }
  }

  function stopListening(event) {
    event.preventDefault();
    held = false;
    if (recognition) { try { recognition.stop(); } catch (e) {} }
    setButton(STATE.idle, false);
  }

  function submit(text, confidence, audioDurationMs) {
    setButton("\u2026 DOING", true);
    fetch("/voice-gateway/command", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: text,
        confidence: confidence,
        audio_duration_ms: audioDurationMs,
        source: "phone-push-to-talk",
      }),
    }).then(function (r) { return r.json(); }).then(function (data) {
      setButton(STATE.idle, false);
      buzz(data.matched ? [30, 40, 30] : 120);
      if (!data.matched) {
        showStatus("Not understood: " + text + (data.hint ? "\n" + data.hint : ""), false);
      } else if (data.authority_required) {
        showStatus("Needs authority (demo gate): " + data.operation_id, false);
      } else if (data.status === "ok") {
        showStatus("\u2713 " + data.operation_id.replace("system.", ""), true);
      } else {
        showStatus("Failed: " + (data.error || data.status), false);
      }
    }).catch(function () {
      setButton(STATE.idle, false);
      showStatus("Gateway unreachable", false);
      buzz(120);
    });
  }

  button.addEventListener("pointerdown", startListening);
  button.addEventListener("pointerup", stopListening);
  button.addEventListener("pointercancel", stopListening);
  button.addEventListener("pointerleave", function (e) { if (held) stopListening(e); });
  button.addEventListener("contextmenu", function (e) { e.preventDefault(); });

  function mount() {
    if (!document.getElementById("veragensia-talk")) {
      document.body.appendChild(button);
      document.body.appendChild(status);
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
  setInterval(mount, 3000); // the selkies client re-renders; stay mounted
})();
