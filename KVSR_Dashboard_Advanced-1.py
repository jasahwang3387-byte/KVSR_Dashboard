"""KVSR Smart Campus Dashboard.
Install: python -m pip install "streamlit>=1.40,<2" "plotly>=5.24,<7" "pandas>=2.2,<3"
Run: python -m streamlit run KVSR_Dashboard_Advanced.py
Attendance and section assignments are demonstration data, not live college records.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime

st.set_page_config(
    page_title="KVSR Smart Campus Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PREMIUM CAMPUS UI
# ============================================================
st.markdown("""
<style>
:root {
 --navy:#07182e; --blue:#1769aa; --cyan:#0ea5e9; --green:#16a34a;
 --orange:#f59e0b; --purple:#7c3aed; --red:#dc2626;
 --ink:#14233c; --muted:#66758a; --line:#dfe7f1; --bg:#eef4fb;
}
html,body,[class*="css"]{font-family:Inter,"Segoe UI",Arial,sans-serif}
.stApp{
 background:
 radial-gradient(circle at 100% 0%,rgba(14,165,233,.10),transparent 25%),
 linear-gradient(145deg,#f5f9fe,#edf4fb);
 color:var(--ink);
}
.block-container{padding-top:1.15rem;padding-bottom:2rem;max-width:1550px}

[data-testid="stSidebar"]{
 background:linear-gradient(180deg,#06162b 0%,#0b3156 55%,#0c5279 100%);
 border-right:1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span{
 color:#f7fbff !important;
}
div[data-baseweb="popover"]{z-index:999999!important}
div[data-baseweb="popover"] ul,div[data-baseweb="menu"],ul[role="listbox"]{
 background:#fff!important;border:1px solid #cbd5e1!important;border-radius:12px!important;
 box-shadow:0 14px 30px rgba(15,23,42,.18)!important;
}
li[role="option"]{background:#fff!important;color:#10233d!important;font-weight:600!important}
li[role="option"]:hover{background:#eaf4ff!important;color:#0b4f82!important}

.hero{
 position:relative;overflow:hidden;
 background:linear-gradient(110deg,#071d39 0%,#0b4c7b 52%,#0ea5e9 120%);
 padding:30px 32px;border-radius:24px;color:white;
 box-shadow:0 18px 42px rgba(12,48,84,.20);margin-bottom:18px;
}
.hero:after{content:"";position:absolute;width:320px;height:320px;border-radius:50%;
 right:-100px;top:-170px;background:rgba(255,255,255,.09)}
.hero-grid{display:flex;justify-content:space-between;align-items:center;gap:20px}
.hero h1{color:white!important;margin:0;font-size:37px;font-weight:900;letter-spacing:-.6px}
.hero p{color:#e6f5ff!important;margin:8px 0 0;font-size:15px}
.hero-badge{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);
 color:white;padding:11px 16px;border-radius:14px;white-space:nowrap;font-weight:750}

.section-title{color:#12213a!important;font-size:24px;font-weight:900;margin:18px 0 4px}
.section-sub{color:#607086!important;margin-bottom:15px}

.kpi{background:#fff;border:1px solid var(--line);border-radius:19px;padding:18px;min-height:122px;
 box-shadow:0 9px 25px rgba(31,58,93,.075);position:relative;overflow:hidden}
.kpi:before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--accent)}
.kpi .icon{font-size:25px} .kpi .label{color:#66758a;font-size:12px;font-weight:800;margin-top:6px}
.kpi .value{color:#14233c;font-size:28px;font-weight:900;margin-top:4px}
.kpi .hint{color:#8793a5;font-size:11px;margin-top:5px}

.insight{background:linear-gradient(90deg,#e9f7ff,#f2f8ff);color:#17466a!important;
 border:1px solid #c9e8fb;border-left:5px solid #0ea5e9;padding:14px 16px;border-radius:13px;margin:10px 0 16px}
.risk{background:#fff4f2;color:#8a2b20!important;border:1px solid #ffd5cf;border-left:5px solid #ef4444;
 padding:14px 16px;border-radius:13px;margin:10px 0 16px}
.success{background:#eefbf3;color:#166534!important;border:1px solid #c9efd7;border-left:5px solid #16a34a;
 padding:14px 16px;border-radius:13px;margin:10px 0 16px}

div[data-testid="stMetric"]{background:#fff!important;border:1px solid var(--line);border-radius:16px;
 padding:15px;box-shadow:0 7px 20px rgba(31,58,93,.06)}
div[data-testid="stMetric"] label,div[data-testid="stMetric"] label *{color:#66758a!important}
div[data-testid="stMetricValue"],div[data-testid="stMetricValue"] *{color:#14233c!important}

.stTabs [data-baseweb="tab-list"]{gap:7px;flex-wrap:wrap}
.stTabs [data-baseweb="tab"]{background:#fff;border-radius:11px;border:1px solid var(--line);padding:8px 15px}
.stTabs [aria-selected="true"]{background:#e8f4ff!important;border-color:#9ed7f7!important}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:14px;overflow:hidden}
h1,h2,h3,h4,h5,h6{color:#14233c!important}
p,li,.stMarkdown{color:#26354d}

/* ===== SMART FILTER DARK BOX + WHITE TEXT OVERRIDE ===== */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background:#173e65 !important;
    border:1px solid rgba(255,255,255,.12) !important;
    border-radius:10px !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
    border-color:#38bdf8 !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
    border-color:#38bdf8 !important;
    box-shadow:0 0 0 2px rgba(56,189,248,.18) !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div *,
[data-testid="stSidebar"] div[data-baseweb="select"] span,
[data-testid="stSidebar"] div[data-baseweb="select"] input {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    opacity:1 !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill:#ffffff !important;
    color:#ffffff !important;
}
[data-testid="stMain"] label,[data-testid="stMain"] [data-baseweb="tab"]{color:#14233c!important}
[data-testid="stPlotlyChart"]{background:white;border:1px solid #dfe7f1;border-radius:18px;padding:8px;box-shadow:0 8px 26px #18395a0a}
[data-testid="stMain"] input{background:#fff!important;color:#14233c!important}
@media(max-width:750px){.hero-grid{display:block}.hero h1{font-size:26px}.hero-badge{display:inline-block;margin-top:16px}.hero{padding:22px}.kpi .value{font-size:23px}}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

# ============================================================
# ORIGINAL USER-SUPPLIED DATA GENERATOR (PRESERVED)
# ============================================================
@st.cache_data
def create_data():
    random.seed(72)
    departments = [
        ("CSE","Computer Science & Engineering"),
        ("CSE (AI & ML)","Artificial Intelligence & Machine Learning"),
        ("CSE (DS)","Data Science"),
        ("ECE","Electronics & Communication Engineering"),
        ("EEE","Electrical & Electronics Engineering"),
        ("CIVIL","Civil Engineering"),
        ("MECH","Mechanical Engineering"),
        ("MBA","Master of Business Administration"),
    ]
    years = ["1st Year","2nd Year","3rd Year","4th Year"]
    sections = ["A","B"]
    aiml_third_year_students = [('24FH1A3301', 'BUKKE LAVANYA GAYATRI'), ('24FH1A3302', 'BUTRA SHIREESHA'), ('24FH1A3303', 'CHAKALI BHUVANESWARI'), ('24FH1A3304', 'CHANDRIKI SHRAVANI'), ('24FH1A3305', 'CHERUVU SREE LAKSHMI'), ('24FH1A3306', 'DEEMANGULA RADHIKA'), ('24FH1A3307', 'DUBBA BINDU SREE'), ('24FH1A3308', 'GOBBARI MAMATHA'), ('24FH1A3309', 'GOPALAPPA GARI VARSHITHA'), ('24FH1A3310', 'JALLA SRAVANI'), ('24FH1A3311', 'JERRIPOTHULA VENKATA LAKSHMI'), ('24FH1A3312', 'KADAPALA BHAVYA SRI'), ('24FH1A3313', 'KURUBA HEMALATHA'), ('24FH1A3314', 'KURUBA LIKITHA'), ('24FH1A3315', 'MANDLA SRAVANI'), ('24FH1A3316', 'POTHULA SRI TEJA REDDY'), ('24FH1A3317', 'SHAIK HEENA'), ('24FH1A3318', 'SHAIK .K. MISBAH AMENA'), ('24FH1A3319', 'SHAIK KHAJABEE'), ('24FH1A3320', 'TIPPLURI MRUDULA SAI'), ('24FH1A3321', 'UDIPI VEENA SREE ADIGA'), ('24FH1A3322', 'UTUKURI USHA'), ('24FH1A3323', 'VALMEEKI GANGADHAR GARI JAHNAVI'), ('24FH1A3324', 'AMMALADINNESIVASAI'), ('24FH1A3325', 'B AJAY KUMAR'), ('24FH1A3326', 'BADRI NAGENDRA'), ('24FH1A3327', 'BARMA YASWANTH'), ('24FH1A3328', 'BASIREDDY GARI YUVAKIRAN REDDY'), ('24FH1A3329', 'CHAKALI VINOD KUMAR'), ('24FH1A3330', 'CHARUKONDA NARENDRA'), ('24FH1A3331', 'D MOHAMMED RAFIQ'), ('24FH1A3332', 'G.H.NAVEEN'), ('24FH1A3333', 'GUVVALA JASWANTH'), ('24FH1A3334', 'J.RAJESH'), ('24FH1A3335', 'JAGADAM HARSHAVARDHAN'), ('24FH1A3336', 'JAMBULAPATI SHIVAKRISHNA'), ('24FH1A3337', 'K.AMAR NATH'), ('24FH1A3338', 'KALLE GURUNATH'), ('24FH1A3339', 'KAMMARI SREEDHAR'), ('24FH1A3340', 'KASAPOGU SHYAM RAJ'), ('24FH1A3341', 'KASIKI MANOHAR'), ('24FH1A3342', 'KEELA RAJU'), ('24FH1A3344', 'KURUBA VASANTH'), ('24FH1A3345', 'KURUVA SHIVA KUMAR'), ('24FH1A3346', 'K.UMESH CHANDRA'), ('24FH1A3347', 'LANKE PRADEEP'), ('24FH1A3348', 'MAHESH'), ('24FH1A3349', 'MALIREDDY RAJASEKHAR REDDY'), ('24FH1A3350', 'MANGALI KARTHIK'), ('24FH1A3351', 'MONE JAGADEESH'), ('24FH1A3352', 'MURAHARI VIJAY KUMAR'), ('24FH1A3353', 'NAGARAJU GARI ESWAR'), ('24FH1A3354', 'P HARSHA VARDHAN'), ('24FH1A3355', 'PINJARI SHASHAVALI'), ('24FH1A3356', 'POLDAS THILAK'), ('24FH1A3357', 'POOJARI VARAPRASAD'), ('24FH1A3358', 'PUTLURU HEMANTH'), ('24FH1A3359', 'R.S.HEMANTH'), ('24FH1A3360', 'RAYADURGAM MAHENDRA KUMAR REDDY'), ('24FH1A3361', 'REDDYVANDLA AJITH KUMAR REDDY'), ('24FH1A3362', 'S.SHAIKSHAVALI'), ('24FH1A3363', 'SINGA TEJA VARDHAN REDDY'), ('24FH1A3364', 'TELUGU NAVEEN KUMAR'), ('24FH1A3365', 'VADDEPALLI JAGAN MOHAN'), ('24FH1A3366', 'YARRABALEM CHANDRA MOULI'), ('25FH1A3301', 'GOLLA VINUSHA'), ('25FH1A3302', 'PUTTAPPA GARI BHAVYA'), ('25FH1A3303', 'G CHARAN KUMAR'), ('25FH1A3304', 'MAHAMMAD RAFIQ'), ('25FH1A3305', 'T PRAVEEN KUMAR')]
    rows=[]; sid=1001
    first=["Aarav","Aditya","Akash","Ananya","Bhavya","Charan","Deepika","Harsha","Jaswanth","Kavya",
           "Kiran","Likitha","Manoj","Meghana","Naveen","Pavan","Priya","Rahul","Sai","Sanjana","Teja","Varun"]
    last=["Reddy","Kumar","Naidu","Rao","Sharma","Babu","Devi","Prasad"]
    for code,full in departments:
        for year in years:
            if code=="MBA" and year in ["3rd Year","4th Year"]:
                continue

            # Official CSE (AI & ML) 3rd Year student list supplied for this dashboard.
            if code=="CSE (AI & ML)" and year=="3rd Year":
                for roll_no, student_name in aiml_third_year_students:
                    gender = "Female" if roll_no <= "24FH1A3323" or roll_no in ["25FH1A3301","25FH1A3302"] else "Male"
                    attendance=round(random.uniform(62,98),1)
                    rows.append({
                        "Student ID":roll_no,
                        "Name":student_name,
                        "Department":code, "Department Name":full,
                        "Year":year, "Section":random.choice(sections), "Gender":gender,
                        "Attendance":attendance
                    })
                continue

            n=random.randint(38,58)
            for _ in range(n):
                gender=random.choice(["Male","Female"])
                attendance=round(random.uniform(62,98),1)
                rows.append({
                    "Student ID":f"KVSR{sid}",
                    "Name":f"{random.choice(first)} {random.choice(last)}",
                    "Department":code, "Department Name":full,
                    "Year":year, "Section":random.choice(sections), "Gender":gender,
                    "Attendance":attendance
                })
                sid+=1
    return pd.DataFrame(rows)

df = create_data()

# ============================================================
# HELPERS
# ============================================================
def kpi(icon,label,value,hint,accent):
    st.markdown(f"""<div class="kpi" style="--accent:{accent}">
    <div class="icon">{icon}</div><div class="label">{label}</div>
    <div class="value">{value}</div><div class="hint">{hint}</div></div>""",
    unsafe_allow_html=True)

PALETTE=["#2563eb","#0d9488","#7c3aed","#f59e0b","#e11d48","#0891b2","#4f46e5","#64748b"]
STATUS_COLORS={"Excellent 90%+":"#0d9488","Good 75–89.9%":"#2563eb","Risk <75%":"#e11d48"}
px.defaults.color_discrete_sequence=PALETTE

def donut(data, names, values, title, colors=None):
    fig=px.pie(data,names=names,values=values,hole=.72,title=title,
               color=names,color_discrete_map=colors)
    fig.update_traces(sort=False,textinfo="percent",textposition="inside",
        insidetextfont=dict(color="white",size=15),
        marker=dict(line=dict(color="white",width=3)),
        hovertemplate="<b>%{label}</b><br>%{value:,} students<br>%{percent}<extra></extra>")
    fig.add_annotation(x=.5,y=.5,text=f"<b>{int(data[values].sum()):,}</b><br>students",
                       showarrow=False,font=dict(size=23,color="#14233c"))
    fig.update_layout(showlegend=True)
    return fig

chart_counter=0
def plot(fig):
    global chart_counter
    chart_counter += 1
    fig.update_layout(
        paper_bgcolor="white",plot_bgcolor="white",
        font=dict(color="#26354d",size=13,family="Segoe UI, Arial, sans-serif"),
        colorway=PALETTE, height=430, hoverlabel=dict(bgcolor="#14233c",font_color="white"),
        title_font=dict(color="#14233c",size=18),
        margin=dict(l=30,r=30,t=70,b=85),
        legend=dict(orientation="h",y=-.18,x=0,font=dict(size=12,color="#26354d")),
        legend_title_text=""
    )
    fig.update_xaxes(gridcolor="#edf2f7",linecolor="#dfe7f1")
    fig.update_yaxes(gridcolor="#edf2f7",linecolor="#dfe7f1")
    st.plotly_chart(fig,use_container_width=True,
                    theme=None, config={"displayModeBar":True,"displaylogo":False,
                    "modeBarButtonsToRemove":["select2d","lasso2d"],
                    "toImageButtonOptions":{"format":"png","scale":2}},
                    key=f"kvsr_adv_chart_{chart_counter}")

def csv_bytes(data):
    return data.to_csv(index=False).encode("utf-8")

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("## 🎓 KVSR COLLEGE")
st.sidebar.caption("Smart Campus Intelligence")
st.sidebar.markdown("---")

page=st.sidebar.radio("MAIN MENU",[
    "🏠 Executive Overview",
    "🏢 Department Intelligence",
    "👨‍🎓 Student Directory",
    "📅 Attendance Command Center",
    "⚠️ Risk Analytics",
    "📈 Comparative Analytics",
    "📑 Reports & Export"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Smart Filters")
dept=st.sidebar.selectbox("Department",["All Departments"]+sorted(df["Department"].unique()))
year=st.sidebar.selectbox("Academic Year",["All Years","1st Year","2nd Year","3rd Year","4th Year"])
gender=st.sidebar.selectbox("Gender",["All","Male","Female"])
section=st.sidebar.selectbox("Section",["All","A","B"])
attendance_band=st.sidebar.selectbox("Attendance Band",["All","Excellent (90%+)","Good (75-89.9%)","Risk (<75%)"])

f=df.copy()
if dept!="All Departments": f=f[f["Department"]==dept]
if year!="All Years": f=f[f["Year"]==year]
if gender!="All": f=f[f["Gender"]==gender]
if section!="All": f=f[f["Section"]==section]
if attendance_band=="Excellent (90%+)": f=f[f["Attendance"]>=90]
elif attendance_band=="Good (75-89.9%)": f=f[(f["Attendance"]>=75)&(f["Attendance"]<90)]
elif attendance_band=="Risk (<75%)": f=f[f["Attendance"]<75]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Active records:** {len(f):,}")
st.sidebar.caption("Advanced single-file Streamlit dashboard")

# ============================================================
# HEADER
# ============================================================
today=datetime.now().strftime("%d %b %Y")
st.markdown(f"""
<div class="hero"><div class="hero-grid">
<div><h1>🎓 KVSR Smart Campus Intelligence</h1>
<p>Advanced institutional analytics for students, departments, attendance performance and early-risk identification.</p></div>
<div class="hero-badge">📅 {today}<br><span style="font-size:11px;font-weight:500">Academic Intelligence Portal</span></div>
</div></div>
""",unsafe_allow_html=True)

st.info("Demo analytics: attendance values and most student records are generated sample data. The supplied AI & ML third-year names and IDs are retained; their attendance and section assignments are also simulated.")
if f.empty:
    st.warning("No students match these filters. Choose a different department, year or attendance band.")
    st.stop()
st.caption(f"{len(f):,} of {len(df):,} students · {dept} · {year} · {gender} · Section: {section} · {attendance_band}")
avg_att=f["Attendance"].mean() if len(f) else 0
good=int((f["Attendance"]>=75).sum()) if len(f) else 0
risk=int((f["Attendance"]<75).sum()) if len(f) else 0
excellent=int((f["Attendance"]>=90).sum()) if len(f) else 0

# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================
if page=="🏠 Executive Overview":
    st.markdown('<div class="section-title">Executive Campus Overview</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-sub">A clear snapshot of the selected student population. All charts follow your sidebar filters.</div>',unsafe_allow_html=True)

    c1,c2,c3,c4,c5=st.columns(5)
    with c1:kpi("👨‍🎓","STUDENTS",f"{len(f):,}","Filtered records","#1769aa")
    with c2:kpi("🏢","DEPARTMENTS",f"{f['Department'].nunique()}","Active departments","#7c3aed")
    with c3:kpi("📅","AVG ATTENDANCE",f"{avg_att:.1f}%","Institutional average","#16a34a")
    with c4:kpi("🏆","EXCELLENT",f"{excellent:,}","90% and above","#f59e0b")
    with c5:kpi("⚠️","AT RISK",f"{risk:,}","Below 75%","#dc2626")

    if len(f):
        risk_pct=risk/len(f)*100
        if risk_pct >= 30:
            st.markdown(f'<div class="risk"><b>⚠️ Attendance alert:</b> {risk_pct:.1f}% of the current filtered students are below 75% attendance and may require intervention.</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success"><b>✅ Attendance status:</b> {100-risk_pct:.1f}% of current students are meeting the 75% attendance benchmark.</div>',unsafe_allow_html=True)

    a,b=st.columns([1.3,1])
    with a:
        d=f.groupby("Department").size().reset_index(name="Students").sort_values("Students",ascending=False)
        fig=px.bar(d,x="Department",y="Students",text="Students",title="Student Strength by Department",
                   color="Students",color_continuous_scale="Blues")
        fig.update_coloraxes(showscale=False); plot(fig)
    with b:
        bands=pd.DataFrame({
            "Status":["Excellent 90%+","Good 75–89.9%","Risk <75%"],
            "Students":[excellent,good-excellent,risk]
        })
        fig=donut(bands,"Status","Students","Attendance Health",STATUS_COLORS)
        plot(fig)

    a,b=st.columns(2)
    with a:
        y=f.groupby("Year").size().reset_index(name="Students")
        order=["1st Year","2nd Year","3rd Year","4th Year"]
        y["Year"]=pd.Categorical(y["Year"],categories=order,ordered=True);y=y.sort_values("Year")
        fig=px.bar(y,x="Year",y="Students",text="Students",title="Student Distribution by Year")
        plot(fig)
    with b:
        g=f["Gender"].value_counts().reset_index();g.columns=["Gender","Students"]
        fig=donut(g,"Gender","Students","Gender Distribution",{"Male":"#2563eb","Female":"#7c3aed"})
        plot(fig)

    st.markdown("### Explore the campus")
    tab1,tab2,tab3=st.tabs(["Department & year", "Attendance heatmap", "Attendance spread"])
    with tab1:
        hierarchy=f.groupby(["Department","Year"],as_index=False).size().rename(columns={"size":"Students"})
        fig=px.sunburst(hierarchy,path=["Department","Year"],values="Students",color="Department",
                        title="Student Composition · Department → Year")
        fig.update_traces(textinfo="label+percent root",insidetextorientation="radial",
                          marker=dict(line=dict(color="white",width=2)))
        plot(fig)
        st.caption("Click a department to explore its academic years; click the centre to return.")
    with tab2:
        heat=f.pivot_table(index="Department",columns="Year",values="Attendance",aggfunc="mean")
        fig=go.Figure(go.Heatmap(z=heat.values,x=heat.columns.tolist(),y=heat.index.tolist(),
                     zmin=0,zmax=100,colorscale=[[0,"#ffe4e6"],[.65,"#fecdd3"],[.75,"#dbeafe"],[1,"#0d9488"]],
                     text=heat.round(1).values,texttemplate="%{text:.1f}%",textfont=dict(color="#14233c"),
                     xgap=4,ygap=4,colorbar=dict(title="Attendance %"),
                     hoverongaps=False,hovertemplate="%{y} · %{x}<br>Mean: %{z:.1f}%<extra></extra>"))
        fig.update_layout(title="Average Attendance · Department × Year")
        plot(fig)
        st.caption("Blank cells mean no matching students; they are not zero attendance.")
    with tab3:
        fig=px.box(f,x="Department",y="Attendance",color="Department",points=False,
                   title="Attendance Spread by Department")
        fig.add_hline(y=75,line_dash="dash",line_color="#e11d48",annotation_text="75% benchmark")
        fig.update_layout(showlegend=False)
        fig.update_yaxes(range=[0,100])
        plot(fig)
        st.caption("The box shows the middle 50% of values; the line inside marks the median.")

# ============================================================
# DEPARTMENT INTELLIGENCE
# ============================================================
elif page=="🏢 Department Intelligence":
    st.markdown('<div class="section-title">Department Intelligence</div>',unsafe_allow_html=True)
    summary=f.groupby(["Department","Department Name"],as_index=False).agg(
        Students=("Student ID","count"),
        Average_Attendance=("Attendance","mean"),
        Highest_Attendance=("Attendance","max"),
        Lowest_Attendance=("Attendance","min")
    )
    summary["Average Attendance"]=summary["Average_Attendance"].round(1)
    summary["At Risk"]=summary["Department"].map(
        f[f.Attendance<75].groupby("Department").size()
    ).fillna(0).astype(int)

    st.dataframe(summary[["Department","Department Name","Students","Average Attendance","At Risk"]],
                 use_container_width=True,hide_index=True)

    a,b=st.columns(2)
    with a:
        fig=px.bar(summary,x="Department",y="Students",text="Students",
                   color="Students",color_continuous_scale="Blues",
                   title="Department Strength")
        fig.update_coloraxes(showscale=False);plot(fig)
    with b:
        fig=px.bar(summary,x="Department",y="Average_Attendance",text_auto=".1f",
                   color="Average_Attendance",color_continuous_scale="Tealgrn",
                   title="Average Attendance by Department")
        fig.update_yaxes(range=[0,100]);fig.update_coloraxes(showscale=False);plot(fig)

    if len(summary):
        best_dept=summary.sort_values("Average_Attendance",ascending=False).iloc[0]
        st.markdown(f'<div class="insight"><b>🏆 Department insight:</b> {best_dept["Department"]} currently has the highest average attendance at <b>{best_dept["Average Attendance"]:.1f}%</b>.</div>',unsafe_allow_html=True)

# ============================================================
# STUDENT DIRECTORY
# ============================================================
elif page=="👨‍🎓 Student Directory":
    st.markdown('<div class="section-title">Advanced Student Directory</div>',unsafe_allow_html=True)
    q=st.text_input("🔎 Search by student ID or name",placeholder="Example: 24FH1A3333 or Jaswanth")
    view=f.copy()
    if q:
        view=view[
            view["Student ID"].str.contains(q,case=False,na=False,regex=False) |
            view["Name"].str.contains(q,case=False,na=False,regex=False)
        ]

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Students",len(view))
    c2.metric("Male",int((view.Gender=="Male").sum()))
    c3.metric("Female",int((view.Gender=="Female").sum()))
    c4.metric("Average Attendance",f"{view.Attendance.mean():.1f}%" if len(view) else "0%")

    st.dataframe(view,use_container_width=True,hide_index=True,height=540)

    st.download_button("⬇️ Download Current Student List",csv_bytes(view),
                       "KVSR_students_filtered.csv","text/csv",use_container_width=True)

# ============================================================
# ATTENDANCE COMMAND CENTER
# ============================================================
elif page=="📅 Attendance Command Center":
    st.markdown('<div class="section-title">Attendance Command Center</div>',unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Average",f"{avg_att:.1f}%")
    c2.metric("75% & Above",f"{good:,}")
    c3.metric("Below 75%",f"{risk:,}")
    c4.metric("Highest",f"{f.Attendance.max():.1f}%" if len(f) else "0%")

    a,b=st.columns([1.2,1])
    with a:
        d=f.groupby("Department",as_index=False)["Attendance"].mean()
        fig=px.bar(d,x="Department",y="Attendance",text_auto=".1f",
                   color="Attendance",color_continuous_scale="Blues",
                   title="Department Attendance Performance")
        fig.update_yaxes(range=[0,100]);fig.update_coloraxes(showscale=False);plot(fig)
    with b:
        bins=pd.cut(f["Attendance"],bins=[0,65,75,85,90,101],right=False,
                    labels=["Critical <65%","Risk 65–<75%","Good 75–<85%","Very Good 85–<90%","Excellent 90%+"])
        dist=bins.value_counts().sort_index().reset_index()
        dist.columns=["Attendance Band","Students"]
        fig=px.bar(dist,x="Students",y="Attendance Band",orientation="h",text="Students",
                   title="Attendance Distribution")
        plot(fig)

    st.markdown("#### ⚠️ Students Requiring Attendance Attention")
    low=f[f.Attendance<75].sort_values("Attendance")
    st.dataframe(low[["Student ID","Name","Department","Year","Section","Attendance"]],
                 use_container_width=True,hide_index=True,height=420)

# ============================================================
# RISK ANALYTICS
# ============================================================
elif page=="⚠️ Risk Analytics":
    st.markdown('<div class="section-title">Early Attendance Risk Analytics</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Identify students and academic groups requiring attendance intervention.</div>',unsafe_allow_html=True)

    risk_df=f[f.Attendance<75].copy()
    critical=f[f.Attendance<65].copy()

    c1,c2,c3,c4=st.columns(4)
    c1.metric("At Risk",len(risk_df))
    c2.metric("Critical <65%",len(critical))
    c3.metric("Risk Rate",f"{(len(risk_df)/len(f)*100):.1f}%" if len(f) else "0%")
    c4.metric("Lowest Attendance",f"{f.Attendance.min():.1f}%" if len(f) else "0%")

    if len(risk_df):
        a,b=st.columns(2)
        with a:
            rd=risk_df.groupby("Department").size().reset_index(name="At Risk")
            fig=px.bar(rd,x="Department",y="At Risk",text="At Risk",
                       color="At Risk",color_continuous_scale="Reds",
                       title="At-Risk Students by Department")
            fig.update_coloraxes(showscale=False);plot(fig)
        with b:
            ry=risk_df.groupby("Year").size().reset_index(name="At Risk")
            fig=donut(ry,"Year","At Risk","Risk Distribution by Year")
            plot(fig)

        st.dataframe(risk_df.sort_values("Attendance")[
            ["Student ID","Name","Department","Year","Section","Gender","Attendance"]
        ],use_container_width=True,hide_index=True,height=450)
    else:
        st.success("No students in the current filter are below 75% attendance.")

# ============================================================
# COMPARATIVE ANALYTICS
# ============================================================
elif page=="📈 Comparative Analytics":
    st.markdown('<div class="section-title">Comparative Academic Analytics</div>',unsafe_allow_html=True)

    matrix=f.groupby(["Department","Year"],as_index=False).agg(
        Students=("Student ID","count"),Attendance=("Attendance","mean")
    )
    matrix["Attendance"]=matrix.Attendance.round(1)

    metric=st.radio("Compare using",["Student Strength","Average Attendance"],horizontal=True)
    if metric=="Student Strength":
        fig=px.bar(matrix,x="Department",y="Students",color="Year",barmode="group",
                   title="Department × Year Student Strength")
    else:
        fig=px.bar(matrix,x="Department",y="Attendance",color="Year",barmode="group",
                   title="Department × Year Attendance Comparison")
        fig.update_yaxes(range=[0,100])
    plot(fig)

    pivot=matrix.pivot(index="Department",columns="Year",
                       values="Attendance" if metric=="Average Attendance" else "Students")
    st.dataframe(pivot,use_container_width=True)

# ============================================================
# REPORTS & EXPORT
# ============================================================
else:
    st.markdown('<div class="section-title">Reports & Data Export Center</div>',unsafe_allow_html=True)
    report=f.groupby("Department",as_index=False).agg(
        Students=("Student ID","count"),
        Average_Attendance=("Attendance","mean"),
        Highest=("Attendance","max"),
        Lowest=("Attendance","min")
    )
    report["Average_Attendance"]=report.Average_Attendance.round(1)
    report["Below_75"]=report["Department"].map(
        f[f.Attendance<75].groupby("Department").size()
    ).fillna(0).astype(int)

    st.dataframe(report,use_container_width=True,hide_index=True)

    a,b=st.columns(2)
    with a:
        st.download_button("⬇️ Download Department Summary",csv_bytes(report),
                           "KVSR_department_summary.csv","text/csv",use_container_width=True)
    with b:
        st.download_button("⬇️ Download Filtered Master Data",csv_bytes(f),
                           "KVSR_filtered_master_data.csv","text/csv",use_container_width=True)

    fig=px.bar(report,x="Department",y="Average_Attendance",text_auto=".1f",
               color="Average_Attendance",color_continuous_scale="Blues",
               title="Department Attendance Report")
    fig.update_yaxes(range=[0,100]);fig.update_coloraxes(showscale=False);plot(fig)

st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#718096;font-size:12px;">'
    'KVSR Smart Campus Intelligence • Advanced Student & Attendance Analytics • Python • Streamlit • Pandas • Plotly'
    '</div>',unsafe_allow_html=True
)
