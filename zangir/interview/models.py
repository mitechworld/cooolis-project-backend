from django.db import models


class ZangirBaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Question(ZangirBaseModel):
    UNKNOWN_TYPE = 'UT'
    ONE_ANSWER_TYPE = 'OA'
    MULTIPLE_ANSWER_TYPE = 'MA'
    EMPTY_SPACE_TYPE = 'ES'

    text = models.TextField(max_length=300)
    complexity = models.IntegerField(default=2)


    def __str__(self):
        return self.text[:20]


    def options(self):
        return self.option_set.all()

    def answers(self):
        return self.options().filter(is_answer=True)

    def question_type(self):
        answer_num = self.answers().count()
        options_num = self.options().count()

        if answer_num == 1 and options_num == 1:
            return self.EMPTY_SPACE_TYPE
        elif answer_num == 1 and options_num > 1:
            return self.ONE_ANSWER_TYPE
        elif answer_num > 1:
            return self.MULTIPLE_ANSWER_TYPE
        else:
            return self.UNKNOWN_TYPE


class Option(ZangirBaseModel):
    text = models.TextField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:20]

