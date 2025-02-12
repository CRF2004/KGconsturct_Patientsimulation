init_prompt = """
    "You are a top-tier algorithm designed for extracting information in structured "
    "formats to build a knowledge graph.\n"
    "Try to capture as much information from the patient's case report as possible without "
    "sacrifing accuracy. Do not add any information that is not explicitly "
    """
    #"Ensuring that the resulting knowledge graph is comprehensive and centered around the patient with a rich structure.""
    #"The graph should capture and link all relevant entities and relationships in the medical domain related to the patient."

ner_prompt = """
    **Task**: Extract all entities from the provided text and format them as a JSON array.  
    **Instructions**:  
    1. **Identify New Entities**:  
    - Extract all entities mentioned in the text that are **not already in the provided list below**.  
    - For each new entity, provide:  
        - `name`: The name of the entity (capitalized).  
        - `label`: One of the following labels: [{entity_labels}]. **Do not create new labels unless necessary**.  
        - `description`: A detailed description of the entity's attributes, activities, or context. If no description is available, use an empty string ("").  

    **Output Format**:  
    - Format each entity as a JSON object.  
    - Return all new entities as a JSON array.  
    - **Strictly follow the example format below**:  
    **Example Output**:  
    [
        {{
            "name": "Patient",
            "label": "Person",
            "description": "A 45-year-old male who presented to the emergency service with symptoms of fever and difficulty breathing."
        }},
        {{
            "name": "Total Leukocyte Count",
            "label": "Laboratory Test",
            "description": "2,900/𝜇L, below the reference range of 4,000-11,000/𝜇L."
        }}
    ]
    
    **Rules**:  
    - **Global Entity List**: `[{entity_name}]`The provided list contains all names and labels of each entities you've extracted. Do not add any entities that are already in the list.
    - **Strict Deduplication**: Do not extract any entity that matches (case-insensitively) or is a synonym of an entity in the list above.  
    - **Do not invent entities** that are not explicitly mentioned in the text.  
    - **Do not add new labels unless necessary** outside the provided list: [{entity_labels}].  

    **Text to Analyze**:  
    {text}
    **Output**:
"""
gleaning_prompt="""
    You are a top-tier algorithm designed for extracting relationships in structured formats to build a knowledge graph.\n"
    "Try to capture as much information from the patient's case report as possible without sacrifing accuracy. Do not add any information that is not explicitly "
    -Now You've recognized the following entities in the text:{entity_name}

    *MANY entities were missed in the last extraction
    *Task*: Now you need to extract the left entities in the text.
    *Do not add new labels unless necessary** outside the provided list: [{entity_labels}].  
    **Output Format**:  
    - Format each entity as a JSON object.  
    - Return all new entities as a JSON array.   
    *Strictly follow the example format below**:  
    **Example Output**:  
    [
        {{
            "name": "Patient",
            "label": "Person",
            "description": "A 45-year-old male who presented to the emergency service with symptoms of fever and difficulty breathing."
        }},
        {{
            "name": "Total Leukocyte Count",
            "label": "Laboratory Test",
            "description": "2,900/𝜇L, below the reference range of 4,000-11,000/𝜇L."
        }}
    ]
    **Rule**: Strictly adhere to the provided list of entities. If an entity has already been included in the list, do not include it again. Any entity that matches (even partially or case-insensitively) with the already provided entities must be excluded.
    -text:{text}
    
    -output:
"""

    
re_prompt = """
    1. **Entities Identified** (use ONLY these entities):
    [{entity_name}]

    2. **Relationship Extraction Rules**:
    - **Broad Relationship Scope**: Extract ALL possible relationships, even if weak or indirect.
    - **Key Signals to Capture**:
    - Co-occurrence in the same sentence or adjacent sentences
    - Verb-based interactions (e.g., "treated with", "caused by")
    - Attribute associations (e.g., "level of glucose", "dose of metformin")
    - Implicit connections (e.g., "diabetes" and "hyperglycemia" are clinically related)
    - **Strength Scoring**:
    - 1-3: Weak (e.g., co-occurrence without clear interaction)
    - 4-6: Moderate (e.g., one entity describes another)
    - 7-9: Strong (e.g., direct action or causation)
    - 10: Very Strong (e.g., explicit verb or clinical guideline)

    3. **Output Requirements**:
    - Generate AT LEAST 5 relationships per text (if possible).
    - Include relationships even if they are weak (strength 1-3).
    - If a relationship does not fit the rules, use '""' to fullfill the requirement. Such as "relationship_description": "",
    - Use the following JSON format for each relationship:
    {{
        "source": "<source_entity>",
        "target": "<target_entity>",
        "relationship_label": "<relationship_label>",
        "relationship_description": "<description>",
        "relationship_strength": <strength>
    }}

    4. **Examples**:
    - Strong Relationship:
    {{
        "source": "metformin",
        "target": "diabetes",
        "relationship_label": "TREATS",
        "relationship_description": "Metformin is prescribed to manage diabetes.",
        "relationship_strength": 9
    }}
    - Weak Relationship:
    {{
        "source": "glucose",
        "target": "9.8 mmol/L",
        "relationship_label": "HAS_VALUE",
        "relationship_description": "The glucose level is measured at 9.8 mmol/L.",
        "relationship_strength": 3
    }}

    Text: {text}
"""
    
