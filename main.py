import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Grant Data Dashboard", layout="wide")

# Mobile-responsive CSS
st.markdown("""
<style>
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 1rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        /* Make tables scrollable on mobile */
        .stDataFrame {
            font-size: 11px;
        }
        
        /* Improve button sizes for touch */
        .stSelectbox > div > div {
            font-size: 14px;
        }
        
        /* Better spacing for metrics */
        [data-testid="metric-container"] {
            margin-bottom: 0.5rem;
        }
        
        /* Adjust tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 6px 8px;
            font-size: 11px;
        }
        
        /* Hide legends on mobile for plotly charts */
        .js-plotly-plot .plotly .legend {
            display: none !important;
        }
        
        /* Hide color scales on mobile */
        .js-plotly-plot .plotly .colorbar {
            display: none !important;
        }
    }
    
    /* Desktop - show legends positioned underneath */
    @media (min-width: 769px) {
        .js-plotly-plot .plotly .legend {
            display: block !important;
        }
        
        .js-plotly-plot .plotly .colorbar {
            display: block !important;
        }
    }
    
    /* Improve touch targets */
    .stButton > button {
        min-height: 44px;
    }
    
    .stDownloadButton > button {
        min-height: 44px;
    }
</style>
""", unsafe_allow_html=True)

