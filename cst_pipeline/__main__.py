# main.py
import subprocess

def run_step(step_name, command):
    print(f"\n=== Running: {step_name} ===")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Step failed: {step_name}")
        exit(result.returncode)
    print(f"Done: {step_name}")

if __name__ == "__main__":
    steps = [
        ("Ingest Raw Data", "python -u cst_pipeline/ingest.py"),
        ("Analyze Conversations", "python -m cst_pipeline.conversation_analysis.analyze"),
        ("Cluster Conversations", "python -m cst_pipeline.conversation_analysis.clustering_features"),
        ("Interpret Clusters", "python -m cst_pipeline.conversation_analysis.conversation_clusters"),
        ("Train MBTI Classifier", "echo 3 | python -m cst_pipeline.mbti_modelling.train_mbti_classifier"),
        ("Tag CST Users with MBTI", "python -m cst_pipeline.mbti_modelling.tag_cst_users"),
        ("Run NBA Pipeline", "python -u cst_pipeline/run_nba.py"),
        ("Evaluate NBA", "python -m cst_pipeline.evaluate_nba"),
        ("Evaluate Personalized NBA", "python -m cst_pipeline.evaluate_personalized_nba"),
    ]

    for name, cmd in steps:
        run_step(name, cmd)

    print("\nAll steps completed successfully!")
