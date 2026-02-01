import io
import os
import zipfile
import pandas as pd
import plotly.io as pio
from fpdf import FPDF
from datetime import datetime
from typing import List, Dict, Any
from src.config.constants import DATA_DIR, PDF_REPORT_SUFFIX, ZIP_PACKAGE_SUFFIX

class ReportExporter:
    """Service to generate professional PDF, Excel and ZIP reports."""
    
    def __init__(self, domain: str):
        self.domain = domain
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
    def to_excel(self, df: pd.DataFrame) -> bytes:
        """Generates an Excel (XLSX) buffer with styles and professional formatting."""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Opiniones Analizadas', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Opiniones Analizadas']
            
            # Formatos
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Aplicar formato a cabeceras
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Ajuste de columnas
            for i, col in enumerate(df.columns):
                column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, min(column_len, 60))
                
        return output.getvalue()

    def generate_pdf_report(self, df: pd.DataFrame, figures: Dict[str, Any]) -> bytes:
        """Creates a professional PDF report with executive KPIs and dashboard charts."""
        pdf = FPDF()
        pdf.add_page()
        
        # --- Header ---
        pdf.set_font("helvetica", "B", 24)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 20, "Informe de Inteligencia de Opinión", ln=True, align="C")
        
        pdf.set_font("helvetica", "I", 12)
        pdf.set_text_color(100)
        pdf.cell(0, 10, f"Análisis de Marca: {self.domain} | Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
        pdf.ln(10)
        
        # --- Resumen Ejecutivo ---
        pdf.set_font("helvetica", "B", 16)
        pdf.set_text_color(0)
        pdf.cell(0, 10, "Resumen Ejecutivo", ln=True)
        pdf.set_font("helvetica", "", 12)
        
        avg_score = df['sentimiento_score'].mean()
        pdf.cell(0, 8, f"- Sentimiento Promedio: {avg_score:.2f}", ln=True)
        pdf.cell(0, 8, f"- Total de Reseñas Analizadas: {len(df)}", ln=True)
        pdf.cell(0, 8, f"- Porcentaje de Opiniones Positivas: {(len(df[df['sentimiento'] == 'positivo']) / len(df)):.1%}", ln=True)
        pdf.ln(10)
        
        # --- Visual Analytics (Plots) ---
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "Análisis Visual de Reputación", ln=True)
        pdf.ln(5)
        
        # Directorio temporal para gráficas
        os.makedirs(os.path.join(DATA_DIR, "pdf_plots"), exist_ok=True)
        
        for name, fig in figures.items():
            img_path = os.path.join(DATA_DIR, "pdf_plots", f"{name}.png")
            # Kaleido engine for static images
            try:
                pio.write_image(fig, img_path, scale=2, width=800, height=500)
                
                # Gestión de salto de página inteligente
                if pdf.get_y() > 180:
                    pdf.add_page()
                
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(0, 10, f"Gráfica: {name.replace('_', ' ').title()}", ln=True)
                pdf.image(img_path, w=180)
                pdf.ln(10)
            except Exception as e:
                pdf.set_font("helvetica", "I", 10)
                pdf.cell(0, 10, f"(Error al renderizar {name}: {str(e)})", ln=True)

        return bytes(pdf.output())

    def create_zip_bundle(self, domain: str, excel_bytes: bytes, pdf_bytes: bytes, figures: Dict[str, Any]) -> bytes:
        """Packages all analytical assets into a professional ZIP bundle."""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            # Añadir archivos principales
            zf.writestr(f"{domain}_data_analisis.xlsx", excel_bytes)
            zf.writestr(f"{domain}_informe_profesional.pdf", pdf_bytes)
            
            # Añadir imágenes de gráficas individuales
            for name, fig in figures.items():
                img_bytes = pio.to_image(fig, format="png", scale=2)
                zf.writestr(f"graficas/{name}.png", img_bytes)
                
        return zip_buffer.getvalue()