# Language translations
TRANSLATIONS = {
    "en": {
        "title": "📊 2025 Grant Data Dashboard",
        "language": "Language",
        "university_level": "🏛️ University Level",
        "program_level": "📚 Program Level",
        "subject_level": "📖 Subject Level",
        "raw_data": "📋 Raw Data",
        "methodology": "📖 Methodology",
        "university_analysis": "University Level Analysis",
        "avg_grant_by_uni": "Average Grant Percentage by University",
        "grant_dist_by_uni": "Grant Distribution by University",
        "grant_dist_sorted": "Student Distribution by Grant Percentage (Sorted by Average Grant %)",
        "uni_summary_table": "University Summary Table",
        "total_grant_money": "Total Grant Money Distribution by University",
        "grant_money_pie": "Total Grant Money Distribution by University (in Lari)",
        "program_analysis": "Program Level Analysis",
        "subject_analysis": "Subject Level Analysis (Optional Subject 1)",
        "avg_grant_by_subject": "Average Grant Percentage by Optional Subject",
        "subject_summary_table": "Subject Summary Table",
        "total_programs": "Total Programs",
        "total_subjects": "Total Subjects",
        "avg_grant": "Average Grant %",
        "total_students": "Total Students",
        "top_30_programs": "Top 30 Programs by Average Grant Percentage with Grant Distribution",
        "top_30_title": "Top 30 Programs: Grant Distribution (Sorted by Average Grant %)",
        "program_details": "Program Details Table",
        "subject_details": "Subject Details Table",
        "search_programs": "Search programs:",
        "search_subjects": "Search subjects:",
        "raw_data_view": "Raw Data View",
        "select_columns": "Select Columns to Display",
        "choose_columns": "Choose columns to display:",
        "sort_by": "Sort by:",
        "sort_order": "Sort order:",
        "descending": "Descending",
        "ascending": "Ascending",
        "download_csv": "Download filtered data as CSV",
        "summary_stats": "Summary Statistics",
        "total_records": "Total Records",
        "universities": "Universities",
        "50_grant": "50% Grant",
        "70_grant": "70% Grant",
        "100_grant": "100% Grant",
        "methodology_content": """
        ## Data Source and Scope
        
        This dashboard analyzes grant allocation data for Georgian universities from the **National Assessment and Examinations Center (NAEC)**.
        
        **Data Source**: ჩარიცხულთა სია მოპოვებული სახელმწიფო სასწავლო გრანტის მითითებით – აკადემიური (საბაკალავრო) პროგრამები და ქართულ ენაში მომზადების საგანმანათლებლო პროგრამები
        
        **Source URL**: [https://edu.aris.ge/news/2025-wels-charicxulta-ranjirebuli-sia-fakultetebisa-da-archeviti-sagnebis-mixedvit.html](https://edu.aris.ge/news/2025-wels-charicxulta-ranjirebuli-sia-fakultetebisa-da-archeviti-sagnebis-mixedvit.html)
        
        The analysis focuses specifically on:
        - **Academic programs only** (`აკად/მოსამზად == "აკად"`)
        - Grant percentages of 50%, 70%, and 100% of the base amount
        - Base grant amount: **2,250 Georgian Lari**
        
        ## Data Processing and Filters
        
        ### University Level Analysis
        - **Minimum student threshold**: Universities with fewer than 50 students are excluded
        - **Grant calculation**: Average grant percentage across all students in each university
        - **Total grant money**: Calculated as `(Grant % / 100) × 2,250 × Number of Students`
        
        ### Program Level Analysis
        - **Minimum student threshold**: Programs with fewer than 10 students are excluded
        - **Program consolidation**: Programs with identical names within the same university are combined, regardless of program codes
        - **Grant calculation**: Average grant percentage across all students in each program
        
        ### Subject Level Analysis
        - **Subject focus**: Based on Optional Subject 1 (`არჩევითი საგანი 1`)
        - **Minimum student threshold**: Subjects with fewer than 20 students are excluded
        - **Grant calculation**: Average grant percentage across all students taking each optional subject
        
        ## Key Metrics Explained
        
        ### Average Grant Percentage
        - Simple arithmetic mean of all grant percentages for students in the given category
        - Missing grant data is treated as 0%
        
        ### Grant Distribution
        - **50% Grant**: Number of students receiving 50% of base amount (1,125 Lari)
        - **70% Grant**: Number of students receiving 70% of base amount (1,575 Lari)  
        - **100% Grant**: Number of students receiving 100% of base amount (2,250 Lari)
        
        ### Total Grant Money
        - Sum of all individual student grants within the category
        - Formula: `Σ(Individual Grant % × 2,250)` for all students
        
        ## Data Quality Notes
        
        ### Exclusions
        1. **Non-academic programs**: Only academic programs (`აკად`) are included
        2. **Small cohorts**: Universities < 50 students, programs < 10 students, and subjects < 20 students are excluded
        3. **Missing data**: Grant percentages with null values are treated as 0%
        
        ### Program Consolidation Logic
        Programs are grouped by:
        - University name (`უსდ`)
        - Program name (`პროგრამა`)
        
        **Note**: Program codes (`პროგ. კოდი`) are ignored to combine duplicate programs with different codes within the same university.
        
        ## Sorting and Ranking
        
        - **Universities**: Sorted by average grant percentage (descending), then by university code
        - **Programs**: Sorted by average grant percentage (descending), then by program name
        - **Subjects**: Sorted by average grant percentage (descending), then by subject name
        - **Visualizations**: All charts maintain this consistent sorting for easy comparison
        
        ## Limitations
        
        1. **Temporal scope**: Analysis represents a snapshot in time
        2. **Sample bias**: Small programs and universities are excluded, which may affect representativeness
        3. **Data completeness**: Results depend on completeness of source data
        4. **Program classification**: Relies on university-provided program names and classifications
        
        ## Technical Implementation
        
        - **Data processing**: Python pandas for aggregation and filtering
        - **Visualizations**: Plotly for interactive charts
        - **Interface**: Streamlit for web dashboard
        - **Caching**: Data is cached for performance optimization
        """
    },
    "ka": {
        "title": "📊 2025 ჩარიცხვის მონაცემები",
        "language": "ენა",
        "university_level": "🏛️ უნივერსიტეტის რენკინგი",
        "program_level": "📚 პროგრამის რენკინგი",
        "subject_level": "📖 საგნის რენკინგი",
        "raw_data": "📋 ნედლი მონაცემები",
        "methodology": "📖 მეთოდოლოგია",
        "university_analysis": "უნივერსიტეტის საშუალო გრანტი",
        "avg_grant_by_uni": "საშუალო გრანტის პროცენტი უნივერსიტეტების მიხედვით",
        "grant_dist_by_uni": "გრანტის განაწილება უნივერსიტეტების მიხედვით",
        "grant_dist_sorted": "სტუდენტების განაწილება გრანტის პროცენტის მიხედვით (დალაგებული საშუალო გრანტით %)",
        "uni_summary_table": "უნივერსიტეტის შემაჯამებელი ცხრილი",
        "total_grant_money": "გრანტის მთლიანი თანხა უნივერსიტეტების მიხედვით",
        "grant_money_pie": "გრანტის მთლიანი თანხის განაწილება უნივერსიტეტების მიხედვით (ლარში)",
        "program_analysis": "პროგრამის საშუალო გრანტი",
        "subject_analysis": "საგნის საშუალო გრანტი (არჩევითი საგანი 1)",
        "avg_grant_by_subject": "საშუალო გრანტის პროცენტი არჩევითი საგნების მიხედვით",
        "subject_summary_table": "საგნის შემაჯამებელი ცხრილი",
        "total_programs": "მთლიანი პროგრამები",
        "total_subjects": "მთლიანი საგნები",
        "avg_grant": "საშუალო გრანტი %",
        "total_students": "მთლიანი სტუდენტები",
        "top_30_programs": "ტოპ 30 პროგრამა საშუალო გრანტის პროცენტით გრანტის განაწილებით",
        "top_30_title": "ტოპ 30 პროგრამა: გრანტის განაწილება (დალაგებული საშუალო გრანტით %)",
        "program_details": "პროგრამის დეტალების ცხრილი",
        "subject_details": "საგნის დეტალების ცხრილი",
        "search_programs": "მოძებნე პროგრამები:",
        "search_subjects": "მოძებნე საგნები:",
        "raw_data_view": "ნედლი მონაცემების ნახვა",
        "select_columns": "აირჩიე სვეტები საჩვენებლად",
        "choose_columns": "აირჩიე სვეტები საჩვენებლად:",
        "sort_by": "დალაგება:",
        "sort_order": "დალაგების წესი:",
        "descending": "კლებადობით",
        "ascending": "ზრდადობით",
        "download_csv": "ჩამოტვირთე ფილტრირებული მონაცემები CSV ფორმატში",
        "summary_stats": "შემაჯამებელი სტატისტიკა",
        "total_records": "მთლიანი ჩანაწერები",
        "universities": "უნივერსიტეტები",
        "50_grant": "50% გრანტი",
        "70_grant": "70% გრანტი",
        "100_grant": "100% გრანტი",
        "methodology_content": """
        **მონაცემთა წყარო**: ჩარიცხულთა სია მოპოვებული სახელმწიფო სასწავლო გრანტის მითითებით – აკადემიური (საბაკალავრო) პროგრამები და ქართულ ენაში მომზადების საგანმანათლებლო პროგრამები
        
        **წყაროს ბმული**: [https://edu.aris.ge/news/2025-wels-charicxulta-ranjirebuli-sia-fakultetebisa-da-archeviti-sagnebis-mixedvit.html](https://edu.aris.ge/news/2025-wels-charicxulta-ranjirebuli-sia-fakultetebisa-da-archeviti-sagnebis-mixedvit.html)
        
        ანალიზი კონკრეტულად ფოკუსირდება:
        - **მხოლოდ აკადემიურ პროგრამებზე, ენის მოსამზადებელი პროგრამების გარეშე** (`აკად/მოსამზად == "აკად"`)
        - გრანტის 50%, 70% და 100% პროცენტებზე საბაზო თანხისა
        - საბაზო გრანტის თანხა: **2,250 ლარი**
        
        ## მონაცემთა დამუშავება და ფილტრები
        
        ### უნივერსიტეტის დონის ანალიზი
        - **მინიმალური სტუდენტების ზღვარი**: 50-ზე ნაკლები სტუდენტის მქონე უნივერსიტეტები გამოირიცხება
        - **გრანტის გამოთვლა**: საშუალო გრანტის პროცენტი ყველა სტუდენტისთვის თითოეულ უნივერსიტეტში
        - **მთლიანი გრანტის თანხა**: გამოითვლება როგორც `(გრანტის % / 100) × 2,250 × სტუდენტების რაოდენობა`
        
        ### პროგრამის დონის ანალიზი
        - **მინიმალური სტუდენტების ზღვარი**: 10-ზე ნაკლები სტუდენტის მქონე პროგრამები გამოირიცხება
        - **პროგრამების კონსოლიდაცია**: ერთნაირი სახელების მქონე პროგრამები ერთ უნივერსიტეტში გაერთიანდება, პროგრამის კოდების მიუხედავად
        - **გრანტის გამოთვლა**: საშუალო გრანტის პროცენტი ყველა სტუდენტისთვის თითოეულ პროგრამაში
        
        ### საგნის დონის ანალიზი
        - **საგნის ფოკუსი**: ეფუძნება არჩევით საგანს 1 (`არჩევითი საგანი 1`)
        - **მინიმალური სტუდენტების ზღვარი**: 20-ზე ნაკლები სტუდენტის მქონე საგნები გამოირიცხება
        - **გრანტის გამოთვლა**: საშუალო გრანტის პროცენტი ყველა სტუდენტისთვის, რომელიც იღებს თითოეულ არჩევით საგანს
        
        ## ძირითადი მეტრიკების განმარტება
        
        ### საშუალო გრანტის პროცენტი
        - მარტივი არითმეტიკული საშუალო ყველა სტუდენტის გრანტის პროცენტისა მოცემულ კატეგორიაში
        - გამოტოვებული გრანტის მონაცემები ითვლება 0%-ად
        
        ### გრანტის განაწილება
        - **50% გრანტი**: სტუდენტების რაოდენობა, რომლებიც იღებენ საბაზო თანხის 50%-ს (1,125 ლარი)
        - **70% გრანტი**: სტუდენტების რაოდენობა, რომლებიც იღებენ საბაზო თანხის 70%-ს (1,575 ლარი)
        - **100% გრანტი**: სტუდენტების რაოდენობა, რომლებიც იღებენ საბაზო თანხის 100%-ს (2,250 ლარი)
        
        ### მთლიანი გრანტის თანხა
        - ყველა ინდივიდუალური სტუდენტის გრანტის ჯამი კატეგორიის ფარგლებში
        - ფორმულა: `Σ(ინდივიდუალური გრანტის % × 2,250)` ყველა სტუდენტისთვის
        
        ## მონაცემთა ხარისხის შენიშვნები
        
        ### გამორიცხვები
        1. **არააკადემიური პროგრამები**: მხოლოდ აკადემიური პროგრამები (`აკად`) ითვლება
        2. **მცირე ჯგუფები**: უნივერსიტეტები < 50 სტუდენტი, პროგრამები < 10 სტუდენტი და საგნები < 20 სტუდენტი გამოირიცხება
        3. **გამოტოვებული მონაცემები**: ნულოვანი მნიშვნელობების მქონე გრანტის პროცენტები ითვლება 0%-ად
        
        ### პროგრამების კონსოლიდაციის ლოგიკა
        პროგრამები ჯგუფდება:
        - უნივერსიტეტის სახელით (`უსდ`)
        - პროგრამის სახელით (`პროგრამა`)
        
        **შენიშვნა**: პროგრამის კოდები (`პროგ. კოდი`) იგნორირდება დუბლიკატი პროგრამების გასაერთიანებლად ერთ უნივერსიტეტში, განსხვავებული ჩასაბარებელი საგნების შემთხვევაში.
        
        ## დალაგება და რენკინგი
        
        - **უნივერსიტეტები**: დალაგებული საშუალო გრანტის პროცენტით (კლებადობით), შემდეგ უნივერსიტეტის კოდით
        - **პროგრამები**: დალაგებული საშუალო გრანტის პროცენტით (კლებადობით), შემდეგ პროგრამის სახელით
        - **საგნები**: დალაგებული საშუალო გრანტის პროცენტით (კლებადობით), შემდეგ საგნის სახელით
        - **ვიზუალიზაციები**: ყველა დიაგრამა ინარჩუნებს ამ თანმიმდევრულ დალაგებას ადვილი შედარებისთვის
        
        ## შეზღუდვები
        
        1. **დროითი ფარგლები**: ანალიზი წარმოადგენს დროის მომენტის სურათს
        2. **ნიმუშის მიკერძოება**: მცირე პროგრამები და უნივერსიტეტები გამოირიცხება, რაც შეიძლება იმოქმედოს რეპრეზენტაციულობაზე
        3. **მონაცემთა სისრულე**: შედეგები დამოკიდებულია წყარო მონაცემების სისრულეზე
        4. **პროგრამების კლასიფიკაცია**: ეყრდნობა უნივერსიტეტის მიერ მოწოდებულ პროგრამების სახელებსა და კლასიფიკაციებს
        
        ## ტექნიკური იმპლემენტაცია
        
        - **მონაცემთა დამუშავება**: Python pandas აგრეგაციისა და ფილტრაციისთვის
        - **ვიზუალიზაციები**: Plotly ინტერაქციული დიაგრამებისთვის
        - **ინტერფეისი**: Streamlit ვებ დაშბორდისთვის
        - **კეშირება**: მონაცემები კეშირდება შესრულების ოპტიმიზაციისთვის
        """
    }
}

