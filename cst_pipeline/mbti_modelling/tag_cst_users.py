import pandas as pd
from cst_pipeline.mbti_modelling.predict_mbti import predict_mbti

# Load CST data
input = "cst_pipeline/data/processed/conversation_analysis.csv"
output = "cst_pipeline/data/processed/cst_mbti_tags.csv"

# # Group tweets by customer
# grouped = cst_df.groupby("author_id")["text_clean"].apply(lambda x: " ".join(x.dropna().astype(str)))

# # Predict MBTI per author
# mbti_labels = grouped.apply(predict_mbti).reset_index()
# mbti_labels.columns = ["author_id", "predicted_mbti"]

# # Save tagged output
# mbti_labels.to_csv("cst_pipeline/data/processed/cst_mbti_tags.csv", index=False)

def tag_cst_users_with_mbti(input_path, output_path):
    cst_df = pd.read_csv(input_path)
    grouped = cst_df.groupby("author_id")["text_clean"].apply(lambda x: " ".join(x.dropna().astype(str)))
    mbti_labels = grouped.apply(predict_mbti).reset_index()
    mbti_labels.columns = ["author_id", "predicted_mbti"]
    mbti_labels.to_csv(output_path, index=False)
    print(f"Saved MBTI tags to {output_path}")

tag_cst_users_with_mbti(input, output)