import streamlit as st
import re
import json
import os
import sys
import warnings
import logging
from datetime import datetime

warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.query_analyzer import QueryAnalyzer
from core.router import route_query

from agents.it_agent import ITAgent
from agents.pharma_agent import PharmaAgent
from agents.banking_agent import BankingAgent
from agents.energy_agent import EnergyAgent
from agents.fmcg_agent import FMCGAgent
from agents.auto_agent import AutoAgent
from agents.telecom_agent import TelecomAgent
from agents.realestate_agent import RealEstateAgent
from agents.metals_agent import MetalsAgent
from agents.insurance_agent import InsuranceAgent
from agents.cement_agent import CementAgent
from agents.chemicals_agent import ChemicalsAgent
from agents.consumer_agent import ConsumerAgent
from agents.infrastructure_agent import InfrastructureAgent
from agents.media_agent import MediaAgent
from agents.aviation_agent import AviationAgent
from agents.retail_agent import RetailAgent
from agents.hospitality_agent import HospitalityAgent
from agents.agriculture_agent import AgricultureAgent
from agents.defense_agent import DefenseAgent

st.set_page_config(
    page_title="FinSight AI — Financial Research Agent",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

agent_map = {
    "IT": ITAgent, "Pharma": PharmaAgent, "Banking": BankingAgent,
    "Energy": EnergyAgent, "FMCG": FMCGAgent, "Auto": AutoAgent,
    "Telecom": TelecomAgent, "RealEstate": RealEstateAgent,
    "Metals": MetalsAgent, "Insurance": InsuranceAgent,
    "Cement": CementAgent, "Chemicals": ChemicalsAgent,
    "Consumer": ConsumerAgent, "Infrastructure": InfrastructureAgent,
    "Media": MediaAgent, "Aviation": AviationAgent,
    "Retail": RetailAgent, "Hospitality": HospitalityAgent,
    "Agriculture": AgricultureAgent, "Defense": DefenseAgent
}

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

def load_users():
    default = {"admin": {"password": "admin123", "email": "admin@demo.com"}}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            return default
    return default

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def validate_username(u):
    if len(u) < 4: return False, "Min 4 characters required"
    if not re.match("^[a-zA-Z0-9_]+$", u): return False, "Only letters, numbers, underscore"
    return True, "Looks good"

def validate_email(e):
    if e != e.lower(): return False, "Must be lowercase"
    if not re.match(r'^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$', e):
        return False, "Invalid email format"
    return True, "Valid email"

def validate_password(p):
    errs = []
    if len(p) < 8: errs.append("8+ chars")
    if not re.search(r'[A-Z]', p): errs.append("1 uppercase")
    if not re.search(r'[a-z]', p): errs.append("1 lowercase")
    if not re.search(r'[0-9]', p): errs.append("1 number")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-]', p): errs.append("1 special char")
    if errs: return False, "Need: " + ", ".join(errs)
    return True, "Strong password ✓"

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in [
    ("logged_in", False), ("username", ""), ("query_value", ""),
    ("show_sectors", False), ("show_terms", False),
    # Research flow states
    ("analysis_done", False), ("analysis_result", {}),
    ("sector", ""), ("research_plan", []),
    ("research_done", False), ("report_text", ""), ("report_file", ""),
    ("current_query", ""), ("report_streamed", False),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Tailwind CSS + Custom Futuristic Styles ────────────────────────────────────
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  theme: {
    extend: {
      colors: {
        cyber: { 50:'#f0fdff', 100:'#ccfbff', 400:'#22d3ee', 500:'#06b6d4', 600:'#0891b2', 900:'#0c4a6e' },
        neon:  { 400:'#a78bfa', 500:'#8b5cf6', 600:'#7c3aed' },
        plasma:{ 400:'#f472b6', 500:'#ec4899' },
      },
      fontFamily: { mono: ['JetBrains Mono','Fira Code','monospace'], sans: ['Inter','system-ui','sans-serif'] },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4,0,0.6,1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'scan': 'scan 2s linear infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: { '0%,100%': {transform:'translateY(0)'}, '50%': {transform:'translateY(-8px)'} },
        scan: { '0%': {top:'-10%'}, '100%': {top:'110%'} },
        glow: { from: {textShadow:'0 0 10px #22d3ee,0 0 20px #22d3ee'}, to: {textShadow:'0 0 20px #a78bfa,0 0 40px #a78bfa'} },
      }
    }
  }
}
</script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

  #MainMenu, footer, header { visibility: hidden; }
  .stApp { background: #020817 !important; }
  section[data-testid="stSidebar"] { display: none; }

  /* ── Zoom keyframes ─────────────────────────────────────────────────────── */
  @keyframes zoomIn {
    from { opacity: 0; transform: scale(0.88); }
    to   { opacity: 1; transform: scale(1); }
  }
  @keyframes zoomInUp {
    from { opacity: 0; transform: scale(0.92) translateY(24px); }
    to   { opacity: 1; transform: scale(1)    translateY(0); }
  }
  @keyframes zoomInFast {
    from { opacity: 0; transform: scale(0.94); }
    to   { opacity: 1; transform: scale(1); }
  }
  @keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-16px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0)     scale(1); }
  }
  @keyframes popIn {
    0%   { opacity: 0; transform: scale(0.7); }
    70%  { transform: scale(1.04); }
    100% { opacity: 1; transform: scale(1); }
  }

  /* ── Page entry — entire block container zooms in ──────────────────────── */
  .main .block-container {
    position: relative; z-index: 1;
    padding: 1rem 2rem 3rem !important;
    max-width: 1400px !important;
    animation: zoomIn 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  /* ── Every Streamlit element fades+zooms in staggered ───────────────────── */
  .element-container {
    animation: zoomInUp 0.45s cubic-bezier(0.22, 1, 0.36, 1) both;
  }
  /* Stagger children */
  .element-container:nth-child(1)  { animation-delay: 0.04s; }
  .element-container:nth-child(2)  { animation-delay: 0.08s; }
  .element-container:nth-child(3)  { animation-delay: 0.12s; }
  .element-container:nth-child(4)  { animation-delay: 0.16s; }
  .element-container:nth-child(5)  { animation-delay: 0.20s; }
  .element-container:nth-child(6)  { animation-delay: 0.24s; }
  .element-container:nth-child(7)  { animation-delay: 0.28s; }
  .element-container:nth-child(8)  { animation-delay: 0.32s; }
  .element-container:nth-child(n+9){ animation-delay: 0.36s; }

  /* ── Stat cards — zoom + bounce on hover ───────────────────────────────── */
  div[style*="border-radius:14px"] {
    transition: transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1),
                box-shadow 0.28s ease,
                border-color 0.28s ease !important;
  }
  div[style*="border-radius:14px"]:hover {
    transform: scale(1.06) !important;
    box-shadow: 0 0 40px rgba(6,182,212,0.18), 0 8px 32px rgba(0,0,0,0.4) !important;
    border-color: rgba(6,182,212,0.4) !important;
  }

  /* ── Sector pills — pop on hover ───────────────────────────────────────── */
  span[style*="border-radius:999px"] {
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1),
                box-shadow 0.22s ease,
                border-color 0.22s ease !important;
    display: inline-block !important;
  }
  span[style*="border-radius:999px"]:hover {
    transform: scale(1.14) !important;
    box-shadow: 0 0 14px rgba(6,182,212,0.35) !important;
    border-color: rgba(6,182,212,0.6) !important;
  }

  /* ── Tabs — zoom in on mount ────────────────────────────────────────────── */
  .stTabs {
    animation: zoomInFast 0.4s cubic-bezier(0.22, 1, 0.36, 1) both;
    animation-delay: 0.1s;
  }
  .stTabs [data-baseweb="tab-panel"] {
    animation: zoomInUp 0.38s cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  /* ── Buttons — zoom on hover + click ───────────────────────────────────── */
  .stButton > button {
    background: linear-gradient(135deg, rgba(6,182,212,0.15), rgba(139,92,246,0.15)) !important;
    border: 1px solid rgba(6,182,212,0.4) !important;
    color: #22d3ee !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.03em !important;
    transition: transform 0.22s cubic-bezier(0.34,1.56,0.64,1),
                box-shadow 0.22s ease,
                background 0.22s ease,
                border-color 0.22s ease !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, rgba(6,182,212,0.3), rgba(139,92,246,0.3)) !important;
    border-color: rgba(6,182,212,0.8) !important;
    color: #fff !important;
    box-shadow: 0 0 24px rgba(6,182,212,0.35), 0 0 48px rgba(6,182,212,0.1) !important;
    transform: scale(1.04) translateY(-2px) !important;
  }
  .stButton > button:active {
    transform: scale(0.96) !important;
    transition: transform 0.1s ease !important;
  }
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0891b2, #7c3aed) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 0 30px rgba(6,182,212,0.4) !important;
  }
  .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #06b6d4, #8b5cf6) !important;
    box-shadow: 0 0 50px rgba(6,182,212,0.6), 0 0 80px rgba(139,92,246,0.3) !important;
    transform: scale(1.05) translateY(-2px) !important;
  }
  .stButton > button[kind="primary"]:active {
    transform: scale(0.97) !important;
  }
  .stDownloadButton > button {
    background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(6,182,212,0.2)) !important;
    border: 1px solid rgba(16,185,129,0.5) !important;
    color: #34d399 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: transform 0.22s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.22s ease !important;
  }
  .stDownloadButton > button:hover {
    background: linear-gradient(135deg, rgba(16,185,129,0.4), rgba(6,182,212,0.4)) !important;
    box-shadow: 0 0 25px rgba(16,185,129,0.4) !important;
    transform: scale(1.04) translateY(-1px) !important;
  }

  /* ── Inputs — zoom focus ring ───────────────────────────────────────────── */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea {
    background: rgba(2,8,23,0.8) !important;
    border: 1px solid rgba(6,182,212,0.25) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: all 0.3s cubic-bezier(0.22,1,0.36,1) !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus {
    border-color: rgba(6,182,212,0.7) !important;
    box-shadow: 0 0 0 3px rgba(6,182,212,0.15), inset 0 1px 3px rgba(0,0,0,0.5) !important;
    background: rgba(2,8,23,0.95) !important;
    transform: scale(1.01) !important;
  }
  .stTextInput > label, .stTextArea > label { color: #94a3b8 !important; font-size: 0.8rem !important; }

  /* ── Tabs ───────────────────────────────────────────────────────────────── */
  .stTabs [data-baseweb="tab-list"] {
    background: rgba(2,8,23,0.6) !important;
    border: 1px solid rgba(6,182,212,0.15) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: transform 0.2s cubic-bezier(0.34,1.56,0.64,1), color 0.2s, background 0.2s !important;
  }
  .stTabs [data-baseweb="tab"]:hover {
    transform: scale(1.06) !important;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(139,92,246,0.2)) !important;
    color: #22d3ee !important;
    border: 1px solid rgba(6,182,212,0.3) !important;
    transform: scale(1.04) !important;
  }

  /* ── Alert / banner divs — zoom in on appear ────────────────────────────── */
  div[style*="border-radius:16px"],
  div[style*="border-radius:14px"],
  div[style*="border-radius:10px"] {
    animation: zoomInFast 0.35s cubic-bezier(0.22,1,0.36,1) both;
  }

  /* ── Plan step rows — slide+zoom in ────────────────────────────────────── */
  div[style*="border-left:3px solid"] {
    transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
                background 0.25s ease,
                border-color 0.25s ease !important;
  }
  div[style*="border-left:3px solid"]:hover {
    transform: scale(1.02) translateX(4px) !important;
    background: rgba(6,182,212,0.06) !important;
  }

  /* ── Animated grid background ───────────────────────────────────────────── */
  .stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background-image:
      linear-gradient(rgba(6,182,212,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(6,182,212,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
  }

  /* ── Orb glows ──────────────────────────────────────────────────────────── */
  .stApp::after {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background:
      radial-gradient(ellipse 60% 40% at 20% 10%, rgba(6,182,212,0.12) 0%, transparent 60%),
      radial-gradient(ellipse 50% 35% at 80% 80%, rgba(139,92,246,0.10) 0%, transparent 60%),
      radial-gradient(ellipse 40% 30% at 60% 30%, rgba(236,72,153,0.06) 0%, transparent 60%);
    pointer-events: none;
  }

  /* ── Stat cards ─────────────────────────────────────────────────────────── */
  .finsight-stat-card {
    background: rgba(2,8,23,0.82);
    border: 1px solid rgba(6,182,212,0.14);
    border-radius: 14px;
    padding: 1.25rem 1rem;
    text-align: center;
    backdrop-filter: blur(16px);
    position: relative;
    overflow: hidden;
    cursor: default;
    animation: statZoomIn 0.55s cubic-bezier(0.22,1,0.36,1) both;
    transition:
      transform 0.3s cubic-bezier(0.34,1.56,0.64,1),
      box-shadow 0.3s ease,
      border-color 0.3s ease,
      background 0.3s ease;
  }
  @keyframes statZoomIn {
    0%   { opacity:0; transform: scale(0.72) translateY(20px); }
    60%  { opacity:1; transform: scale(1.04) translateY(-4px); }
    100% { opacity:1; transform: scale(1)    translateY(0); }
  }
  .finsight-stat-card:hover {
    transform: scale(1.09) translateY(-6px) !important;
    border-color: var(--sc-color, #22d3ee) !important;
    box-shadow:
      0 0 0 1px var(--sc-color, #22d3ee),
      0 0 30px rgba(6,182,212,0.3),
      0 12px 40px rgba(0,0,0,0.5) !important;
    background: rgba(6,18,40,0.95) !important;
  }
  .finsight-stat-topline {
    position: absolute; top:0; left:0; right:0; height:1px;
  }
  .finsight-stat-glow {
    position: absolute; inset:0; pointer-events:none;
    opacity: 0; transition: opacity 0.3s ease;
  }
  .finsight-stat-card:hover .finsight-stat-glow { opacity: 1; }
  .finsight-stat-icon {
    font-size: 1.6rem; margin-bottom: 6px;
    transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1);
    display: block;
  }
  .finsight-stat-card:hover .finsight-stat-icon {
    transform: scale(1.28) rotate(-6deg);
  }
  .finsight-stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem; font-weight: 700; margin-bottom: 4px;
    transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1);
    display: block;
  }
  .finsight-stat-card:hover .finsight-stat-value {
    transform: scale(1.1);
  }
  .finsight-stat-label {
    font-size: 0.62rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.13em; font-weight: 600;
    transition: color 0.3s ease; display: block;
  }
  .finsight-stat-card:hover .finsight-stat-label { color: #94a3b8; }

  /* ── Misc ───────────────────────────────────────────────────────────────── */
  .stCheckbox > label { color: #94a3b8 !important; font-size: 0.85rem !important; }
  .stSpinner > div { border-top-color: #22d3ee !important; }
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: rgba(2,8,23,0.5); }
  ::-webkit-scrollbar-thumb { background: rgba(6,182,212,0.4); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: rgba(6,182,212,0.7); }
  .stProgress > div > div > div { background: linear-gradient(90deg, #06b6d4, #8b5cf6) !important; border-radius: 4px !important; }
</style>
""", unsafe_allow_html=True)

# ── Helper HTML components ─────────────────────────────────────────────────────
def card(content, extra_class=""):
    return f"""
    <div style="
      background: rgba(2,8,23,0.7);
      border: 1px solid rgba(6,182,212,0.18);
      border-radius: 16px;
      padding: 1.5rem;
      backdrop-filter: blur(20px);
      box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(6,182,212,0.1);
      position: relative; overflow: hidden;
      {extra_class}
    ">
      <div style="position:absolute;top:0;left:0;right:0;height:1px;
        background:linear-gradient(90deg,transparent,rgba(6,182,212,0.5),transparent)"></div>
      {content}
    </div>"""

def badge(text, color="#22d3ee"):
    return f"""<span style="
      display:inline-flex;align-items:center;gap:4px;
      background:rgba(6,182,212,0.08);
      border:1px solid rgba(6,182,212,0.25);
      color:{color};font-size:0.72rem;font-weight:600;
      padding:3px 10px;border-radius:999px;
      font-family:'JetBrains Mono',monospace;letter-spacing:0.05em;
    ">{text}</span>"""

def sector_pill(text):
    return f"""<span style="
      display:inline-block;
      background:linear-gradient(135deg,rgba(6,182,212,0.08),rgba(139,92,246,0.08));
      border:1px solid rgba(6,182,212,0.2);
      color:#7dd3fc;font-size:0.7rem;font-weight:600;
      padding:3px 10px;border-radius:999px;margin:2px;
      font-family:'Inter',sans-serif;
      transition:all 0.2s;
    ">{text}</span>"""

def stat_card(value, label, icon, color="#22d3ee", delay="0s"):
    return f"""
    <div class="finsight-stat-card" style="
      --sc-color:{color};
      animation-delay:{delay};
    ">
      <div class="finsight-stat-topline" style="background:linear-gradient(90deg,transparent,{color}66,transparent)"></div>
      <div class="finsight-stat-glow" style="background:radial-gradient(circle at 50% 100%,{color}18 0%,transparent 70%)"></div>
      <div class="finsight-stat-icon">{icon}</div>
      <div class="finsight-stat-value" style="color:{color};text-shadow:0 0 24px {color}55">{value}</div>
      <div class="finsight-stat-label">{label}</div>
    </div>"""

def hint(msg, ok):
    color = "#34d399" if ok else "#f87171"
    icon = "✓" if ok else "✗"
    return f'<div style="color:{color};font-size:0.75rem;margin-top:3px;font-family:Inter,sans-serif">{icon} {msg}</div>'

def alert(msg, kind="error"):
    cfg = {
        "error":   ("#f87171","rgba(239,68,68,0.08)","rgba(239,68,68,0.25)"),
        "success": ("#34d399","rgba(16,185,129,0.08)","rgba(16,185,129,0.25)"),
        "info":    ("#22d3ee","rgba(6,182,212,0.08)","rgba(6,182,212,0.25)"),
        "warn":    ("#fbbf24","rgba(245,158,11,0.08)","rgba(245,158,11,0.25)"),
    }
    c, bg, border = cfg.get(kind, cfg["info"])
    return f"""<div style="background:{bg};border:1px solid {border};color:{c};
      border-radius:10px;padding:0.85rem 1rem;font-size:0.85rem;
      font-family:Inter,sans-serif;margin:8px 0">{msg}</div>"""

# ══════════════════════════════════════════════════════════════════════════════
# AUTH SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:

    # ── Hero header ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:3rem 0 2rem">
      <div style="display:inline-flex;align-items:center;justify-content:center;
        width:72px;height:72px;border-radius:20px;margin-bottom:1.25rem;
        background:linear-gradient(135deg,rgba(6,182,212,0.2),rgba(139,92,246,0.2));
        border:1px solid rgba(6,182,212,0.3);
        box-shadow:0 0 40px rgba(6,182,212,0.2)">
        <span style="font-size:2rem">📡</span>
      </div>
      <h1 style="font-family:'Inter',sans-serif;font-size:2.6rem;font-weight:900;
        background:linear-gradient(135deg,#22d3ee 0%,#a78bfa 50%,#f472b6 100%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        margin:0 0 1.5rem;letter-spacing:-0.03em">FinSight AI</h1>
      <div style="display:flex;justify-content:center;gap:8px;flex-wrap:wrap">
    """ +
    badge("🤖 AI-Powered") + " " +
    badge("📈 20 Sectors", "#a78bfa") + " " +
    badge("⚡ NSE Live Data", "#f472b6") + " " +
    badge("🔍 10-Step Research", "#34d399") +
    """
      </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:

        # ── Glowing form container open ───────────────────────────────────────
        st.markdown("""
        <div style="
          background: linear-gradient(145deg, rgba(6,18,40,0.95), rgba(2,8,23,0.98));
          border: 1px solid rgba(6,182,212,0.2);
          border-radius: 20px;
          padding: 2rem 2rem 0.5rem;
          box-shadow: 0 0 60px rgba(6,182,212,0.08), 0 0 120px rgba(139,92,246,0.05),
                      inset 0 1px 0 rgba(6,182,212,0.15);
          position: relative; overflow: hidden;
        ">
          <div style="position:absolute;top:0;left:0;right:0;height:1px;
            background:linear-gradient(90deg,transparent,#22d3ee,#a78bfa,transparent)"></div>
          <div style="position:absolute;top:-60px;right:-60px;width:180px;height:180px;
            background:radial-gradient(circle,rgba(6,182,212,0.06) 0%,transparent 70%);
            border-radius:50%;pointer-events:none"></div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔐  Sign In", "🚀  Create Account"])

        # ── LOGIN ─────────────────────────────────────────────────────────────
        with tab_login:
            st.markdown('<div style="height:0.25rem"></div>', unsafe_allow_html=True)

            login_user = st.text_input("", placeholder="👤  Username", key="li_u",
                                       label_visibility="collapsed")
            login_pass = st.text_input("", type="password", placeholder="🔒  Password",
                                       key="li_p", label_visibility="collapsed")

            st.markdown('<div style="height:0.25rem"></div>', unsafe_allow_html=True)

            if st.button("🔐  Sign In", use_container_width=True, key="li_btn"):
                USERS = load_users()
                if not login_user or not login_pass:
                    st.markdown(alert("Please fill in all fields.", "error"), unsafe_allow_html=True)
                elif login_user in USERS and USERS[login_user]["password"] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.username  = login_user
                    st.rerun()
                else:
                    st.markdown(alert("Invalid username or password.", "error"), unsafe_allow_html=True)

            st.markdown("""
            <div style="margin:1rem 0 0.5rem;padding:0.6rem 1rem;
              background:rgba(6,182,212,0.04);
              border:1px solid rgba(6,182,212,0.12);
              border-radius:10px;text-align:center;
              font-size:0.75rem;color:#475569;
              font-family:'JetBrains Mono',monospace;letter-spacing:0.03em">
              Demo &nbsp;→&nbsp;
              <span style="color:#22d3ee;font-weight:600">admin</span>
              &nbsp;/&nbsp;
              <span style="color:#22d3ee;font-weight:600">admin123</span>
            </div>""", unsafe_allow_html=True)

        # ── SIGN UP ───────────────────────────────────────────────────────────
        with tab_signup:
            st.markdown('<div style="height:0.25rem"></div>', unsafe_allow_html=True)

            su_user = st.text_input("", placeholder="👤  Username (min 4 chars)", key="su_u",
                                    label_visibility="collapsed")
            if su_user:
                v, m = validate_username(su_user)
                st.markdown(hint(m, v), unsafe_allow_html=True)

            su_email = st.text_input("", placeholder="📧  Email address", key="su_e",
                                     label_visibility="collapsed")
            if su_email:
                v, m = validate_email(su_email)
                st.markdown(hint(m, v), unsafe_allow_html=True)

            su_pass = st.text_input("", type="password", placeholder="🔒  Password (min 8 chars)",
                                    key="su_p", label_visibility="collapsed")
            if su_pass:
                v, m = validate_password(su_pass)
                score = sum([
                    len(su_pass) >= 8,
                    bool(re.search(r'[A-Z]', su_pass)),
                    bool(re.search(r'[a-z]', su_pass)),
                    bool(re.search(r'[0-9]', su_pass)),
                    bool(re.search(r'[!@#$%^&*(),.?":{}|<>_\-]', su_pass)),
                ])
                strength = ["","Weak","Weak","Fair","Good","Strong ✦"][score]
                s_color  = ["","#f87171","#f87171","#fbbf24","#34d399","#22d3ee"][score]
                bar_w    = [0, 20, 20, 50, 75, 100][score]
                st.markdown(f"""
                <div style="margin-top:4px">
                  <div style="height:3px;background:rgba(255,255,255,0.06);border-radius:2px;margin-bottom:4px">
                    <div style="height:3px;width:{bar_w}%;background:{s_color};border-radius:2px;
                      transition:width 0.3s;box-shadow:0 0 8px {s_color}88"></div>
                  </div>
                  <span style="color:{s_color};font-size:0.72rem">
                    {"✓" if v else "✗"} {m} &nbsp;·&nbsp; <b>{strength}</b>
                  </span>
                </div>""", unsafe_allow_html=True)

            su_conf = st.text_input("", type="password", placeholder="🔒  Confirm password",
                                    key="su_c", label_visibility="collapsed")
            if su_conf:
                match = su_pass == su_conf
                st.markdown(hint("Passwords match" if match else "Passwords do not match", match),
                            unsafe_allow_html=True)

            # Terms row
            tc_col, terms_col = st.columns([2, 1])
            with tc_col:
                agree = st.checkbox("I agree to Terms & Conditions", key="tc")
            with terms_col:
                if st.button("View Terms", key="vt_btn", use_container_width=True):
                    st.session_state.show_terms = not st.session_state.show_terms

            if st.session_state.show_terms:
                st.markdown("""
                <div style="background:rgba(2,8,23,0.9);
                  border:1px solid rgba(6,182,212,0.12);border-radius:10px;
                  padding:0.85rem 1rem;font-size:0.72rem;color:#475569;
                  max-height:140px;overflow-y:auto;line-height:1.9;margin:6px 0">
                  <span style="color:#22d3ee">1.</span> Research & demo only — not financial advice.<br>
                  <span style="color:#22d3ee">2.</span> Data from public sources; accuracy not guaranteed.<br>
                  <span style="color:#22d3ee">3.</span> Credentials stored locally only.<br>
                  <span style="color:#22d3ee">4.</span> Not liable for investment decisions.<br>
                  <span style="color:#22d3ee">5.</span> Use a strong password to protect your account.
                </div>""", unsafe_allow_html=True)

            st.markdown('<div style="height:0.25rem"></div>', unsafe_allow_html=True)

            if st.button("🚀  Create Account", use_container_width=True, key="su_btn"):
                USERS = load_users()
                errs  = []
                if not su_user: errs.append("Username required")
                else:
                    v, m = validate_username(su_user)
                    if not v: errs.append(m)
                    if su_user in USERS: errs.append("Username already taken")
                if not su_email: errs.append("Email required")
                else:
                    v, m = validate_email(su_email)
                    if not v: errs.append(m)
                if not su_pass: errs.append("Password required")
                else:
                    v, m = validate_password(su_pass)
                    if not v: errs.append(m)
                if su_pass and su_conf and su_pass != su_conf: errs.append("Passwords don't match")
                if not agree: errs.append("Accept Terms & Conditions")
                if errs:
                    st.markdown(alert(" · ".join(errs), "error"), unsafe_allow_html=True)
                else:
                    USERS[su_user] = {"password": su_pass, "email": su_email}
                    save_users(USERS)
                    st.markdown(alert("✓ Account created! Switch to Sign In tab.", "success"),
                                unsafe_allow_html=True)

        # ── Close glowing container ───────────────────────────────────────────
        st.markdown('<div style="height:1.25rem"></div></div>', unsafe_allow_html=True)

    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD (logged in)
# ══════════════════════════════════════════════════════════════════════════════

# ── Top nav bar ───────────────────────────────────────────────────────────────
nav_l, nav_r = st.columns([5, 1])
with nav_l:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:6px 0">
      <div style="width:36px;height:36px;border-radius:10px;
        background:linear-gradient(135deg,rgba(6,182,212,0.2),rgba(139,92,246,0.2));
        border:1px solid rgba(6,182,212,0.3);display:flex;align-items:center;
        justify-content:center;font-size:1.1rem">📡</div>
      <div>
        <div style="font-family:'Inter',sans-serif;font-weight:800;font-size:1rem;
          background:linear-gradient(135deg,#22d3ee,#a78bfa);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent">FinSight AI</div>
        <div style="font-size:0.7rem;color:#475569;font-family:'JetBrains Mono',monospace">
          Logged in as <span style="color:#22d3ee">{st.session_state.username}</span>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)
with nav_r:
    if st.button("⏻  Logout", key="logout"):
        for k in ["logged_in","username","query_value"]:
            st.session_state[k] = "" if k != "logged_in" else False
        st.rerun()

# ── Hero section ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 1.5rem">
  <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
    color:#06b6d4;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.75rem">
    ◈ AI-POWERED FINANCIAL INTELLIGENCE ◈
  </div>
  <h1 style="font-family:'Inter',sans-serif;font-size:3rem;font-weight:900;
    background:linear-gradient(135deg,#e0f2fe 0%,#22d3ee 40%,#a78bfa 80%,#f472b6 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    margin:0 0 0.75rem;letter-spacing:-0.04em;line-height:1.1">
    Deep Research Engine
  </h1>
  <p style="color:#475569;font-size:1rem;font-family:Inter,sans-serif;margin:0 0 1.5rem">
    Real-time AI analysis across 20 Indian market sectors
  </p>
</div>
""", unsafe_allow_html=True)

# ── Stats row ─────────────────────────────────────────────────────────────────
s1, s2, s3, s4, s5 = st.columns(5)
with s1: st.markdown(stat_card("20","Sectors","🏭","#22d3ee","0.05s"), unsafe_allow_html=True)
with s2: st.markdown(stat_card("10+","Research Steps","🔍","#a78bfa","0.12s"), unsafe_allow_html=True)
with s3: st.markdown(stat_card("Live","NSE Data","📈","#f472b6","0.19s"), unsafe_allow_html=True)
with s4: st.markdown(stat_card("AI","Groq LLM","🤖","#34d399","0.26s"), unsafe_allow_html=True)
with s5: st.markdown(stat_card("Auto","PDF Report","📄","#fbbf24","0.33s"), unsafe_allow_html=True)

st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(6,182,212,0.3),transparent);margin:1.5rem 0"></div>', unsafe_allow_html=True)

# ── Main query area ───────────────────────────────────────────────────────────
q_col, side_col = st.columns([3, 1], gap="large")

with q_col:
    st.markdown("""
    <div style="font-size:0.75rem;font-weight:700;color:#64748b;
      text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.5rem;
      font-family:'JetBrains Mono',monospace">
      ▸ Research Query
    </div>""", unsafe_allow_html=True)

    query = st.text_area(
        "query_input",
        value=st.session_state.query_value,
        placeholder="e.g. Analyze TCS and Infosys Q4 FY25 earnings and FY26 outlook...",
        height=110,
        label_visibility="collapsed",
        key="main_q"
    )

    # Quick-fill examples
    st.markdown("""
    <div style="font-size:0.7rem;color:#475569;font-family:Inter,sans-serif;
      margin:0.5rem 0 0.35rem">⚡ Quick examples:</div>""", unsafe_allow_html=True)

    ex1, ex2, ex3, ex4 = st.columns(4)
    examples = [
        ("💻 TCS & Infosys", "Analyze TCS and Infosys Q4 FY25 performance and FY26 outlook"),
        ("🏦 HDFC vs ICICI", "Compare HDFC Bank and ICICI Bank Q4 FY25 financials"),
        ("💊 Sun Pharma", "Analyze Sun Pharma and Dr Reddy FY25 performance"),
        ("⚡ Reliance Energy", "Reliance and ONGC energy sector outlook FY26"),
    ]
    for col, (label, val) in zip([ex1, ex2, ex3, ex4], examples):
        with col:
            if st.button(label, key=f"ex_{label}"):
                st.session_state.query_value = val
                st.rerun()

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    run_btn = st.button("🚀  Launch Deep Research", type="primary", use_container_width=True, key="run")

with side_col:
    st.markdown("""
    <div style="font-size:0.75rem;font-weight:700;color:#64748b;
      text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.5rem;
      font-family:'JetBrains Mono',monospace">▸ Sectors</div>""", unsafe_allow_html=True)

    top_sectors = ["IT","Pharma","Banking","Energy","FMCG","Auto","Telecom","RealEstate","Metals","Insurance"]
    pills_html = "".join(sector_pill(s) for s in top_sectors)
    st.markdown(f'<div style="line-height:2">{pills_html}</div>', unsafe_allow_html=True)

    if st.button("🔭 View All 20 Sectors", use_container_width=True, key="all_sec"):
        st.session_state.show_sectors = not st.session_state.show_sectors

    if st.session_state.show_sectors:
        all_s = ["IT","Pharma","Banking","Energy","FMCG","Auto","Telecom","RealEstate",
                 "Metals","Insurance","Cement","Chemicals","Consumer","Infrastructure",
                 "Media","Aviation","Retail","Hospitality","Agriculture","Defense"]
        all_pills = "".join(sector_pill(s) for s in all_s)
        st.markdown(card(f"""
          <div style="font-size:0.75rem;font-weight:700;color:#22d3ee;
            margin-bottom:0.75rem;font-family:'JetBrains Mono',monospace">
            ALL 20 SECTORS
          </div>
          <div style="line-height:2.2">{all_pills}</div>
        """), unsafe_allow_html=True)
        if st.button("✕ Close", key="cls_sec"):
            st.session_state.show_sectors = False
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Analyze query when "Launch" is clicked
# ══════════════════════════════════════════════════════════════════════════════
if run_btn:
    if not query.strip():
        st.markdown(alert("⚠️ Please enter a research query before launching.", "warn"), unsafe_allow_html=True)
    else:
        # Reset any previous research state
        st.session_state.analysis_done  = False
        st.session_state.research_done  = False
        st.session_state.report_text    = ""
        st.session_state.report_file    = ""
        st.session_state.current_query  = query

        with st.spinner("🧠  Analyzing query with AI..."):
            analyzer = QueryAnalyzer()
            result   = analyzer.analyze(query)

        sector        = result.get("sector", "Unknown")
        research_plan = result.get("research_plan", [])

        if sector == "Unknown":
            st.markdown(alert(
                "⚠️ Query is outside supported sectors. Please ask about IT, Pharma, Banking, Energy, or any of the 20 supported Indian market sectors.",
                "warn"), unsafe_allow_html=True)
        else:
            # Persist to session state so confirm button can access them
            st.session_state.analysis_done   = True
            st.session_state.analysis_result = result
            st.session_state.sector          = sector
            st.session_state.research_plan   = research_plan

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Show plan + confirm button (persists across reruns)
# ══════════════════════════════════════════════════════════════════════════════
SECTOR_COLORS = {
    "IT":"#22d3ee","Pharma":"#34d399","Banking":"#fbbf24","Energy":"#f97316",
    "FMCG":"#f472b6","Auto":"#06b6d4","Telecom":"#60a5fa","RealEstate":"#4ade80",
    "Metals":"#f87171","Insurance":"#c084fc","Cement":"#94a3b8","Chemicals":"#facc15",
    "Consumer":"#67e8f9","Infrastructure":"#e2e8f0","Media":"#a78bfa",
    "Aviation":"#7dd3fc","Retail":"#fb7185","Hospitality":"#fcd34d",
    "Agriculture":"#86efac","Defense":"#fca5a5"
}

if st.session_state.analysis_done and not st.session_state.research_done:
    sector        = st.session_state.sector
    research_plan = st.session_state.research_plan
    sc            = SECTOR_COLORS.get(sector, "#22d3ee")

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(6,182,212,0.3),transparent);margin:1.5rem 0"></div>', unsafe_allow_html=True)

    # Sector banner
    st.markdown(f"""
    <div style="text-align:center;padding:1.25rem;
      background:linear-gradient(135deg,rgba(6,182,212,0.06),rgba(139,92,246,0.06));
      border:1px solid rgba(6,182,212,0.2);border-radius:14px;margin-bottom:1rem">
      <div style="font-size:0.65rem;color:#475569;letter-spacing:0.15em;
        text-transform:uppercase;font-family:'JetBrains Mono',monospace;margin-bottom:4px">
        SECTOR IDENTIFIED
      </div>
      <div style="font-family:'Inter',sans-serif;font-size:1.8rem;font-weight:900;
        color:{sc};text-shadow:0 0 30px {sc}66;letter-spacing:-0.02em">
        {sector}
      </div>
    </div>""", unsafe_allow_html=True)

    # Research plan steps
    if research_plan:
        st.markdown("""
        <div style="font-size:0.75rem;font-weight:700;color:#64748b;
          text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.75rem;
          font-family:'JetBrains Mono',monospace">▸ Research Plan</div>""",
        unsafe_allow_html=True)
        plan_html = ""
        for i, point in enumerate(research_plan, 1):
            plan_html += f"""
            <div style="display:flex;align-items:flex-start;gap:12px;
              background:rgba(2,8,23,0.6);border:1px solid rgba(6,182,212,0.12);
              border-left:3px solid {sc};border-radius:10px;
              padding:0.75rem 1rem;margin-bottom:6px;
              font-family:Inter,sans-serif;font-size:0.85rem;color:#cbd5e1">
              <span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;
                color:{sc};font-weight:700;min-width:20px;margin-top:1px">
                {str(i).zfill(2)}
              </span>
              <span>{point}</span>
            </div>"""
        st.markdown(plan_html, unsafe_allow_html=True)

    st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)
    confirm_col, _ = st.columns([1, 2])
    with confirm_col:
        confirm_btn = st.button("✅  Confirm & Start Research", type="primary",
                                use_container_width=True, key="confirm")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 3 — Run research when confirm is clicked
    # ══════════════════════════════════════════════════════════════════════════
    if confirm_btn:
        routed = route_query(st.session_state.analysis_result)
        if routed is None:
            st.markdown(alert("❌ Could not route query to a sector agent.", "error"), unsafe_allow_html=True)
            st.stop()

        AgentClass = agent_map.get(routed)
        if not AgentClass:
            st.markdown(alert(f"❌ No agent found for sector: {routed}", "error"), unsafe_allow_html=True)
            st.stop()

        st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(6,182,212,0.3),transparent);margin:1rem 0"></div>', unsafe_allow_html=True)

        prog_bar  = st.progress(0)
        status_ph = st.empty()

        def show_status(pct, msg):
            prog_bar.progress(pct)
            status_ph.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;
              background:rgba(2,8,23,0.7);border:1px solid rgba(6,182,212,0.15);
              border-radius:10px;padding:0.75rem 1rem;
              font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#22d3ee">
              ◉ &nbsp;{msg}
            </div>""", unsafe_allow_html=True)

        show_status(10, "Initializing sector agent...")
        agent = AgentClass()

        show_status(25, f"Running deep research loop for {routed} sector (10 steps)...")
        try:
            agent.run(st.session_state.current_query)
        except Exception as e:
            st.markdown(alert(f"❌ Research error: {str(e)}", "error"), unsafe_allow_html=True)
            st.stop()

        show_status(90, "Finalizing report...")

        # Find the generated report
        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
        today       = datetime.now().strftime("%Y-%m-%d")
        report_file = os.path.join(reports_dir, f"{today}_{routed.lower()}_report.md")
        report_md   = ""
        if os.path.exists(report_file):
            with open(report_file, "r", encoding="utf-8") as f:
                report_md = f.read()

        # Persist results
        st.session_state.research_done = True
        st.session_state.report_text   = report_md
        st.session_state.report_file   = report_file

        prog_bar.progress(100)
        status_ph.empty()
        st.rerun()  # rerun to show the report section cleanly

# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Display completed report with typewriter streaming effect
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.research_done and st.session_state.report_text:
    import time

    sector = st.session_state.sector
    sc     = SECTOR_COLORS.get(sector, "#22d3ee")

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(6,182,212,0.3),transparent);margin:1.5rem 0"></div>', unsafe_allow_html=True)

    # Success banner
    st.markdown(f"""
    <div style="text-align:center;padding:1.5rem;
      background:linear-gradient(135deg,rgba(16,185,129,0.08),rgba(6,182,212,0.08));
      border:1px solid rgba(16,185,129,0.25);border-radius:16px;margin-bottom:1.5rem">
      <div style="font-size:2rem;margin-bottom:0.4rem">✅</div>
      <div style="font-family:'Inter',sans-serif;font-size:1.3rem;font-weight:800;
        color:#34d399;margin-bottom:0.2rem">Research Complete!</div>
      <div style="font-size:0.75rem;color:#475569;font-family:'JetBrains Mono',monospace">
        {sector} sector · Report saved → reports/
      </div>
    </div>""", unsafe_allow_html=True)

    # Report header
    st.markdown("""
    <div style="font-size:0.75rem;font-weight:700;color:#64748b;
      text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.75rem;
      font-family:'JetBrains Mono',monospace">▸ Research Report</div>""",
    unsafe_allow_html=True)

    # ── Typewriter stream — only plays once on first render ───────────────────
    # We use a flag so refreshing the page doesn't re-stream
    if not st.session_state.get("report_streamed", False):
        def word_stream(text):
            """Yield word-by-word with a small delay — ChatGPT style."""
            for word in text.split(" "):
                yield word + " "
                time.sleep(0.018)

        st.write_stream(word_stream(st.session_state.report_text))
        st.session_state.report_streamed = True
    else:
        # Already streamed — just render normally
        st.markdown(st.session_state.report_text)

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

    # Action buttons
    btn_col1, btn_col2, _ = st.columns([1, 1, 2])
    with btn_col1:
        st.download_button(
            "⬇️  Download Report",
            data=st.session_state.report_text,
            file_name=os.path.basename(st.session_state.report_file),
            mime="text/markdown",
            use_container_width=True
        )
    with btn_col2:
        if st.button("🔄  New Research", use_container_width=True, key="new_research"):
            for k in ["analysis_done", "research_done", "report_text", "report_file",
                      "sector", "research_plan", "analysis_result", "current_query",
                      "report_streamed"]:
                st.session_state[k] = (
                    False if k in ["analysis_done", "research_done", "report_streamed"]
                    else "" if isinstance(st.session_state.get(k), str)
                    else {} if isinstance(st.session_state.get(k), dict)
                    else []
                )
            st.session_state.query_value = ""
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3rem 0 1rem;
  font-size:0.7rem;color:#1e293b;font-family:'JetBrains Mono',monospace">
  FinSight AI · Powered by Groq LLaMA · NSE Live Data · Tavily Search
</div>""", unsafe_allow_html=True)
