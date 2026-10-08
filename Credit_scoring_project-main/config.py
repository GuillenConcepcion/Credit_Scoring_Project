import sys
from pathlib import Path

this_file = Path(__file__).resolve()
project_root = this_file.parent

data_path = project_root / "datasets"   
src_path = project_root / "src" 
data_output_path = project_root / "data_analysis_output"
folds_path = project_root / "folds"

# Ensure output directories exist
data_path.mkdir(parents=True, exist_ok=True)
data_output_path.mkdir(parents=True, exist_ok=True)
(data_output_path / "eda_output").mkdir(parents=True, exist_ok=True)
(data_output_path / "data_cleaning_output").mkdir(parents=True, exist_ok=True)
(data_output_path / "correlation").mkdir(parents=True, exist_ok=True)
folds_path.mkdir(parents=True, exist_ok=True)

# Register paths in sys.path
for p in [str(project_root), str(src_path)]:
    if p not in sys.path:
        sys.path.insert(0, p)



