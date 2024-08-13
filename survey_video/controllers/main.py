from odoo import http
from odoo.http import request, Response

from odoo.addons.survey.controllers.main import Survey


class SurveyInherit(Survey):

    @http.route('/web/content/get_background_video/<string:model_name>/<string:field_name>/<string:token>', type='http', auth="public", website=True, sitemap=False)
    def get_survey_video(self, model_name, field_name, token):
        try:
            model_obj = request.env[model_name].sudo()
            record_sudo = model_obj.search([('access_token', '=', token)])
        except KeyError or ValueError:
            return Response("Invalid URL", status=400)
        except Exception as e:
            return Response(e.__str__(), status=520)

        if not record_sudo:
            return Response("Record Not Found", status=404)

        return request.env['ir.binary']._get_image_stream_from(record_sudo, field_name).get_response()

