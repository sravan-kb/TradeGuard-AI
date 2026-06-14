# 🛡️ TradeGuard-AI

AI-Powered Vendor Risk & Compliance Screening Tool

Built for the Microsoft Agents League Hackathon 2026

---

## Demo Video

[![TradeGuard-AI Demo](https://img.youtube.com/vi/uUobIoqkc9Y/0.jpg)](https://youtu.be/uUobIoqkc9Y)

---

## What it does

TradeGuard-AI helps businesses screen companies and vendors before onboarding them.

### Screening Datasets
- **OFAC SDN List** (US Treasury) — Global sanctions screening
- **SEBI Debarred Entities** (NSE India) — Indian securities market debarments

### How it works
1. User enters a company or vendor name
2. Tool screens against OFAC sanctions list (USA)
3. Tool screens against SEBI debarred entities list (India)
4. Azure AI generates a detailed risk assessment based on screening results
5. Screening findings are presented for human review before any vendor decision is made

---

## Tech Stack

- **Frontend:** Streamlit
- **AI:** Azure OpenAI (GPT) via Microsoft Foundry IQ
- **Data:** OFAC SDN List, SEBI Debarred Entities (NSE India)
- **Language:** Python

---

## Microsoft IQ Integration

This project uses **Foundry IQ** via Azure OpenAI to power multi-step reasoning:
- Screening results are passed as context to the AI
- AI generates jurisdiction-aware risk assessments
- Responses are grounded in actual screening data

---

## Data Sources

| Dataset | Source | License |
|---------|--------|---------|
| OFAC SDN List | US Treasury Department | Public Domain |
| SEBI Debarred Entities | NSE India | Public Regulatory Data |

---

## Setup

1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Create a `.env` file:
```
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_DEPLOYMENT=your_deployment
```
4. Run the app:
```
streamlit run app.py
```

---

## Ethical AI Notice

TradeGuard-AI presents screening findings only. It does not approve or reject vendors. All final vendor decisions must be made by a qualified compliance officer.

---

## Disclaimer

This tool is for informational purposes only and does not constitute legal or compliance advice. Sanctions data is sourced from public domain government datasets.