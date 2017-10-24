from enum import Enum


class Error_code(object):
    class Object_not_found(Enum):
        Kelaas = 4041
        Post = 4042
        Story = 4043
        Comment = 4044

        Person = 4045
        Student = 4046
        Parent = 4047
        Teacher = 4048

        Conversation = 4049
        Message = 40410

        Task = 40411

        Certificate = 40412
        Badge = 40413
        Phone_number = 40414
        Notification = 40415

    class Phone_number(Enum):
        Invalid_number = 1001
        Invalid_number_validator = 1005
        Number_is_registered = 1002
        Number_is_not_registered = 1003
        Delay_required = 1004
        Server_in_development = 1005
        Server_is_busy = 1006

    class Authentication(Enum):
        User_not_authenticated = 4011
        Login_failed = 4016
        Permission_denied = 4032
        Only_teacher = 4033
        Only_student = 4034
        Only_parent = 4035
        Invalid_captcha = 40306

    class Kelaas(Enum):
        Gender_doesnt_match = 3002
        Id_required = 3001

    class Student(Enum):
        Id_required = 6001
        Permission_denied = 4032
        Has_parent = 6002
        Bad_gender = 6003
        Bad_age = 6004
        Invalid_username = 4017
        Duplicate_username = 40013

    class Teacher(Enum):
        Bad_gender = 6003

    class Parent(Enum):
        Id_required = 7001

    class Certificate(Enum):
        # TODO complete from here
        Permisson_denied = 4032
        Duplicate_title = 8002
        Duplicate_level = 8003

    # TODO switch to this for later.
    @staticmethod
    def message(obj):
        return errors[obj.value]['message']

    @staticmethod
    def status_code(obj):
        return errors[obj.value]['status']

    @staticmethod
    def error_code(obj):
        return errors[obj.value]['code']


errors = {
    Error_code.Object_not_found.Kelaas.value: {
        'message': 'Kelaas not found.',
        'status': 404
    },
    Error_code.Object_not_found.Post.value: {
        'message': 'Kelaas-Post not found',
        'status': 404
    },
    Error_code.Object_not_found.Story.value: {
        'message': 'Story not found',
        'status': 404
    },
    Error_code.Object_not_found.Student.value: {
        'message': 'Student not found',
        'status': 404
    },
    Error_code.Object_not_found.Parent.value: {
        'message': 'Parent not found',
        'status': 404
    },
    Error_code.Object_not_found.Teacher.value: {
        'message': 'Teacher not found',
        'status': 404
    },
    Error_code.Object_not_found.Conversation.value: {
        'message': 'Conversation not found',
        'status': 404
    },
    Error_code.Object_not_found.Message.value: {
        'message': 'Message not found',
        'status': 404
    },
    Error_code.Object_not_found.Task.value: {
        'message': 'Task not found',
        'status': 404
    },
    Error_code.Object_not_found.Comment.value: {
        'message': 'Comment not found',
        'status': 404
    },
    Error_code.Object_not_found.Person.value: {
        'message': 'Person not found',
        'status': 404
    },
    Error_code.Object_not_found.Badge.value: {
        'message': 'Badge not found',
        'status': 404
    },
    Error_code.Object_not_found.Phone_number.value: {
        'message': 'Phone number not found, please submit it first',
        'status': 404
    },
    Error_code.Object_not_found.Certificate.value: {
        'message': 'Certificate not found',
        'status': 404
    },
    Error_code.Object_not_found.Notification.value: {
        'message': 'Notification not found',
        'status': 404
    },


    Error_code.Phone_number.Invalid_number.value: {
        'message': 'Invalid phone number',
        'status': 400
    },

    Error_code.Phone_number.Server_in_development.value: {
        'message': 'Sms server is in development, please try again later',
        'status': 503
    },
    Error_code.Phone_number.Server_is_busy.value: {
        'message': 'Sms server is busy, try again later.',
        'status': 503
    },
    Error_code.Phone_number.Number_is_registered.value: {
        'message': 'Phone number is already registered',
        'status': 400
    },
    Error_code.Phone_number.Number_is_not_registered.value: {
        'message': 'Phone number is not registered',
        'status': 400
    },
    Error_code.Phone_number.Delay_required.value: {
        'message': 'You should at least wait for 1min to request sending new message',
        'status': 400
    },
    Error_code.Phone_number.Invalid_number_validator.value: {
        'message': 'Invalid phone number validator',
        'status': 400
    },

    Error_code.Authentication.User_not_authenticated.value: {
        'message': 'User not authenticated.',
        'status': 401,
    },
    Error_code.Authentication.Login_failed.value: {
        'message': 'Username or Password is wrong',
        # TODO change status code
        'status': 401,
    },
    Error_code.Authentication.Only_parent.value: {
        'message': 'Only available for parent',
        'status': 403
    },
    Error_code.Authentication.Only_student.value: {
        'message': 'Only available for student',
        'status': 403
    },
    Error_code.Authentication.Only_teacher.value: {
        'message': 'Only available for teacher',
        'status': 403
    },
    Error_code.Authentication.Permission_denied.value: {
        'message': 'Permission denied',
        'status': 403
    },
    Error_code.Authentication.Invalid_captcha.value: {
        'message': 'Given captcha is invalid',
        'status': 400
    },

    Error_code.Kelaas.Gender_doesnt_match.value: {
        'message': "gender doesn't match",
        'status': 400
    },

    Error_code.Student.Id_required.value: {
        'message': '"student_id" is necessary',
        'status': 400
    },
    Error_code.Student.Bad_gender.value: {
        'message': 'invalid gender value',
        'status': 400
    },
    Error_code.Student.Bad_age.value: {
        'message': 'invalid age value',
        'status': 400
    },
    Error_code.Student.Has_parent.value: {
        'message': 'student already has parent, cant assign any more',
        'status': 400
    },
    Error_code.Student.Invalid_username.value: {
        'message': 'given username has invalid values',
        'status': 400,
    },
    Error_code.Student.Duplicate_username.value: {
        'message': 'duplicate username',
        'status': 400,
    },

    Error_code.Kelaas.Id_required.value: {
        'message': 'Kelaas id is required',
        'status': 400
    },

    Error_code.Teacher.Bad_gender.value: {
        'message': 'invalid gender value',
        'status': 400
    },

    Error_code.Parent.Id_required.value: {
        'message': '"parent_id" is necessary',
        'status': 400
    },

    Error_code.Certificate.Duplicate_title.value: {
        'message': 'duplicate certificate title',
        'status': 400
    },
    Error_code.Certificate.Duplicate_level.value: {
        'message': 'duplicate certificate-level',
        'status': 400
    },

    '4033': {
        'message': 'Parent is necessary',
        'status': 403
    },
}
