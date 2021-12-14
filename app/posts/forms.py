from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField('Title')
    abstract = StringField('Abstract')
    body = TextAreaField('Body')


class CommentForm(Form):
    comment = StringField('Comment')


