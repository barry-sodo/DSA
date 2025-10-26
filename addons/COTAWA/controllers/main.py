from odoo import http # type: ignore
from odoo.http import request # type: ignore

class RapportController(http.Controller):

    @http.route('/rapport/<int:rapport_id>/pdf', type='http', auth='user')
    def download_pdf(self, rapport_id):
        rapport = request.env['rapport.rapport'].browse(rapport_id)
        if not rapport.exists():
            return request.not_found()
        
        html_content = f"""
        <html>
            <head>
                <meta charset="utf-8"/>
                <style>
                    body {{ font-family: 'DejaVu Sans', sans-serif; margin: 40px; }}
                    h1, h2, h3 {{ color: #2c3e50; }}
                    .header {{ text-align:center; font-size:18px; font-weight:bold; margin-bottom:20px; }}
                    .content {{ font-size:13px; line-height:1.6; }}
                </style>
            </head>
            <body>
                <div class="header">Rapport : {rapport.name}</div>
                <div><strong>Session :</strong> {rapport.session_id.name if rapport.session_id else ''}</div>
                <div><strong>Auteur :</strong> {rapport.auteur_id.name if rapport.auteur_id else ''}</div>
                <div><strong>Date :</strong> {rapport.date_creation.strftime('%d/%m/%Y %H:%M')}</div>
                <hr/>
                <div class="content">{rapport.contenu or ''}</div>
            </body>
        </html>
        """
        pdf_content = request.env['ir.actions.report']._run_wkhtmltopdf([html_content])

        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', f'attachment; filename=rapport_{rapport.id}.pdf')
        ]
        return request.make_response(pdf_content, headers)