eval_prompt1 = """
**Role**: You are a meticulous **Quality Assurance Analyst** specialized in information extraction. Your task is to rigorously audit entity extraction completeness. You must:  
- Approach the task with extreme skepticism.  
- Assume missing entities exist unless proven otherwise.  
- Prioritize recall over speed - false negatives are unacceptable.  
- Strictly follow decision criteria without improvisation.  

**Task**: Assess whether all entities have been fully extracted from the current text chunk.  

**Instructions**:  
1. Review the text chunk below and the list of entities already extracted.  
2. Determine if any entities (e.g., named entities, domain-specific terms, or contextual concepts) remain unextracted.  
3. Respond **strictly with "YES" or "NO"** based on the following criteria:  
   - **YES**: If entities are clearly missing (e.g., obvious names, terms, or contextual references not in the extracted list).  
   - **NO**: If no additional entities can be reasonably identified.  

**Text Chunk**:  
"{text}"  

**Extracted Entities**:  
{entity_name}  

**Response**: [YES/NO]  
"""
eval_prompt2 = """
    **Role**: You are a **Relationship Extraction Auditor** specializing in evaluating the completeness of semantic relationships extracted from text. Your task is to rigorously assess whether all meaningful relationships have been captured, based on the provided entities and text.

    **Task**: Evaluate whether all relevant relationships in the text chunk have been fully extracted, including both explicit and implicit connections, using the extracted entities as a reference.

    **Evaluation Criteria**:
    1. **Explicit Relationships**:
    - Verb-based connections (e.g., "Apple announced a partnership").
    - Prepositional relationships (e.g., "features for iOS devices").
    2. **Implicit Relationships**:
    - Co-occurrence relationships (e.g., entities appearing in the same context).
    - Causal relationships (e.g., "due to", "because of").
    - Comparative relationships (e.g., "better than", "similar to").
    3. **Cross-Sentence Relationships**:
    - Pronoun references (e.g., "it", "they").
    - Contextual dependencies across sentences.

    **Instructions**:
    1. Review the text chunk, the extracted entities, and the extracted relationships.
    2. Identify any missing relationships based on the evaluation criteria above.
    3. Respond **strictly with one of the following options**:
    - **YES**: If any meaningful relationships are missing.
    - **NO**: If no additional relationships or entities can be reasonably identified.

    **Text Chunk**:
    "{text}"

    **Extracted Entities**:
    {entity_name}

    **Extracted Relationships**:
    {relationships}

    **Response**: [YES/NO]
"""

re_prompt000 = """

    1. You have identified all entities in the text.They are listed below:
    [{entity_name}]
    2. *From the entities identified in step 1*, identify all pairs of (source_entity, target_entity) that are *related* to each other.
    For each pair of related entities, extract the following information:
    - source_entity: name of the source entity, as identified in step 1
    - target_entity: name of the target entity, as identified in step 1
    - relationship_label: a label describing the relationship between the source entity and target entity
    - relationship_description: explanation as to why you think the source entity and the target entity are related to each other
    - relationship_strength: an integer score between 1 to 10, indicating strength of the relationship between the source entity and target entity
    Each relationship should be strictly formatted as a JSON object like output_example, as follows:
    {{
        "source": "<source_entity>",
        "target": "<target_entity>",
        "relationship_label": "<relationship_label>",
        "relationship_description": "<relationship_description>",
        "relationship_strength": <strength>
    }}
    Text: {text}
    output_example:
        [
        {{
            "source": "Patient",
            "target": "Chit-wan Medical College Teaching Hospital",
            "relationship_label": "Treated At",
            "relationship_description": "The patient visited the emergency service of Chit-wan Medical College Teaching Hospital (CMCTH) for treatment.",
            "relationship_strength": 9
        }},
        {{
            "source": "Prick Injury",
            "target": "Pus Sample",
            "relationship_label": "Source Of",
            "relationship_description": "The pus sample is collected from the site of the prick injury.",
            "relationship_strength": 9
        }},
        {{    
            "source": "Severe Sepsis",
            "target": "Septic Shock",
            "relationship_label": "Progresses To",
            "relationship_description": "Severe sepsis can progress to septic shock, as seen in the patient's condition.",
            "relationship_strength": 9
        }}
        ]
    """