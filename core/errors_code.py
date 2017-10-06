errors = {
    '4011': {
        'message': 'User not authenticated.',
        'status': 401
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


def get_errors_code():
    return errors
