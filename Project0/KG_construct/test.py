ner_prompt = """
    **Task**: Extract all entities from the provided text and format them as a JSON array.  

    **Instructions**:  
    1. **Identify New Entities**:  
    - Extract all entities mentioned in the text that are **not already in the provided list**.  
    - For each new entity, provide:  
        - `name`: The name of the entity (capitalized).  
        - `label`: One of the following labels: [{entity_labels}]. **Do not create new labels unless necessary**.  
        - `description`: A detailed description of the entity's attributes, activities, or context. If no description is available, use an empty string ("").  

    2. **Output Format**:  
    - Format each entity as a JSON object.  
    - Return all new entities as a JSON array.  
    - **Strictly follow the example format below**:  

    **Example Output**:  
    [
        {{
            "name": "Oxidase Test",
            "label": "Laboratory Test",
            "description": "The result was positive for the isolated bacteria."
        }},
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
    - **Do not extract entities already in the provided list**: [{entity_name}].  
    - **Do not invent entities** that are not explicitly mentioned in the text.  
    - **Do not add new labels unless necessary** outside the provided list: [{entity_labels}].  
    - If no description is available, set `description` to an empty string ("").  

    **Text to Analyze**:  
    {text}

    **Output**:
"""
formatted_entity_name=""
labels = ""
text=""
ner_prompt.format(entity_name=formatted_entity_name, entity_labels=str(labels), text=text)