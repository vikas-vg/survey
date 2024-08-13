from ..lib.chatgpt.chatgpt import GenerateContent

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SurveyQuestionsAI(models.Model):
    _name = 'survey.generate.question'
    _description = 'Survey Generate Questions'
    _order = 'id desc'

    survey_id = fields.Many2one('survey.survey', string="Survey")
    survey_method = fields.Selection([('quantitative', 'Quantitative')], string='Survey Method', required=True)
    survey_goal = fields.Text('Survey Goal', required=True, help="What's your Goal with this survey?")
    industry = fields.Char('Industry', required=True)
    target_audience = fields.Char('Target Audience', required=True)
    survey_length = fields.Integer("# Questions", required=True, help='Number of Questions required.')
    initial_question = fields.Char('Initial Question')
    kpis = fields.Text("KPI's", required=True)

    @api.constrains('survey_length')
    def _check_conversation_question_no(self):
        for record in self:
            if record.survey_length < 1:
                raise ValidationError(_("Number of questions should at-least 1."))

    def generate_context(self):
        for record in self:
            if record.survey_method == 'quantitative':
                self.survey_id.write({'quantitative_record_id': self.id})
                return self.generate_quantitative_questions()
            else:
                return UserError(_("Invalid Survey Method"))

    def generate_quantitative_questions(self):
        key = self.env['ir.config_parameter'].sudo().get_param('chatgpt_core.openapi_api_key')
        if not key:
            raise UserError("Please configure CHATGPT API KEY in settings.")

        model = self.env['ir.config_parameter'].sudo().get_param('chatgpt_core.chatgpt_model')
        if not model:
            raise UserError("Please configure ChatGPT Model in settings.")
        model = self.env['chatgpt.model'].browse(int(model)).name

        content_obj = GenerateContent(key, model)
        contents = content_obj.generate_questions(self.survey_goal, self.industry, self.target_audience,
                                                  self.survey_length, self.kpis)
        return self.survey_id.create_quantitative_questions(contents)
