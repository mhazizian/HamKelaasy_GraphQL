# -*- coding: utf-8 -*-t
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User

from core.models import *
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


class Test(APITestCase):
    def setUp(self):
        print "__________________________________________________________"

        self.index_url = reverse('index')

        self.temp_user = User(username="temp")
        self.temp_user.save()

        # create some user!
        num = 5
        self.parents = []
        for x in xrange(num):
            user = User(username="parent_" + str(x))
            user.save()
            parent = Parent(
                user=user,
                first_name="firstname_parent" + str(x),
                last_name="lastname_parent" + str(x),
                email="test@test.ir",
                gender=1,
                fard_access_token="12345678901234567890",
            )
            parent.save()
            self.parents.append(parent)

        self.teachers = []
        for x in xrange(num):
            user = User(username="teacher_" + str(x))
            user.save()
            teacher = Teacher(
                user=user,
                first_name="firstname_teacher" + str(x),
                last_name="lastname_teacher" + str(x),
                email="test@test.ir",
                gender=1,
                fard_access_token="12345678901234567890",
            )
            teacher.save()
            self.teachers.append(teacher)

        self.students = []
        for x in xrange(num):
            user = User(username="student_" + str(x))
            user.save()
            student = Student(
                user=user,
                first_name="firstname_student" + str(x),
                last_name="lastname_student" + str(x),
                email="test@test.ir",
                gender=1,
                fard_access_token="12345678901234567890",
                age=17,
                nickname="Ye DaneshAmooz Sade!"
            )
            student.save()
            self.students.append(student)

        # add parent for existing students
        for x in xrange(num):
            self.students[x].parents = self.parents[x]
            self.students[x].save()

        # create a global kelaas:
        # students : all students, teacher: self.teachers[0]
        self.global_kelaas = Kelaas(
            title="general_kelaas",
            description="General kelaas dige :D"
        )
        self.global_kelaas.save()
        for student in self.students:
            self.global_kelaas.students.add(student)

        self.teachers[0].kelaases.add(self.global_kelaas)
        self.teachers[0].save()

        # create some badges:
        self.badges = []
        for x in xrange(10):
            badge = Badge(title="System Badge_" + str(x))
            badge.save()
            self.badges.append(badge)

        # create some certificate:
        # creator of this certificates : self.teachers[1]
        # each certificate comes with 4 levels : from 1 to 4
        self.certificates = []
        for x in xrange(10):
            certi = Certificate(
                title="Sys Certificate_" + str(x),
                description="sample description",
                creator=self.teachers[1]
            )
            certi.save()
            for i in xrange(4):
                level = Certificate_level(
                    type=certi,
                    level_description="Sys certi Leve_" + str(i),
                    level=i + 1
                )
                level.save()
            self.certificates.append(certi)

        # create some tags:
        self.tags = []
        for i in xrange(10):
            tag = Tag(title="Sys tag_" + str(i))
            tag.save()
            self.tags.append(tag)