# Language selector
lang = st.selectbox(
    "🌐 Language / ენა:",
    options=["en", "ka"],
    format_func=lambda x: "English" if x == "en" else "ქართული",
    index=0
)

t = TRANSLATIONS[lang]

# Load data
@st.cache_data
def load_data():
    data = pd.read_excel("grants.xlsx")
    filtered_data = data[data["აკად/მოსამზად"] == "აკად"]
    filtered_data["გრანტი %"].fillna(0, inplace=True)
    return filtered_data

filtered_data = load_data()

st.title(t["title"])

# Use all data without filtering
display_data = filtered_data

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([t["university_level"], t["program_level"], t["subject_level"], t["raw_data"], t["methodology"]])

with tab1:
    st.header(t["university_analysis"])

    # University aggregated data - filter universities with less than 50 students
    uni_data = display_data.groupby(["უსდ კოდი", "უსდ"]).agg({
        "გრანტი %": "mean",
        "პროგრამა": "count"
    }).round(2).reset_index()

    # Calculate grant counts per university
    grant_counts = display_data.groupby(["უსდ კოდი", "უსდ"]).apply(lambda x: pd.Series({
        "სტუდ. 50% გრანტი": (x["გრანტი %"] == 50).sum(),
        "სტუდ. 70% გრანტი": (x["გრანტი %"] == 70).sum(),
        "სტუდ. 100% გრანტი": (x["გრანტი %"] == 100).sum(),
        "სულ სტუდენტები": len(x)
    })).reset_index()

    # Merge the data and filter universities with less than 50 students
    uni_data = uni_data.merge(grant_counts, on=["უსდ კოდი", "უსდ"])
    uni_data = uni_data[uni_data["სულ სტუდენტები"] >= 50]
    uni_data = uni_data.sort_values("გრანტი %", ascending=False)

    uni_data.columns = ["უსდ კოდი", "უსდ", "საშ. გრანტი %", "პროგრამების რაოდ.", "სტუდ. 50%",
                       "სტუდ. 70%", "სტუდ. 100%", "სულ სტუდ."]

    # Grant percentage visualization - full width
    fig_grant = px.bar(uni_data,
                      x="უსდ", y="საშ. გრანტი %",
                      title=t["avg_grant_by_uni"],
                      color="საშ. გრანტი %",
                      color_continuous_scale="Viridis")
    fig_grant.update_layout(
        xaxis_title="",
        xaxis_showticklabels=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=10),
        title_font_size=14,
        coloraxis_showscale=False  # Hide color scale on mobile
    )
    st.plotly_chart(fig_grant, use_container_width=True)

    # Grant distribution stacked bar chart
    st.subheader(t["grant_dist_by_uni"])
    fig_grants = go.Figure()
    fig_grants.add_trace(go.Bar(
        name=t["50_grant"],
        x=uni_data['უსდ'],
        y=uni_data['სტუდ. 50%'],
        marker_color='lightblue',
        hovertemplate='<b>%{x}</b><br>50% Grant: %{y}<extra></extra>'
    ))
    fig_grants.add_trace(go.Bar(
        name=t["70_grant"],
        x=uni_data['უსდ'],
        y=uni_data['სტუდ. 70%'],
        marker_color='orange',
        hovertemplate='<b>%{x}</b><br>70% Grant: %{y}<extra></extra>'
    ))
    fig_grants.add_trace(go.Bar(
        name=t["100_grant"],
        x=uni_data['უსდ'],
        y=uni_data['სტუდ. 100%'],
        marker_color='green',
        hovertemplate='<b>%{x}</b><br>100% Grant: %{y}<extra></extra>'
    ))
    fig_grants.update_layout(
        barmode='stack',
        title=t["grant_dist_sorted"],
        xaxis_title="",
        yaxis_title='Students' if lang == "en" else 'სტუდ.',
        xaxis_showticklabels=False,
        height=450,  # Increased height to accommodate legend underneath
        margin=dict(l=20, r=20, t=40, b=80),  # Increased bottom margin for legend
        font=dict(size=10),
        title_font_size=14,
        showlegend=True,  # Show legend - will be hidden on mobile via CSS
        legend=dict(
            orientation="h",  # Horizontal legend underneath
            yanchor="top",
            y=-0.15,  # Position below the chart
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )
    st.plotly_chart(fig_grants, use_container_width=True)

    # University data table
    st.subheader(t["uni_summary_table"])
    st.dataframe(uni_data, use_container_width=True)

    # Total grant money pie chart
    st.subheader(t["total_grant_money"])

    # Calculate total grant money per university
    # Grant money = (Grant % / 100) * 2250 * Number of students
    uni_data['სულ გრანტის თანხა (ლარი)'] = (uni_data['საშ. გრანტი %'] / 100) * 2250 * uni_data['სულ სტუდ.']

    # Create pie chart
    fig_pie = px.pie(uni_data,
                     values='სულ გრანტის თანხა (ლარი)',
                     names='უსდ',
                     title=t["grant_money_pie"],
                     hover_data=['სულ სტუდ.', 'საშ. გრანტი %'])

    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent',
        textfont_size=9
    )
    fig_pie.update_layout(
        height=450,  # Increased height for legend
        margin=dict(l=10, r=10, t=40, b=80),  # Increased bottom margin for legend
        font=dict(size=9),
        title_font_size=14,
        showlegend=False  # Remove legend from pie chart
    )

    st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.header(t["program_analysis"])

    # Program aggregated data - filter programs with less than 10 students
    # Group by university and program name only (ignoring program codes)
    prog_counts = display_data.groupby(["უსდ", "პროგრამა"]).size().reset_index(name='student_count')
    valid_programs = prog_counts[prog_counts['student_count'] >= 10][['უსდ', 'პროგრამა']]

    # Filter display_data to only include valid programs
    prog_filtered_data = display_data.merge(valid_programs, on=['უსდ', 'პროგრამა'])

    # Calculate program data with grant distribution
    def calculate_program_stats(group):
        return pd.Series({
            'საშ. გრანტი %': group['გრანტი %'].mean(),
            'სტუდ. 50%': (group['გრანტი %'] == 50).sum(),
            'სტუდ. 70%': (group['გრანტი %'] == 70).sum(),
            'სტუდ. 100%': (group['გრანტი %'] == 100).sum(),
            'სტუდ. რაოდ.': len(group)
        })

    prog_data = prog_filtered_data.groupby(["უსდ", "პროგრამა"]).apply(calculate_program_stats).reset_index()

    # Sort by average grant percentage, then by program name
    prog_data = prog_data.sort_values(["საშ. გრანტი %", "პროგრამა"], ascending=[False, True])

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t["total_programs"], len(prog_data))
    with col2:
        st.metric(t["avg_grant"], f"{prog_data['საშ. გრანტი %'].mean():.1f}%")
    with col3:
        st.metric(t["total_students"], prog_data["სტუდ. რაოდ."].sum())

    # Single comprehensive graph showing top programs with grant distribution
    st.subheader(t["top_30_programs"])

    top_30_programs = prog_data.head(30)

    fig_prog_dist = go.Figure()
    fig_prog_dist.add_trace(go.Bar(
        name='50% Grant',
        x=list(range(len(top_30_programs))),
        y=top_30_programs['სტუდ. 50%'],
        hovertemplate='<b>%{customdata}</b><br>50% Grant: %{y}<extra></extra>',
        customdata=top_30_programs['პროგრამა'],
        marker_color='lightblue'
    ))
    fig_prog_dist.add_trace(go.Bar(
        name='70% Grant',
        x=list(range(len(top_30_programs))),
        y=top_30_programs['სტუდ. 70%'],
        hovertemplate='<b>%{customdata}</b><br>70% Grant: %{y}<extra></extra>',
        customdata=top_30_programs['პროგრამა'],
        marker_color='orange'
    ))
    fig_prog_dist.add_trace(go.Bar(
        name='100% Grant',
        x=list(range(len(top_30_programs))),
        y=top_30_programs['სტუდ. 100%'],
        hovertemplate='<b>%{customdata}</b><br>100% Grant: %{y}<extra></extra>',
        customdata=top_30_programs['პროგრამა'],
        marker_color='green'
    ))

    fig_prog_dist.update_layout(
        barmode='stack',
        title=t["top_30_title"],
        xaxis_title="",
        yaxis_title='Students' if lang == "en" else 'სტუდ.',
        xaxis_showticklabels=False,
        height=550,  # Increased height for legend
        margin=dict(l=20, r=20, t=40, b=80),  # Increased bottom margin for legend
        font=dict(size=10),
        title_font_size=14,
        showlegend=True,  # Show legend - will be hidden on mobile via CSS
        legend=dict(
            orientation="h",  # Horizontal legend underneath
            yanchor="top",
            y=-0.12,  # Position below the chart
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )

    st.plotly_chart(fig_prog_dist, use_container_width=True)

    # Program data table with search
    st.subheader(t["program_details"])
    search_term = st.text_input(t["search_programs"], "")
    if search_term:
        prog_display = prog_data[prog_data["პროგრამა"].str.contains(search_term, case=False, na=False)]
    else:
        prog_display = prog_data

    st.dataframe(prog_display, use_container_width=True)

with tab3:
    st.header(t["subject_analysis"])

    # Subject aggregated data - filter subjects with less than 20 students
    subject_counts = display_data[display_data["არჩევითი საგანი 1"].notna()].groupby("არჩევითი საგანი 1").size().reset_index(name='student_count')
    valid_subjects = subject_counts[subject_counts['student_count'] >= 20]["არჩევითი საგანი 1"].tolist()

    # Filter display_data to only include valid subjects
    subject_filtered_data = display_data[display_data["არჩევითი საგანი 1"].isin(valid_subjects)]

    # Calculate subject data
    def calculate_subject_stats(group):
        return pd.Series({
            'საშ. გრანტი %': group['გრანტი %'].mean(),
            'სტუდ. 50%': (group['გრანტი %'] == 50).sum(),
            'სტუდ. 70%': (group['გრანტი %'] == 70).sum(),
            'სტუდ. 100%': (group['გრანტი %'] == 100).sum(),
            'სტუდ. რაოდ.': len(group)
        })

    subject_data = subject_filtered_data.groupby("არჩევითი საგანი 1").apply(calculate_subject_stats).reset_index()
    subject_data.columns = ["არჩევითი საგანი", "საშ. გრანტი %", "სტუდ. 50%", "სტუდ. 70%", "სტუდ. 100%", "სტუდ. რაოდ."]

    # Sort by average grant percentage
    subject_data = subject_data.sort_values("საშ. გრანტი %", ascending=False)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t["total_subjects"], len(subject_data))
    with col2:
        st.metric(t["avg_grant"], f"{subject_data['საშ. გრანტი %'].mean():.1f}%")
    with col3:
        st.metric(t["total_students"], subject_data["სტუდ. რაოდ."].sum())

    # Subject grant percentage chart
    fig_subject = px.bar(subject_data,
                        x="არჩევითი საგანი", y="საშ. გრანტი %",
                        title=t["avg_grant_by_subject"],
                        color="საშ. გრანტი %",
                        color_continuous_scale="Viridis",
                        hover_data=["სტუდ. რაოდ."])
    fig_subject.update_layout(
        xaxis_title="",
        xaxis_tickangle=45,
        height=450,
        margin=dict(l=20, r=20, t=40, b=80),
        font=dict(size=10),
        title_font_size=14,
        coloraxis_showscale=False,  # Hide color scale
        xaxis=dict(
            tickfont=dict(size=8)
        )
    )
    st.plotly_chart(fig_subject, use_container_width=True)

    # Subject data table with search
    st.subheader(t["subject_details"])
    search_term_subject = st.text_input(t["search_subjects"], "")
    if search_term_subject:
        subject_display = subject_data[subject_data["არჩევითი საგანი"].str.contains(search_term_subject, case=False, na=False)]
    else:
        subject_display = subject_data

    st.dataframe(subject_display, use_container_width=True)

