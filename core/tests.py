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
        signup_url = reverse('signup')

        for x in xrange(30):
            data = {
                "type": "teacher",
                "userName": "teacher_mha" + str(x),
                "firstName": "mahdi" + str(x),
                "lastName": "rezaii" + str(x),
                "email": "test@test.ir",
                "gender": "1",
                "accessToken": "123451234asdf5678901234567890",
            }
            print ">> Teacher:"
            response = self.client.post(signup_url, {'data': json.dumps(data)})
            print response

        for x in xrange(20):
            data = {
                "type": "parent",
                "userName": "parent_mha" + str(x),
                "firstName": "morteza" + str(x),
                "lastName": "abrari" + str(x),
                "email": "test@test.ir",
                "gender": "1",
                "accessToken": "123451234asdf5678901234567890",
            }
            print ">> Parent:"
            response = self.client.post(signup_url, {'data': json.dumps(data)})
            print response

        for x in xrange(20):
            data = {
                "type": "student",
                "userName": "student_mha" + str(x),
                "firstName": "mohammad hosein" + str(x),
                "lastName": "azizian" + str(x),
                "email": "test@test.ir",
                "gender": "1",
                "accessToken": "1234asdf5678901234567890",

                "age": "14",
                "nickName": "mha76",
            }
            print ">> Student:"
            response = self.client.post(signup_url, {'data': json.dumps(data)})
            print response

        for x in xrange(20):
            student = User.objects.get(username="student_mha" + str(x)).person.student
            parent = User.objects.get(username="parent_mha" + str(x)).person.parent

            student.parents = parent
            student.save()

        for x in xrange(4):
            kelaas = Kelaas(
                title="test_kelaas" + str(x),
                description="kelaas desc" + str(x),
            )
            kelaas.save()
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5 + 1)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5 + 2)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5 + 3)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5 + 4)).person.student)
            teacher = User.objects.get(username="teacher_mha" + str(x)).person.teacher
            teacher.kelasses.add(kelaas)
            teacher.save()
            kelaas.save()
            print kelaas.id

        for x in xrange(3):
            kelaas = Kelaas(
                title="test_kelaas V2" + str(x),
                description="kelaas desc V2" + str(x),
            )
            kelaas.save()
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5 + 1)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5 + 2)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5 + 3)).person.student)
            kelaas.students.add(User.objects.get(username="student_mha" + str(x*5 + 4)).person.student)
            teacher = User.objects.get(username="teacher_mha" + str(x)).person.teacher
            teacher.kelasses.add(kelaas)
            teacher.save()
            kelaas.save()
            print kelaas.id

    def test_query_data(self):
        user = User.objects.get(username="teacher_mha3")
        print ">> user_type: " + user.person.type

        self.client.force_authenticate(user=user)

        query1 = """
        {
            students(kelaasId:4){
                username
                id
            }
        }
        
        """


        query = """
            {
              student(id:69){
                id
                username
                kelaases{
                    id
                    students{
                        id
                        firstName
                        kelaases{
                            id
                            title
                        }
                    }
                }
              }
              me{
                id
                firstName
                lastName
              }
            }
        """

        index_url = reverse('index')

        response = self.client.post(index_url, {'query': query})
        res = json.dumps(json.loads(response.content), indent=4, sort_keys=True)
        print res
