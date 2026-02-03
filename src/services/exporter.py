import io
import os
import zipfile
import pandas as pd
import plotly.io as pio
from fpdf import FPDF
from datetime import datetime
from typing import List, Dict, Any
import matplotlib.pyplot as plt
from src.config.constants import DATA_DIR, PDF_REPORT_SUFFIX, ZIP_PACKAGE_SUFFIX
from src.services import viz_engine

class ReportExporter:
    """Service to generate professional PDF, Excel and ZIP reports."""
    
    def __init__(self, domain: str):
        self.domain = domain
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
    def to_excel(self, df: pd.DataFrame) -> bytes:
        """Generates an Excel (XLSX) buffer with styles and professional formatting."""
        # Solución de compatibilidad: Excel no soporta zonas horarias (Timezones)
        df_export = df.copy()
        
        # Convertir columnas datetime con zona horaria a 'naive' (sin zona horaria)
        # Esto soluciona el ValueError: Excel does not support datetimes with timezones
        for col in df_export.select_dtypes(include=['datetimetz', 'datetime64[ns, UTC]']).columns:
            df_export[col] = df_export[col].dt.tz_localize(None)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, sheet_name='Opiniones Analizadas', index=False)
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
            for col_num, value in enumerate(df_export.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Ajuste de columnas
            for i, col in enumerate(df_export.columns):
                # Calcular el ancho máximo basado en el contenido
                max_val = df_export[col].astype(str).map(len).max()
                column_len = max(max_val, len(col)) + 2
                worksheet.set_column(i, i, min(column_len, 60))
        
        # Capturar el contenido del buffer y cerrarlo
        excel_data = output.getvalue()
        output.close()
        return excel_data

    def _generate_report_charts(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Internal helper to centralize chart generation logic."""
        return {
            "Distribución por Categorías": viz_engine.generate_category_chart(df),
            "Distribución de Sentimiento": viz_engine.generate_sentiment_pie(df),
            "Histograma de Intensidad": viz_engine.generate_sentiment_hist(df),
            "Evolución Temporal": viz_engine.generate_evolution_chart(df),
            "Top 20 Palabras Clave": viz_engine.generate_word_freq_chart(df),
            "Nube de Palabras": viz_engine.generate_wordcloud_static(df),
            "Métricas por Sentimiento": viz_engine.generate_boxplot_insight(df),
            "Drivers de Opinión": viz_engine.generate_drivers_chart(df),
            "Matriz de Correlación": viz_engine.generate_correlation_heatmap(df)
        }

    def generate_pdf_report(self, df: pd.DataFrame, df_comp: pd.DataFrame = None) -> bytes:
        """Creates a professional PDF report with executive KPIs and dashboard charts."""
        pdf = FPDF()
        pdf.add_page()
        
        # --- Header ---
        pdf.set_font("helvetica", "B", 24)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 20, "Informe de Inteligencia de Opinión", ln=True, align="C")
        
        pdf.set_font("helvetica", "I", 12)
        pdf.set_text_color(100)
        report_title = f"Análisis de Marca: {self.domain} | Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        pdf.cell(0, 10, report_title, ln=True, align="C")
        pdf.ln(10)
        
        # --- Resumen Ejecutivo ---
        pdf.set_font("helvetica", "B", 16)
        pdf.set_text_color(0)
        
        if df_comp is not None and not df_comp.empty:
            dom1 = df['domain'].iloc[0]
            dom2 = df_comp['domain'].iloc[0]
            pdf.cell(0, 10, f"Resumen Ejecutivo Comparativo: {dom1} vs {dom2}", ln=True)
            pdf.set_font("helvetica", "", 12)
            
            # Domain 1
            pdf.set_text_color(0, 100, 200) # Blue-ish
            pdf.cell(0, 8, f"🟦 {dom1}:", ln=True)
            pdf.set_text_color(0)
            avg1 = df['sentimiento_score'].mean()
            pdf.cell(0, 8, f"   - Sentimiento Promedio: {avg1:.2f}", ln=True)
            pdf.cell(0, 8, f"   - % Positivo: {(len(df[df['sentimiento'] == 'positivo']) / len(df)):.1%}", ln=True)
            
            pdf.ln(2)
            
            # Domain 2
            pdf.set_text_color(200, 100, 0) # Orange-ish
            pdf.cell(0, 8, f"🟧 {dom2}:", ln=True)
            pdf.set_text_color(0)
            avg2 = df_comp['sentimiento_score'].mean()
            pdf.cell(0, 8, f"   - Sentimiento Promedio: {avg2:.2f}", ln=True)
            pdf.cell(0, 8, f"   - % Positivo: {(len(df_comp[df_comp['sentimiento'] == 'positivo']) / len(df_comp)):.1%}", ln=True)
            
        else:
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
        
        # Generate standard charts (for primary domain)
        report_charts = self._generate_report_charts(df)
        
        # If comparison, render comparison charts that are compatible with static export
        if df_comp is not None and not df_comp.empty:
            try:
                # Add comparison time series if available
                nom1 = df['domain'].iloc[0]
                nom2 = df_comp['domain'].iloc[0]
                fig_comp = viz_engine.generate_time_series_comparison(df, df_comp, nom1, nom2)
                if fig_comp:
                    report_charts["Evolución Comparativa"] = fig_comp
            except:
                pass

        for name, fig in report_charts.items():
            if fig is None: continue
            
            try:
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
                plt.close(fig) 
                
                img_buffer.seek(0)
                
                # Check for page break
                if pdf.get_y() > 200:
                    pdf.add_page()
                
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(0, 10, f"Gráfica: {name}", ln=True)
                
                pdf.image(img_buffer, w=170)
                pdf.ln(10)
                img_buffer.close()
            except Exception as e:
                pdf.set_font("helvetica", "I", 10)
                pdf.cell(0, 10, f"(Error al renderizar {name}: {str(e)})", ln=True)

        return bytes(pdf.output())

        return bytes(pdf.output())

    def create_zip_bundle(self, domain: str, excel_bytes: bytes, pdf_bytes: bytes, df: pd.DataFrame) -> bytes:
        """Packages all analytical assets into a professional ZIP bundle."""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            # Añadir archivos principales
            zf.writestr(f"{domain}_data_analisis.xlsx", excel_bytes)
            zf.writestr(f"{domain}_informe_profesional.pdf", pdf_bytes)
            
            # Añadir imágenes de gráficas individuales (Matplotlib para estabilidad en nube)
            report_charts = self._generate_report_charts(df)
            for name, fig in report_charts.items():
                if fig is None: continue
                try:
                    img_buffer = io.BytesIO()
                    fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
                    plt.close(fig)
                    zf.writestr(f"graficas/{name.replace(' ', '_').lower()}.png", img_buffer.getvalue())
                    img_buffer.close()
                except Exception:
                    pass
                
        zip_data = zip_buffer.getvalue()
        zip_buffer.close()
        return zip_data
