import os
import io
import sys
import tempfile
import zipfile
import shutil

from flask import Flask, render_template, request, send_file
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import threading
from comparator_app.comparator.compare_zip import compare_directory
from comparator_app.reports.report_methods import highlighted_report, total_report
# from comparator.compare_zip import compare_directory
# from reports.report_methods import highlighted_report, total_report

# from comparator_app.comparator.compare_zip

app = Flask(__name__)

generated_dataframes = {
    "total": None,
    "differences": [],
    "highlighted": []
}

# def schedule_cleanup(delay_minutes=10):
#     def cleanup():
#         generated_dataframes["total"] = None
#         generated_dataframes["differences"] = None
#         generated_dataframes["highlighted"] = []
#         print("🧹 Automatic cleanup complete.")
#     threading.Timer(delay_minutes * 0.5, cleanup).start()

def extract_and_locate_root(zip_file, extract_to):
    with zipfile.ZipFile(zip_file) as zip_ref:
        zip_ref.extractall(extract_to)

    entries = [entry for entry in os.listdir(extract_to) if os.path.isdir(os.path.join(extract_to, entry))]
    if len(entries) == 1:
        return os.path.join(extract_to, entries[0])
    return extract_to

@app.route('/')
def index():
    temp_dir = os.path.join(app.root_path, 'temp')
    if os.path.exists(temp_dir):
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"⚠️ Failed to delete {file_path}: {e}")
    generated_dataframes["total"] = None
    # generated_dataframes["differences"] = None
    generated_dataframes["highlighted"] = []
    
    return render_template('index.html')

@app.route('/download_total')
def download_total():
    records = generated_dataframes.get("total")
    if records is None:
        return "❌ No Total report generated yet.", 400

    output_file = os.path.join(tempfile.gettempdir(), 'Total_Report.xlsx')
    total_report(records, output_file)

    return send_file(
        output_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Total_Report.xlsx'
    )
   

@app.route('/download_highlighted/<int:index>')
def download_highlighted(index):
    try:
        report_data = generated_dataframes["highlighted"][index]
    except (IndexError, TypeError):
        return "❌ Highlighted report not found. Possible couse for rendered version - not enough CPU. To get access for whole functionality you can use branch prototype in File_comparator on github", 400

    file_name = report_data.get('file_name', f"file_{index}")
    
    # print(file_name)
    sheet_name = report_data.get('sheet_name', f"sheet_{index}")
    records = report_data.get('highlighted', [])
    
    # print("records\n\n\n",records)
    
    output_file = os.path.join(tempfile.gettempdir(), f'{file_name}_{sheet_name}_Highlighted_Report.xlsx')

    highlighted_report(file_name, sheet_name, records, output_file)

    if not os.path.exists(output_file):
        return "❌ Failed to generate highlighted report.", 500

    return send_file(
        output_file,
        as_attachment=True,
        download_name=os.path.basename(output_file),
        # download_name=f'{file_name}_{sheet_name}_Highlighted_Report.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if 'zip1' not in request.files or 'zip2' not in request.files:
        return render_template('result.html', output='❌ Both files are required.')

    file1 = request.files['zip1']
    file2 = request.files['zip2']

    with tempfile.TemporaryDirectory() as temp_dir:
        dir1_root = os.path.join(temp_dir, 'dir1')
        dir2_root = os.path.join(temp_dir, 'dir2')
        os.makedirs(dir1_root, exist_ok=True)
        os.makedirs(dir2_root, exist_ok=True)

        def is_zip(f): return f.filename.lower().endswith('.zip')

        try:
            if is_zip(file1) and is_zip(file2):
                dir1 = extract_and_locate_root(file1, dir1_root)
                dir2 = extract_and_locate_root(file2, dir2_root)
            elif not is_zip(file1) and not is_zip(file2):
                path1 = os.path.join(dir1_root, file1.filename)
                path2 = os.path.join(dir2_root, file2.filename)
                file1.save(path1)
                file2.save(path2)
                dir1 = dir1_root
                dir2 = dir2_root
            else:
                return render_template('result.html', output='❌ Either upload 2 ZIPs or 2 individual files (not one of each).')
        except zipfile.BadZipFile:
            return render_template('result.html', output='❌ Invalid ZIP file(s).')
        except Exception as e:
            return render_template('result.html', output=f'❌ Error: {str(e)}')

        decimal = int(request.form.get('decimal', 5))
        create_reports = 'create_reports' in request.form
        highlighted_output = 'highlighted_output' in request.form
        sorting = 'sorting' in request.form

        config = {
            'decimal': decimal,
            'highlighted_output': highlighted_output,
            'create_reports': create_reports,
            'errors': [],
            'sorting': sorting
        }

        buffer = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = buffer

        try:
            df_total, highlighted_dfs  = compare_directory(dir1, dir2, config)
            generated_dataframes["total"] = df_total
            generated_dataframes["highlighted"] = highlighted_dfs or []
        except Exception as e:
            sys.stdout = sys_stdout_original
            return render_template('result.html', output=f'❌ Comparison failed: {str(e)}')

        sys.stdout = sys_stdout_original
        final_output = buffer.getvalue()
        

        results = df_total.to_dict(orient='records') 
      
        return render_template("result.html", output=final_output,
                               total="/download_total", highlighted_output=highlighted_output,
                               highlighted=[f"/download_highlighted/{i}" for i in range(len(generated_dataframes["highlighted"]))],
                               results=results, create_reports=create_reports,)

if __name__ == '__main__':
    app.run()


