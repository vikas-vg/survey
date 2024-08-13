import uuid

from odoo import fields, models, api, _


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    access_token = fields.Char('Access Token', copy=False)

    background_video = fields.Binary('Background Video', attachment=True)
    background_video_name = fields.Char('Background Video Name')
    background_video_url = fields.Char('Background Video URL', compute="_compute_background_video_url", store=True)

    def _generate_access_token(self):
        for record in self:
            record.access_token = str(uuid.uuid4())

    @api.depends('background_video')
    def _compute_background_video_url(self):
        for record in self:
            if not record.background_video:
                record.write({'background_video_url': False})
                continue

            if not record.access_token:
                record._generate_access_token()

            record.background_video_url = f"/web/content/get_background_video/survey.question/background_video/{record.access_token}"
