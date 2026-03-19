"""
Enhanced Medical Knowledge Base
More detailed and comprehensive PD information for better accuracy
"""

def get_enhanced_medical_knowledge():
    """
    Returns comprehensive medical knowledge for PD screening
    Includes detailed clinical information, research findings, and diagnostic criteria
    """
    
    enhanced_documents = [
        # Cardinal Motor Symptoms - Detailed
        {
            'text': """Resting tremor in Parkinson's disease typically presents as a 4-6 Hz rhythmic oscillation, 
            most commonly manifesting as a pill-rolling movement of the thumb and fingers. The tremor is characteristically 
            present at rest, diminishes with voluntary movement, and may be exacerbated by stress, fatigue, or cognitive tasks. 
            It usually begins unilaterally (asymmetric onset) in one hand or arm and may later spread to the contralateral side. 
            The tremor may also affect the legs, jaw, or lips. Re-emergent tremor (reappearing after maintaining a posture) 
            is highly specific for PD. Essential tremor, in contrast, is typically bilateral, faster (6-12 Hz), 
            and occurs during action rather than at rest.""",
            'metadata': {'source': 'Clinical_Neurology', 'category': 'cardinal_symptoms', 'type': 'tremor', 'detail_level': 'high'}
        },
        {
            'text': """Bradykinesia, or slowness of movement, is the most specific motor feature of Parkinson's disease 
            and must be present for diagnosis. It manifests as reduced speed, reduced amplitude of movement, 
            progressive fatigue and decrement in amplitude with repetitive movements (sequence effect), and difficulty 
            initiating movements (akinesia). Clinical assessment includes finger tapping (rapidly touching thumb to index finger), 
            hand movements (opening and closing fist), and pronation-supination of hands. Patients often report difficulty 
            with fine motor tasks like buttoning shirts, using utensils, typing, or handwriting. Gait is affected with 
            reduced arm swing, shorter steps, and shuffling. The MDS-UPDRS specifically evaluates bradykinesia through 
            timed repetitive movements, looking for decreasing amplitude and speed.""",
            'metadata': {'source': 'MDS-UPDRS_Manual', 'category': 'cardinal_symptoms', 'type': 'bradykinesia', 'detail_level': 'high'}
        },
        {
            'text': """Rigidity in PD is characterized by increased muscle tone throughout the entire range of passive movement 
            of a limb, affecting both flexor and extensor muscles equally (lead-pipe rigidity). When combined with tremor, 
            it produces cogwheel rigidity - a ratchet-like resistance to passive movement. Rigidity contributes to the 
            stooped posture common in PD, reduced arm swing during walking, muscle aches and pains (often misdiagnosed 
            as arthritis), and the masked facies (reduced facial expression) due to facial muscle rigidity. Unlike spasticity 
            seen in upper motor neuron lesions, parkinsonian rigidity is not velocity-dependent and affects proximal 
            and distal muscles similarly. Patients may describe this as stiffness, particularly in the neck, shoulders, or legs.""",
            'metadata': {'source': 'Movement_Disorders_Textbook', 'category': 'cardinal_symptoms', 'type': 'rigidity', 'detail_level': 'high'}
        },
        
        # Speech and Voice - Comprehensive
        {
            'text': """Hypokinetic dysarthria in Parkinson's disease encompasses multiple speech dimensions. 
            Hypophonia (reduced loudness) is often the earliest and most prominent feature, with patients speaking 
            at 3-5 dB below normal conversational levels. Speech becomes monotonous with reduced pitch variability 
            (monopitch) and reduced loudness variability (monoloudness), losing the normal prosodic patterns that 
            convey emotion and emphasis. Articulatory precision decreases, with consonants becoming imprecise and 
            vowels centralized. Speech rate may be increased (festinating speech) or decreased, with short rushes 
            of speech and inappropriate silent intervals. Patients often exhibit reduced phrase length and increased 
            pause time ratio. Voice quality may be breathy, harsh, or tremulous. Importantly, patients frequently 
            lack awareness of their reduced volume, a phenomenon related to impaired self-monitoring. 
            Family members typically report that they must ask the patient to repeat themselves frequently, 
            or that the patient seems to mumble.""",
            'metadata': {'source': 'Speech_Pathology_Research', 'category': 'speech', 'type': 'comprehensive', 'detail_level': 'high'}
        },
        
        # Micrographia - Detailed
        {
            'text': """Micrographia, the production of abnormally small handwriting, is a highly specific sign of 
            Parkinson's disease affecting approximately 63% of patients. It can be present before motor symptom onset. 
            There are two types: consistent micrographia where writing is uniformly small from the start, and 
            progressive micrographia where writing starts normal-sized but becomes progressively smaller (more common in PD). 
            The progressive nature reflects the sequence effect characteristic of bradykinesia. Patients may report that 
            signatures have become illegible, checks are difficult to write, or writing requires more effort and concentration. 
            Micrographia worsens with fatigue, stress, or when attention is divided. It improves temporarily with 
            cueing (e.g., "write larger") but deteriorates again quickly. The mechanism involves dysfunction of 
            basal ganglia circuits controlling motor program scaling and amplitude.""",
            'metadata': {'source': 'Journal_Movement_Disorders', 'category': 'writing', 'type': 'micrographia', 'detail_level': 'high'}
        },
        
        # Early Signs and Prodromal Symptoms
        {
            'text': """Prodromal or premotor features of Parkinson's disease can precede motor symptoms by years or decades. 
            REM sleep behavior disorder (RBD) is one of the strongest predictors, with 80-90% of patients with idiopathic RBD 
            eventually developing PD or related synucleinopathy within 10-15 years. Hyposmia (reduced sense of smell) 
            affects 90% of PD patients and can precede motor symptoms by 4-6 years. Constipation, defined as fewer than 
            3 bowel movements per week, occurs in 50-80% of patients and may precede diagnosis by up to 20 years. 
            Depression and anxiety affect 40-50% of patients, often preceding motor symptoms. Other prodromal features 
            include subtle cognitive changes (executive dysfunction), excessive daytime sleepiness, urinary dysfunction, 
            erectile dysfunction, and subtle motor signs like reduced arm swing or slight slowing. The presence of 
            multiple prodromal markers significantly increases risk of developing PD.""",
            'metadata': {'source': 'Prodromal_PD_Research', 'category': 'early_signs', 'type': 'prodromal', 'detail_level': 'high'}
        },
        
        # Linguistic and Cognitive Features
        {
            'text': """Linguistic analysis reveals specific patterns in PD speech beyond motor dysarthria. 
            Lexical-semantic features include reduced lexical diversity (type-token ratio), decreased use of 
            complex vocabulary, and increased use of high-frequency words. Syntactic complexity decreases, with 
            shorter sentences, simpler grammatical structures, and reduced use of embedded clauses. Discourse 
            features show reduced information content, tangential speech, and difficulty with topic maintenance. 
            Word-finding difficulties (anomia) are common, manifesting as increased word-finding pauses, circumlocutions, 
            and substitution with generic terms (e.g., "thing" instead of specific noun). These changes reflect 
            both the motor aspects of speech production and the cognitive changes (executive dysfunction, 
            working memory deficits) that frequently accompany PD. Automated speech analysis using natural language 
            processing can detect these patterns with 85-90% accuracy in distinguishing PD from healthy controls.""",
            'metadata': {'source': 'Computational_Linguistics_PD', 'category': 'linguistic', 'type': 'comprehensive', 'detail_level': 'high'}
        },
        
        # Differential Diagnosis Considerations
        {
            'text': """Differential diagnosis is critical in PD screening. Essential tremor presents with bilateral 
            action/postural tremor (not rest tremor), no bradykinesia, and often positive family history. Drug-induced 
            parkinsonism (from antipsychotics, antiemetics) typically has symmetric onset, no tremor, and temporal 
            relationship to medication. Vascular parkinsonism shows lower body predominance, gait difficulties out 
            of proportion to upper body symptoms, and step-wise progression. Progressive supranuclear palsy (PSP) 
            presents with early falls, vertical gaze palsy, axial rigidity, and symmetric onset. Multiple system 
            atrophy (MSA) shows early autonomic failure, cerebellar signs, and poor levodopa response. Normal aging 
            may cause mild slowing but lacks the progression, asymmetry, and specific features of PD. Red flags 
            suggesting alternative diagnoses include: symmetric onset, rapid progression, early severe dementia, 
            early falls, poor levodopa response, pyramidal signs, cerebellar signs, or prominent autonomic failure 
            at onset.""",
            'metadata': {'source': 'Differential_Diagnosis_Guide', 'category': 'differential', 'type': 'comprehensive', 'detail_level': 'high'}
        },
        
        # Asymmetry and Progression
        {
            'text': """Asymmetric onset and progression is a hallmark of idiopathic Parkinson's disease. 
            Symptoms typically begin unilaterally (one side of the body), most commonly in one hand or arm, 
            and remain asymmetric throughout the disease course, though the initially less affected side 
            eventually develops symptoms. The side first affected usually remains more severely affected. 
            This asymmetry helps distinguish PD from conditions like vascular parkinsonism or drug-induced 
            parkinsonism, which tend to be symmetric. Progression in PD is gradual, typically over months 
            to years, not days to weeks. Patients or family members often can identify a specific side 
            where symptoms began (e.g., "my right hand started shaking about a year ago"). The rate of 
            progression varies but follows a relatively predictable pattern, with motor symptoms progressing 
            according to Hoehn and Yahr stages. Sudden onset or rapid progression suggests alternative diagnosis.""",
            'metadata': {'source': 'PD_Natural_History', 'category': 'progression', 'type': 'asymmetry', 'detail_level': 'high'}
        },
        
        # Family Observations
        {
            'text': """Family member observations are often more reliable than patient self-report for certain 
            PD features. Relatives typically notice masked facies (reduced facial expression) before patients 
            are aware of it, often commenting that the patient "looks sad" or "seems less expressive." 
            Changes in voice volume (hypophonia) are frequently first noted by family members who must ask 
            the patient to speak up. Reduced arm swing during walking is typically observed by others rather 
            than reported by patients. Family may notice changes in handwriting before the patient does. 
            REM sleep behavior disorder (acting out dreams) is almost always reported by a bed partner. 
            Family members may observe shuffling gait, decreased blinking, or difficulty arising from chairs. 
            In medical history taking, asking "Have family members or friends noticed any changes?" often 
            yields more diagnostic information than asking the patient directly about subtle symptoms they 
            may not have perceived.""",
            'metadata': {'source': 'Clinical_Assessment_PD', 'category': 'observation', 'type': 'family_report', 'detail_level': 'high'}
        },
        
        # Age and Demographics
        {
            'text': """Age is a critical factor in PD risk assessment. The incidence of PD increases dramatically 
            with age: approximately 0.3% of the population over 40, 1% over 60, and 3-4% over 80 are affected. 
            Mean age of onset is 60 years. Young-onset PD (YOPD), defined as onset before age 50, occurs in 
            5-10% of cases and often has genetic factors. Very early onset (before 40) warrants genetic testing. 
            However, PD can occur at any age. In younger individuals, symptoms may be more subtle, progression 
            slower, and dystonia more prominent. Late-onset PD (after 70) may progress faster and have more 
            cognitive involvement. Gender affects risk - men are 1.5 times more likely to develop PD than women. 
            Race/ethnicity also influences risk, with higher rates in Caucasians and Hispanics compared to 
            African Americans and Asians. When evaluating screening results, these demographic factors provide 
            important context for risk stratification.""",
            'metadata': {'source': 'Epidemiology_PD', 'category': 'demographics', 'type': 'risk_factors', 'detail_level': 'high'}
        },
        
        # MDS-UPDRS Screening Context
        {
            'text': """The Movement Disorder Society-Unified Parkinson's Disease Rating Scale (MDS-UPDRS) is 
            the gold standard clinical assessment tool. Part I assesses non-motor experiences of daily living 
            (13 items including cognitive impairment, depression, anxiety, sleep). Part II evaluates motor 
            experiences of daily living (13 items including speech, swallowing, handwriting, eating tasks). 
            Part III is the motor examination (18 items scored 0-4, including speech assessment, facial expression, 
        rigidity in all limbs, finger tapping, hand movements, rapid alternating movements, toe tapping, 
            leg agility, arising from chair, gait, postural stability, and posture). Part IV assesses motor 
            complications. For screening purposes, presence and pattern of symptoms rather than precise scoring 
            is most relevant. Key MDS-UPDRS screening indicators include: speech difficulties (question 3.1), 
            facial expression changes (3.2), tremor at rest (3.17-3.18), and bradykinesia in finger tapping 
            (3.4), hand movements (3.5), or rapid alternating movements (3.6).""",
            'metadata': {'source': 'MDS-UPDRS_Guidelines', 'category': 'assessment', 'type': 'clinical_tool', 'detail_level': 'high'}
        },
        
        # Timeline and Progression Patterns
        {
            'text': """Understanding typical PD timelines aids in risk assessment. Initial symptoms are often 
            subtle and may be attributed to normal aging or ignored for 1-3 years before medical consultation. 
            The prodromal phase can extend 5-20 years before motor diagnosis. Once motor symptoms appear, 
            progression typically follows this pattern: First 2-5 years - asymmetric tremor and/or bradykinesia, 
            good medication response. Years 5-10 - bilateral involvement, possible motor fluctuations and dyskinesias 
            if on levodopa, gait difficulties emerging. Years 10-15 - postural instability, increased falls, 
            possible cognitive changes. After 15 years - more severe motor disability, cognitive impairment common, 
            autonomic dysfunction. Key point for screening: Gradual onset over months to years is characteristic. 
            Symptoms appearing and progressing over days to weeks suggest alternative diagnosis (stroke, drug reaction, 
            other neurological conditions). When patients describe symptom timeline, look for: (1) slow evolution, 
            (2) progression rather than fluctuation, (3) asymmetric onset, (4) addition of new symptoms over time.""",
            'metadata': {'source': 'Natural_History_PD', 'category': 'progression', 'type': 'timeline', 'detail_level': 'high'}
        },
        
        # Combination Patterns - High Risk
        {
            'text': """Certain symptom combinations are particularly significant for PD screening. HIGH RISK patterns: 
            (1) Resting tremor + bradykinesia + micrographia (three cardinal features across domains), 
            (2) Unilateral tremor + ipsilateral arm swing reduction + speech changes (asymmetric multi-domain involvement), 
            (3) Progressive micrographia + hypophonia + masked facies (motor control across speech, writing, facial expression), 
            (4) Bradykinesia + rigidity + hyposmia/RBD (motor symptoms with prodromal markers), 
            (5) Multiple symptoms noticed by family + patient less aware (characteristic of PD presentation). 
            MODERATE RISK patterns: (1) Isolated resting tremor with progression, (2) Speech changes + writing changes without other motor signs, 
            (3) Multiple non-motor symptoms (sleep, mood, constipation) + subtle motor slowing. LOW RISK patterns: 
            (1) Bilateral action tremor only (suggests essential tremor), (2) Sudden onset symptoms, (3) Symmetric presentation, 
            (4) Isolated symptom with no progression.""",
            'metadata': {'source': 'Clinical_Decision_Making', 'category': 'patterns', 'type': 'combinations', 'detail_level': 'high'}
        },
        
        # Severity Indicators
        {
            'text': """Symptom severity indicators help gauge urgency of referral. IMMEDIATE REFERRAL indicators: 
            Frequent falls (suggests postural instability or alternative diagnosis), rapid progression over weeks to months, 
            significant functional impairment in activities of daily living, severe speech difficulties affecting communication, 
            dystonia or severe rigidity, symptoms in young adult (genetic workup needed), new neurological signs (weakness, numbness, 
            vision changes). URGENT REFERRAL indicators: Two or more cardinal symptoms, progressive worsening over 6-12 months, 
            family members expressing significant concern, symptoms affecting work or social function, writing becoming illegible, 
            voice barely audible. ROUTINE REFERRAL indicators: Single cardinal symptom with slow progression, mild symptoms 
            not yet affecting function, family history of PD, multiple prodromal symptoms. MONITOR indicators: Vague or 
            non-specific symptoms, no clear progression, alternative explanations likely, patient very concerned but objective 
            findings minimal.""",
            'metadata': {'source': 'Referral_Guidelines', 'category': 'severity', 'type': 'urgency', 'detail_level': 'high'}
        }
    ]
    
    return enhanced_documents


if __name__ == "__main__":
    docs = get_enhanced_medical_knowledge()
    print(f"Enhanced knowledge base contains {len(docs)} documents")
    print(f"\nCategories: {set(d['metadata']['category'] for d in docs)}")
    print(f"Detail levels: {set(d['metadata']['detail_level'] for d in docs)}")