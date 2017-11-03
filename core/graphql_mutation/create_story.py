import graphene
import core.services as services
from core import HamkelaasyError
from core import Error_code

from core.graphql_query import StoryType


class Story_input(graphene.InputObjectType):
    kelaas_id = graphene.Int(required=True)
    title = graphene.String(default_value="")
    description = graphene.String(default_value="")
    pic = graphene.Int(description="uploaded pic id")
    pics = graphene.String(description="a string of files id.\n\nexample: '1,2,10,4'", default_value="")


class Create_story(graphene.Mutation):
    class Arguments:
        data = Story_input(required=True)

    Output = StoryType

    def mutate(self, info, data):
        return Create_story.make_story(info, data)

    @staticmethod
    def make_story(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person
        input_data = {
            'user': user,
            'kelaas_id': data.kelaas_id,
            'title': data.title,
            'description': data.description
        }
        if data.pic:
            input_data['pics_id'] = str(data.pic)
        if data.pics != "":
            input_data['pics_id'] = data.pics

        return services.create_story(**input_data)