with tab4:
    st.header(t["raw_data_view"])

    # Column selection for raw data
    st.subheader(t["select_columns"])

    # Most relevant columns in order - all columns from the dataset
    relevant_columns = [
        "უსდ კოდი", "უსდ", "პროგ. კოდი", "პროგრამა", "საგამოცდო",
        "ქართული ენა ნედლი ქულა", "ქართული ენა სკალ.", "უცხო ენა",
        "უცხო ენა ნედლი ქულა", "უცხო ენა სკალ.", "არჩევითი საგანი 1",
        "არჩევითი ნედლი ქულა", "არჩევითი სკალ.", "არჩევითი საგანი 2",
        "არჩევითი 2 ნედლი ქულა", "არჩევითი 2 სკალ.", "საკონკ. ქულა",
        "გრანტი %", "არჩევანი", "აკად/მოსამზად"
    ]

    # Filter available columns
    available_columns = [col for col in relevant_columns if col in display_data.columns]

    selected_columns = st.multiselect(
        t["choose_columns"],
        options=available_columns,
        default=available_columns  # Show all available columns by default
    )

    if selected_columns:
        # Add sorting options
        sort_by = st.selectbox(t["sort_by"], options=selected_columns,
                              index=selected_columns.index("გრანტი %") if "გრანტი %" in selected_columns else 0)
        sort_order = st.radio(t["sort_order"], [t["descending"], t["ascending"]])

        # Display filtered and sorted data
        sorted_data = display_data[selected_columns].sort_values(
            sort_by, ascending=(sort_order == t["ascending"])
        )

        st.dataframe(sorted_data, use_container_width=True)

        # Download option
        csv = sorted_data.to_csv(index=False)
        st.download_button(
            label=t["download_csv"],
            data=csv,
            file_name="grant_data_filtered.csv",
            mime="text/csv"
        )

    # Summary statistics
    st.subheader(t["summary_stats"])
    if len(display_data) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t["total_records"], len(display_data))
        with col2:
            st.metric(t["avg_grant"], f"{display_data['გრანტი %'].mean():.1f}%")
        with col3:
            if "საკონკ. ქულა" in display_data.columns:
                st.metric("Average Score" if lang == "en" else "საშუალო ქულა", f"{display_data['საკონკ. ქულა'].mean():.1f}")
        with col4:
            st.metric(t["universities"], display_data["უსდ"].nunique())

