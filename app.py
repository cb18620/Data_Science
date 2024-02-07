from flask import Flask, render_template, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Función para extraer datos válidos de un DataFrame basado en los índices de las columnas especificadas
# Diccionarios y listas de palabras clave
column_indices_1 = {
    "Tipo Doc.": 0, "Tipo Reg.": 2, "Ent.": 5, "DA": 7, "Nº Prev.": 9,
    "Nº": 12, "Nº Dev.": 13, "Nº Pag.": 14, "Sec.": 15, "C. G.": 16,
    "SISIN": 17, "SIGADE": 18, "Sist.": 19, "Tipo Doc. Rdo.": 20, "Nº Doc.": 23,
    "Nº de Pago": 22, "Fecha de Aprobación": 23, "Fecha de Firma": 25,
    "Total Autorizado": 26, "Deducciones": 27, "Multas": 28,
    "Liquido Pagable": 29, "Estado": 30
}

keywords_2 = ["Fte.", "Org.", "Banco", "Cuenta", "Libreta"]

keywords_3 = [
    "UE", "Prog.", "Proy.", "Act.", "Obj.", "Ent. Trans.",
    "Importe Preventivo", "Importe Compromiso", "Importe Devengado", "Importe Pago"
]
def extract_valid_data(df, column_indices):
    extracted_data = []
    for row_idx in range(1, len(df)):
        tipo_doc_cell = df.iloc[row_idx, column_indices["Tipo Doc."]]
        ent_cell = df.iloc[row_idx, column_indices["Ent."]]
        if (pd.notna(tipo_doc_cell) and tipo_doc_cell != "Tipo Doc." and pd.notna(ent_cell) and isinstance(ent_cell, (int, float))):
            row_data = {field: df.iloc[row_idx, col_idx] for field, col_idx in column_indices.items()}
            extracted_data.append(row_data)
    return pd.DataFrame(extracted_data)

# Funciones del segundo script (2.py)
# Función para extraer datos basados en una lista de palabras clave
def extract_data(df, keywords):
    extracted_values = []
    for i in range(len(df)):
        if all(df.iloc[i].str.contains(keyword, na=False).any() for keyword in keywords):
            next_row_data = df.iloc[i + 1] if i + 1 < len(df) else None
            if next_row_data is not None:
                values = [next_row_data[df.iloc[i][df.iloc[i] == keyword].index[0]] for keyword in keywords]
                extracted_values.append(values)
    return pd.DataFrame(extracted_values, columns=keywords)

# Funciones del tercer script (3.py)
# Función para extraer datos dinámicos basada en palabras clave
def extract_dynamic_data(df, keywords):
    extracted_values = []
    i = 0
    while i < len(df) - 1:
        if all(df.iloc[i].str.contains(keyword, na=False).any() for keyword in keywords):
            next_row_data = df.iloc[i + 1]
            extracted_row = {keyword: next_row_data[df.iloc[i][df.iloc[i] == keyword].index[0]] for keyword in keywords}
            extracted_values.append(extracted_row)
            i += 2
        else:
            i += 1
    return pd.DataFrame(extracted_values)

# Función del cuarto script
# Función para extraer un resumen de datos
def extract_resumen(df):
    resumen_df = df.iloc[1:, 4].to_frame()  # Selecciona la columna E, excluyendo la primera fila
    resumen_df.columns = ['Resumen:']
    resumen_df.dropna(subset=['Resumen:'], inplace=True)
    return resumen_df

# Función del quinto script adaptada
# Función para extraer totales de ciertas columnas
def extract_totals(df):
    total_row_indices = df[df.iloc[:, 13].astype(str).str.contains("Total:", na=False)].index
    totals_data = df.loc[total_row_indices, [15, 18, 21, 24]]
    totals_data.columns = ['TotImportePreventivo', 'TotImporteCompromiso', 'TotImporteDevengado', 'TotImportePago']
    return totals_data.reset_index(drop=True)

# Encuentra el archivo más reciente en un directorio
def find_latest_file(directory):
    files_paths = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    latest_file = max(files_paths, key=os.path.getctime)
    return latest_file

# Procesa el archivo transformado encontrando el más reciente en 'downloads'
def process_transformed_file(directory):
    file_path = find_latest_file(directory)
    df = pd.read_excel(file_path, header=None)

    # Aplicando las funciones definidas anteriormente para procesar los datos
    df1 = extract_valid_data(df, column_indices_1).reset_index(drop=True)
    df2 = extract_data(df, keywords_2).reset_index(drop=True)
    df3 = extract_dynamic_data(df, keywords_3).reset_index(drop=True)
    df5 = extract_totals(df).reset_index(drop=True)
    df4 = extract_resumen(df).reset_index(drop=True)  

    combined_df = pd.concat([df1, df2, df3, df5, df4], axis=1)

    timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file_name = f'processed_{timestamp_str}.xlsx'
    output_file_path = os.path.join(directory, output_file_name)
    combined_df.to_excel(output_file_path, index=False)
    return output_file_path

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    download_link = None
    processed_file_link = None
    downloads_dir = 'downloads'

    if request.method == 'POST':
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)

        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join('uploads', uploaded_file.filename)
            try:
                uploaded_file.save(file_path)
                df = pd.read_excel(file_path)  # Asume alguna transformación inicial aquí
                transformed_file_path = os.path.join(downloads_dir, 'transformado.xlsx')
                df.to_excel(transformed_file_path, index=False)  # Guarda el archivo transformado

                download_link = transformed_file_path  # Enlace para descargar el archivo transformado
                processed_file_link = process_transformed_file(downloads_dir)  # Procesa el archivo y obtiene el enlace al archivo procesado
            except Exception as e:
                error = str(e)

    return render_template('index.html', download_link=download_link, processed_file_link=processed_file_link, error=error)

if __name__ == '__main__':
    app.run(debug=True)