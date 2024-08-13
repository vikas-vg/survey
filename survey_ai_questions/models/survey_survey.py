import requests
from odoo.exceptions import ValidationError, UserError
from odoo import models, fields, api, _


class SurveySurveyInherit(models.Model):
    _inherit = 'survey.survey'

    quantitative_record_id = fields.Many2one('survey.generate.question', string='AI Questions')

    survey_method = fields.Selection([
        ('quantitative', 'Quantitative Survey'),
    ], string='Survey Method', required=True, default="quantitative")

    @api.constrains('conversation_question_no')
    def _check_conversation_question_no(self):
        for record in self:
            if record.survey_method in ('conversational', 'both') and record.conversation_question_no < 1:
                raise ValidationError(_("Number of questions should at-least 1."))

    def generate_qualitative_context(self):
        self.ensure_one()
        base_url = self.get_base_url()

        payload = dict(
            base_url=base_url,
            sid=self.access_token,
            no_of_question=self.conversation_question_no,
            industry=self.qualitative_record_id.industry,
            target_audience=self.qualitative_record_id.target_audience,
            survey_goal=self.qualitative_record_id.survey_goal,
            kpis=self.qualitative_record_id.kpis,
        )

        if self.conversation_avatar:
            payload.update({'avatar_url': f"{base_url}/web/content/get_background_image/survey.survey/conversation_avatar/{self.access_token}"})
        if self.conversation_question:
            payload.update({'next_question': self.conversation_question})

        url = "https://survey.xpbrand.ai/api/generateURL/"
        response = requests.post(url, json=payload)

        if response.status_code == 201:
            self.with_context({'force_save': True}).write({
                'conversation_url': response.json().get('url'),
                'conversation_question': response.json().get('que'),
            })
        return response.json() or None

    def create_quantitative_questions(self, content):
        self.ensure_one()
        self.question_and_page_ids.write({'active': False})
        self.question_ids.write({'active': False})

        vals = dict(
            script=content.get('story_script', False),
            question_and_page_ids=[]
        )

        question_list = content['questions']
        for question in question_list:
            question_content = False
            if question.get('question_type') == 'mcq':
                question_content = [0, 0, {
                    'title': question.get('question'),
                    'question_type': 'simple_choice',
                    'suggested_answer_ids': [[0, 0, {'value': value}] for value in question.get('options')],
                    'conversation_script': question.get('story_script'),
                }]
            elif question.get('question_type') == 'text':
                question_content = [0, 0, {
                    'title': question.get('question'),
                    'question_type': 'text_box',
                    'conversation_script': question.get('story_script'),
                }]

            if question_content:
                vals['question_and_page_ids'].append(question_content)

        self.write(vals)

    def action_open_conversation_view(self):
        self.ensure_one()
        if self._context.get('default_survey_method') == 'quantitative':
            name = 'Quantitative'
            res_id = self.quantitative_record_id.id
        elif self._context.get('default_survey_method') == 'qualitative':
            name = 'Qualitative'
            res_id = self.qualitative_record_id.id
        else:
            raise ValidationError(_("Something went wrong. Please contact System Admin."))
        return {
            'name': _(name),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('survey_ai_questions.survey_ai_inherit_form').id,
            'res_model': 'survey.generate.question',
            'res_id': res_id,
            'target': 'new',
        }

