"""
PDF Report Generator
Creates detailed pest infestation report
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


class PestReportGenerator:
    def __init__(self):
        self.output_dir = os.path.join(Config.BASE_DIR, 'data', 'reports')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_report(self, weather_data=None, detection_result=None, forecast_data=None):
        """
        Generate comprehensive PDF report
        """
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pest_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        title = Paragraph("🌾 Pest Infestation Report", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        date_text = f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        location_text = f"<b>Farm Location:</b> {Config.FARM_LAT}°N, {Config.FARM_LON}°E (Patna, Bihar)"
        
        story.append(Paragraph(date_text, styles['Normal']))
        story.append(Paragraph(location_text, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Weather Section
        if weather_data:
            story.append(Paragraph("🌦️ Weather Forecast (3 Days)", heading_style))
            
            weather_table_data = [
                ['Day', 'Temperature', 'Wind Speed', 'Risk Factor']
            ]
            
            for day in weather_data.get('forecast', []):
                temp = f"{day['avg_temperature']}°C"
                wind = f"{day['avg_wind_speed']} km/h"
                risk = "Low" if day['avg_temperature'] < 27 else "Medium"
                weather_table_data.append([f"Day {day['day']}", temp, wind, risk])
            
            weather_table = Table(weather_table_data, colWidths=[1.5*inch, 2*inch, 2*inch, 1.5*inch])
            weather_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(weather_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Detection Results
        if detection_result:
            story.append(Paragraph("🐛 Pest Detection Results", heading_style))
            
            classification = detection_result.get('classification', 'Unknown')
            probability = detection_result.get('pest_probability', 0) * 100
            
            # Risk level
            if probability < 30:
                risk_level = "Low Risk"
                risk_color = colors.green
            elif probability < 70:
                risk_level = "Medium Risk"
                risk_color = colors.orange
            else:
                risk_level = "High Risk"
                risk_color = colors.red
            
            detection_data = [
                ['Status', classification],
                ['Pest Probability', f'{probability:.1f}%'],
                ['Risk Level', risk_level],
                ['Confidence', 'High' if probability > 60 or probability < 40 else 'Medium']
            ]
            
            detection_table = Table(detection_data, colWidths=[3*inch, 4*inch])
            detection_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            story.append(detection_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Forecast Section
        if forecast_data:
            story.append(Paragraph("📊 3-Day Pest Spread Forecast", heading_style))
            
            forecast_table_data = [
                ['Day', 'Risk Level', 'Spread Probability', 'Recommended Action']
            ]
            
            for day_forecast in forecast_data:
                day_num = f"Day {day_forecast['day']}"
                risk = day_forecast['risk_level'].upper()
                spread_prob = f"{day_forecast['spread_probability']*100:.0f}%"
                action = day_forecast['recommended_action']
                
                forecast_table_data.append([day_num, risk, spread_prob, action])
            
            forecast_table = Table(forecast_table_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 3*inch])
            forecast_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            
            story.append(forecast_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        story.append(Paragraph("💡 Recommendations", heading_style))
        
        recommendations = [
            "• Monitor crop health daily for early pest detection",
            "• Apply preventive treatments during high-risk periods",
            "• Maintain proper field hygiene and crop rotation",
            "• Use biological control methods when possible",
            "• Keep weather conditions in mind for pest management timing"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = "Generated by Hyper-local Pest Infestation Forecaster | Developed for Precision Agriculture"
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph(footer_text, footer_style))
        
        # Build PDF
        doc.build(story)
        
        print(f"✅ PDF Report generated: {filepath}")
        return filepath


# Test function
if __name__ == "__main__":
    print("📄 Testing PDF Report Generator...")
    
    generator = PestReportGenerator()
    
    # Mock data
    weather = {
        'forecast': [
            {'day': 1, 'avg_temperature': 28.05, 'avg_wind_speed': 2.9},
            {'day': 2, 'avg_temperature': 27.47, 'avg_wind_speed': 2.56},
            {'day': 3, 'avg_temperature': 27.35, 'avg_wind_speed': 1.59}
        ]
    }
    
    detection = {
        'classification': 'Healthy',
        'pest_probability': 0.35
    }
    
    forecast = [
        {'day': 1, 'risk_level': 'medium', 'spread_probability': 0.45, 'recommended_action': 'Monitor closely'},
        {'day': 2, 'risk_level': 'high', 'spread_probability': 0.60, 'recommended_action': 'Consider preventive treatment'},
        {'day': 3, 'risk_level': 'high', 'spread_probability': 0.75, 'recommended_action': 'Apply treatment if needed'}
    ]
    
    filepath = generator.generate_report(weather, detection, forecast)
    print(f"📂 Report saved at: {filepath}")