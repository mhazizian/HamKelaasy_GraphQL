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
        print
        print ">>> Running Setup:"
        print

        num = 20

        for x in xrange(num):
            user = User(username="parent_mha_" + str(x))
            user.save()
            parent = Parent(
                user=user,
                first_name="Parent mohammad hosein__" + str(x),
                last_name="Parent azizian__" + str(x),
                email="test@test.ir___" + str(x),
                gender=1,
                fard_access_token="1234567890qwertyuiopasdfghjkl",
            )
            parent.save()

        for x in xrange(num):
            user = User(username="teacher_mha_" + str(x))
            user.save()
            teacher = Teacher(
                user=user,
                first_name="Teacher mohammad hosein__" + str(x),
                last_name="Teacher azizian__" + str(x),
                email="test@test.ir___" + str(x),
                gender=1,
                fard_access_token="1234567890qwertyuiopasdfghjkl",
            )
            teacher.save()

        for x in xrange(num):
            user = User(username="student_mha_" + str(x))
            user.save()
            student = Student(
                user=user,
                first_name="Student mohammad hosein__" + str(x),
                last_name="Student azizian__" + str(x),
                email="test@test.ir___" + str(x),
                gender=1,
                fard_access_token="1234567890qwertyuiopasdfghjkl",
                age=17,
                nickname="Ye DaneshAmooz Sade!"
            )
            student.save()

        for x in xrange(num):
            student = User.objects.get(username="student_mha_" + str(x)).person.student
            parent = User.objects.get(username="parent_mha_" + str(x)).person.parent

            student.parents = parent
            student.save()

        kelaas = Kelaas(
            title="general_kelaas",
            description="General kelaas dige :D"
        )
        kelaas.save()
        for student in Student.objects.all():
            kelaas.students.add(student)
        teacher = Teacher.objects.all()[0]
        teacher.kelaases.add(kelaas)
        teacher.save()
        kelaas.save()

        story = Story(
            title="first story of all",
            description="my very first story!!",
            kelaas=kelaas,
            owner=teacher,
        )
        story.save()

        post = Kelaas_post(
            title="first post of all",
            description="my very first post!!",
            owner=teacher,
            kelaas=kelaas
        )
        post.save()

        comment = Comment(
            body="the very first comment in the universe!!!!!",
            post=post,
            owner=Person.objects.all()[0]
        )
        comment.save()
        comment = Comment(
            body="the very second!!! :( comment in the universe!!!!!",
            post=story,
            owner=teacher
        )
        comment.save()

        for x in xrange(4):
            kelaas = Kelaas(
                title="test_kelaas__" + str(x),
                description="kelaas desc__" + str(x),
            )
            kelaas.save()
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 1)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 2)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 3)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 4)).person.student)

            teacher = User.objects.get(username="teacher_mha_" + str(x)).person.teacher
            teacher.kelaases.add(kelaas)
            teacher.save()
            kelaas.save()

        for x in xrange(3):
            kelaas = Kelaas(
                title="test_kelaas VVV2" + str(x),
                description="kelaas desc VVV2" + str(x),
            )
            kelaas.save()
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 1)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 2)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 3)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha_" + str(x * 5 + 4)).person.student)
            teacher = User.objects.get(username="teacher_mha_" + str(x)).person.teacher
            teacher.kelaases.add(kelaas)
            teacher.save()
            kelaas.save()

    def test_query_teacher(self):
        user = User.objects.get(username="teacher_mha_0")
        print ">>> Test: Query for teacher: id=" + str(user.person.id)

        self.client.force_authenticate(user=user)
        index_url = reverse('index')

        query = """
        {
            me{
                id,
                firstName,
                lastName,
                username,
                pic,
            }
        }
        """
        print ">>>  Qeury on 'me'"
        response = self.client.post(index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        print res

        query = """
        {
            teacher{
                kelaases{
                    inviteCode
                }
            }
            
        }
        """
        print ">>>  Query on 'kelaases'"
        response = self.client.post(index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        print res

    def test_create_kelaas(self):
        user = User.objects.get(username="teacher_mha_4")
        print ">>> Test: Mutate for create kelaas"

        self.client.force_authenticate(user=user)
        index_url = reverse('index')

        query = """
          {
              kelaases{
                  title
              }
          }
          """
        print ">>>  Query on 'kelaases'"
        response = self.client.post(index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        print res

        mutate = """
        mutation{
            createKelaas(data:{title:"new kelaas with mutation", description:"salam be hame:DD", tags:"1,2"}){
                type
                message
            }
        }
        """
        print ">>>  Mutate on 'createKelaas'"
        response = self.client.post(index_url, json.dumps({'query': mutate}), content_type='application/json')
        res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        print res

        query = """
          {
              kelaases{
                  title
              }
          }
          """
        print ">>>  Query on 'kelaases'"
        response = self.client.post(index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        print res

    def test_student(self):
        c1 = Certificate(
            title="first certificate type",
            description="thank",
            creator_id=User.objects.get(username="teacher_mha_0").person.id
        )
        c1.save()
        c2 = Certificate(
            title="second certificate type",
            description="god",
            creator_id=User.objects.get(username="teacher_mha_1").person.id
        )
        c2.save()



        c1_level = Certificate_level(
            level=1,
            level_description="1:an awseme certi",
            type_id=c1.id
        )
        c1_level.save()
        c2_level = Certificate_level(
            level=2,
            level_description="2:an awseme certi",
            type_id=c1.id
        )
        c2_level.save()

        c3_level = Certificate_level(
            level=3,
            level_description="3:an awseme certi",
            type_id=c2.id
        )
        c3_level.save()
        c4_level = Certificate_level(
            level=4,
            level_description="4:an awseme certi",
            type_id=c2.id
        )
        c4_level.save()

        user = User.objects.get(username="student_mha_0")
        print user.person.student



        c_link = Certificate_link(
            owner=user.person.student,
            certificate_level=c1_level,
            assigner_id=User.objects.get(username="teacher_mha_4").person.id
        )
        c_link.save()
        c_link = Certificate_link(
            owner=user.person.student,
            certificate_level=c3_level,
            assigner_id=User.objects.get(username="teacher_mha_4").person.id
        )
        c_link.save()

        print ">>> :D"
        print ">>> Test: Query for Student: id=" + str(user.person.id)

        self.client.force_authenticate(user=user)
        index_url = reverse('index')

        query = """
          {
              student{
                  firstName
                  certificates{
                        title
                        creator{
                            firstName
                        }
                        levels{
                            level
                            assigner{
                                firstName
                            }
                        }
                  }
    
              }
          }
          """
        print ">>>  Query on 'kelaases'"
        response = self.client.post(index_url, json.dumps({'query': query}), content_type='application/json')
        res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        print res

        # def test_create_student(self):
        #     signup_url = reverse('signup')
        #     data = {
        #         "type": "student",
        #         "userName": "Student_for_test",
        #         "firstName": "Test first name",
        #         "lastName": "Test Last Name",
        #         "email": "test@test.ir",
        #         "gender": "1",
        #         "accessToken": "Test_1234asdf5678901234567890",
        #
        #         "age": "14",
        #         "nickName": "mha76",
        #     }
        #     print ">>> Test: Creating Student, response:"
        #     response = self.client.post(signup_url, {'data': json.dumps(data)})
        #     print response
        #     print User.objects.get(username="Student_for_test").person.student.pic

        # def test_create_parent(self):
        #     signup_url = reverse('signup')
        #     data = {
        #         "type": "parent",
        #         "userName": "Parent_for_test",
        #         "firstName": "Test first name P",
        #         "lastName": "Test Last Name P",
        #         "email": "test@test.ir",
        #         "gender": "1",
        #         "accessToken": "Test_1234asdf5678901234567890",
        #     }
        #     print ">>> Test: Creating Parent, response:"
        #     response = self.client.post(signup_url, {'data': json.dumps(data)})
        #     print response

        # def test_create_teacher(self):
        #     signup_url = reverse('signup')
        #     data = {
        #         "type": "teacher",
        #         "userName": "Teacher_for_test",
        #         "firstName": "Test first name T",
        #         "lastName": "Test Last Name T",
        #         "email": "test@test.ir",
        #         "gender": "1",
        #         "accessToken": "Test_1234asdf5678901234567890",
        #     }
        #     print ">>> Test: Creating Teacher, response:"
        #     response = self.client.post(signup_url, {'data': json.dumps(data)})
        #     print response
