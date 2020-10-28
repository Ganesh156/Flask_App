from flask import Flask, request, url_for, render_template, send_file
import pandas as pd
app = Flask(__name__)


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


@app.route('/success', methods=['POST'])
# This method for accessing file which is uploaded by user and also performs mulptiple operation on a file.
def success():
    if request.method == 'POST':
        f = request.files['file']
        data = pd.read_excel(f)

        # renaming the columens in the file.
        data.rename(
            columns={'Accepted Compound ID': 'Accepted_Compound_ID', 'Retention time (min)': 'Retention_time_(min)'}, inplace=True)

        # Fetching Accepted_Compound_ID which has PC
        data1 = data.loc[data.Accepted_Compound_ID.str.contains(
            'PC', na=False)]
        # Fetching Accepted_Compound_ID which has plasmalogen
        data2 = data.loc[data.Accepted_Compound_ID.str.contains(
            'plasmalogen', na=False)]
        # Fetching Accepted_Compound_ID which has LPC
        data3 = data.loc[data.Accepted_Compound_ID.str.contains(
            'LPC', na=False)]

        # converting to excel file
        data1.to_excel('data1.xlsx', index=False)
        data2.to_excel('data2.xlsx', index=False)
        data3.to_excel('data3.xlsx', index=False)
        # Roundoffing the Retention_time_(min)
        data4 = data["Retention_time_(min)"].round(decimals=0)
        # Adding Retention_time_Roundoff(min) column for parent file
        data.insert(2, "Retention_time_Roundoff(min)", data4)
        # converting to excel file
        data.to_excel('data4.xlsx', index=False)
        # Finding the mean based on Retention_time_Roundoff(min)
        data5 = data.groupby('Retention_time_Roundoff(min)')['m/z'].mean()
        # converting to excel file
        data5.to_excel('data5.xlsx', index=False)

    return render_template("success.html")

# Functions for downloading the files


@app.route('/download1')
def download_file_PC():

    path_pc = 'data1.xlsx'
    return send_file(path_pc, as_attachment=True)


@app.route('/download2')
def download_file_plasmalogen():
    path_plasmalogen = 'data2.xlsx'
    return send_file(path_plasmalogen, as_attachment=True)


@app.route('/download3')
def download_file_LPC():
    path_lpc = 'data3.xlsx'
    return send_file(path_lpc, as_attachment=True)


@app.route('/download4')
def download_file_new():
    path_new_file = 'data4.xlsx'
    return send_file(path_new_file, as_attachment=True)


@app.route('/download5')
def download_file_mean():
    path_new_mean = 'data5.xlsx'
    return send_file(path_new_mean, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
