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

    class Kelaas(Enum):
        Gender_doesnt_match = 3001

    class Student(Enum):
        Id_required = 6001
        Permission_denied = 4032
        Has_parent = 6002
        Bad_gender = 6003
        Bad_age = 6004

    class Teacher(Enum):
        Bad_gender = 6003

    class Parent(Enum):
        Id_required = 7001

    class Certificate(Enum):
        # TODO complete from here
        Permisson_denied = 8001
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
    '4011': {
        'message': 'User not authenticated.',
        'status': 401,
        'code': 4011
    },

    '4041': {
        'message': 'Kelaas not found.',
        'status': 400
    },
    '4042': {
        'message': 'Student not found',
        'status': 400
    },
    '4043': {
        'message': 'Parent not found',
        'status': 400
    },
    '4044': {
        'message': 'Certificate not found',
        'status': 400
    },
    '4045': {
        'message': 'Conversation not found',
        'status': 400
    },
    '4046': {
        'message': 'Child not found',
        'status': 400
    },
    '4047': {
        'message': 'Post not found',
        'status': 400
    },
    '4048': {
        'message': 'Badge not found',
        'status': 400
    },
    '4049': {
        'message': 'Owner not found',
        'status': 400
    },
    '4050': {
        'message': 'Person not found',
        'status': 400
    },
    '4051': {
        'message': 'Task not found',
        'status': 400
    },
    '4052': {
        'message': 'Comment not found',
        'status': 400
    },

    '4001': {
        'message': 'Invalid phone number',
        'status': 400
    },
    '4002': {
        'message': 'Phone number is already registered',
        'status': 400
    },
    '4003': {
        'message': 'Phone number is not registered',
        'status': 400
    },
    '4004': {
        'message': 'You should at least wait for 1min to request sending new message',
        'status': 400
    },
    '4005': {
        'message': 'Invalid phone number validator',
        'status': 400
    },
    '4006': {
        'message': '"id" is necessary',
        'status': 400
    },
    '4007': {
        'message': "gender doesn't match",
        'status': 400
    },
    '4008': {
        'message': 'duplicate certificate',
        'status': 400
    },
    '4009': {
        'message': 'duplicate certificate-level',
        'status': 400
    },

    '5031': {
        'message': 'Sms server is in development, please try again later',
        'status': 503
    },
    '5032': {
        'message': 'Sms server is busy, try again later.',
        'status': 503
    },
    '4031': {
        'message': 'Only available for parent',
        'status': 403
    },
    '4032': {
        'message': 'Permission denied',
        'status': 403
    },
    '4033': {
        'message': 'Parent is necessary',
        'status': 403
    },

}
