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
        
    def to_excel(self, df: pd.DataFrame, df_comp: pd.DataFrame = None) -> bytes:
        """Generates an Excel (XLSX) buffer. In comparison mode, combines both brands."""
        def _prepare_df(d):
            d_export = d.copy()
            for col in d_export.select_dtypes(include=['datetimetz', 'datetime64[ns, UTC]']).columns:
                d_export[col] = d_export[col].dt.tz_localize(None)
            return d_export

        df_main = _prepare_df(df)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Sheet 1: Main Domain
            sheet_name = df_main['domain'].iloc[0][:30] if not df_main.empty else "Principal"
            df_main.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Sheet 2: Comparison (if exists)
            if df_comp is not None and not df_comp.empty:
                df_c = _prepare_df(df_comp)
                comp_sheet = df_c['domain'].iloc[0][:30]
                df_c.to_excel(writer, sheet_name=comp_sheet, index=False)
                
                # Sheet 3: Unified Comparison View
                combined = pd.concat([df_main, df_c], ignore_index=True)
                combined.to_excel(writer, sheet_name='Benchmark Comparativo', index=False)

            workbook = writer.book
            header_format = workbook.add_format({
                'bold': True, 'text_wrap': True, 'valign': 'top',
                'fg_color': '#D7E4BC', 'border': 1
            })
            
            # Apply format to all sheets
            for sheet in writer.sheets.values():
                for col_num, value in enumerate(df_main.columns.values):
                    sheet.write(0, col_num, value, header_format)
                sheet.set_column(0, len(df_main.columns), 20)

        excel_data = output.getvalue()
        output.close()
        return excel_data

    def _generate_report_charts(self, df: pd.DataFrame, df_comp: pd.DataFrame = None) -> Dict[str, Any]:
        """Internal helper to centralize chart generation logic, including comparative ones."""
        charts = {}
        nom1 = df['domain'].iloc[0] if not df.empty else "Principal"
        
        # --- PHASE 1: Main Brand Analysis ---
        charts[f"[{nom1}] - Distribución por Categorías"] = viz_engine.generate_category_chart(df)
        charts[f"[{nom1}] - Distribución de Sentimiento"] = viz_engine.generate_sentiment_pie(df)
        charts[f"[{nom1}] - Nube de Inteligencia Semántica"] = viz_engine.generate_wordcloud_static(df)
        charts[f"[{nom1}] - Drivers de Opinión"] = viz_engine.generate_drivers_chart(df)
        
        # --- PHASE 2: Competitive Insight & Individual Competitor ---
        if df_comp is not None and not df_comp.empty:
            nom2 = df_comp['domain'].iloc[0]
            
            # Comparative Asset (Top Priority)
            charts[f"BENCHMARK - Evolución Temporal"] = viz_engine.generate_time_series_comparison(df, df_comp, nom1, nom2)
            charts["BENCHMARK - Distribución de Sentimiento"] = viz_engine.generate_sentiment_comparison_bar(df, df_comp, nom1, nom2)
            charts["BENCHMARK - Distribución por Temas"] = viz_engine.generate_category_comparison_bar(df, df_comp, nom1, nom2)
            
            # Competitor Details
            charts[f"[{nom2}] - Distribución por Categorías"] = viz_engine.generate_category_chart(df_comp)
            charts[f"[{nom2}] - Distribución de Sentimiento"] = viz_engine.generate_sentiment_pie(df_comp)
            charts[f"[{nom2}] - Nube de Inteligencia Semántica"] = viz_engine.generate_wordcloud_static(df_comp)
            
            # Technical Insight
            charts["BENCHMARK - Matriz de Correlación Unificada"] = viz_engine.generate_correlation_heatmap(pd.concat([df, df_comp]))
            
        else:
            # Single Mode extra charts
            charts["Evolución Temporal"] = viz_engine.generate_evolution_chart(df)
            charts["Top 20 Palabras Clave"] = viz_engine.generate_word_freq_chart(df)
            charts["Matriz de Correlación"] = viz_engine.generate_correlation_heatmap(df)
            charts["Métricas por Sentimiento"] = viz_engine.generate_boxplot_insight(df)
            
        return charts

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
            pdf.cell(0, 8, f"[PRINCIPAL] {dom1}:", ln=True)
            pdf.set_text_color(0)
            avg1 = df['sentimiento_score'].mean()
            pdf.cell(0, 8, f"   - Sentimiento Promedio: {avg1:.2f}", ln=True)
            pdf.cell(0, 8, f"   - % Positivo: {(len(df[df['sentimiento'] == 'positivo']) / len(df)):.1%}", ln=True)
            
            pdf.ln(2)
            
            # Domain 2
            pdf.set_text_color(200, 100, 0) # Orange-ish
            pdf.cell(0, 8, f"[COMPARATIVA] {dom2}:", ln=True)
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
        
        # Generate complete set of charts (Logic is now inside _generate_report_charts)
        report_charts = self._generate_report_charts(df, df_comp)

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

    def create_zip_bundle(self, domain: str, excel_bytes: bytes, pdf_bytes: bytes, df: pd.DataFrame, df_comp: pd.DataFrame = None) -> bytes:
        """Packages all analytical assets into a professional ZIP bundle."""
        zip_buffer = io.BytesIO()
        safe_name = domain.replace(" ", "_").lower()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            # Main files
            zf.writestr(f"{safe_name}_data_analisis.xlsx", excel_bytes)
            zf.writestr(f"{safe_name}_informe_profesional.pdf", pdf_bytes)
            
            # Individual and comparative charts
            report_charts = self._generate_report_charts(df, df_comp)
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
