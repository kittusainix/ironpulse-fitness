/**
 * IRONPULSE FITNESS - INTERACTIVE BMI CALCULATOR
 * Real-time BMI evaluation, category classification, and fitness guidance
 */

function calculateBmiStats(heightCm, weightKg) {
  if (!heightCm || !weightKg || heightCm <= 0 || weightKg <= 0) {
    return null;
  }

  const heightM = heightCm / 100.0;
  const bmi = weightKg / (heightM * heightM);
  const roundedBmi = parseFloat(bmi.toFixed(1));

  let category = "Normal Weight";
  let color = "#10b981";
  let bgClass = "badge-success";
  let recommendation = "Maintain balanced diet, progressive overload training, and 1.6-2g protein per kg of bodyweight.";

  if (roundedBmi < 18.5) {
    category = "Underweight";
    color = "#3b82f6";
    bgClass = "badge-info";
    recommendation = "Focus on a healthy 300-500 kcal daily surplus, heavy compound lifts, and high-calorie mass gainers.";
  } else if (roundedBmi <= 24.9) {
    category = "Normal Weight / Athletic";
    color = "#10b981";
    bgClass = "badge-success";
    recommendation = "Excellent physical conditioning! Keep focusing on muscle hypertrophy, recovery, and pure whey protein.";
  } else if (roundedBmi <= 29.9) {
    category = "Overweight";
    color = "#f59e0b";
    bgClass = "badge-warning";
    recommendation = "Incorporate 20-30 mins of post-lift cardio, stay in a mild calorie deficit, and use L-Carnitine / Pre-workout.";
  } else {
    category = "Obese (High Body Fat)";
    color = "#ef4444";
    bgClass = "badge-danger";
    recommendation = "Prioritize low-impact aerobic conditioning, dedicated nutrition coaching, and consistent daily deficit.";
  }

  const idealMin = parseFloat((18.5 * (heightM * heightM)).toFixed(1));
  const idealMax = parseFloat((24.9 * (heightM * heightM)).toFixed(1));
  const waterLiters = parseFloat((weightKg * 0.035).toFixed(1));
  const calorieEst = Math.round(weightKg * 32);

  return {
    bmi: roundedBmi,
    category,
    color,
    bgClass,
    recommendation,
    idealWeightRange: `${idealMin} - ${idealMax} kg`,
    waterLiters: `${waterLiters} Liters/day`,
    calorieEst: `${calorieEst} kcal/day`
  };
}

// Hook into Calculator Widget
function setupBmiCalculator(heightInputId, weightInputId, outputPrefix = "bmi") {
  const hInput = document.getElementById(heightInputId);
  const wInput = document.getElementById(weightInputId);

  if (!hInput || !wInput) return;

  function handleCalculate() {
    const height = parseFloat(hInput.value);
    const weight = parseFloat(wInput.value);

    const stats = calculateBmiStats(height, weight);
    if (!stats) return;

    const valEl = document.getElementById(`${outputPrefix}Val`);
    const catEl = document.getElementById(`${outputPrefix}Category`);
    const recEl = document.getElementById(`${outputPrefix}Recommendation`);
    const idealEl = document.getElementById(`${outputPrefix}Ideal`);
    const waterEl = document.getElementById(`${outputPrefix}Water`);

    if (valEl) {
      valEl.innerText = stats.bmi;
      valEl.style.color = stats.color;
    }
    if (catEl) {
      catEl.innerText = stats.category;
      catEl.className = `badge ${stats.bgClass}`;
    }
    if (recEl) recEl.innerText = stats.recommendation;
    if (idealEl) idealEl.innerText = stats.idealWeightRange;
    if (waterEl) waterEl.innerText = stats.waterLiters;
  }

  hInput.addEventListener("input", handleCalculate);
  wInput.addEventListener("input", handleCalculate);
  handleCalculate();
}

window.setupBmiCalculator = setupBmiCalculator;
window.calculateBmiStats = calculateBmiStats;
