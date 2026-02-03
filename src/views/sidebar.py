import streamlit as st
import io
import pandas as pd
from src.config.constants import SIDEBAR_HEADER, ANALYZE_BUTTON, DEFAULT_DOMAIN, DEFAULT_COMPARE_DOMAIN, SCRAPE_MAX_REVIEWS
from src.services.exporter import ReportExporter

def render_sidebar():
    """Renders the main control sidebar component."""
    with st.sidebar:
        st.title("📊 Monitor")
        st.header(SIDEBAR_HEADER)
        st.markdown("---")
        
        # Domain Input Section
        st.subheader("🌐 Configuración de Marca")
        domain_input = st.text_input(
            "Dominio Principal",
            placeholder=f"ej: {DEFAULT_DOMAIN}",
            value=DEFAULT_DOMAIN,
            help="Introduce el nombre tal como aparece en Trustpilot."
        )

        with st.expander("⚔️ Modo Comparativa (Opcional)"):
            compare_mode = st.checkbox("Activar comparación", value=st.session_state.get('compare_mode', False))
            compare_domain = st.text_input(
                "Segundo Dominio",
                placeholder=f"ej: {DEFAULT_COMPARE_DOMAIN}",
                value=st.session_state.get('compare_domain', ""),
                disabled=not compare_mode
            )
            st.session_state.compare_mode = compare_mode
            st.session_state.compare_domain = compare_domain
        
        max_reviews = st.slider(
            "Cantidad de reseñas",
            min_value=20,
            max_value=500,
            value=SCRAPE_MAX_REVIEWS if SCRAPE_MAX_REVIEWS <= 500 else 200,
            step=20,
            help="""
            💡 **Recomendación Pro**: 
            - **300 reseñas**: Es el punto óptimo para que los modelos de PageRank y Filtrado Colaborativo detecten patrones significativos.
            - **500 reseñas**: Límite máximo para garantizar la velocidad de análisis y evitar bloqueos por seguridad/privacidad de la plataforma.
            """
        )
        
        # Status detection
        has_data = not st.session_state.df.empty if 'df' in st.session_state else False

        # Action Button (Polymorphic)
        analyze_clicked = False
        if not has_data:
            analyze_clicked = st.button(ANALYZE_BUTTON, type="primary", use_container_width=True)
        else:
            if st.button("🧹 Nuevo Análisis (Limpiar)", type="secondary", use_container_width=True):
                # Full Reset of analytical state
                keys_to_clear = [
                    'data_ready', 'df', 'df_comp', 'export_data', 'export_type', 
                    'analyzed_domain', 'compare_domain_name', 'figures',
                    'compare_mode', 'compare_domain'
                ]
                for key in keys_to_clear:
                    if key in st.session_state:
                        # Reset to defaults where appropriate
                        if key == 'df' or key == 'df_comp':
                            st.session_state[key] = pd.DataFrame()
                        elif key == 'data_ready':
                            st.session_state[key] = False
                        else:
                            del st.session_state[key]
                st.rerun()
        
        st.markdown("---")
        
        # Export Suite
        st.subheader("📥 Exportación Profesional")
        export_mode = st.selectbox(
            "Formato de Reporte",
            ["Dataset Excel (XLSX)", "Informe PDF Pro", "Pack Completo (ZIP)"]
        )
        
        if st.session_state.get('data_ready', False):
            df = st.session_state.df
            
            # Update label to include comparison if active
            analyzed_domain = st.session_state.get('analyzed_domain', domain_input)
            comp_dom = st.session_state.get('compare_domain_name', None)
            df_comp = st.session_state.get('df_comp', pd.DataFrame())
            
            if not df_comp.empty and comp_dom:
                analyzed_domain = f"{analyzed_domain} vs {comp_dom}"
                
            exporter = ReportExporter(analyzed_domain)
            
            # Use session state to hold export data and avoid re-generation on rerun
            if 'export_data' not in st.session_state:
                st.session_state.export_data = None
            if 'export_type' not in st.session_state:
                st.session_state.export_type = None

            # Reset export data if mode changes
            if st.session_state.export_type != export_mode:
                st.session_state.export_data = None
                st.session_state.export_type = export_mode

            if export_mode == "Dataset Excel (XLSX)":
                if st.button("🛠️ Preparar Excel"):
                    with st.spinner("Generando archivo Excel..."):
                        st.session_state.export_data = bytes(exporter.to_excel(df, df_comp))
                
                if st.session_state.export_data and st.session_state.export_type == "Dataset Excel (XLSX)":
                    st.download_button(
                        label="📂 Descargar Excel (XLSX)",
                        data=st.session_state.export_data,
                        file_name=f"{analyzed_domain}_analisis.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            elif export_mode == "Informe PDF Pro":
                if st.button("📄 Preparar Informe PDF"):
                    with st.spinner("Renderizando gráficas y generando informe..."):
                        # Identify if comparison data is available
                        st.session_state.export_data = bytes(exporter.generate_pdf_report(df, df_comp))
                
                if st.session_state.export_data and st.session_state.export_type == "Informe PDF Pro":
                    st.download_button(
                        label="📥 Descargar PDF",
                        data=st.session_state.export_data,
                        file_name=f"{analyzed_domain}_informe.pdf",
                        mime="application/pdf"
                    )
            
            elif export_mode == "Pack Completo (ZIP)":
                if st.button("📦 Preparar Pack ZIP"):
                    with st.spinner("Empaquetando activos analíticos..."):
                        xlsx_data = exporter.to_excel(df, df_comp)
                        pdf_data = exporter.generate_pdf_report(df, df_comp)
                        st.session_state.export_data = bytes(exporter.create_zip_bundle(analyzed_domain, xlsx_data, pdf_data, df, df_comp))
                
                if st.session_state.export_data and st.session_state.export_type == "Pack Completo (ZIP)":
                    st.download_button(
                        label="📥 Descargar ZIP",
                        data=st.session_state.export_data,
                        file_name=f"{analyzed_domain}_intelligence_pack.zip",
                        mime="application/zip"
                    )
                
            st.success(f"✅ Análisis de {analyzed_domain} listo")
        else:
            st.info("Realiza un análisis para habilitar las opciones.")

        st.markdown("---")
        from datetime import datetime
        current_year = datetime.now().year
        from src.config.constants import APP_VERSION
        st.caption(f"© {current_year} Business Intelligence v.{APP_VERSION}")
        st.caption("📢 **Nota:** Herramienta desarrollada con fines educativos universitarios.")
        
    return domain_input, max_reviews, analyze_clicked, compare_mode, compare_domain
