/**
 * IRONPULSE FITNESS - SUBSCRIPTION COUNTDOWN TIMER
 * Real-time dynamic countdown: "Kitna time bacha hai"
 */

function initSubscriptionCountdown(targetIsoDateStr) {
  if (!targetIsoDateStr) return;

  const daysEl = document.getElementById("timerDays");
  const hoursEl = document.getElementById("timerHours");
  const minsEl = document.getElementById("timerMins");
  const secsEl = document.getElementById("timerSecs");
  const tickerContainer = document.getElementById("subscriptionTicker");
  const expiredMsg = document.getElementById("subscriptionExpiredNotice");

  const targetDate = new Date(targetIsoDateStr).getTime();

  function updateTicker() {
    const now = new Date().getTime();
    const distance = targetDate - now;

    if (distance <= 0) {
      if (daysEl) daysEl.innerText = "00";
      if (hoursEl) hoursEl.innerText = "00";
      if (minsEl) minsEl.innerText = "00";
      if (secsEl) secsEl.innerText = "00";

      if (tickerContainer) tickerContainer.style.display = "none";
      if (expiredMsg) expiredMsg.style.display = "block";
      return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    if (daysEl) daysEl.innerText = String(days).padStart(2, "0");
    if (hoursEl) hoursEl.innerText = String(hours).padStart(2, "0");
    if (minsEl) minsEl.innerText = String(minutes).padStart(2, "0");
    if (secsEl) secsEl.innerText = String(seconds).padStart(2, "0");
  }

  updateTicker();
  setInterval(updateTicker, 1000);
}

window.initSubscriptionCountdown = initSubscriptionCountdown;
