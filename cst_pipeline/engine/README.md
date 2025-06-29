## `engine/README.md`

This folder contains the **core logic** for the Next-Best-Action (NBA) system.

---

## Files Explained

### `nba_pipeline.py`
- **Purpose:**  
  Runs the complete NBA pipeline:
  - Loads clustered conversations and MBTI tags.
  - Decides next best action for each customer.
  - Generates and saves recommendations.
- **Outputs:**  
  - `nba_output.json` (raw NBA actions)
  - `nba_audit_log.csv` (traceable audit log)

---

### `nba_rules.py`
- **Purpose:**  
  Defines the **decision logic** for which NBA action to recommend.
- **Key Parts:**  
  - Rules based on urgency, sentiment, clusters, MBTI type, etc.
  - Calls utility helpers and personalized message generation.

---

### `utils.py`
- **Purpose:**  
  Contains helper functions for:
  - Parsing datetimes
  - Computing best send times
  - Other reusable utility logic

---

### `generate_mbti_message.py`
- **Purpose:**  
  Generates a **personalized message** template using the customer’s MBTI type.
- **Usage:**  
  Called inside `nba_rules.py` and `evaluate_personalized_nba.py`.

---

## Data Flow

- Loads `conversation_analysis.csv` + `cst_mbti_tags.csv`  
- Processes rows with NBA logic (`nba_rules.py`)  
- Generates output: `nba_output.json` + `nba_audit_log.csv`

---

## Usage

Called by:
```bash
python -m cst_pipeline.run_nba
