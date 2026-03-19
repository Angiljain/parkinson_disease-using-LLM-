"""
Enhanced Streamlit Web Interface for PD Screening System
Beautiful, modern UI with improved user experience
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

from main import PDScreeningSystem

# Page configuration
st.set_page_config(
    page_title="PD Screening Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .info-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .success-card {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ff6b6b;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .danger-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #666;
        font-weight: 500;
    }
    
    /* Disclaimer box */
    .disclaimer-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        border: 2px solid #ffc107;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .disclaimer-box h3 {
        color: #856404;
        margin-top: 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Text area */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'system' not in st.session_state:
        with st.spinner("🔄 Initializing AI system..."):
            st.session_state.system = PDScreeningSystem()
            st.session_state.history = []
            st.session_state.total_screenings = 0


def create_risk_gauge(risk_score, confidence):
    """Create a beautiful risk gauge chart"""
    
    # Determine color based on risk
    if risk_score < 0.4:
        color = "#28a745"  # Green
        risk_text = "LOW RISK"
    elif risk_score < 0.7:
        color = "#ffc107"  # Yellow
        risk_text = "MODERATE RISK"
    else:
        color = "#dc3545"  # Red
        risk_text = "HIGHER RISK"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"<b>{risk_text}</b><br><span style='font-size:0.8em'>Confidence: {confidence.upper()}</span>", 
                 'font': {'size': 20}},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#d4edda'},
                {'range': [40, 70], 'color': '#fff3cd'},
                {'range': [70, 100], 'color': '#f8d7da'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig


def create_feature_chart(features):
    """Create feature visualization chart"""
    if not features:
        return None
    
    # Prepare data
    metrics = {
        'Word Count': features.get('word_count', 0),
        'Sentences': features.get('sentence_count', 0),
        'Unique Words': features.get('unique_words', 0),
        'Avg Word Length': features.get('avg_word_length', 0) * 2,  # Scale for visibility
        'Lexical Diversity': features.get('lexical_diversity', 0) * 100
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(metrics.keys()),
            y=list(metrics.values()),
            marker_color=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'],
            text=list(metrics.values()),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Linguistic Features Analysis",
        xaxis_title="Feature",
        yaxis_title="Value",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12)
    )
    
    return fig


def display_results(results):
    """Display screening results with enhanced visuals"""
    response = results['screening_response']
    
    st.markdown("## 📊 Screening Results")
    
    # Risk gauge
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = create_risk_gauge(response['risk_score'], response['confidence'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Metrics
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-label'>Risk Score</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{response['risk_score']:.2f}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='metric-card' style='margin-top: 1rem;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-label'>Confidence Level</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{response['confidence'].upper()}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Rationale
    st.markdown("### 🔍 Detailed Analysis")
    
    for i, point in enumerate(response['rationale'], 1):
        with st.expander(f"**Finding {i}**", expanded=True):
            st.markdown(f"✓ {point}")
    
    st.markdown("---")
    
    # Recommendation
    st.markdown("### 💡 Recommendation")
    
    rec = response['recommendation']
    
    if rec == 'refer for evaluation':
        st.markdown(f"""
        <div class='danger-card'>
            <h3>⚠️ REFER FOR PROFESSIONAL EVALUATION</h3>
            <p>Based on the analysis, we recommend consulting with a healthcare professional 
            (neurologist or movement disorder specialist) for comprehensive evaluation.</p>
            <p><strong>Next Steps:</strong></p>
            <ul>
                <li>Schedule appointment with neurologist</li>
                <li>Bring this screening report</li>
                <li>Note any symptom progression</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif rec == 'monitor':
        st.markdown(f"""
        <div class='warning-card'>
            <h3>👀 MONITOR SYMPTOMS</h3>
            <p>Continue to monitor symptoms and consult a healthcare provider if changes occur.</p>
            <p><strong>Recommendations:</strong></p>
            <ul>
                <li>Keep symptom diary</li>
                <li>Rescreen in 3-6 months</li>
                <li>Contact doctor if symptoms worsen</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='info-card'>
            <h3>ℹ️ INSUFFICIENT DATA</h3>
            <p>More detailed information needed for meaningful assessment.</p>
            <p><strong>Please provide:</strong></p>
            <ul>
                <li>More detailed symptom description</li>
                <li>Timeline of any changes</li>
                <li>Specific examples of difficulties</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Linguistic features
    if 'metadata' in results and 'preprocessing' in results['metadata']:
        features = results['metadata']['preprocessing'].get('features', {})
        if features:
            st.markdown("---")
            st.markdown("### 📈 Linguistic Analysis")
            fig = create_feature_chart(features)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Retrieved context (collapsible)
    if 'metadata' in results and 'retrieval' in results['metadata']:
        with st.expander("📚 Medical Knowledge Used"):
            passages = results['metadata']['retrieval'].get('passages', [])
            if passages:
                for i, passage in enumerate(passages, 1):
                    st.markdown(f"**Source {i}** (Relevance: {passage.get('similarity', 0):.1%})")
                    st.info(passage.get('text', 'N/A')[:300] + "...")
            else:
                st.info("No specific medical context retrieved")


def main():
    """Main Streamlit application"""
    
    # Initialize
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class='main-header'>
        <h1>🧠 Parkinson's Disease Screening Assistant</h1>
        <p>AI-powered text analysis for early detection indicators</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class='disclaimer-box'>
        <h3>⚠️ IMPORTANT MEDICAL DISCLAIMER</h3>
        <p><strong>This tool provides screening only and is NOT a medical diagnosis.</strong></p>
        <p>It uses artificial intelligence to assess potential risk indicators based on text patterns 
        and medical literature. Always consult a qualified healthcare professional for proper medical 
        evaluation and diagnosis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ℹ️ About This Tool")
        
        st.markdown("""
        This system analyzes text transcripts to identify potential linguistic and speech 
        patterns associated with Parkinson's Disease using:
        
        - 🤖 **Advanced AI** (Groq LLaMA 3.1)
        - 📚 **Medical Knowledge Base**
        - 🔍 **Evidence-Based Analysis**
        """)
        
        st.markdown("---")
        
        st.markdown("### 📊 Statistics")
        stats = st.session_state.system.get_system_stats()
        st.metric("Knowledge Base", f"{stats['vector_store']['document_count']} documents")
        st.metric("LLM Model", stats['llm']['model'])
        st.metric("Total Screenings", st.session_state.total_screenings)
        
        st.markdown("---")
        
        # Example transcripts
        st.markdown("### 📝 Try Examples")
        
        if st.button("🟢 Low Risk Example", use_container_width=True):
            st.session_state.example_text = "I feel great today and have been very active lately. I exercise regularly and have no movement or speech issues."
        
        if st.button("🟡 Moderate Risk Example", use_container_width=True):
            st.session_state.example_text = "I've noticed my handwriting getting smaller and my voice seems softer than before. Sometimes I feel a bit stiff in the morning."
        
        if st.button("🔴 Higher Risk Example", use_container_width=True):
            st.session_state.example_text = "My right hand trembles when resting, I'm moving slower than usual, and people say I don't smile as much. My handwriting has become very small."
        
        st.markdown("---")
        
        # Download history
        if st.session_state.history:
            history_df = pd.DataFrame(st.session_state.history)
            csv = history_df.to_csv(index=False)
            st.download_button(
                label="📥 Download History",
                data=csv,
                file_name=f"screening_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Main content
    st.markdown("## 📝 Enter Your Transcript")
    
    st.markdown("""
    <div class='info-card'>
        <strong>💡 Tips for Better Results:</strong>
        <ul>
            <li>Be specific about symptoms (tremor, stiffness, speech changes, etc.)</li>
            <li>Mention when symptoms started and how they've progressed</li>
            <li>Include details about daily activities affected</li>
            <li>Use at least 2-3 sentences for meaningful analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input
    default_text = st.session_state.get('example_text', '')
    transcript = st.text_area(
        "Describe your symptoms or health observations:",
        value=default_text,
        height=150,
        placeholder="Example: Over the past few months, I've noticed my handwriting has become much smaller. My voice seems softer and people often ask me to repeat myself. I also have a slight tremor in my right hand when it's resting...",
        help="Provide detailed description of any symptoms, changes in movement, speech, handwriting, or other concerns"
    )
    
    # Clear example text after use
    if 'example_text' in st.session_state:
        del st.session_state.example_text
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        analyze_button = st.button("🔍 Analyze Transcript", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    with col3:
        show_help = st.button("❓ Help", use_container_width=True)
    
    if show_help:
        st.info("""
        **How to use:**
        1. Type or paste a description of symptoms in the text box
        2. Click 'Analyze Transcript' to run the screening
        3. Review the risk assessment and recommendations
        4. Download results if needed
        
        **What to include:**
        - Movement changes (tremor, stiffness, slowness)
        - Speech or voice changes
        - Handwriting changes
        - Balance or walking difficulties
        - Facial expression changes
        - Timeline and progression
        """)
    
    if clear_button:
        st.rerun()
    
    # Analysis
    if analyze_button:
        if not transcript or len(transcript.strip()) < 10:
            st.error("⚠️ Please enter a more detailed transcript (at least 10 characters).")
        else:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Preprocessing
                status_text.text("🔄 Step 1/3: Preprocessing transcript...")
                progress_bar.progress(33)
                
                # Step 2: Retrieving context
                status_text.text("🔄 Step 2/3: Retrieving medical knowledge...")
                progress_bar.progress(66)
                
                # Step 3: AI Analysis
                status_text.text("🔄 Step 3/3: AI analysis in progress...")
                progress_bar.progress(90)
                
                # Run screening
                results = st.session_state.system.screen_transcript(
                    transcript,
                    include_details=True
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                # Update statistics
                st.session_state.total_screenings += 1
                
                # Save to history
                st.session_state.history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'transcript': transcript[:100] + "..." if len(transcript) > 100 else transcript,
                    'risk_score': results['screening_response']['risk_score'],
                    'confidence': results['screening_response']['confidence'],
                    'recommendation': results['screening_response']['recommendation']
                })
                
                # Clear progress
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                st.markdown("---")
                display_results(results)
                
                # Download option
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    results_json = json.dumps(results, indent=2)
                    st.download_button(
                        label="📥 Download Results (JSON)",
                        data=results_json,
                        file_name=f"pd_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col2:
                    # Generate PDF-style report
                    report = f"""
PARKINSON'S DISEASE SCREENING REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

RISK ASSESSMENT:
- Risk Score: {results['screening_response']['risk_score']:.2f}
- Confidence: {results['screening_response']['confidence'].upper()}
- Recommendation: {results['screening_response']['recommendation'].upper()}

ANALYSIS:
{chr(10).join(f"• {point}" for point in results['screening_response']['rationale'])}

TRANSCRIPT:
{transcript}

DISCLAIMER: This is a screening tool only, not a medical diagnosis.
Consult a healthcare professional for proper evaluation.
                    """
                    st.download_button(
                        label="📄 Download Report (TXT)",
                        data=report,
                        file_name=f"screening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ An error occurred: {str(e)}")
                st.error("Please check your configuration and API keys.")
                with st.expander("Error Details"):
                    st.code(str(e))
    
    # History section
    if st.session_state.history:
        st.markdown("---")
        st.markdown("## 📜 Recent Screenings")
        
        # Create DataFrame
        history_df = pd.DataFrame(st.session_state.history[-10:])  # Last 10
        
        # Display as cards
        for idx, item in enumerate(reversed(st.session_state.history[-5:]), 1):
            risk = item['risk_score']
            if risk < 0.4:
                card_class = "success-card"
                icon = "🟢"
            elif risk < 0.7:
                card_class = "warning-card"
                icon = "🟡"
            else:
                card_class = "danger-card"
                icon = "🔴"
            
            with st.expander(f"{icon} Screening {len(st.session_state.history) - idx + 1} - {item['timestamp']}"):
                st.markdown(f"**Transcript:** {item['transcript']}")
                col1, col2, col3 = st.columns(3)
                col1.metric("Risk Score", f"{item['risk_score']:.2f}")
                col2.metric("Confidence", item['confidence'].upper())
                col3.metric("Recommendation", item['recommendation'][:20] + "...")


if __name__ == "__main__":
    main()