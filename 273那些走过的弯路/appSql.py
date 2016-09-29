#!flask/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


@app.route('/')
def index():
    return 'Flask is running!'


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_no = db.Column(db.Integer)
    creation_date = db.Column(db.String(250))
    readable_title = db.Column(db.Text)


class IssueSchema(ma.ModelSchema):
    class Meta:
        model = Issue


tagmap = db.Table('tagmap',
                  db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                  db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                  db.PrimaryKeyConstraint('post_id', 'tag_id'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tag = db.Column(db.String(250))


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    post_no = db.Column(db.Integer)

    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    issue = db.relationship(
        'Issue', backref=db.backref('posts', lazy='dynamic'))

    readable_title = db.Column(db.String(250))
    title = db.Column(db.String(250))
    readable_article = db.Column(db.Text)
    readable_summary = db.Column(db.Text)
    summary = db.Column(db.Text)
    read_time_minutes = db.Column(db.Integer)
    url_domain = db.Column(db.String(250))
    slug = db.Column(db.String(500))
    url = db.Column(db.String(500))
    creation_date = db.Column(db.String(250))

    tags = db.relationship(
        'Tag', secondary=tagmap, backref=db.backref('posts', lazy='dynamic'))


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post


issue_schema = IssueSchema(strict=True)
post_schema = PostSchema(strict=True)
tag_schema = TagSchema(strict=True)


class IssuesResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, help='Pagination cannot be find')
        args = parser.parse_args()
        page = args.get('page')
        print(page)
        issues_query = Issue.query.order_by(Issue.issue_no.desc()).paginate(
            page=page, per_page=20, error_out=False)
        result = issue_schema.dump(issues_query.items, many=True).data
        return result


class IssueResource(Resource):
    def get(self, issue_no):
        issue_query = Post.query.join(Issue).filter(Post.issue_id == Issue.id) \
            .filter(Issue.issue_no == issue_no).all()
        result = post_schema.dump(issue_query, many=True).data
        return result


class PostsResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, help='Pagination cannot be find')
        args = parser.parse_args()
        page = args.get('page')
        print(page)
        posts_query = Post.query.order_by(Post.post_no.desc()).paginate(
            page=page, per_page=5, error_out=False)
        result = post_schema.dump(posts_query.items, many=True).data
        return result


class PostResource(Resource):
    def get(self, post_no):
        post_query = Post.query.filter(post_no == post_no).first()
        result = post_schema.dump(post_query).data
        return result


class TagsResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, help='Pagination cannot be find')
        args = parser.parse_args()
        page = args.get('page')
        print(page)
        tags_query = Tag.query.paginate(
            page=page, per_page=50, error_out=False)
        result = tag_schema.dump(tags_query.items, many=True).data
        return result


class TagResource(Resource):
    def get(self, id):
        tag_query = Tag.query.get_or_404(id)
        result = tag_schema.dump(tag_query).data
        return result


api.add_resource(IssuesResource, '/api/v1/issues')
api.add_resource(IssueResource, '/api/v1/issues/<string:issue_no>')
api.add_resource(PostsResource, '/api/v1/posts')
api.add_resource(PostResource, '/api/v1/posts/<string:post_no>')
api.add_resource(TagsResource, '/api/v1/tags')
api.add_resource(TagResource, '/api/v1/tags/<string:id>')

if __name__ == '__main__':
    app.run()