# ____________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________

    def test_assign_badge(self):
        print ">>> Test: Mutate for create kelaas"

        teacher = Teacher(
            user=self.temp_user,
            first_name="fname_teacher",
            last_name="lname_teacher",
            email="test@test.ir",
            gender=1,
            fard_access_token="12345678901234567890",
        )
        teacher.save()
        self.client.force_authenticate(user=teacher.user)

        mutate = """
        mutation{
            createKelaas(data:{title:"new kelaas with mutation", description:"salam be hame:DD", tags:"1,2"}){
                type
                message
            }
        }
        """
        print "> send mutation"
        response = self.client.post(self.index_url, json.dumps({'query': mutate}), content_type='application/json')
        res = json.dumps(json.loads(response.content))
        self.assertEqual(res, '{"createKelaas": {"message": "Kelaas added.", "type": "success"}}')
        print "done"

        query = """
          {
              kelaases{
                  title
              }
          }
          """
        print ">  check kelaas query"
        response = self.client.post(self.index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content))
        self.assertEqual(res, '{"kelaases": [{"title": "new kelaas with mutation"}]}')
        print "done"

    def test_assign_badge_mutation(self):
        print ">>> Test: assign_badge"

        self.client.force_authenticate(user=self.teachers[0].user)

        mutation = """
            mutation{
                 assignBadge(data:{kelaasId:%d, studentId:%d, badges:"%d,%d"}){
                    type
                    message
                }
            }

        """ % (self.global_kelaas.id, self.students[0].id, self.badges[0].id, self.badges[1].id)

        print "> send mutation"
        response = self.client.post(self.index_url, json.dumps({'query': mutation}), content_type='application/json')
        res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        # TODO asssert required.
        print "done"

        self.client.force_authenticate(user=self.students[0].user)
        query = """
          {
            student{
              badges{
                  title
              }
            }
          }
          """
        print ">  check badges query"
        response = self.client.post(self.index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content))
        self.assertEqual(res, '{"student": {"badges": [{"title": "System Badge_0"}, {"title": "System Badge_1"}]}}')
        print "done"

    def test_badge_type_query(self):
        print ">>> Test: badgeType_query"
        self.client.force_authenticate(user=self.students[0].user)

        query = """
            query{
              badgeTypes{
                title
              }
            }
        """
        print ">  check badges query"
        response = self.client.post(self.index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content))
        self.assertEqual(res, '{"badgeTypes": [{"title": "System Badge_0"}, '
                              '{"title": "System Badge_1"}, {"title": "System Badge_2"}, '
                              '{"title": "System Badge_3"}, {"title": "System Badge_4"}, '
                              '{"title": "System Badge_5"}, {"title": "System Badge_6"}, '
                              '{"title": "System Badge_7"}, {"title": "System Badge_8"}, '
                              '{"title": "System Badge_9"}]}')
        print "done"

    def test_tags_query(self):
        print ">>> Test: tags_query"
        self.client.force_authenticate(user=self.students[0].user)

        query = """
            query{
              tags{
                title
              }
            }
        """
        print ">  check tags query"
        response = self.client.post(self.index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content))
        self.assertEqual(res, '{"tags": [{"title": "Sys tag_0"}, {"title": "Sys tag_1"}, '
                              '{"title": "Sys tag_2"}, {"title": "Sys tag_3"}, '
                              '{"title": "Sys tag_4"}, {"title": "Sys tag_5"}, '
                              '{"title": "Sys tag_6"}, {"title": "Sys tag_7"}, '
                              '{"title": "Sys tag_8"}, {"title": "Sys tag_9"}]}')
        print "done"

    def test_certificate_query(self):
        print ">>> Test: certificate_query"
        self.client.force_authenticate(user=self.students[0].user)

        query = """
            query{
                certificate(id:1){
                title
                description
                creator{
                  username
                }
                levels{
                  level
                  levelDescription
                }
              }
            }
        """
        print ">  check certificates query"
        response = self.client.post(self.index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content))
        self.assertEqual(res, '{"certificate": {"creator": {"username": "teacher_1"}, '
                              '"description": "sample description", "levels": [{"levelDescription": '
                              '"Sys certi Leve_0", "level": 1}, {"levelDescription": "Sys certi Leve_1", "level": 2}, '
                              '{"levelDescription": "Sys certi Leve_2", "level": 3}, '
                              '{"levelDescription": "Sys certi Leve_3", "level": 4}], "title": "Sys Certificate_0"}}')
        print "done"

    def test_me_query(self):
        print ">>> Test: me_query"
        self.client.force_authenticate(user=self.students[3].user)

        query = """
            query{
              me{
                username
                firstName
                lastName
                id
                email
                signupCompleted
                pic
                type
              }
            }
                """
        print ">  check me query"
        response = self.client.post(self.index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content))
        self.assertEqual(res, '{"me": {"username": "student_3", "firstName": '
                              '"firstname_student3", "lastName": "lastname_student3", '
                              '"pic": "http://94.182.227.193:8080/media/student.svg", "email": "test@test.ir", '
                              '"signupCompleted": false, "type": "student", "id": 14}}')
        print "done"

    def test_variable_graphQL(self):
        print ">>> Test: graphql variables"
        self.client.force_authenticate(user=self.students[3].user)

        query = """
            query TEST($tid: Int!){
                certificate(id: $tid){
                    title
                    description
                    creator{
                      username
                    }
                }
            }
        """
        var = """
        {
            "tid": 1
        }
        """
        response = self.client.post(self.index_url, json.dumps({'query': query, 'variables': {'tid': 1}}), content_type='application/json')
        print response
        res = json.dumps(json.loads(response.content))
        print res


        # mutation = """
        #     mutation{
        #          assignBadge(data:{kelaasId:%d, studentId:%d, badges:"%d,%d"}){
        #             type
        #             message
        #         }
        #     }
        #
        # """ % (self.global_kelaas.id, self.students[0].id, self.badges[0].id, self.badges[1].id)
        #
        # print "> send mutation"
        # response = self.client.post(self.index_url, json.dumps({'query': mutation}), content_type='application/json')
        # res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)


        # story = Story(
        #     title="first story of all",
        #     description="my very first story!!",
        #     kelaas=kelaas,
        #     owner=teacher,
        # )
        # story.save()
        #
        # post = Kelaas_post(
        #     title="first post of all",
        #     description="my very first post!!",
        #     owner=teacher,
        #     kelaas=kelaas
        # )
        # post.save()
        #
        # comment = Comment(
        #     body="the very first comment in the universe!!!!!",
        #     post=post,
        #     owner=Person.objects.all()[0]
        # )
        # comment.save()
        # comment = Comment(
        #     body="the very second!!! :( comment in the universe!!!!!",
        #     post=story,
        #     owner=teacher
        # )
        # comment.save()
        #
        # for x in xrange(4):
        #     kelaas = Kelaas(
        #         title="test_kelaas__" + str(x),
        #         description="kelaas desc__" + str(x),
        #     )
        #     kelaas.save()
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5)).person.student)
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 1)).person.student)
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 2)).person.student)
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 3)).person.student)
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 4)).person.student)
        #
        #     teacher = User.objects.get(username="teacher_mha_" + str(x)).person.teacher
        #     teacher.kelaases.add(kelaas)
        #     teacher.save()
        #     kelaas.save()
        #
        # for x in xrange(3):
        #     kelaas = Kelaas(
        #         title="test_kelaas VVV2" + str(x),
        #         description="kelaas desc VVV2" + str(x),
        #     )
        #     kelaas.save()
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5)).person.student)
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 1)).person.student)
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 2)).person.student)
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 3)).person.student)
        #     kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 4)).person.student)
        #     teacher = User.objects.get(username="teacher_mha_" + str(x)).person.teacher
        #     teacher.kelaases.add(kelaas)
        #     teacher.save()
        #     kelaas.save()
        #
        #     query = """
        #     {
        #         teacher{
        #             kelaases{
        #                 id
        #                 students{
        #                     username
        #                     firstName
        #                     id
        #                 }
        #             }
        #         }
        #
        #     }
        #     """
        #     print ">>>  Query on 'kelaases'"
        #     response = self.client.post(index_url, json.dumps({'query': query}), content_type='application/json')
        #     res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        #     print res
        #
        # def test_student(self):
        #     c1 = Certificate(
        #         title="first certificate type",
        #         description="thank",
        #         creator_id=User.objects.get(username="teacher_mha_0").person.id
        #     )
        #     c1.save()
        #     c2 = Certificate(
        #         title="second certificate type",
        #         description="god",
        #         creator_id=User.objects.get(username="teacher_mha_1").person.id
        #     )
        #     c2.save()
        #
        #
        #
        #     c1_level = Certificate_level(
        #         level=1,
        #         level_description="1:an awseme certi",
        #         type_id=c1.id
        #     )
        #     c1_level.save()
        #     c2_level = Certificate_level(
        #         level=2,
        #         level_description="2:an awseme certi",
        #         type_id=c1.id
        #     )
        #     c2_level.save()
        #
        #     c3_level = Certificate_level(
        #         level=3,
        #         level_description="3:an awseme certi",
        #         type_id=c2.id
        #     )
        #     c3_level.save()
        #     c4_level = Certificate_level(
        #         level=4,
        #         level_description="4:an awseme certi",
        #         type_id=c2.id
        #     )
        #     c4_level.save()
        #
        #     user = User.objects.get(username="student_mha_0")
        #     print user.person.student
        #
        #
        #
        #     c_link = Certificate_link(
        #         owner=user.person.student,
        #         certificate_level=c1_level,
        #         assigner_id=User.objects.get(username="teacher_mha_4").person.id
        #     )
        #     c_link.save()
        #     c_link = Certificate_link(
        #         owner=user.person.student,
        #         certificate_level=c3_level,
        #         assigner_id=User.objects.get(username="teacher_mha_4").person.id
        #     )
        #     c_link.save()
        #
        #     print ">>> :D"
        #     print ">>> Test: Query for Student: id=" + str(user.person.id)
        #
        #     self.client.force_authenticate(user=user)
        #     index_url = reverse('index')
        #
        #     query = """
        #       {
        #           student{
        #               firstName
        #               certificates{
        #                     title
        #                     creator{
        #                         firstName
        #                     }
        #                     levels{
        #                         level
        #                         assigner{
        #                             firstName
        #                         }
        #                     }
        #               }
        #
        #           }
        #       }
        #       """
        #     print ">>>  Query on 'kelaases'"
        #     response = self.client.post(index_url, json.dumps({'query': query}), content_type='application/json')
        #     res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        #     print res
