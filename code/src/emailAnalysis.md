```mermaid
graph TD
    A[Email Ingestion] --> B[Preprocessing]
    B --> C{Attachments?}
    C -- Yes --> D[Attachment Handling]
    C -- No --> E[LLM Processing]
    D --> E[LLM Processing]
    E --> F{Multiple Requests?}
    F -- Yes --> G[Multi-Request Handling]
    F -- No --> H[Classification]
    G --> H[Classification]
    H --> I[Key Field Extraction]
    I --> J[Duplicate Detection]
    J --> K[Confidence Scoring]
    K --> L[Skill-Based Routing]
    L --> M[Output Results]

    M --> N[Request types with confidence scores]
    M --> O[Extracted fields]
    M --> P[Duplicate detection flags]