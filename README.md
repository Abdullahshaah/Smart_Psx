# 📈 Stock Market Advisor — Smart PSX

**Investing on the Pakistan Stock Exchange, minus the guesswork.**

Stock Market Advisor is a simple, web-based app that brings technical indicators and company fundamentals together in one place. It gives retail investors clear Buy, Hold, or Sell calls, and tells you *why* behind each one.

---

## 🤔 Why This Exists

Investing on the PSX can feel overwhelming, especially for small investors:

- Thousands of listed instruments make it slow to screen companies
- Technical and fundamental signals usually live in separate places
- Learning SMA, RSI, PE, and EPS takes time and experience
- Most existing apps tell you *what* to do, but rarely explain *why*

We built this to close that gap.

## 💡 What It Does

Built with **Streamlit** and wrapped in a clean dark theme, the app combines:

- **Technical signals:** SMA, RSI, and price momentum
- **Fundamentals:** EPS and PE ratio

Together they produce a single score and a numbered recommendation, with the reasoning shown right next to it. No black boxes.

## ✨ Key Features

| Feature | What You Get |
|---|---|
| 🕯️ **Price Movement** | Zoomable candlestick charts with timeline controls, from daily to multi-year views |
| 📊 **RSI** | Plotted alongside price, with thresholds and automated overbought/oversold signals |
| 📉 **SMA** | Short and long moving averages (e.g., 20/50/200) with crossover alerts and trend-speed metrics |
| 🧠 **Transparent Reasoning** | A plain-language explanation for every recommendation |
| 📥 **Downloadable Reports** | Portable records for taxes, compliance, and performance tracking |

## ⚙️ How Recommendations Work

1. **Technical scoring:** looks at SMA crossovers, RSI thresholds, and momentum speed to judge timing.
2. **Fundamental scoring:** looks at EPS growth, trailing PE against the sector median, and earnings stability to judge company health.
3. **Combined decision:** a weighted blend of both gives a final label with an explanation and a confidence metric.

### 🎯 Decision Thresholds

| Recommendation | When It Applies |
|---|---|
| 🟢 **Strong Purchase** | Score ≥ 85, positive trend (MA50 > MA200), RSI between 40–70 |
| 🟩 **Buy** | Score 70–84, improving momentum, acceptable fundamentals |
| 🟡 **Hold** | Score 45–69, mixed signals; keep watching for a breakout or deterioration |
| 🔴 **Sell** | Score < 45, negative trend, weak fundamentals, or high downside risk |

## 🌟 Why It Helps

- **Clear recommendations:** actionable calls with confidence scores and simple rationale
- **Better decisions:** data-backed signals reduce emotional trading and speed up research
- **Portable records:** export reports whenever you need them

## ⚠️ Disclaimer

This project is for educational and informational purposes only and does not constitute financial advice. Always do your own research before investing.

---

⭐ If you find this project useful, consider giving it a star!
