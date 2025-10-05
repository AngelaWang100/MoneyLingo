# Generate financial data 
import json
import os
from generators import MoneyLingoDataGenerator

def create_data_files():
    """Generate and save financial data to JSON files"""
    
    # Create output directory at the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, "generated_data")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate all data
    generator = MoneyLingoDataGenerator()
    all_data = generator.generate_all_data()
    
    # Save each data type to separate JSON files
    for data_type, data_list in all_data.items():
        filename = f"{output_dir}/{data_type}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(data_list)} {data_type}")
    
    print("Data generation complete!")


if __name__ == "__main__":
    create_data_files()