with tab5:
    st.header("📖 " + (t["methodology"] if lang == "ka" else "Methodology"))

    st.markdown(t["methodology_content"])

    # Add some summary statistics about the data
    st.subheader("📊 " + ("მონაცემთა შემაჯამებელი სტატისტიკა" if lang == "ka" else "Data Summary Statistics"))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Records Processed",
            f"{len(filtered_data):,}"
        )
        st.metric(
            "Academic Records Only",
            f"{len(display_data):,}"
        )

    with col2:
        universities_total = display_data["უსდ"].nunique()
        universities_filtered = len(display_data.groupby(["უსდ კოდი", "უსდ"]).size()[display_data.groupby(["უსდ კოდი", "უსდ"]).size() >= 50])
        st.metric(
            "Total Universities",
            universities_total
        )
        st.metric(
            "Universities (≥50 students)",
            universities_filtered
        )

    with col3:
        programs_total = display_data.groupby(["უსდ", "პროგრამა"]).size().shape[0]
        programs_filtered = len(display_data.groupby(["უსდ", "პროგრამა"]).size()[display_data.groupby(["უსდ", "პროგრამა"]).size() >= 10])
        st.metric(
            "Total Programs",
            programs_total
        )
        st.metric(
            "Programs (≥10 students)",
            programs_filtered
        )
