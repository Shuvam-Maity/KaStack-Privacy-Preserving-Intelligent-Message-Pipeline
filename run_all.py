import run_stage1_masking
import run_stage2_classify
import run_stage3_extraction

if __name__ == "__main__":
    print("=== Starting End-to-End Pipeline Execution ===\n")
    run_stage1_masking.main()
    run_stage2_classify.main()
    run_stage3_extraction.main()
    print("=== Pipeline Execution Complete! All output files generated in /output ===")