import uuid

from odoo import fields, models, api, _


class SurveySurveyVideoInherit(models.Model):
    _inherit = "survey.survey"

    survey_start_video = fields.Binary('Survey Start Video', attachment=True)
    survey_start_video_name = fields.Char('Survey Start Video Name')
    survey_start_video_url = fields.Char('Survey Start Video URL', compute='_compute_survey_start_video_url', store=True)

    survey_end_video = fields.Binary('Survey End Video', attachment=True)
    survey_end_video_name = fields.Char('Survey End Video Name')
    survey_end_video_url = fields.Char('Survey End Video URL', compute='_compute_survey_end_video_url', store=True)

    @api.depends('survey_start_video')
    def _compute_survey_start_video_url(self):
        for record in self:
            if not record.survey_start_video:
                record.write({'survey_start_video_url': False})

            record.survey_start_video_url = f"/web/content/get_background_video/survey.survey/survey_start_video/{record.access_token}"

    @api.depends('survey_end_video')
    def _compute_survey_end_video_url(self):
        for record in self:
            if not record.survey_end_video:
                record.write({'survey_end_video_url': False})

            record.survey_end_video_url = f"/web/content/get_background_video/survey.survey/survey_end_video/{record.access_token}"
